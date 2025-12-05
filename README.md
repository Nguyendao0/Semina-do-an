# Trợ lý Phân Loại Cảm Xúc Tiếng Việt

Ứng dụng web dùng **PhoBERT** để phân loại cảm xúc câu tiếng Việt thành: **POSITIVE** (Tích cực), **NEGATIVE** (Tiêu cực), hoặc **NEUTRAL** (Trung tính).

---

## Yêu Cầu Hệ Thống

- **Python *3.10.11** ([Tải tại đây](https://www.python.org/))
- **Git** (để clone repo)
- **RAM**: Tối thiểu 4GB (model PhoBERT khá nặng)

---

## Hướng Dẫn Cài Đặt & Chạy (Quickstart)

### **Cách 1: chạy file run_app.bat**
### **Bước 1: Clone Repository**
```bash
git clone https://github.com/Nguyendao0/Semina-do-an.git
cd Semina-do-an
```
### **Bước 2: chạy run_app.bat**
Mở thư mục Semina-do-an
Nháy đúp chuột file run_app.bat

### **Cách 2: chạy ứng dụng từng bước **
### **Bước 1: Clone Repository**
```bash
git clone https://github.com/Nguyendao0/Semina-do-an.git
cd Semina-do-an
```

### **Bước 2: Tạo Môi Trường Ảo (Virtual Environment)**
```bash
# Windows (PowerShell)
python -m venv venv
.\venv\Scripts\Activate.ps1

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

### **Bước 3: Cài Đặt Dependencies**
```bash
pip install -r requirements.txt
```
**Lưu ý:** Lần đầu sẽ mất **5-10 phút** do tải model PhoBERT (~1.5GB)

### **Bước 4: Chạy Ứng Dụng**
```bash
streamlit run app.py
```

Ứng dụng sẽ tự mở tại: `http://localhost:8501`

---

## 📁 Cấu Trúc Dự Án

```
Semina-do-an/
├── app.py                 # 🎨 Giao diện Streamlit (UI chính)
├── analyzer.py            # 🧠 Hàm tổng hợp phân tích
├── classifier.py          # 🤖 Model PhoBERT
├── preprocess.py          # 📝 Tiền xử lý text
├── postprocess.py         # ✅ Kiểm tra input
├── database.py            # 💾 Lưu lịch sử (SQLite)
├── test.py                # 🧪 File test
├── requirements.txt       # 📦 Danh sách dependencies
├── data/                  # 📂 Thư mục lưu trữ
│   └── history.db         # 📋 Database lịch sử (SQLite)
└── README.md              # 📖 File này
```

---

## 🔄 Luồng Hoạt Động

```
       [Nhập câu Tiếng Việt]
              ↓
    ┌─────────────────────────┐
    │  1. PREPROCESS (Tiền xử lý) │
    │  • Chuyển thường         │
    │  • Chuẩn hóa teencode    │
    │  • Xóa ký tự đặc biệt   │
    │  • Tokenize từ          │
    └─────────────────────────┘
              ↓
    ┌─────────────────────────┐
    │  2. CLASSIFY (Phân loại) │
    │  • Model: PhoBERT       │
    │  • Output: POSITIVE/    │
    │    NEGATIVE/NEUTRAL     │
    └─────────────────────────┘
              ↓
    ┌─────────────────────────┐
    │  3. POSTPROCESS (Hậu xử lý)│
    │  • Validate input       │
    │  • Adjust by score      │
    │  • Format output        │
    └─────────────────────────┘
              ↓
    [Hiển thị kết quả + Lưu lịch sử]
```

---

## 💡 Cách Sử Dụng

### **1. Phân Loại Cảm Xúc**
- Gõ câu tiếng Việt vào ô input
- **Ấn Enter** hoặc click **"Phân loại cảm xúc"**
- Xem kết quả với biểu tượng & độ tin cậy (%)

**Ví dụ:**
```
Input:  "Tôi rất vui hôm nay"
Output: 🎉 Cảm xúc: POSITIVE (Độ tin cậy: 95.30%)
```

### **2. Xem Lịch Sử**
- Mỗi lần phân loại sẽ lưu vào database SQLite
- Bảng hiển thị: **Nội dung** → **Kết quả** → **Thời gian** → **Điểm số**
- Tự động lưu vào file `data/history.db`
- Click **🗑️ Xóa toàn bộ lịch sử** để xóa (có xác nhận)

---

## 📄 License

MIT License - Tự do sử dụng & sửa đổi
