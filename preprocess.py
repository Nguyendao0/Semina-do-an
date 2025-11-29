# preprocess.py
import re
from underthesea import word_tokenize

# -------------------------------
# 1. Từ điển Teencode (Từ điển nhỏ 10-20 từ theo yêu cầu đồ án)
# -------------------------------
TEENCODE_DICT = {
    "mk": "mình",
    "mik": "mình",
    "dc": "được",
    "đc": "được",
    "ko": "không",
    "kg": "không",
    "hok": "không",
    "nt": "nhắn tin",
    "thic": "thích",
    "thich": "thích",
    "iu": "yêu",
    "rat": "rất",
    "wa": "quá",
    "wá": "quá",
    "h": "giờ",
    "gd": "gia đình",
    "vk": "vợ",
    "ck": "chồng",
    "ox": "ông xã",
    "bx": "bà xã",
    "bth": "bình thường",
    "buon": "buồn",
    "vuii": "vui"
}

# -------------------------------
# 2. Các hàm xử lý thành phần
# -------------------------------

def lowercase_text(text: str) -> str:
    """Chuyển toàn bộ văn bản về chữ thường."""
    return text.lower().strip()

def normalize_teencode(text: str) -> str:
    """Thay thế các từ viết tắt bằng từ đầy đủ."""
    words = text.split()
    # Duyệt qua từng từ, nếu có trong từ điển thì thay thế
    new_words = [TEENCODE_DICT.get(word, word) for word in words]
    return " ".join(new_words)

def remove_unnecessary_characters(text: str) -> str:
    """Loại bỏ ký tự đặc biệt không cần thiết, giữ lại dấu câu cơ bản."""
    # Chỉ giữ lại chữ cái, số và các dấu câu thông dụng (. , ? !)
    text = re.sub(r'[^\w\s.,?!]', ' ', text)
    text = re.sub(r'\s+', ' ', text).strip() # Xóa khoảng trắng thừa
    return text

def tokenize_vietnamese(text: str) -> str:
    """
    Tách từ tiếng Việt chuẩn cho PhoBERT.
    Sử dụng format="text" để nối từ ghép bằng "_".
    VD: "rất vui" -> "rất_vui"
    """
    return word_tokenize(text, format="text")

# -------------------------------
# 3. Hàm Preprocess Tổng Hợp (Main Pipeline)
# -------------------------------
def preprocess_text(text: str) -> str:
    """
    Hàm chính để gọi từ bên ngoài.
    Thứ tự: Lowercase -> Teencode -> Clean Rác -> Tokenize
    """
    if not text:
        return ""
    
    # Bước 1: Chuyển thường
    text = lowercase_text(text)
    
    # Bước 2: Chuẩn hóa Teencode
    text = normalize_teencode(text)
    
    # Bước 3: Xóa ký tự lạ (Optional - giữ lại dấu câu để model hiểu cảm xúc)
    text = remove_unnecessary_characters(text)
    
    # Bước 4: Tách từ (QUAN TRỌNG NHẤT)
    text = tokenize_vietnamese(text)
    
    return text

# --- Block kiểm thử (Chỉ chạy khi bạn run trực tiếp file này) ---
if __name__ == "__main__":
    print("--- TEST MODULE PREPROCESS ---")
    samples = [
        "Hôm nay mk rat vui",           # Test teencode + không dấu
        "San pham nay dung ko tot!!!",  # Test teencode + dấu câu
        "Món ăn dở wa trơi oi",         # Test teencode
        "Giao hàng chậm, thái độ lồi lõm" # Test từ ghép (lồi lõm)
    ]

    for s in samples:
        print(f"Gốc:   {s}")
        print(f"Xử lý: {preprocess_text(s)}")
        print("-" * 30)