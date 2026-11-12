
import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from pathlib import Path

# ==========================================
# 1. 페이지 설정
# ==========================================

st.set_page_config(
    page_title="월별 기온분석",
    page_icon="🌡️",
    layout="wide"
)

st.title("🌡️ 월별 기온분석")
st.write("원하는 월을 선택하여 연도별 최고기온과 최저기온을 비교해 보세요.")

# ==========================================
# 2. CSV 파일 경로
# Python 파일은 pages 폴더
# CSV 파일은 상위 폴더
# ==========================================

BASE_DIR = Path(__file__).resolve().parent.parent

CSV_CANDIDATES = [
    BASE_DIR / "temperature.csv",
    BASE_DIR / "temperature(3).csv",
    BASE_DIR / "temperature(2).csv",
    BASE_DIR / "temperature(1).csv"
]

CSV_PATH = next(
    (path for path in CSV_CANDIDATES if path.exists()),
    None
)

# ==========================================
# 3. 데이터 불러오기
# ==========================================

@st.cache_data
def load_data():

    if CSV_PATH is None:
        raise FileNotFoundError(
            "상위 폴더에서 temperature.csv 파일을 찾을 수 없습니다."
        )

    df = None
    encoding_used = None

    # 한글 인코딩 자동 처리
    for encoding in ["cp949", "euc-kr", "utf-8-sig", "utf-8"]:

        try:
            df = pd.read_csv(
                CSV_PATH,
                encoding=encoding
            )

            encoding_used = encoding
            break

        except UnicodeDecodeError:
            continue

    if df is None:
        raise ValueError("CSV 인코딩을 확인해 주세요.")

    # 열 이름 정리
    df.columns = [
        str(col)
        .replace("\ufeff", "")
        .replace("\t", "")
        .strip()
        for col in df.columns
    ]

    # 필요한 열 확인
    required_columns = [
        "일시",
        "최고기온(℃)",
        "최저기온(℃)"
    ]

    for col in required_columns:
        if col not in df.columns:
            raise ValueError(
                f"필요한 열이 없습니다: {col}"
            )

    # 날짜 변환
    # Oct-07 -> 2007년 10월
    # Nov-07 -> 2007년 11월
    df["일시"] = pd.to_datetime(
        df["일시"].astype(str).str.strip(),
        format="%b-%y",
        errors="coerce"
    )

    # 기온 숫자 변환
    df["최고기온(℃)"] = pd.to_numeric(
        df["최고기온(℃)"],
        errors="coerce"
    )

    df["최저기온(℃)"] = pd.to_numeric(
        df["최저기온(℃)"],
        errors="coerce"
    )

    # 날짜가 없는 데이터 제거
    df = df.dropna(
        subset=["일시"]
    ).copy()

    # 연도와 월 추출
    df["연도"] = df["일시"].dt.year
    df["월"] = df["일시"].dt.month

    return df.sort_values("일시"), encoding_used


# ==========================================
# 4. 데이터 실행
# ==========================================

try:

    df, encoding_used = load_data()

except Exception as e:

    st.error(f"데이터 오류: {e}")
    st.stop()


# ==========================================
# 5. 월 선택
# ==========================================

month_names = {
    1: "1월",
    2: "2월",
    3: "3월",
    4: "4월",
    5: "5월",
    6: "6월",
    7: "7월",
    8: "8월",
    9: "9월",
    10: "10월",
    11: "11월",
    12: "12월"
}

selected_month_name = st.selectbox(
    "📅 분석할 월을 선택하세요",
    options=list(month_names.values())
)

selected_month = next(
    month
    for month, name in month_names.items()
    if name == selected_month_name
)


# ==========================================
# 6. 선택한 월의 데이터 추출
# ==========================================

chart_data = df[
    df["월"] == selected_month
][
    ["연도", "최고기온(℃)", "최저기온(℃)"]
].copy()

chart_data = chart_data.sort_values("연도")

# 같은 연도에 중복 데이터가 있을 경우 정리
chart_data = (
    chart_data
    .groupby("연도", as_index=False)
    .agg({
        "최고기온(℃)": "mean",
        "최저기온(℃)": "mean"
    })
)

if chart_data.empty:

    st.warning(
        f"{selected_month_name} 데이터가 없습니다."
    )

    st.stop()


# ==========================================
# 7. 그래프 생성
# ==========================================

fig = go.Figure()

# 최고기온 - 파스텔 빨간색
fig.add_trace(
    go.Scatter(
        x=chart_data["연도"],
        y=chart_data["최고기온(℃)"],
        mode="lines+markers",
        name="최고기온",
        line=dict(
            color="#F2A3A3",
            width=3
        ),
        marker=dict(
            color="#F2A3A3",
            size=7
        ),
        connectgaps=False,
        hovertemplate=
        "%{x}년<br>최고기온: %{y:.1f}℃<extra></extra>"
    )
)

# 최저기온 - 파스텔 파란색
fig.add_trace(
    go.Scatter(
        x=chart_data["연도"],
        y=chart_data["최저기온(℃)"],
        mode="lines+markers",
        name="최저기온",
        line=dict(
            color="#9CC9F5",
            width=3
        ),
        marker=dict(
            color="#9CC9F5",
            size=7
        ),
        connectgaps=False,
        hovertemplate=
        "%{x}년<br>최저기온: %{y:.1f}℃<extra></extra>"
    )
)


# ==========================================
# 8. 그래프 디자인
# ==========================================

fig.update_layout(

    title=dict(
        text="월별 기온분석",
        x=0.5,
        xanchor="center",
        font=dict(size=25)
    ),

    xaxis_title="연도",

    yaxis_title="온도(℃)",

    legend=dict(
        title="범례",
        orientation="h",
        yanchor="bottom",
        y=1.02,
        xanchor="right",
        x=1
    ),

    template="plotly_white",

    hovermode="x unified",

    height=550,

    margin=dict(
        l=50,
        r=40,
        t=110,
        b=60
    )
)

# 가로축 설정
fig.update_xaxes(
    title="연도",
    showgrid=True,
    gridcolor="#EEEEEE",
    tickformat="d"
)

# 세로축 설정
fig.update_yaxes(
    title="온도(℃)",
    showgrid=True,
    gridcolor="#EEEEEE",
    zeroline=True,
    zerolinecolor="#BBBBBB"
)


# ==========================================
# 9. 그래프 출력
# ==========================================

st.plotly_chart(
    fig,
    use_container_width=True
)


# ==========================================
# 10. 데이터 표
# ==========================================

with st.expander("📊 연도별 기온 데이터 확인"):

    display_data = chart_data.copy()

    display_data = display_data.round(1)

    st.dataframe(
        display_data,
        use_container_width=True,
        hide_index=True
    )


# ==========================================
# 11. 하단 안내
# ==========================================

st.caption(
    f"자료: {CSV_PATH.name} | "
    f"한글 인코딩: {encoding_used}"
)
