# Giao diện Streamlit
# app.py

import streamlit as st
import pandas as pd
from analyzer import analyze
from database import save_history, get_history

st.set_page_config(
    page_title="Assistant phân loại cảm xúc",
    layout="centered"
)

st.title("Trợ lý phân loại cảm xúc Tiếng Việt")
st.markdown("---")

# 1. Nhập câu từ người dùng
# -------------------------
def process_input():
    text = st.session_state.text_input_sentiment
    
    if not text.strip():
        return
    
    result = analyze(text)

    # Lưu vào session state để hiển thị
    st.session_state.last_result = result


# Nhập với callback (tự động khi Enter)
st.text_input(
    "Nhập câu tiếng Việt để phân loại cảm xúc:", 
    key="text_input_sentiment",
    on_change=process_input
)

if st.button("Phân loại cảm xúc"):
    process_input()

# Hiển thị kết quả (nếu có)
if "last_result" in st.session_state:
    result = st.session_state.last_result
    
    # Nếu lỗi
    if "error" in result:
        st.error(result["error"])
    else:
        sentiment = result["sentiment"]
        score_percent = f"{result.get('score', 0.0) * 100:.2f}%"
        
        if sentiment == "POSITIVE":
            st.success(f"🎉 Cảm xúc: {sentiment} (Độ tin cậy: {score_percent})")
        elif sentiment == "NEGATIVE":
            st.error(f"😞 Cảm xúc: {sentiment} (Độ tin cậy: {score_percent})")
        else:
            st.warning(f"😐 Cảm xúc: {sentiment} (Độ tin cậy: {score_percent})")

        # Lưu lịch sử vào DB
        save_history(result["text"], sentiment, result.get("score", 0.0))

# 2. Hiển thị lịch sử phân loại
# -------------------------
st.subheader("📜 Lịch sử phân loại gần đây:")

history = get_history()

if len(history) == 0:
    st.info("Chưa có dữ liệu lịch sử.")
else:
    # Biến lịch sử JSON → DataFrame
    df = pd.DataFrame(history)

    # Đổi tên cột cho đẹp
    df = df.rename(columns={
        "text": "Nội dung",
        "sentiment": "Kết quả",
        "time": "Thời gian",
        "score": "Điểm số"
    })

    # Hiển thị bảng có scrollbar
    st.dataframe(
        df,
        use_container_width=True,
        hide_index=True
    )
