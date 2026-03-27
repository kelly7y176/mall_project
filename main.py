import cv2
import sqlite3
import os
import time
from ultralytics import YOLO

# 設定
RECORD_PATH = os.path.expanduser("~/mall_project/data/recordings")
os.makedirs(RECORD_PATH, exist_ok=True)
model = YOLO("yolo11s.engine", task='detect')
cap = cv2.VideoCapture("test_video.mp4") # 實測時改回 gstreamer_pipeline(0)

# 變數
line_y = 300
track_history = {}
min_in, min_out = 0, 0 # 每分鐘計數
last_min_time = time.time()
video_writer = None
file_start_time = 0

def get_new_video_writer(frame, cam_id=0):
    t = time.localtime()
    start_str = time.strftime("%H%M", t)
    # 預估 10 分鐘後的結束時間
    end_str = time.strftime("%H%M", time.localtime(time.time() + 600))
    filename = os.path.join(RECORD_PATH, f"cam{cam_id}_{start_str}-{end_str}.mp4")
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    return cv2.VideoWriter(filename, fourcc, 20.0, (frame.shape[1], frame.shape[0])), time.time()

def save_min_stats(cam_id, in_c, out_c):
    conn = sqlite3.connect('mall_data.db')
    conn.execute('INSERT INTO hourly_stats (cam_id, in_count, out_count) VALUES (?, ?, ?)', (cam_id, in_c, out_c))
    conn.commit()
    conn.close()

try:
    while cap.isOpened():
        success, frame = cap.read()
        if not success: break
        
        # 1. AI 偵測
        results = model.track(frame, persist=True, classes=[0], verbose=False)
        annotated_frame = results[0].plot()
        
        # 2. 每分鐘結算邏輯 (PDF 3.2 Step 4)
        if time.time() - last_min_time > 60:
            save_min_stats(0, min_in, min_out)
            min_in, min_out = 0, 0
            last_min_time = time.time()

        # 3. 過線判定
        if results[0].boxes.id is not None:
            for box, track_id in zip(results[0].boxes.xywh.cpu(), results[0].boxes.id.int().cpu().tolist()):
                y_center = float(box[1])
                prev_y = track_history.get(track_id, y_center)
                if prev_y < line_y and y_center >= line_y:
                    min_in += 1
                elif prev_y > line_y and y_center <= line_y:
                    min_out += 1
                track_history[track_id] = y_center

        # 4. 符合規格的錄影 (PDF 3.2 Step 5)
        if video_writer is None or (time.time() - file_start_time) > 600:
            if video_writer: video_writer.release()
            video_writer, file_start_time = get_new_video_writer(annotated_frame, 0)
        
        video_writer.write(annotated_frame)
        cv2.imshow("Jetson Daily Mode", annotated_frame)
        if cv2.waitKey(1) & 0xFF == ord("q"): break
finally:
    if video_writer: video_writer.release()
    cap.release()
    cv2.destroyAllWindows()
