
import streamlit as st
import pandas as pd
from pathlib import Path

# --------------------------------------------------
# 1. 페이지 설정
# --------------------------------------------------
st.set_page_config(
    page_title="말랑말랑 식품 섭취 연구소",
    page_icon="🍡",
    layout="wide"
)

# --------------------------------------------------
# 2. CSV 경로
# pages 폴더의 상위 폴더에서 CSV 찾기
# --------------------------------------------------
BASE_DIR = Path(__file__).resolve().parent.parent

CSV_PATH = BASE_DIR / "한국보건산업진흥원_국민영양통계 식품별 평균섭취량_20231231.csv"


# --------------------------------------------------
# 3. 귀여운 파스텔 디자인
# --------------------------------------------------
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
    color: #765d70 !important;
}

[data-testid="stMetric"] {
    background: #ffffff;
    border: 1px solid #f4dce5;
    padding: 16px 18px;
    border-radius: 18px;
    box-shadow: 0 4px 12px rgba(190,153,170,0.08);
}

[data-testid="stMetricLabel"] {
    color: #987b8d;
}

[data-testid="stMetricValue"] {
    color: #765d70;
}

div[data-testid="stSelectbox"] label {
    color: #765d70;
    font-weight: 700;
}

div[data-testid="stDataFrame"] {
    border: 1px solid #f3dce5;
    border-radius: 14px;
    overflow: hidden;
}

[data-testid="stVerticalBlockBorderWrapper"] {
    background: linear-gradient(
        120deg,
        #ffe2e8,
        #fff0d9,
        #e8efff
    );
    border-radius: 24px;
}

