# app/classifier.py
from transformers import pipeline

class SentimentClassifier:
    # Hằng số giới hạn độ dài text
    MIN_TEXT_LENGTH = 1      # Ít nhất 1 ký tự
    MAX_TEXT_LENGTH = 100    # Tối đa 100 ký tự
    
    def __init__(self):

        self.model_name = "wonrax/phobert-base-vietnamese-sentiment"
        
        print(f"Đang tải model {self.model_name}...")
        
        self.pipe = pipeline("sentiment-analysis", model=self.model_name)
        print("Đã tải model thành công!")

    def check_text_length(self, text: str) -> dict:
        """
        Kiểm tra độ dài của text có hợp lệ không.
        """
        text_stripped = text.strip()
        text_length = len(text_stripped)
        
        if text_length < self.MIN_TEXT_LENGTH:
            return {
                'is_valid': False,
                'message': f'Text quá ngắn! Tối thiểu {self.MIN_TEXT_LENGTH} ký tự (hiện tại: {text_length})',
                'length': text_length
            }
        
        if text_length > self.MAX_TEXT_LENGTH:
            return {
                'is_valid': False,
                'message': f'Text quá dài! Tối đa {self.MAX_TEXT_LENGTH} ký tự (hiện tại: {text_length})',
                'length': text_length
            }
        
        return {
            'is_valid': True,
            'message': f'Độ dài hợp lệ ({text_length} ký tự)',
            'length': text_length
        }

    def predict(self, text):

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
            
            final_label = "NEUTRAL" # Mặc định là trung tính cho an toàn
            
            if raw_label == 'POS':
                final_label = "POSITIVE"
            elif raw_label == 'NEG':
                final_label = "NEGATIVE"
            elif raw_label == 'NEU':
                final_label = "NEUTRAL"

            # Nếu độ tin cậy thấp (< 0.5), hãy coi là trung tính.
            if score < 0.5:
                final_label = "NEUTRAL"

            return {
                "label": final_label,
                "score": round(score, 4) # Làm tròn 4 chữ số cho gọn đẹp
            }

        except Exception as e:
            print(f"❌ Lỗi phân loại: {e}")
            return {"label": "ERROR", "score": 0.0}
