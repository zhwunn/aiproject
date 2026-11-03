
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import numpy as np

# -----------------------------
# 페이지 설정
# -----------------------------
st.set_page_config(
    page_title="WORLD MBTI",
    page_icon="🌎",
    layout="wide"
)

# -----------------------------
# 디자인 CSS
# -----------------------------
st.markdown("""
<style>
    .stApp {
        background-color: #FFFDF9;
    }

    h1, h2, h3 {
        color: #514B48;
    }

    .main-title {
        text-align: center;
        color: #E99BB6;
        font-size: 42px;
        font-weight: 800;
        margin-bottom: 5px;
    }

    .sub-title {
        text-align: center;
        color: #99918B;
        font-size: 15px;
        margin-bottom: 35px;
    }

    .info-box {
        background-color: #FFF1F4;
        padding: 18px;
        border-radius: 15px;
        text-align: center;
        margin-bottom: 15px;
    }

    .info-label {
        color: #A88C91;
        font-size: 14px;
    }

    .info-value {
        color: #DE8FA9;
        font-size: 25px;
        font-weight: bold;
    }

    div[data-testid="stSelectbox"] {
        background-color: #FFF8EB;
        border-radius: 12px;
    }
</style>
""", unsafe_allow_html=True)

# -----------------------------
# CSV 데이터 불러오기
# -----------------------------
@st.cache_data
def load_data():
    df = pd.read_csv("countriesMBTI_16types.csv")

    df.columns = df.columns.str.strip()
    df["Country"] = df["Country"].astype(str).str.strip()

    mbti_columns = [
        "INFJ", "ISFJ", "INTP", "ISFP",
        "ENTP", "INFP", "ENTJ", "ISTP",
        "INTJ", "ESFP", "ESTJ", "ENFP",
        "ESTP", "ISTJ", "ENFJ", "ESFJ"
    ]

    for col in mbti_columns:
        df[col] = pd.to_numeric(df[col], errors="coerce")

    df = df.dropna(subset=["Country"] + mbti_columns)

    return df, mbti_columns


try:
    df, mbti_columns = load_data()

except Exception as e:
    st.error("CSV 파일을 불러오지 못했어요.")
    st.info(
        "countriesMBTI_16types.csv 파일이 "
        "app.py와 같은 폴더에 있는지 확인해 주세요."
    )
    st.stop()


# -----------------------------
# 제목
# -----------------------------
st.markdown(
    '<div class="main-title">🌎 WORLD MBTI</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="sub-title">'
    'Discover the MBTI distribution around the world'
    '</div>',
    unsafe_allow_html=True
)

st.divider()

# -----------------------------
# 국가 선택
# -----------------------------
st.subheader("🗺️ 국가 선택")

countries = sorted(df["Country"].unique())

selected_country = st.selectbox(
    "MBTI 비율을 확인하고 싶은 국가를 선택하세요.",
    countries,
    index=countries.index("South Korea")
    if "South Korea" in countries else 0
)

# -----------------------------
# 선택한 국가 데이터
# -----------------------------
country_data = df[df["Country"] == selected_country].iloc[0]

chart_data = pd.DataFrame({
    "MBTI": mbti_columns,
    "Percentage": [
        country_data[mbti] * 100
        for mbti in mbti_columns
    ]
})

# 높은 비율 순으로 정렬
chart_data = chart_data.sort_values(
    by="Percentage",
    ascending=False
).reset_index(drop=True)

# -----------------------------
# 주요 정보
# -----------------------------
first_mbti = chart_data.iloc[0]["MBTI"]
first_percentage = chart_data.iloc[0]["Percentage"]

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown(
        f"""
        <div class="info-box">
            <div class="info-label">🌍 선택 국가</div>
            <div class="info-value">{selected_country}</div>
        </div>
        """,
        unsafe_allow_html=True
    )

with col2:
    st.markdown(
        f"""
        <div class="info-box">
            <div class="info-label">🏆 가장 높은 MBTI</div>
            <div class="info-value">{first_mbti}</div>
        </div>
        """,
        unsafe_allow_html=True
    )