</style>
""", unsafe_allow_html=True)


# --------------------------------------------------
# 4. CSV 데이터 불러오기
# --------------------------------------------------
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


# --------------------------------------------------
# 5. 제목 영역
# HTML 대신 Streamlit 기본 기능 사용
# --------------------------------------------------
with st.container(border=True):

    st.title("🍡 말랑말랑 식품 섭취 연구소")

    st.write(
        "성별과 식품군을 선택하고, "
        "우리 식탁 속 식품 섭취 데이터를 귀엽게 살펴봐요!"
    )


# --------------------------------------------------
# 6. CSV 파일 존재 여부 확인
# --------------------------------------------------
if not CSV_PATH.exists():

    st.error("CSV 파일을 찾을 수 없어요.")

    st.write("현재 찾고 있는 경로:")

    st.code(str(CSV_PATH))

    st.info(
        "CSV 파일은 메인.py가 있는 최상위 폴더에 넣어 주세요. "
        "분석 파일은 pages 폴더 안에 있어야 해요."
    )

    st.stop()


# --------------------------------------------------
# 7. 데이터 읽기
# --------------------------------------------------
try:

    df = load_data(CSV_PATH)

except Exception as error:

    st.error(
        f"CSV 파일을 읽지 못했어요: {error}"
    )

    st.stop()


# --------------------------------------------------
# 8. 필요한 열 확인
# --------------------------------------------------
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
        "CSV 파일에 필요한 열이 없어요: "
        + ", ".join(missing_columns)
    )

    st.stop()


# --------------------------------------------------
# 9. 데이터 정리
# --------------------------------------------------
for column in [
    "연도",
    "평균",
    "표준오차"
]:

    df[column] = pd.to_numeric(
        df[column],
        errors="coerce"
    )


df = df.dropna(
    subset=[
        "연도",
        "평균",
        "식품군",
        "식품",
        "분석기준",
        "기준값"
    ]
).copy()


df["연도"] = df["연도"].astype(int)


# 성별 자료만 추출
sex_df = df[
    df["분석기준"] == "성별"
].copy()


if sex_df.empty:

    st.error("성별 기준 데이터를 찾을 수 없어요.")

    st.stop()


# --------------------------------------------------
# 10. 검색 조건 선택
# --------------------------------------------------
st.header("🎀 나만의 식품 데이터 고르기")


col1, col2, col3 = st.columns(3)


with col1:

    gender_options = [
        "전체",
        "남자",
        "여자"
    ]

    selected_gender = st.selectbox(
        "👧 성별 선택",
        gender_options
    )


with col2:

    food_groups = sorted(
        sex_df["식품군"].dropna().unique().tolist()
    )

    selected_group = st.selectbox(
        "🍰 식품군 선택",
        food_groups
    )


with col3:

    years = sorted(
        sex_df["연도"].dropna().unique().tolist()
    )

    selected_year = st.selectbox(
        "📅 조사 연도 선택",
        years,
        index=len(years) - 1
    )


# --------------------------------------------------
# 11. 선택 조건에 해당하는 데이터 추출
# --------------------------------------------------
filtered = sex_df[
    (sex_df["기준값"] == selected_gender)
    & (sex_df["식품군"] == selected_group)
    & (sex_df["연도"] == selected_year)
].copy()


filtered = filtered.sort_values(
    "평균",
    ascending=False
)


st.divider()


if filtered.empty:

    st.warning(
        "선택한 조건에 해당하는 자료가 없어요. "
        "다른 조건을 선택해 주세요."
    )

    st.stop()


# --------------------------------------------------
# 12. 요약 정보
# --------------------------------------------------
top_row = filtered.iloc[0]

food_count = filtered["식품"].nunique()


st.subheader("🌷 선택한 조건의 분석 결과")


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
    "📅 선택한 연도",
    f"{selected_year}년"
)


st.info(
    f"{selected_year}년 / {selected_gender} / {selected_group} 조건에서 "
    f"평균값이 가장 높은 식품은 '{top_row['식품']}'이며, "
    f"평균값은 {top_row['평균']:.2f}입니다."
)


# --------------------------------------------------
# 13. 그래프와 데이터 표
# --------------------------------------------------
graph_col, table_col = st.columns([1.1, 1])


with graph_col:

    st.subheader("📊 식품별 평균값 그래프")

    chart_data = filtered[
        ["식품", "평균"]
    ].set_index("식품")


    st.bar_chart(
        chart_data,
        color="#E9AFC2",
        height=420
    )


    st.caption(
        "막대가 길수록 원본 자료의 평균값이 높아요."
    )


with table_col:

    st.subheader("🍬 식품별 상세 데이터")

    result_table = filtered[
        ["식품", "평균", "표준오차"]
    ].rename(
        columns={
            "식품": "식품명",
            "평균": "평균값"
        }
    )


    st.dataframe(
        result_table.style.format({
            "평균값": "{:.2f}",
            "표준오차": "{:.2f}"
        }),
        use_container_width=True,
        height=420,
        hide_index=True
    )


# --------------------------------------------------
# 14. 개별 식품 자세히 보기
# --------------------------------------------------
st.divider()

st.subheader("🔎 식품 하나 자세히 보기")


food_options = (
    filtered["식품"]
    .dropna()
    .sort_values()
    .unique()
    .tolist()
)


selected_food = st.selectbox(
    "자세히 확인할 식품을 선택해 주세요.",
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


# --------------------------------------------------
# 15. 데이터 설명
# --------------------------------------------------
with st.expander("📚 데이터와 분석 기준 알아보기"):

    st.write(
        "- 자료: 한국보건산업진흥원 국민영양통계 식품별 평균섭취량\n"
        "- 분석 기준: 성별\n"
        "- 성별 선택: 전체, 남자, 여자\n"
        "- 식품군: 원본 CSV에 포함된 식품군 분류\n"
        "- 조사 연도: 원본 자료에 포함된 연도\n"
        "- 평균값과 표준오차: 원본 CSV의 수치"
    )

    st.caption(
        f"불러온 CSV 파일: {CSV_PATH.name}"
    )

    st.caption(
        "이 자료는 식품별 평균 섭취량이며, "
        "개인의 선호도 조사 결과는 아닙니다."
    )


# --------------------------------------------------
# 16. 하단 문구
# --------------------------------------------------
st.divider()

st.caption(
    "🍓 오늘도 맛있고 즐거운 데이터 탐험! · Snack Data Lab 🍓"
)
