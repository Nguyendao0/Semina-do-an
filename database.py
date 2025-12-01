# database.py
import sqlite3
from datetime import datetime
import os

DB_PATH = "data/history.db"

# Tạo thư mục data nếu chưa tồn tại
os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)

def init_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    # Tạo bảng history gồm: id, câu gốc, kết quả, điểm số, thời gian
    c.execute('''
        CREATE TABLE IF NOT EXISTS history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            text TEXT,
            sentiment TEXT,
            score REAL,
            created_at TIMESTAMP
        )
    ''')
    conn.commit()
    conn.close()

def save_history(text, sentiment, score=0.0):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    cursor.execute(
        "INSERT INTO history(text, sentiment, score, created_at) VALUES (?, ?, ?, ?)",
        (text, sentiment, score, timestamp)
    )

    conn.commit()
    conn.close()

def get_history():
    
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM history ORDER BY id DESC")

    rows = cursor.fetchall()
    conn.close()

    return rows

# Tạo DB ngay khi import
init_db()