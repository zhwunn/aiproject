# ==========================================
# 제목 영역
# ==========================================

st.markdown("""
<style>
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
    box-shadow: 0 8px 22px rgba(190,153,170,0.13);
    margin-bottom: 22px;
}

.hero-title {
    font-family: 'Noto Sans KR', sans-serif;
    font-weight: 700;
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
