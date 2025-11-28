# Semina-do-an

#Clone dự án
....
# Tạo môi trường ảo với tên là 'venv'
python -m venv venv
# Kích hoạt môi trường ảo
venv\Scripts\activate
# Cài môi trường:
pip install -r requirements.txt

luồng hoạt động
                   [Câu tiếng Việt]
                           |
                           v
                ┌────────────────────┐
                │  1. Preprocessing  │
                │ - Chuẩn hóa Unicode│
                │ - Viết thường      │
                │ - Xử lý viết tắt   │
                │ - Tokenize (optional)│
                └────────────────────┘
                           |
                           v
            ┌────────────────────────────┐
            │ 2. Transformer Sentiment   │
            │  - POSITIVE / NEUTRAL / NEGATIVE│
            └────────────────────────────┘
                           |
                           v
                ┌─────────────────────┐
                │ 3. Postprocessing   │
                │ - Validation        │
                │ - Score <0.5 → Neutral│
                │ - Tạo dictionary    │
                └─────────────────────┘
                           |
                           v
               [Output: {text, sentiment}]
                           |
                           v
                  Lưu SQLite + Hiển thị UI
