import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# ---------------------------------------
# 페이지 설정
# ---------------------------------------
st.set_page_config(
    page_title="WORLD MBTI",
    page_icon="🌎",
    layout="wide"
)

# ---------------------------------------
# 파스텔톤 디자인
# ---------------------------------------
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
        margin-bottom: 30px;
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
</style>
""", unsafe_allow_html=True)

# ---------------------------------------
# MBTI 및 색상 설정
# ---------------------------------------
MBTI_COLUMNS = [
    "INFJ", "ISFJ", "INTP", "ISFP",
    "ENTP", "INFP", "ENTJ", "ISTP",
    "INTJ", "ESFP", "ESTJ", "ENFP",
    "ESTP", "ISTJ", "ENFJ", "ESFJ"
]

FIRST_COLOR = "#F2A0BB"  # 1위 핑크색
YELLOW_COLORS = [
    "#F4D35E", "#F6DC7D", "#F7E39A", "#F8E9B4",
    "#F9EDC7", "#FAF0D5", "#FBF3DF", "#FCF5E5",
    "#FCF7EA", "#FDF8EE", "#FDF9F1", "#FEFAF4",
    "#FEFBF6", "#FFFDF9", "#FFFDF9"
]

def make_rank_colors(count):
    """1위는 핑크, 2위부터는 점점 흐려지는 노란색."""
    if count <= 0:
        return []
    return [FIRST_COLOR] + [
        YELLOW_COLORS[min(i, len(YELLOW_COLORS) - 1)]
        for i in range(count - 1)
    ]


def draw_bar_chart(data, category_col, value_col, title, xlabel,
                   height_per_bar=0.38, max_height=24):
    """정렬된 데이터로 파스텔톤 가로 막대그래프를 그린다."""
    count = len(data)
    fig_height = min(max(5, count * height_per_bar), max_height)

    fig, ax = plt.subplots(figsize=(11, fig_height))
    fig.patch.set_facecolor("#FFFDF9")
    ax.set_facecolor("#FFFDF9")

    bars = ax.barh(
        data[category_col].astype(str),
        data[value_col],
        color=make_rank_colors(count),
        edgecolor="none",
        height=0.68
    )

    ax.invert_yaxis()

    max_value = max(float(data[value_col].max()), 0.1)
    ax.set_xlim(0, max_value * 1.20)

    for bar, value in zip(bars, data[value_col]):
        ax.text(
            bar.get_width() + max_value * 0.012,
            bar.get_y() + bar.get_height() / 2,
            f"{value:.2f}%",
            va="center",
            fontsize=9,
            color="#6E6660"
        )

    ax.set_title(
        title,
        fontsize=16,
        fontweight="bold",
        color="#514B48",
        pad=18
    )
    ax.set_xlabel(xlabel, fontsize=10, color="#8C817A", labelpad=10)
    ax.set_ylabel("")
    ax.tick_params(axis="y", labelsize=9, colors="#655D58", length=0)
    ax.tick_params(axis="x", labelsize=9, colors="#A49A93")
    ax.xaxis.grid(
        True,
        linestyle="--",
        alpha=0.25,
        color="#BEB5AE"
    )
    ax.set_axisbelow(True)

    for spine in ax.spines.values():
        spine.set_visible(False)

    plt.tight_layout()
    st.pyplot(fig, use_container_width=True)
    plt.close(fig)


# ---------------------------------------
# CSV 불러오기
# ---------------------------------------
@st.cache_data
def load_data():
    df = pd.read_csv("countriesMBTI_16types.csv")
    df.columns = df.columns.str.strip()

    if "Country" not in df.columns:
        raise ValueError("CSV 파일에 Country 열이 없습니다.")

    missing_columns = [col for col in MBTI_COLUMNS if col not in df.columns]
    if missing_columns:
        raise ValueError(
            "CSV 파일에서 다음 MBTI 열을 찾을 수 없습니다: "
            + ", ".join(missing_columns)
        )

    df["Country"] = df["Country"].astype(str).str.strip()

    for col in MBTI_COLUMNS:
        df[col] = pd.to_numeric(df[col], errors="coerce")

    df = df.dropna(subset=["Country"] + MBTI_COLUMNS)
    df = df[df["Country"] != ""]

    return df


try:
    df = load_data()
except Exception as error:
    st.error("CSV 파일을 불러오지 못했어요.")
    st.info(
        "countriesMBTI_16types.csv 파일이 app.py와 같은 폴더에 있는지, "
        "파일 이름과 열 이름이 정확한지 확인해 주세요."
    )
    st.exception(error)
    st.stop()


# ---------------------------------------
# 제목
# ---------------------------------------
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

st.markdown(
    """
    <div style="
        background:#FFF1F4;
        border-radius:15px;
        padding:16px 20px;
        color:#76666A;
        margin-bottom:18px;
    ">
        국가별 MBTI 비율도 보고, 특정 MBTI가 많이 나타나는 국가도 찾아볼 수 있어.
        <b>원하는 항목을 골라 봐. 그래프는 내가 정리해 줄 테니까.</b>
    </div>
    """,
    unsafe_allow_html=True
)

# =======================================
# 1. 국가를 선택하면 해당 국가의 MBTI 비율
# =======================================
st.header("📊 ① 국가별 MBTI 비율")

countries = sorted(df["Country"].unique())

default_country_index = (
    countries.index("South Korea")
    if "South Korea" in countries else 0
)

selected_country = st.selectbox(
    "MBTI 비율을 확인할 국가를 선택하세요.",
    countries,
    index=default_country_index,
    key="country_selector"
)

country_row = df[df["Country"] == selected_country].iloc[0]

country_chart = pd.DataFrame({
    "MBTI": MBTI_COLUMNS,
    "Percentage": [float(country_row[mbti]) * 100 for mbti in MBTI_COLUMNS]
}).sort_values("Percentage", ascending=False).reset_index(drop=True)

top_country_mbti = country_chart.iloc[0]["MBTI"]
top_country_percentage = country_chart.iloc[0]["Percentage"]

c1, c2, c3 = st.columns(3)

with c1:
    st.markdown(
        f'<div class="info-box"><div class="info-label">🌍 선택 국가</div>'
        f'<div class="info-value">{selected_country}</div></div>',
        unsafe_allow_html=True
    )
with c2:
    st.markdown(
        f'<div class="info-box"><div class="info-label">🏆 가장 높은 MBTI</div>'
        f'<div class="info-value">{top_country_mbti}</div></div>',
        unsafe_allow_html=True
    )
with c3:
    st.markdown(
        f'<div class="info-box"><div class="info-label">💗 1위 비율</div>'
        f'<div class="info-value">{top_country_percentage:.2f}%</div></div>',
        unsafe_allow_html=True
    )

draw_bar_chart(
    country_chart,
    category_col="MBTI",
    value_col="Percentage",
    title=f"{selected_country} MBTI Distribution",
    xlabel="Percentage (%)",
    height_per_bar=0.38,
    max_height=12
)

with st.expander("🏅 선택 국가의 MBTI 전체 순위 보기"):
    display_country = country_chart.copy()
    display_country.insert(0, "Rank", range(1, len(display_country) + 1))
    display_country["Percentage"] = display_country["Percentage"].map(
        lambda value: f"{value:.2f}%"
    )
    st.dataframe(display_country, use_container_width=True, hide_index=True)


# =======================================
# 2. MBTI를 선택하면 해당 유형 비율이 높은 국가
# =======================================
st.divider()
st.header("🌍 ② MBTI별 국가 순위")
st.write(
    "궁금한 MBTI를 선택하면 그 유형의 비율이 높은 국가부터 막대그래프로 보여줄게."
)

selected_mbti = st.selectbox(
    "찾고 싶은 MBTI 유형을 선택하세요.",
    MBTI_COLUMNS,
    index=MBTI_COLUMNS.index("INFP"),
    key="mbti_selector"
)

country_ranking = df[["Country", selected_mbti]].copy()
country_ranking["Percentage"] = country_ranking[selected_mbti] * 100
country_ranking = country_ranking[
    ["Country", "Percentage"]
].sort_values(
    "Percentage",
    ascending=False
).reset_index(drop=True)

top_country = country_ranking.iloc[0]["Country"]
top_percentage = country_ranking.iloc[0]["Percentage"]

r1, r2, r3 = st.columns(3)

with r1:
    st.markdown(
        f'<div class="info-box"><div class="info-label">🧩 선택 MBTI</div>'
        f'<div class="info-value">{selected_mbti}</div></div>',
        unsafe_allow_html=True
    )
with r2:
    st.markdown(
        f'<div class="info-box"><div class="info-label">🥇 1위 국가</div>'
        f'<div class="info-value">{top_country}</div></div>',
        unsafe_allow_html=True
    )
with r3:
    st.markdown(
        f'<div class="info-box"><div class="info-label">💗 1위 비율</div>'
        f'<div class="info-value">{top_percentage:.2f}%</div></div>',
        unsafe_allow_html=True
    )

# 화면에 표시할 국가 수 선택
display_count = st.selectbox(
    "그래프에 표시할 국가 수",
    options=["상위 10개", "상위 20개", "상위 50개", "전체 국가"],
    index=1,
    key="country_count"
)

if display_count == "상위 10개":
    chart_count = 10
elif display_count == "상위 20개":
    chart_count = 20
elif display_count == "상위 50개":
    chart_count = 50
else:
    chart_count = len(country_ranking)

visible_ranking = country_ranking.head(chart_count).copy()
visible_ranking.insert(0, "Rank", range(1, len(visible_ranking) + 1))

draw_bar_chart(
    visible_ranking,
    category_col="Country",
    value_col="Percentage",
    title=f"Countries with the Highest {selected_mbti} Percentage",
    xlabel=f"{selected_mbti} Percentage (%)",
    height_per_bar=0.34,
    max_height=24
)

with st.expander("📋 국가별 전체 순위표 보기"):
    full_ranking = country_ranking.copy()
    full_ranking.insert(0, "Rank", range(1, len(full_ranking) + 1))
    full_ranking["Percentage"] = full_ranking["Percentage"].map(
        lambda value: f"{value:.2f}%"
    )
    st.dataframe(full_ranking, use_container_width=True, hide_index=True)


# ---------------------------------------
# 전체 데이터 안내
# ---------------------------------------
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
