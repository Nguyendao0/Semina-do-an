# database.py (SQLite version)

import sqlite3
from datetime import datetime
import os

DB_DIR = "data"
DB_PATH = os.path.join(DB_DIR, "history.db")

# -------------------------
# 1. Khởi tạo Database SQLite
# -------------------------
def init_db():
    # Tạo thư mục data nếu chưa tồn tại
    if not os.path.exists(DB_DIR):
        os.makedirs(DB_DIR)

    # Kết nối & tạo bảng
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # Tạo bảng history nếu chưa tồn tại
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            text TEXT NOT NULL,
            sentiment TEXT NOT NULL,
            score REAL DEFAULT 0.0,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    conn.commit()
    conn.close()


# -------------------------
# 2. Lưu 1 entry lịch sử
# -------------------------
def save_history(text, sentiment, score=0.0):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    cursor.execute('''
        INSERT INTO history (text, sentiment, score, created_at)
        VALUES (?, ?, ?, ?)
    ''', (text, sentiment, round(score, 4), timestamp))
    
    conn.commit()
    conn.close()


# -------------------------
# 3. Lấy toàn bộ lịch sử
# -------------------------
def get_history():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row  # Trả về dict thay vì tuple
    cursor = conn.cursor()
    
    # Lấy dữ liệu mới nhất trước
    cursor.execute('''
        SELECT id, text, sentiment, score, created_at
        FROM history
        ORDER BY id DESC
    ''')
    
    rows = cursor.fetchall()
    conn.close()
    
    # Convert sqlite3.Row thành dict để dùng với pandas
    return [dict(row) for row in rows]


# -------------------------
# 4. Xóa toàn bộ lịch sử
# -------------------------

def clear_history():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("DELETE FROM history")   # xóa toàn bộ dữ liệu
    conn.commit()

    cursor.execute("VACUUM")  # dọn file DB để giảm dung lượng (không bắt buộc)
    conn.commit()

    conn.close()



# Khởi tạo database khi import module
init_db()
