import sqlite3

conn = sqlite3.connect('mall_data.db')
cursor = conn.cursor()

# 1. 原始事件表 (包含相機 ID)
cursor.execute('''
CREATE TABLE IF NOT EXISTS count_events (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
    cam_id INTEGER,
    direction TEXT,
    track_id INTEGER
)
''')

# 2. 每分鐘統計表 (PDF 3.2 步驟 4 要求)
cursor.execute('''
CREATE TABLE IF NOT EXISTS hourly_stats (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    stat_time DATETIME DEFAULT CURRENT_TIMESTAMP,
    cam_id INTEGER,
    in_count INTEGER,
    out_count INTEGER
)
''')

conn.commit()
conn.close()
print("Database Schema Upgraded!")
