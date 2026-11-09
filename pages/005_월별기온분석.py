
import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from pathlib import Path
import re

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
# 2. 날짜 변환 함수
# ==========================================

def convert_dates(series):

    values = series.astype(str).str.strip()

    result = []
    century = 1900
    previous_year = None

    for value in values:

        if value.lower() in ["nan", "none", ""]:
            result.append(pd.NaT)
            continue

        # Oct-07 형식 처리
        match = re.match(
            r"^([A-Za-z]{3})[-/ ](\d{2})$",
            value
        )

        if match:
            month = match.group(1)
            short_year = int(match.group(2))

            if (
                previous_year is not None
                and short_year < previous_year
            ):
                century += 100

            year = century + short_year
            previous_year = short_year

            date = pd.to_datetime(
                f"{month}-{year}",
                format="%b-%Y",
                errors="coerce"
            )

            result.append(date)
            continue

        # 4자리 연도 또는 일반 날짜 형식 처리
        date = pd.to_datetime(
            value,
            errors="coerce"
        )

        result.append(date)

    return pd.to_datetime(result)


# ==========================================
# 3. CSV 데이터 불러오기
# ==========================================

@st.cache_data
def load_data():

    folder = Path(__file__).parent

    # CSV 파일 자동 검색
    candidates = [
        folder / "temperature.csv",
        folder / "temperature(1).csv",
        folder / "temperature(2).csv"
    ]

    file_path = next(
        (p for p in candidates if p.exists()),
        None
    )

    if file_path is None:
        csv_files = sorted(folder.glob("*.csv"))
        if csv_files:
            file_path = csv_files[0]

    if file_path is None:
        raise FileNotFoundError(
            "temperature.csv 파일을 찾을 수 없습니다."
        )

    # 한글 인코딩 처리
    df = None

    for encoding in ["cp949", "euc-kr", "utf-8-sig", "utf-8"]:

        try:
            df = pd.read_csv(
                file_path,
                encoding=encoding
            )
            break

        except UnicodeDecodeError:
            continue

    if df is None:
        raise ValueError("CSV 파일의 인코딩을 확인해 주세요.")

    # 열 이름 정리
    df.columns = [
        str(col).replace("\ufeff", "").replace("\t", "").strip()
        for col in df.columns
    ]

    # 필요한 열 찾기
    date_col = next(
        (c for c in df.columns if "일시" in c),
        None
    )

    max_col = next(
        (c for c in df.columns if "최고기온" in c),
        None
    )

    min_col = next(
        (c for c in df.columns if "최저기온" in c),
        None
    )

    if not all([date_col, max_col, min_col]):
        raise ValueError(
            "일시, 최고기온, 최저기온 열을 찾을 수 없습니다."
        )

    # 날짜 변환
    df["일시"] = convert_dates(df[date_col])

    # 기온 숫자 변환
    df["최고기온"] = pd.to_numeric(
        df[max_col],
        errors="coerce"
    )

    df["최저기온"] = pd.to_numeric(
        df[min_col],
        errors="coerce"
    )

    # 날짜 없는 행 제거
    df = df.dropna(subset=["일시"]).copy()

    # 연도와 월 추출
    df["연도"] = df["일시"].dt.year
    df["월"] = df["일시"].dt.month

    return df.sort_values("일시")


# ==========================================
# 4. 데이터 실행
# ==========================================

try:
    df = load_data()

except Exception as e:
    st.error(f"데이터를 불러오지 못했습니다: {e}")
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
].copy()

chart_data = chart_data.sort_values("연도")

# 같은 연도에 같은 월의 자료가 여러 개라면 평균 처리
chart_data = (
    chart_data
    .groupby("연도", as_index=False)
    .agg({
        "최고기온": "mean",
        "최저기온": "mean"
    })
)

if chart_data.empty:
    st.warning("선택한 월의 데이터가 없습니다.")
    st.stop()


# ==========================================
# 7. 꺾은 선 그래프
# ==========================================

fig = go.Figure()

# 최고기온 - 파스텔 빨간색
fig.add_trace(
    go.Scatter(
        x=chart_data["연도"],
        y=chart_data["최고기온"],
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
        y=chart_data["최저기온"],
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

# 가로축
fig.update_xaxes(
    title="연도",
    showgrid=True,
    gridcolor="#EEEEEE"
)

# 세로축
fig.update_yaxes(
    title="온도(℃)",
    showgrid=True,
    gridcolor="#EEEEEE",
    zeroline=True
)


# 그래프 출력
st.plotly_chart(
    fig,
    use_container_width=True
)


# ==========================================
# 9. 데이터 표 출력
# ==========================================

with st.expander("📊 연도별 기온 데이터 확인"):

    display_data = chart_data.copy()

    display_data = display_data.rename(
        columns={
            "연도": "연도",
            "최고기온": "최고기온(℃)",
            "최저기온": "최저기온(℃)"
        }
    )

    display_data = display_data.round(1)

    st.dataframe(
        display_data,
        use_container_width=True,
        hide_index=True
    )


# ==========================================
# 10. 하단 안내
# ==========================================

st.caption(
    "자료: temperature.csv | 서울 기온 데이터 분석"
)
