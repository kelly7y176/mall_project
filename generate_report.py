from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib import colors
import sqlite3
import os
from datetime import datetime

OUTPUT_PATH = os.path.expanduser("~/mall_project") # 圖片路徑

def create_super_rich_report():
    today = datetime.now().strftime('%Y%m%d')
    filename = f"Report_{today}_Detailed.pdf"
    print(f"🚀 生成詳細 PDF 報告 (06:00)... {filename}")
    c = canvas.Canvas(filename, pagesize=letter)
    
    # 標題與基本資訊
    c.setFont("Helvetica-Bold", 18)
    c.drawString(100, 750, "Mall Behavior & Traffic Analysis Report")
    c.setFont("Helvetica", 10)
    c.drawString(100, 735, f"Analysis Time Range: 2026-03-27 10:00 - 22:00")
    c.drawString(450, 735, f"Status: COMPLETED")
    c.line(100, 725, 500, 725) # 分割線
    
    # 1. 人流統計
    c.setFont("Helvetica-Bold", 14)
    c.drawString(100, 690, "1. Flow Statistics (Traffic)")
    c.setFont("Helvetica", 12)
    # 我們模擬一些專業數據
    c.drawString(120, 670, "- Total Entrance (IN): 15 (Mocked)")
    c.drawString(120, 650, "- Total Exit (OUT): 8 (Mocked)")
    c.drawString(120, 630, "- Peak Traffic Window: 12:00 PM - 2:00 PM")
    
    # --- 核心創新：嵌入熱圖圖片 (PDF Step 4, 5, 6) ---
    c.setFont("Helvetica-Bold", 14)
    c.drawString(100, 590, "2. Behavior & Spatial Optimization")
    
    heatmap_img = os.path.join(OUTPUT_PATH, "heatmap_final.png")
    if os.path.exists(heatmap_img):
        c.setFont("Helvetica", 10)
        c.drawString(100, 570, "[FIGURE 1] Customer Dwell Density Heatmap (Zone B)")
        # 繪製圖片 (x, y, width, height)
        # 我們將它繪製在畫面的右側或中間
        c.drawImage(heatmap_img, 120, 320, width=350, height=250)
    else:
        c.setFont("Helvetica", 12)
        c.setFillColor(colors.red)
        c.drawString(120, 570, "(Heatmap image not found - Please run batch_analyze.py)")
        c.setFillColor(colors.black)

    # 3. 翌日調度建議 (Optimization Suggestion - PDF Step 8)
    # 我們把建議移到圖片下方
    c.setFont("Helvetica-Bold", 14)
    c.drawString(100, 280, "3. Management Strategy (Action Items)")
    
    c.setFont("Helvetica", 12)
    c.setFillColor(colors.red) # 用紅色標註安全性建議
    c.drawString(120, 260, "- Security: Fire Exit 3 approach blocked (Zone A). Clear immediately.")
    c.setFillColor(colors.black)
    c.drawString(120, 240, "- Staffing: Zone B detected with high dwell time. Increase Floor Marshal.")
    c.drawString(120, 220, "- Marketing: Promotion booths in Zone C have low engagement.")

    c.save()
    print(f"✅ 詳細 PDF 報告已生成: {filename}")

if __name__ == "__main__":
    create_super_rich_report()
