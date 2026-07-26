# 🏢 Mall-Insight: Edge AI Traffic Analytics System

An advanced, edge-computing traffic monitoring and nightly batch analytics system tailored for retail environments, fully optimized for deployment on NVIDIA Jetson Nano.

## 🌟 Key Features

- **Real-time Edge Detection**: Leverages YOLOv11s and TensorRT (FP16 quantized) to achieve highly optimized inference speeds of 20+ FPS on edge hardware.
- **Multi-Object Tracking**: Integrates the ByteTrack algorithm for stable multi-target correlation, ensuring high-precision metrics for bidirectional (IN/OUT) foot traffic tracking.
- **Nightly Batch Processing**: Automates post-business hours video processing via background cron jobs to extract critical business intelligence, including customer dwell-time dynamics and congestion patterns.
- **Spatial Heatmap Analytics**: Generates advanced 2D spatial heatmaps to dynamically visualize and isolate localized high-density congestion hotspots within commercial layouts.
- **Automated Reporting Pipeline**: Deploys a scheduled execution framework that automatically compiles comprehensive, production-grade PDF analytical reports with actionable design recommendations every morning at 06:00.
- **Intelligent Web Dashboard**: Features a high-performance Web UI powered by FastAPI to deliver concurrent real-time data streaming and instant analytical report downloads.
- **Advanced Zone Counting (PoC)**: Integrated Roboflow Supervision to feature custom virtual polygon zones for real-time spatial traffic hotspot tracking & analytics.

## 🛠️ Tech Stack

- **Edge Hardware**: NVIDIA Jetson Nano, IMX219 CSI Camera Module.
- **AI & Computer Vision**: Ultralytics YOLOv11, NVIDIA TensorRT Execution Framework.
- **Backend Architecture**: Python, FastAPI Async Framework, SQLite3.
- **Data Visualization & Reporting**: ReportLab PDF Engine, Matplotlib, Seaborn.
- **System Automation**: Linux Native Cron Utilities.

## 🚀 Quick Start

1. **Install Dependencies**: 
   ```bash
   pip3 install -r requirements.txt
   ```
2. **Execute System Deployment**: 
   ```bash
   ./start_all.sh
   ```
3. **Access Web Interface**: Open your browser and navigate to `http://<jetson-ip>:8000`

## 📊 Analytics & Reporting Samples

The dynamically generated PDF business intelligence reports encompass:
- Peak traffic hourly distribution and bottleneck identification.
- Precision metrics for average customer dwell time across target retail zones.
- Real-time density warning indicators and specialized fire safety routing optimizations.
