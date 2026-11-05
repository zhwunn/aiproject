
import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import re
from pathlib import Path

# ==========================================
# 1. 페이지 디자인
# ==========================================

st.markdown("""
<style>
.stApp {
    background-color: #FFF9D9;
}

[data-testid="stSidebar"] {
    background-color: #FFF2C2;
}

h1, h2, h3, p, label {
    color: #51434A;
}

div[data-baseweb="select"] > div {
    background-color: white;
    border-color: #F2B8C6;
}

div.stButton > button {
    background-color: #F6B6C8;
    color: #513B43;
    border-radius: 10px;
    border: none;
}
</style>
""", unsafe_allow_html=True)


# ==========================================
# 2. CSV 파일 불러오기 및 한글 인코딩
# ==========================================

@st.cache_data
def load_data():

    # pages 폴더의 상위 폴더에서 CSV 찾기
    base_path = Path(__file__).resolve().parent.parent
    file_path = base_path / "population.csv"

    if not file_path.exists():
        raise FileNotFoundError(
            "population.csv 파일이 없습니다. "
            "GitHub 저장소 최상위 폴더에 업로드해주세요."
        )

    # 한글 인코딩 자동 확인
    encodings = [
        "cp949",
        "euc-kr",
        "utf-8-sig",
        "utf-8"
    ]

    data = None

    for encoding in encodings:
        try:
            data = pd.read_csv(
                file_path,
                encoding=encoding
            )
            break

        except UnicodeDecodeError:
            continue

    if data is None:
        raise ValueError(
            "CSV 파일의 인코딩을 확인할 수 없습니다."
        )

    # 행정구역 이름 정리
    data["행정구역"] = (
        data["행정구역"]
        .astype(str)
        .str.replace(
            r"\s*\(\d+\)\s*$",
            "",
            regex=True
        )
        .str.strip()
    )

    # 인구수 숫자 변환
    for col in data.columns:

        if col != "행정구역":

            data[col] = pd.to_numeric(
                data[col]
                .astype(str)
                .str.replace(",", "", regex=False),
                errors="coerce"
            )

    return data


# 데이터 불러오기
try:
    df = load_data()

except Exception as e:
    st.error(f"데이터 불러오기 오류: {e}")
    st.stop()


# ==========================================
# 3. 제목
# ==========================================

st.title("🌸 지역별 인구 통계 분석")

st.write(
    "행정구역, 성별, 연도를 선택하여 "
    "연령별 인구 분포를 확인해보세요."
)


# ==========================================
# 4. 선택 메뉴
# ==========================================

col1, col2, col3 = st.columns(3)

# 행정구역
regions = df["행정구역"].dropna().unique().tolist()

# 연도
years = ["2023", "2024", "2025"]

# 성별
gender_options = {
    "전체": "",
    "남성": "남",
    "여성": "여"
}

with col1:
    selected_region = st.selectbox(
        "행정구역 선택",
        regions
    )

with col2:
    selected_gender = st.selectbox(
        "성별 선택",
        list(gender_options.keys())
    )

with col3:
    selected_year = st.selectbox(
        "연도 선택",
        years,
        index=2
    )


# ==========================================
# 5. 선택한 데이터 추출
# ==========================================

gender_code = gender_options[selected_gender]

if gender_code == "":
    prefix = f"{selected_year}년_거주자_"

else:
    prefix = (
        f"{selected_year}년_"
        f"{gender_code}_거주자_"
    )


# 연령별 열 찾기
age_pattern = re.compile(
    r"^\d+~\d+세$|^100세 이상$"
)

age_columns = []

for column in df.columns:

    if column.startswith(prefix):

        age_name = column[len(prefix):]

        if age_pattern.match(age_name):
            age_columns.append(column)


# 연령 순서 정렬
def age_sort_key(column):

    age_name = column[len(prefix):]

    if age_name == "100세 이상":
        return 100

    return int(age_name.split("~")[0])


age_columns.sort(key=age_sort_key)


# 데이터 확인
if not age_columns:
    st.error(
        "선택한 조건에 해당하는 연령별 데이터가 없습니다."
    )
    st.stop()


region_data = df[
    df["행정구역"] == selected_region
]