with col3:
    st.markdown(
        f"""
        <div class="info-box">
            <div class="info-label">💗 1위 비율</div>
            <div class="info-value">{first_percentage:.2f}%</div>
        </div>
        """,
        unsafe_allow_html=True
    )

# -----------------------------
# 파스텔톤 그라데이션 색상
# -----------------------------
# 1위: 핑크색
first_color = "#F2A0BB"

# 2위부터: 노란색 → 연한 노란색
yellow_colors = [
    "#F4D35E",
    "#F6DC7D",
    "#F7E39A",
    "#F8E9B4",
    "#F9EDC7",
    "#FAF0D5",
    "#FBF3DF",
    "#FCF5E5",
    "#FCF7EA",
    "#FDF8EE",
    "#FDF9F1",
    "#FEFAF4",
    "#FEFBF6",
    "#FFFDF9",
    "#FFFDF9"
]

colors = [first_color] + yellow_colors[:15]

# -----------------------------
# 그래프
# -----------------------------
st.markdown("## 📊 MBTI 비율 그래프")

st.caption(
    f"{selected_country}의 MBTI 유형별 비율을 높은 순서대로 보여줍니다."
)

fig, ax = plt.subplots(figsize=(12, 7))

fig.patch.set_facecolor("#FFFDF9")
ax.set_facecolor("#FFFDF9")

# 순위별 색상
bars = ax.barh(
    chart_data["MBTI"],
    chart_data["Percentage"],
    color=colors,
    edgecolor="none",
    height=0.68
)

# 높은 순위가 위로 오도록 설정
ax.invert_yaxis()

# 막대 끝에 퍼센트 표시
for bar, value in zip(bars, chart_data["Percentage"]):
    ax.text(
        bar.get_width() + 0.15,
        bar.get_y() + bar.get_height() / 2,
        f"{value:.2f}%",
        va="center",
        fontsize=10,
        color="#6E6660",
        fontweight="medium"
    )

# 그래프 꾸미기
ax.set_xlabel(
    "Percentage (%)",
    fontsize=11,
    color="#8C817A",
    labelpad=12
)

ax.set_ylabel("")

ax.set_title(
    f"{selected_country} MBTI Distribution",
    fontsize=17,
    fontweight="bold",
    color="#514B48",
    pad=20
)

ax.tick_params(
    axis="y",
    labelsize=11,
    colors="#655D58",
    length=0
)

ax.tick_params(
    axis="x",
    labelsize=9,
    colors="#A49A93"
)

# 격자
ax.xaxis.grid(
    True,
    linestyle="--",
    alpha=0.25,
    color="#BEB5AE"
)

ax.set_axisbelow(True)

# 그래프 테두리 제거
for spine in ax.spines.values():
    spine.set_visible(False)

# 오른쪽 여백 확보
max_value = chart_data["Percentage"].max()
ax.set_xlim(0, max_value * 1.22)

plt.tight_layout()

st.pyplot(fig, use_container_width=True)
plt.close(fig)

# -----------------------------
# 순위표
# -----------------------------
st.divider()

st.markdown("## 🏅 MBTI 순위")

ranking_data = chart_data.copy()
ranking_data.index = range(1, len(ranking_data) + 1)
ranking_data.index.name = "순위"

ranking_data["Percentage"] = ranking_data[
    "Percentage"
].map(lambda x: f"{x:.2f}%")

st.dataframe(
    ranking_data,
    use_container_width=True
)

# -----------------------------
# 하단 안내
# -----------------------------
st.markdown("---")

st.markdown(
    """
    <div style="
        text-align:center;
        color:#B1A59D;
        font-size:13px;
        padding:15px;
    ">
        🌷 WORLD MBTI · Explore the world through personality
        <br>
        Data source: countriesMBTI_16types.csv
    </div>
    """,
    unsafe_allow_html=True
)
