from fastapi import FastAPI
from fastapi.responses import HTMLResponse, FileResponse
import sqlite3
import os
from datetime import datetime

app = FastAPI()

# 取得最新的 PDF 檔名
def get_latest_report():
    today = datetime.now().strftime('%Y%m%d')
    # 優先尋找深度分析報告
    detailed_file = f"Report_{today}_Detailed.pdf"
    basic_file = f"Report_{today}.pdf"
    
    if os.path.exists(detailed_file):
        return detailed_file
    elif os.path.exists(basic_file):
        return basic_file
    return None

@app.get("/", response_class=HTMLResponse)
async def dashboard():
    conn = sqlite3.connect('mall_data.db')
    cursor = conn.cursor()
    cursor.execute("SELECT SUM(in_count), SUM(out_count) FROM hourly_stats")
    res = cursor.fetchone()
    total_in = res[0] if res[0] else 0
    total_out = res[1] if res[1] else 0
    conn.close()

    report_file = get_latest_report()
    # 如果有報告，顯示下載連結；否則顯示提示
    download_btn = f'<a href="/download_report" style="padding:10px 20px; background:#007bff; color:white; text-decoration:none; border-radius:5px;">Download Daily Report (PDF)</a>' if report_file else '<p style="color:gray;">Today\'s report is generating (Available at 06:00)</p>'

    return f"""
    <html>
        <head>
            <title>Mall Traffic Admin</title>
            <style>
                body {{ font-family: sans-serif; text-align: center; background: #f8f9fa; padding-top: 50px; }}
                .box {{ padding: 30px; border: 1px solid #ddd; display: inline-block; background: white; border-radius: 10px; box-shadow: 0 4px 6px rgba(0,0,0,0.1); margin: 10px; min-width: 150px; }}
                h1 {{ color: #333; }}
                .stat-num {{ font-size: 48px; font-weight: bold; margin: 10px 0; }}
            </style>
        </head>
        <body>
            <h1>🏢 Mall Traffic Analytics Dashboard</h1>
            <div class='box'><h2>Total IN</h2><p class='stat-num' style='color:#28a745;'>{total_in}</p></div>
            <div class='box'><h2>Total OUT</h2><p class='stat-num' style='color:#dc3545;'>{total_out}</p></div>
            <br><br><br>
            {download_btn}
        </body>
    </html>
    """

# 真正處理下載的路由
@app.get("/download_report")
async def download_report():
    report_file = get_latest_report()
    if report_file:
        return FileResponse(path=report_file, filename=report_file, media_type='application/pdf')
    return {"error": "Report not found"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