if region_data.empty:
    st.error("해당 행정구역의 데이터가 없습니다.")
    st.stop()


region_data = region_data.iloc[0]


# ==========================================
# 6. 그래프 데이터 만들기
# ==========================================

ages = [
    column[len(prefix):]
    for column in age_columns
]

population = (
    region_data[age_columns]
    .fillna(0)
    .astype(int)
    .tolist()
)

chart_data = pd.DataFrame({

    "나이": ages,

    "인구수(명)": population

})

# 백 명 단위로 변환
chart_data["인구수(백 명)"] = (
    chart_data["인구수(명)"] / 100
)


# ==========================================
# 7. 인구 통계 요약
# ==========================================

total_population = sum(population)

m1, m2, m3 = st.columns(3)

m1.metric(
    "선택한 행정구역",
    selected_region
)

m2.metric(
    "선택한 성별",
    selected_gender
)

m3.metric(
    "연령별 인구 합계",
    f"{total_population:,}명"
)


# ==========================================
# 8. 꺾은선 그래프
# ==========================================

fig = go.Figure()

fig.add_trace(

    go.Scatter(

        x=chart_data["나이"],

        y=chart_data["인구수(백 명)"],

        mode="lines+markers",

        name="인구수",

        line=dict(
            color="#E98EAD",
            width=4
        ),

        marker=dict(
            color="#F3AFC4",
            size=9,
            line=dict(
                color="white",
                width=1.5
            )
        ),

        customdata=chart_data[["인구수(명)"]],

        hovertemplate=(
            "나이: %{x}<br>"
            "인구수: %{customdata[0]:,.0f}명"
            "<extra></extra>"
        )
    )
)


# ==========================================
# 9. 그래프 디자인
# ==========================================

fig.update_layout(

    title=dict(
        text=(
            f"{selected_region} · "
            f"{selected_gender} · "
            f"{selected_year}년 연령별 인구"
        ),
        x=0.5,
        xanchor="center",
        font=dict(
            size=20,
            color="#51434A"
        )
    ),

    # 가로축
    xaxis=dict(

        title="나이",

        type="category",

        tickmode="array",

        tickvals=ages,

        ticktext=ages,

        showgrid=True,

        gridcolor="#F1DFA8",

        linecolor="#D8C99A"
    ),

    # 세로축
    yaxis=dict(

        title="인구수 (백 명 단위)",

        rangemode="tozero",

        dtick=50,

        showgrid=True,

        gridcolor="#EADBAA",

        zeroline=True,

        zerolinecolor="#D8C99A"
    ),

    # 배경
    plot_bgcolor="#FFFDF3",

    paper_bgcolor="#FFF9D9",

    font=dict(
        family="Malgun Gothic, AppleGothic, NanumGothic, sans-serif",
        color="#51434A",
        size=12
    ),

    hoverlabel=dict(
        bgcolor="#FFF0F5",
        font=dict(color="#51434A")
    ),

    margin=dict(
        l=35,
        r=25,
        t=75,
        b=55
    ),

    height=560
)


# 그래프 출력
st.plotly_chart(
    fig,
    use_container_width=True
)


st.caption(
    "가로축은 5세 단위 연령 구간입니다. "
    "세로축은 백 명 단위이며 눈금 간격 50은 "
    "실제 인구 5,000명을 의미합니다. "
    "그래프의 점에 마우스를 올리면 실제 인구수를 확인할 수 있습니다."
)


# ==========================================
# 10. 데이터 표 및 다운로드
# ==========================================

with st.expander("📊 연령별 인구 데이터 확인"):

    table = chart_data[
        ["나이", "인구수(명)"]
    ].copy()

    st.dataframe(
        table,
        use_container_width=True,
        hide_index=True
    )

    # 한글 엑셀 호환 CSV
    csv_bytes = table.to_csv(
        index=False
    ).encode("utf-8-sig")

    st.download_button(

        label="CSV 파일 다운로드",

        data=csv_bytes,

        file_name=(
            f"인구분석_{selected_region}_"
            f"{selected_gender}_{selected_year}.csv"
        ),

        mime="text/csv"
    )


# ==========================================
# 11. 마무리
# ==========================================

st.markdown("---")

st.caption(
    "데이터 출처: population.csv"
)
