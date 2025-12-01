# Giao diện Streamlit
# app.py

import streamlit as st
from analyzer import analyze
from database import save_history, get_history

st.set_page_config(page_title="Assistant phân loại cảm xúc", layout="centered")

st.title("Trợ lý phân loại cảm xúc Tiếng Việt")

# 1. Nhập câu từ người dùng
# -------------------------
text = st.text_input("Nhập câu tiếng Việt:", key="text_input_sentiment")

if st.button("Phân loại cảm xúc"):
    result = analyze(text)

    # Nếu lỗi (input ngắn / rỗng)
    if "error" in result:
        st.error(result["error"])
    else:
        sentiment = result["sentiment"]

        # Hiển thị màu theo cảm xúc
        if sentiment == "POSITIVE":
            st.success(f"🎉 Cảm xúc: {sentiment}")
        elif sentiment == "NEGATIVE":
            st.error(f"😞 Cảm xúc: {sentiment}")
        else:
            st.warning(f"😐 Cảm xúc: {sentiment}")

        # Lưu lịch sử vào DB
        save_history(result["text"], sentiment, result.get("score", 0.0))

# 2. Hiển thị lịch sử phân loại
# -------------------------
st.subheader("📜 Lịch sử phân loại gần đây:")

history = get_history()

if len(history) == 0:
    st.info("Chưa có lịch sử!")
else:
    for row in history:
        id, text, sent, score, created_at = row
        st.write(f"**[{created_at}]** - *\"{text}\"* → **{sent}** (Độ tin cậy: {score:.1%})")
