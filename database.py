# database.py (JSON version)

import json
from datetime import datetime
import os

DB_PATH = "data/history.json"

# -------------------------
# 1. Khởi tạo file JSON
# -------------------------
def init_db():
    # Nếu chưa có file, tạo file rỗng dạng list
    if not os.path.exists("data"):
        os.makedirs("data")

    if not os.path.exists(DB_PATH):
        with open(DB_PATH, "w", encoding="utf-8") as f:
            json.dump([], f, ensure_ascii=False, indent=4)


# -------------------------
# 2. Lưu 1 entry lịch sử
# -------------------------
def save_history(text, sentiment, score=0.0):
    # Đọc dữ liệu hiện tại
    with open(DB_PATH, "r", encoding="utf-8") as f:
        data = json.load(f)

    # Tạo bản ghi mới
    record = {
        "text": text,
        "sentiment": sentiment,
        "score": round(score, 4),  # Làm tròn 4 chữ số
        "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }

    # Thêm vào danh sách
    data.append(record)

    # Ghi lại file
    with open(DB_PATH, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)


# -------------------------
# 3. Lấy toàn bộ lịch sử
# -------------------------
def get_history():
    with open(DB_PATH, "r", encoding="utf-8") as f:
        data = json.load(f)

    # Đảo ngược để hiện bản mới nhất trước
    return list(reversed(data))


# Khởi tạo file JSON khi import module
init_db()
