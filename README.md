# 🏢 Mall-Insight: Edge AI Traffic Analytics System

基於 NVIDIA Jetson Nano 的商場人流即時監控與夜間批次分析系統。

## 🌟 核心功能 (Key Features)
- **Real-time Detection**: 使用 YOLOv11s + TensorRT (FP16) 實現 20+ FPS 偵測。
- **ByteTrack**: 穩定的多目標追蹤，精準統計 IN/OUT 人流量。
- **Nightly Batch Processing**: 凌晨自動分析全日錄影，提取停留時長與擁擠數據。
- **Spatial Analytics**: 生成空間熱圖 (Heatmap) 識別商場擁擠區域。
- **Automated Reporting**: 每日 06:00 自動生成包含建議的 PDF 專業報表。
- **Web Dashboard**: 透過 FastAPI 提供即時數據與報表下載介面。

## 🛠️ 技術棧 (Tech Stack)
- **Hardware**: NVIDIA Jetson Nano, IMX219 CSI Camera.
- **AI Framework**: Ultralytics YOLOv11, TensorRT.
- **Backend**: Python, FastAPI, SQLite3.
- **Reporting**: ReportLab, Matplotlib, Seaborn.
- **Automation**: Linux Cron Jobs.

## 🚀 快速啟動
1. 安裝依賴: `pip3 install -r requirements.txt`
2. 啟動系統: `./start_all.sh`
3. 訪問 Web UI: `http://<jetson-ip>:8000`

## 📊 數據範例
系統生成的 PDF 報表包含：
- 客流量峰值分析
- 平均停留時間 (Dwell Time)
- 擁擠警告與消防逃生優化建議
