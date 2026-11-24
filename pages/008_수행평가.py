
import streamlit as st
import pandas as pd
from pathlib import Path

# ==========================================
# 1. 페이지 설정
# ==========================================
st.set_page_config(
    page_title="말랑말랑 식품 섭취 연구소",
    page_icon="🍡",
    layout="wide"
)

# ==========================================
# 2. CSV 파일 경로
# pages 폴더의 상위 폴더에서 CSV 찾기
# ==========================================
BASE_DIR = Path(__file__).resolve().parent.parent

CSV_PATH = BASE_DIR / "한국보건산업진흥원_국민영양통계 식품별 평균섭취량_20231231.csv"


# ==========================================
# 3. 귀여운 웹 디자인
# ==========================================
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Jua&family=Noto+Sans+KR:wght@400;500;700&display=swap');

html, body, [class*="css"] {
    font-family: 'Noto Sans KR', sans-serif;
}

.stApp {
    background: linear-gradient(
        135deg,
        #fff8f5 0%,
        #fffafd 55%,
        #f4f8ff 100%
    );
}

.main .block-container {
    max-width: 1200px;
    padding-top: 2rem;
    padding-bottom: 3rem;
}

h1, h2, h3 {
    font-family: 'Jua', sans-serif !important;
    color: #765d70;
}

.hero {
    background: linear-gradient(
        120deg,
        #ffe2e8,
        #fff0d9,
        #e8efff
    );
    padding: 30px 32px;
    border-radius: 25px;
    border: 2px solid white;
    box-shadow: 0 8px 22px rgba(190,153,170,0.13);
    margin-bottom: 22px;
}

.hero-title {
    font-family: 'Jua', sans-serif;
    color: #765d70;
    font-size: 2.25rem;
    margin-bottom: 8px;
}

.hero-sub {
    color: #8c7888;
    font-size: 1rem;
}

div[data-testid="stMetric"] {
    background: white;
    border: 1px solid #f4dce5;
    padding: 17px 18px;
    border-radius: 18px;
    box-shadow: 0 4px 12px rgba(190,153,170,0.08);
}

div[data-testid="stMetricLabel"] {
    color: #987b8d;
}

div[data-testid="stMetricValue"] {
    color: #765d70;
}

.note {
    background: #fff6e8;
    border-left: 5px solid #f2c98b;
    border-radius: 10px;
    padding: 12px 15px;
    color: #806b55;
    font-size: 0.92rem;
}

.footer {
    text-align: center;
    color: #ad98a6;
    font-size: 0.85rem;
    padding-top: 25px;
}
</style>
""", unsafe_allow_html=True)


# ==========================================
# 4. CSV 데이터 불러오기
# ==========================================
@st.cache_data
def load_data(file_path):

    encodings = [
        "utf-8-sig",
        "utf-8",
        "cp949",
        "euc-kr"
    ]

    last_error = None

    for encoding in encodings:
        try:
            return pd.read_csv(
                file_path,
                encoding=encoding
            )

        except UnicodeDecodeError as error:
            last_error = error

    raise last_error


# ==========================================
# 5. 제목
# ==========================================
st.markdown("""
<div class="hero">
    <div class="hero-title">
        🍡 말랑말랑 식품 섭취 연구소
    </div>

    <div class="hero-sub">
        성별과 식품군을 선택하고,
        우리 식탁 속 식품 섭취 데이터를 귀엽게 살펴봐요!
    </div>
