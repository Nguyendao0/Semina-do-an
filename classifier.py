# app/classifier.py
from transformers import pipeline

class SentimentClassifier:
    # Hằng số giới hạn độ dài text
    MIN_TEXT_LENGTH = 1      # Ít nhất 1 ký tự
    MAX_TEXT_LENGTH = 100    # Tối đa 100 ký tự
    
    def __init__(self):
        # --- LÝ DO CHỌN MODEL NÀY ---
        # Thay vì dùng 'vinai/phobert-base-v2' (chưa biết phân loại cảm xúc),
        # ta dùng model của 'wonrax'. Đây thực chất là PhoBERT nhưng đã được
        # dạy trước (fine-tuned) hàng ngàn câu review tiếng Việt.
        # -> Giúp đạt độ chính xác > 80% ngay lập tức mà không cần train lại.
        self.model_name = "wonrax/phobert-base-vietnamese-sentiment"
        
        print(f"⏳ Đang tải model {self.model_name}...")
        
        # --- TẠI SAO DÙNG PIPELINE? ---
        # Pipeline là công cụ "mì ăn liền" của Hugging Face.
        # Nó tự động làm 3 việc:
        # 1. Tokenize (biến chữ thành số)
        # 2. Model Inference (chạy mô hình)
        # 3. Post-processing (biến kết quả số thành nhãn POS/NEG)
        self.pipe = pipeline("sentiment-analysis", model=self.model_name)
        print("✅ Đã tải model thành công!")

    def check_text_length(self, text: str) -> dict:
        """
        Kiểm tra độ dài của text có hợp lệ không.
        """
        text_stripped = text.strip()
        text_length = len(text_stripped)
        
        if text_length < self.MIN_TEXT_LENGTH:
            return {
                'is_valid': False,
                'message': f'❌ Text quá ngắn! Tối thiểu {self.MIN_TEXT_LENGTH} ký tự (hiện tại: {text_length})',
                'length': text_length
            }
        
        if text_length > self.MAX_TEXT_LENGTH:
            return {
                'is_valid': False,
                'message': f'❌ Text quá dài! Tối đa {self.MAX_TEXT_LENGTH} ký tự (hiện tại: {text_length})',
                'length': text_length
            }
        
        return {
            'is_valid': True,
            'message': f'✅ Độ dài hợp lệ ({text_length} ký tự)',
            'length': text_length
        }

    def predict(self, text):
        """
        Input: Câu tiếng Việt (đã qua xử lý ở preprocess.py)
        Output: Dictionary {label, score}
        """
        # Kiểm tra độ dài text
        length_check = self.check_text_length(text)
        if not length_check['is_valid']:
            print(length_check['message'])
            return {"label": "ERROR", "score": 0.0, "error": length_check['message']}

        try:
            # Gọi pipeline để dự đoán
            # Model trả về dạng list: [{'label': 'POS', 'score': 0.99}, {'label': 'NEG', 'score': 0.01}]
            output = self.pipe(text)
            
            # Lấy kết quả có điểm số cao nhất
            # Dòng này tương đương việc chọn xem model tin vào nhãn nào nhất
            result = output[0] 
            
            raw_label = result['label'] # Ví dụ: 'POS'
            score = result['score']     # Ví dụ: 0.98

            # --- TẠI SAO PHẢI CÓ ĐOẠN IF-ELSE NÀY? ---
            # Model trả về 'POS'/'NEG'/'NEU' (ngôn ngữ của model).
            # Nhưng Đề Bài yêu cầu trả về 'POSITIVE'/'NEGATIVE' (ngôn ngữ của đề bài).
            # -> Ta cần lớp "phiên dịch" (Mapping) này.
            
            final_label = "NEUTRAL" # Mặc định là trung tính cho an toàn
            
            if raw_label == 'POS':
                final_label = "POSITIVE"
            elif raw_label == 'NEG':
                final_label = "NEGATIVE"
            elif raw_label == 'NEU':
                final_label = "NEUTRAL"

            # --- XỬ LÝ THEO YÊU CẦU ĐẶC BIỆT CỦA ĐỀ ---
            # Đề bài yêu cầu: Nếu độ tin cậy thấp (< 0.5), hãy coi là trung tính.
            if score < 0.5:
                final_label = "NEUTRAL"

            return {
                "label": final_label,
                "score": round(score, 4) # Làm tròn 4 chữ số cho gọn đẹp
            }

        except Exception as e:
            print(f"❌ Lỗi phân loại: {e}")
            return {"label": "ERROR", "score": 0.0}

# --- PHẦN CHẠY THỬ ---
if __name__ == "__main__":
    clf = SentimentClassifier()
    print(clf.predict("hôm_nay tôi rất vui"))