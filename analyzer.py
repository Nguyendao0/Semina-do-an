from preprocess import preprocess_text
from classifier import SentimentClassifier
from postprocess import validate_input

# Khởi tạo classifier
clf = SentimentClassifier()

def analyze(text: str):
    # 1. Validate input
    ok, msg = validate_input(text)
    if not ok:
        return {"error": msg}

    # 2. Preprocess
    processed = preprocess_text(text)

    # 3. PhoBERT classify → trả về {'label': 'POSITIVE', 'score': 0.99}
    result = clf.predict(processed)

    # 4. Return result (có thể thêm postprocess sau)
    return result
