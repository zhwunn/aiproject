import re
from pathlib import Path

import pandas as pd
import plotly.graph_objects as go
import streamlit as st


# ---------------------------------------------------------
# 페이지 설정
# ---------------------------------------------------------
st.set_page_config(
    page_title="인구 통계 분석",
    page_icon="🌸",
    layout="wide"
)

st.markdown(
    """
    <style>
    .stApp { background-color: #FFF9D9; }
    [data-testid="stSidebar"] { background-color: #FFF2C2; }
    [data-testid="stHeader"] { background-color: rgba(255, 249, 217, 0.85); }
    h1, h2, h3, p, label { color: #51434A; }
    div[data-baseweb="select"] > div {
        background-color: #FFFFFF;
        border-color: #F2B8C6;
    }
    </style>
    """,
    unsafe_allow_html=True
)


# ---------------------------------------------------------
# CSV 읽기
# 이 파일은 pages 폴더 안에 있으므로 CSV는 프로젝트
# 최상위 폴더에 있는 것을 먼저 찾습니다.
# ---------------------------------------------------------
@st.cache_data
def load_population_data():
    project_dir = Path(__file__).resolve().parent.parent
    possible_paths = [
        project_dir / "population.csv",
        Path.cwd() / "population.csv",
    ]

    csv_path = next((p for p in possible_paths if p.exists()), None)

    if csv_path is None:
        raise FileNotFoundError(
            "population.csv 파일을 찾을 수 없습니다. "
            "GitHub 저장소 최상위 폴더에 population.csv를 업로드해주세요."
        )

    last_error = None
    data = None

    # 한글 인코딩 자동 확인
    for encoding in ("cp949", "euc-kr", "utf-8-sig", "utf-8"):
        try:
            data = pd.read_csv(csv_path, encoding=encoding)
            break
        except UnicodeDecodeError as error:
            last_error = error

    if data is None:
        raise UnicodeError(
            "CSV 인코딩을 확인할 수 없습니다. CP949 또는 UTF-8 파일인지 확인해주세요."
        ) from last_error

    if "행정구역" not in data.columns:
        raise ValueError("CSV에 '행정구역' 열이 없습니다.")

    # 행정구역 코드 제거: '광주광역시 동구 (2911000000)' -> '광주광역시 동구'
    data["행정구역"] = (
        data["행정구역"]
        .astype(str)
        .str.replace(r"\s*\(\d+\)\s*$", "", regex=True)
        .str.strip()
    )

    # 숫자 열의 쉼표 제거 및 숫자형 변환
    for col in data.columns:
        if col != "행정구역":
            data[col] = pd.to_numeric(
                data[col].astype(str).str.replace(",", "", regex=False),
                errors="coerce"
            )

    return data


try:
    df = load_population_data()
except Exception as error:
