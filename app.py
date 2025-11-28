# Giao diện Streamlit
# app.py

import streamlit as st

st.title("Trợ lý phân loại cảm xúc Tiếng Việt")

text = st.text_input("Nhập câu tiếng Việt:")

if st.button("Phân loại cảm xúc"):
    st.write("Kết quả sẽ hiển thị ở đây...")
