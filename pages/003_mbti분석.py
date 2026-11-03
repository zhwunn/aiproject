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