</div>
""", unsafe_allow_html=True)


# ==========================================
# 6. CSV 파일 존재 여부 확인
# ==========================================
if not CSV_PATH.exists():

    st.error("CSV 파일을 찾을 수 없어요.")

    st.write("현재 코드가 찾는 경로:")

    st.code(str(CSV_PATH))

    st.info(
        "CSV 파일을 메인.py가 있는 최상위 폴더에 넣어 주세요. "
        "분석 파이썬 파일은 pages 폴더 안에 있어야 해요."
    )

    st.stop()


# ==========================================
# 7. 데이터 읽기
# ==========================================
try:
    df = load_data(CSV_PATH)

except Exception as error:

    st.error(
        f"CSV 파일을 읽는 중 문제가 발생했어요: {error}"
    )

    st.stop()


# 필요한 열 확인
required_columns = [
    "연도",
    "분석기준",
    "기준값",
    "식품군",
    "식품",
    "평균",
    "표준오차"
]

missing_columns = [
    column
    for column in required_columns
    if column not in df.columns
]

if missing_columns:

    st.error(
        "CSV 파일에 다음 열이 없어요: "
        + ", ".join(missing_columns)
    )

    st.stop()


# 숫자 데이터 변환
for column in ["연도", "평균", "표준오차"]:

    df[column] = pd.to_numeric(
        df[column],
        errors="coerce"
    )

df = df.dropna(
    subset=["연도", "평균"]
).copy()

df["연도"] = df["연도"].astype(int)


# ==========================================
# 8. 선택 메뉴
# ==========================================
st.markdown("## 🎀 나만의 식품 데이터 고르기")

col1, col2, col3 = st.columns(3)


with col1:

    gender_options = [
        "전체",
        "남자",
        "여자"
    ]

    selected_gender = st.selectbox(
        "👧 성별",
        gender_options
    )


with col2:

    food_groups = sorted(
        df["식품군"].dropna().unique().tolist()
    )

    selected_group = st.selectbox(
        "🍰 식품군",
        food_groups
    )


with col3:

    years = sorted(
        df["연도"].dropna().unique().tolist()
    )

    selected_year = st.selectbox(
        "📅 조사 연도",
        years,
        index=len(years) - 1
    )


# ==========================================
# 9. 조건에 맞는 데이터 추출
# ==========================================
filtered = df[
    (df["분석기준"] == "성별")
    & (df["기준값"] == selected_gender)
    & (df["식품군"] == selected_group)
    & (df["연도"] == selected_year)
].copy()


filtered = filtered.sort_values(
    "평균",
    ascending=False
)


st.markdown("---")


if filtered.empty:

    st.warning(
        "선택한 조건에 해당하는 자료가 없어요. "
        "다른 조건을 선택해 주세요."
    )

    st.stop()


# ==========================================
# 10. 핵심 분석 결과
# ==========================================
top_row = filtered.iloc[0]

food_count = filtered["식품"].nunique()


metric1, metric2, metric3 = st.columns(3)


metric1.metric(
    "🍓 평균값이 가장 높은 식품",
    str(top_row["식품"])
)

metric2.metric(
    "🧁 해당 식품 수",
    f"{food_count}개"
)

metric3.metric(
    "🌷 선택한 조사 연도",
    f"{selected_year}년"
)


st.markdown(
    f"""
    <div class='note'>
    💡 <b>{selected_year}년 · {selected_gender} · {selected_group}</b>
    조건의 식품별 평균값이에요.
    평균값이 가장 높은 식품은
    <b>{top_row['식품']}</b>이며,
    값은 <b>{top_row['평균']:.2f}</b>예요.
    </div>
    """,
    unsafe_allow_html=True
)


# ==========================================
# 11. 그래프와 데이터 표
# ==========================================
left_col, right_col = st.columns([1.15, 1])


with left_col:

    st.markdown("### 📊 식품별 평균값 그래프")

    chart_data = filtered[
        ["식품", "평균"]
    ].set_index("식품")

    st.bar_chart(
        chart_data,
        color="#E9AFC2",
        height=430
    )

    st.caption(
        "막대가 길수록 해당 식품의 평균값이 높아요."
    )


with right_col:

    st.markdown("### 🍬 자세한 데이터")

    display_df = filtered[
        ["식품", "평균", "표준오차"]
    ].rename(
        columns={
            "식품": "식품명",
            "평균": "평균값"
        }
    )

    st.dataframe(
        display_df.style.format({
            "평균값": "{:.2f}",
            "표준오차": "{:.2f}"
        }),
        use_container_width=True,
        height=430,
        hide_index=True
    )


# ==========================================
# 12. 개별 식품 상세 정보
# ==========================================
st.markdown("---")

st.markdown("## 🔎 식품 하나 더 자세히 보기")


food_options = (
    filtered["식품"]
    .dropna()
    .sort_values()
    .unique()
    .tolist()
)


selected_food = st.selectbox(
    "궁금한 식품을 선택해 주세요.",
    food_options
)


food_detail = filtered[
    filtered["식품"] == selected_food
].iloc[0]


detail_col1, detail_col2 = st.columns(2)


detail_col1.metric(
    f"🍡 {selected_food} 평균값",
    f"{food_detail['평균']:.2f}"
)


detail_col2.metric(
    "📐 표준오차",
    f"{food_detail['표준오차']:.2f}"
)


# ==========================================
# 13. 데이터 설명
# ==========================================
with st.expander("📚 데이터와 분석 기준 알아보기"):

    st.write("""
    - 자료: 한국보건산업진흥원 국민영양통계 식품별 평균섭취량
    - 분석 기준: 성별
    - 성별 선택: 전체, 남자, 여자
    - 식품군: 원본 CSV에 포함된 식품군 분류
    - 평균값과 표준오차: 원본 데이터의 값
    - 조사 연도: 2020~2023년
    """)

    st.caption(
        f"불러온 파일 경로: {CSV_PATH}"
    )

    st.caption(
        "이 화면은 식품별 평균 섭취 데이터를 비교하며, "
        "개인의 선호도를 나타내지는 않아요."
    )


# ==========================================
# 14. 하단 문구
# ==========================================
st.markdown(
    """
    <div class='footer'>
        🍓 오늘도 맛있고 건강한 데이터 탐험! · Snack Data Lab 🍓
    </div>
    """,
    unsafe_allow_html=True
)
