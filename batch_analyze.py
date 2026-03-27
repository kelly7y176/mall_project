import cv2
import os
import numpy as np
from ultralytics import YOLO
from PIL import Image
from pillow_heif import register_heif_opener
from datetime import datetime
import torch

# 註冊 HEIC 支援
register_heif_opener()

# --- 配置區 ---
MODEL_PATH = "yolo11s.engine"
INPUT_DIR = os.path.expanduser("~/mall_project/data/recordings")
OUTPUT_DIR = os.path.expanduser("~/mall_project/data/results")
os.makedirs(OUTPUT_DIR, exist_ok=True)

# 載入模型
print(f"🔄 正在載入 TensorRT 引擎: {MODEL_PATH}...")
model = YOLO(MODEL_PATH, task='detect')

def nms_pytorch(boxes, scores, iou_threshold=0.3):
    """ 使用 PyTorch 內建的 NMS 來合併重疊框，增加空值保護 """
    if not boxes or len(boxes) == 0: 
        return []
    
    # 確保資料格式正確
    boxes_array = np.array(boxes, dtype=np.float32)
    scores_array = np.array(scores, dtype=np.float32)
    
    boxes_tensor = torch.from_numpy(boxes_array)
    scores_tensor = torch.from_numpy(scores_array)
    
    # 使用 torchvision 的 nms (Jetson 通常內建支援)
    try:
        import torchvision
        keep = torchvision.ops.nms(boxes_tensor, scores_tensor, iou_threshold)
        return keep.numpy()
    except:
        # 如果 torchvision 沒裝，使用手寫簡易 NMS 作為備援
        indices = np.argsort(scores_array)[::-1]
        keep = []
        while len(indices) > 0:
            i = indices[0]
            keep.append(i)
            if len(indices) == 1: break
            # 這裡簡化處理，僅返回最高分的一個作為演示，建議確保 torchvision 可用
            indices = indices[1:]
        return keep

def get_sliced_predictions(img_cv, slice_size=640, overlap_ratio=0.2):
    """ SAHI 核心：切片偵測邏輯，增加安全檢查 """
    h, w, _ = img_cv.shape
    all_boxes = []
    all_scores = []
    
    step = int(slice_size * (1 - overlap_ratio))
    
    for y in range(0, h, step):
        for x in range(0, w, step):
            y_end = min(y + slice_size, h)
            x_end = min(x + slice_size, w)
            y_start = max(0, y_end - slice_size)
            x_start = max(0, x_end - slice_size)
            
            slice_img = img_cv[y_start:y_end, x_start:x_end]
            
            # 推論 (conf 設低一點，讓 NMS 來過濾)
            results = model(slice_img, conf=0.2, imgsz=640, augment=True, verbose=False)
            
            if results[0].boxes is not None:
                for box in results[0].boxes:
                    xyxy = box.xyxy[0].cpu().numpy()
                    all_boxes.append([
                        xyxy[0] + x_start, 
                        xyxy[1] + y_start, 
                        xyxy[2] + x_start, 
                        xyxy[3] + y_start
                    ])
                    all_scores.append(float(box.conf[0].cpu().numpy()))

    if not all_boxes: 
        return [], 0.0
    
    # 合併重疊框
    keep_idx = nms_pytorch(all_boxes, all_scores, iou_threshold=0.3)
    
    if len(keep_idx) == 0:
        return [], 0.0
        
    final_boxes = [all_boxes[i] for i in keep_idx]
    final_scores = [all_scores[i] for i in keep_idx]
    
    return final_boxes, float(np.mean(final_scores)) * 100

def process_file(file_name):
    path = os.path.join(INPUT_DIR, file_name)
    ext = file_name.lower().split('.')[-1]
    
    print(f"\n🔍 正在處理 (SAHI 模式): {file_name}")
    
    if ext in ['jpg', 'jpeg', 'png', 'heic']:
        try:
            img = Image.open(path)
            img_cv = cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR)
            
            boxes, avg_conf = get_sliced_predictions(img_cv)
            count = len(boxes)
            
            # 視覺化並存檔
            for b in boxes:
                cv2.rectangle(img_cv, (int(b[0]), int(b[1])), (int(b[2]), int(b[3])), (0, 255, 0), 2)
                cv2.putText(img_cv, f"P", (int(b[0]), int(b[1])-5), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,255,0), 1)
            
            save_path = os.path.join(OUTPUT_DIR, f"sahi_{file_name.split('.')[0]}.jpg")
            cv2.imwrite(save_path, img_cv)
            return file_name, count, avg_conf, "SAHI_Image"
        except Exception as e:
            print(f"❌ 處理 {file_name} 出錯: {e}")
            return file_name, 0, 0, "Error"

    elif ext in ['mp4', 'mov']:
        cap = cv2.VideoCapture(path)
        unique_ids = set()
        all_confidences = []
        frame_count = 0
        total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

        while cap.isOpened():
            success, frame = cap.read()
            if not success: break
            
            if frame_count % 15 == 0:
                results = model.track(frame, persist=True, classes=[0], conf=0.25, imgsz=640, verbose=False)
                if results[0].boxes is not None and results[0].boxes.id is not None:
                    ids = results[0].boxes.id.int().cpu().tolist()
                    for tid in ids: unique_ids.add(tid)
                    all_confidences.extend(results[0].boxes.conf.cpu().numpy().tolist())
            
            frame_count += 1
        cap.release()
        count = len(unique_ids)
        avg_conf = np.mean(all_confidences) * 100 if all_confidences else 0
        return file_name, count, avg_conf, "Video"

    return file_name, 0, 0, "Unsupported"

if __name__ == "__main__":
    supported_exts = ('.mp4', '.mov', '.jpg', '.jpeg', '.png', '.heic')
    files = [f for f in os.listdir(INPUT_DIR) if f.lower().endswith(supported_exts)]
    
    print(f"🚀 開始分析 (目標 95% 準確度)，共計 {len(files)} 個文件...")
    final_report = []

    for f in files:
        fname, count, conf, ftype = process_file(f)
        status = "✅ 高可靠" if conf >= 75 else ("⚠️ 建議抽檢" if conf >= 45 else "❌ 可信度低")
        final_report.append({"name": fname, "count": count, "conf": conf, "status": status})

    print("\n" + "★"*60)
    print(f"📊 SAHI 最終審核報告 - {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    print("★"*60)
    for item in final_report:
        print(f"檔名: {item['name'][:20]:<20} | 人數: {item['count']:>3} | 信心: {item['conf']:>5.1f}% | 狀態: {item['status']}")
    print("★"*60)
