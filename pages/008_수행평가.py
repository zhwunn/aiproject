import streamlit as st
import pandas as pd
from pathlib import Path

st.set_page_config(
    page_title="말랑말랑 식품 섭취 연구소",
    page_icon="🍡",
    layout="wide"
)
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Jua&family=Noto+Sans+KR:wght@400;500;700&display=swap');

html, body, [class*="css"] {
    font-family: 'Noto Sans KR', sans-serif;
}

.stApp {
    background: linear-gradient(
        135deg,
        #fff8f5,
        #fffafd,
        #f4f8ff
    );
}

.hero-box {
    background: linear-gradient(
        120deg,
        #ffe2e8,
        #fff0d9,
        #e8efff
    );
    padding: 30px;
    border-radius: 25px;
    border: 2px solid white;
    margin-bottom: 22px;
}

.hero-title {
    font-family: 'Jua', sans-serif;
    font-size: 30px;
    color: #765d70;
    margin-bottom: 10px;
}

.hero-description {
    font-family: 'Noto Sans KR', sans-serif;
    font-size: 15px;
    color: #8c7888;
    line-height: 1.6;
}
</style>

<div class="hero-box">
    <div class="hero-title">
        🍡 말랑말랑 식품 섭취 연구소
    </div>
    <div class="hero-description">
        성별과 식품군을 선택하고,<br>
        우리 식탁 속 식품 섭취 데이터를 귀엽게 살펴봐요!
    </div>
</div>
""", unsafe_allow_html=True)
