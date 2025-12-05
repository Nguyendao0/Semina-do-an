

# 1. Validation input

def validate_input(text: str):
    """
    Kiểm tra:
    - Câu quá ngắn
    - Câu rỗng
    """
    if not text or len(text.strip()) == 0:
        return False, "Câu nhập vào đang trống!"

    if len(text.strip()) < 2:
        return False, "Câu quá ngắn, vui lòng nhập dài hơn!"
    
    if len(text.strip()) > 500:
        return False, "Câu quá dài, tối đa 500 ký tự."
    
    if all(c in "!?.,;: \n\t" for c in text.strip()):
        return False, "Vui lòng nhập text có ý nghĩa, không phải toàn dấu câu!"
    
    return True, None


# 2. Chuẩn hóa nhãn PhoBERT

def normalize_label(label_id: int) -> str:
    """
    PhoBERT-base-v2 (Sentiment) thường trả về:
    0 = NEGATIVE
    1 = NEUTRAL
    2 = POSITIVE
    """
    if label_id == 0:
        return "NEGATIVE"
    elif label_id == 1:
        return "NEUTRAL"
    else:
        return "POSITIVE"


# 3. Áp dụng logic theo confidence score

def adjust_by_score(sentiment: str, score: float) -> str:
    """
    Nếu độ tự tin thấp, chuyển sang NEUTRAL
    - Điều kiện thường dùng: score < 0.5
    """
    if score < 0.5:
        return "NEUTRAL"
    return sentiment


# 4. Tạo dictionary đầu ra chuẩn

def build_output(original_text: str, sentiment: str):
    return {
        "text": original_text,
        "sentiment": sentiment
    }


# 5. HÀM TỔNG HỢP POSTPROCESSING

def postprocess(original_text: str, label_id: int, score: float):
    # 1. Chuẩn hóa nhãn từ PhoBERT
    sentiment = normalize_label(label_id)

    # 2. Điều chỉnh dựa theo confidence score
    sentiment = adjust_by_score(sentiment, score)

    # 3. Tạo output dictionary
    output = build_output(original_text, sentiment)

    return output
