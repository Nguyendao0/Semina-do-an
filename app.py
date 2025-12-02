# Giao diện Streamlit
# app.py

import streamlit as st
import pandas as pd
from analyzer import analyze
from database import save_history, get_history, clear_history

st.set_page_config(
    page_title="Assistant phân loại cảm xúc",
    layout="centered"
)

st.title("Trợ lý phân loại cảm xúc Tiếng Việt")
st.markdown("---")

# ========================
# 1. PHẦN NHẬP & PHÂN LOẠI
# ========================

def process_input():
    """Phân loại cảm xúc từ input text"""
    text = st.session_state.text_input_sentiment
    if not text.strip():
        return
    
    result = analyze(text)
    st.session_state.last_result = result
    st.session_state.should_save = True


def display_sentiment_result(result):
    """Hiển thị kết quả phân loại với màu sắc"""
    if "error" in result:
        st.error(result["error"])
        return
    
    sentiment = result["sentiment"]
    score_percent = f"{result.get('score', 0.0) * 100:.2f}%"
    
    emoji_map = {
        "POSITIVE": ("🎉", "success"),
        "NEGATIVE": ("😞", "error"),
        "NEUTRAL": ("😐", "warning")
    }
    
    emoji, style = emoji_map.get(sentiment, ("😐", "warning"))
    message = f"{emoji} Cảm xúc: {sentiment} (Độ tin cậy: {score_percent})"
    
    getattr(st, style)(message)
    
    # Lưu lịch sử
    save_history(result["text"], sentiment, result.get("score", 0.0))
    st.session_state.should_save = False


with st.form("sentiment_form"):
    st.text_input(
        "Nhập câu tiếng Việt để phân loại cảm xúc:", 
        key="text_input_sentiment"
    )
    
    if st.form_submit_button("Phân loại cảm xúc"):
        process_input()

# Hiển thị kết quả nếu có
if "last_result" in st.session_state and st.session_state.get('should_save', False):
    display_sentiment_result(st.session_state.last_result)

# ========================
# 2. PHẦN LỊCH SỬ & XÓA
# ========================

st.subheader("📜 Lịch sử phân loại gần đây:")

if st.button("🗑️ Xóa toàn bộ lịch sử"):
    st.session_state['confirm_delete'] = True

if st.session_state.get('confirm_delete', False):
    st.warning("⚠️ Bạn có chắc muốn xóa toàn bộ? Hành động không thể hoàn tác.")
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("✅ Có, xóa"):
            clear_history()
            st.session_state['confirm_delete'] = False
            st.success("✅ Đã xóa toàn bộ lịch sử!")
            st.rerun()
    
    with col2:
        if st.button("❌ Không, hủy"):
            st.session_state['confirm_delete'] = False
            st.rerun()

history = get_history()

if len(history) == 0:
    st.info("Chưa có dữ liệu lịch sử.")
else:
    df = pd.DataFrame(history)
    df = df.rename(columns={
        "text": "Nội dung",
        "sentiment": "Kết quả",
        "created_at": "Thời gian",
        "score": "Điểm số"
    })
    st.dataframe(df, width='stretch', hide_index=True)
