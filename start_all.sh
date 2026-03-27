#!/bin/bash
echo "🚀 啟動商場人流監控系統..."
python3 main.py & 
python3 web_server.py &
echo "✅ 系統已在後台運行。"
