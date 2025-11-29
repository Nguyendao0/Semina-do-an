# test.py - PHIÊN BẢN TÍCH HỢP HOÀN CHỈNH
from preprocess import preprocess_text
from classifier import SentimentClassifier

print("🚀 Đang khởi động hệ thống AI...")
# Khởi tạo bộ phân loại (Chỉ cần load 1 lần duy nhất)
clf = SentimentClassifier()

# Danh sách các câu test "khó nhằn"
test_cases = [
    "San pham nay dung ko tot chút nào.",  # Teencode + Tiêu cực
    "Món ăn ngon xuat sac, se quay lai",   # Teencode + Không dấu + Tích cực
    "Giao hàng binh thuong, tam on",       # Trung tính
    "hàng dở tệ, phí tiền",                # Tiêu cực mạnh
    "Shop phục vụ nhiệt tình, 10 điểm"     # Tích cực mạnh
]

print("\n" + "="*60)
print(f"{'CÂU GỐC':<40} | {'PREPROCESS':<30} | {'KẾT QUẢ'}")
print("="*60)

for text in test_cases:
    # BƯỚC 1: Tiền xử lý (Ngày 2)
    processed_text = preprocess_text(text)
    
    # BƯỚC 2: Phân loại (Ngày 3)
    result = clf.predict(processed_text)
    
    label = result['label']
    score = result['score']
    
    # In ra bảng kết quả đẹp mắt
    # Cắt ngắn text nếu dài quá để bảng không bị vỡ
    display_text = (text[:35] + '..') if len(text) > 35 else text
    display_proc = (processed_text[:25] + '..') if len(processed_text) > 25 else processed_text
    
    print(f"{display_text:<40} | {display_proc:<30} | {label} ({score})")

print("="*60)