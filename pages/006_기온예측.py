
import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from sklearn.linear_model import LinearRegression
from pathlib import Path
from datetime import datetime

# =====================================
# 1. 페이지 설정
# =====================================
st.set_page_config(
    page_title="월별 평균기온 예측",
    page_icon="🌤️",
    layout="wide"
)

# =====================================
# 2. 디자인
# =====================================
st.markdown("""
<style>
.stApp {
    background-color: #FFF9F5;
}

h1, h2, h3 {
    color: #D98282;
}

div[data-testid="stMetric"] {
    background-color: #FFF0EB;
    padding: 18px;
    border-radius: 15px;
}

.stSelectbox, .stNumberInput {
    background-color: #FFFFFF;
}
</style>
""", unsafe_allow_html=True)

st.title("🌤️ 월별 평균기온 예측")
st.write(
    "과거의 월별 평균기온 데이터를 분석하여 "
    "선형회귀 알고리즘으로 미래 기온을 예측합니다."
)

st.divider()

# =====================================
# 3. CSV 파일 경로 설정
# =====================================

# 현재 파일: pages/app.py
# CSV 파일: 프로젝트/temperature.csv

BASE_DIR = Path(__file__).resolve().parent.parent
CSV_PATH = BASE_DIR / "temperature.csv"


# =====================================
# 4. 데이터 불러오기
# =====================================
@st.cache_data
def load_data():

    encodings = ["cp949", "euc-kr", "utf-8-sig"]
    df = None

    for encoding in encodings:
        try:
            df = pd.read_csv(
                CSV_PATH,
                encoding=encoding
            )
            break
        except UnicodeDecodeError:
            continue

    if df is None:
        raise ValueError("CSV 파일 인코딩을 확인해주세요.")

    df.columns = df.columns.str.strip()

    # 필요한 열 확인
    if "일시" not in df.columns:
        raise ValueError("'일시' 열이 없습니다.")

    if "평균기온(℃)" not in df.columns:
        raise ValueError("'평균기온(℃)' 열이 없습니다.")

    # =================================
    # 날짜 데이터 처리
    # =================================

    # 데이터의 월과 두 자리 연도 추출
    date_parts = df["일시"].astype(str).str.strip().str.extract(
        r"^([A-Za-z]{3})-(\d{2})$"
    )

    # 월 이름을 숫자로 변환
    month_map = {
        "Jan": 1, "Feb": 2, "Mar": 3,
        "Apr": 4, "May": 5, "Jun": 6,
        "Jul": 7, "Aug": 8, "Sep": 9,
        "Oct": 10, "Nov": 11, "Dec": 12
    }

    df["월"] = date_parts[0].map(month_map)
    df["두자리연도"] = pd.to_numeric(
        date_parts[1],
        errors="coerce"
    )

    # 마지막 연도를 기준으로 전체 연도 계산
    # 오래된 기온 데이터의 2자리 연도 오인식 방지
    if df["두자리연도"].isna().any() or df["월"].isna().any():
        raise ValueError("날짜 형식을 확인해주세요. 예: Oct-07")

    last_yy = int(df["두자리연도"].iloc[-1])
    current_year = datetime.now().year

    last_year = (current_year // 100) * 100 + last_yy

    if last_year > current_year + 1:
        last_year -= 100

    years = [None] * len(df)

    # 마지막 행부터 과거 방향으로 연도 계산
    years[-1] = last_year

    for i in range(len(df) - 2, -1, -1):

        years[i] = years[i + 1]

        # 과거로 이동하면서 12월에서 1월로 넘어가면
        # 연도를 1년 감소
        if df["월"].iloc[i] > df["월"].iloc[i + 1]:
            years[i] -= 1

    df["연도"] = years

    # 평균기온 숫자 변환
    df["평균기온(℃)"] = pd.to_numeric(
        df["평균기온(℃)"],
        errors="coerce"
    )

    # 결측값 제거
    df = df.dropna(
        subset=["연도", "월", "평균기온(℃)"]
    ).copy()

    df["연도"] = df["연도"].astype(int)
    df["월"] = df["월"].astype(int)

    return df


# =====================================
# 5. 데이터 불러오기 오류 처리
# =====================================
try:

    if not CSV_PATH.exists():
        st.error(
            "temperature.csv 파일을 찾을 수 없습니다. "
            "상위 폴더에 CSV 파일이 있는지 확인해주세요."
        )
        st.stop()

    df = load_data()

except Exception as e:

    st.error(f"데이터 처리 오류: {e}")
    st.stop()


# =====================================
# 6. 사용자 입력
# =====================================
st.subheader("🔍 예측 조건 설정")

col1, col2 = st.columns(2)

with col1:

    selected_month = st.selectbox(
        "분석할 월을 선택하세요.",
        range(1, 13),
        format_func=lambda x: f"{x}월"
    )

with col2:

    forecast_year = st.number_input(
        "예측할 연도를 입력하세요.",
        min_value=1900,
        max_value=2200,
        value=int(df["연도"].max()) + 1,
        step=1
    )

forecast_year = int(forecast_year)


# =====================================
# 7. 선택한 월의 데이터 추출
# =====================================
month_data = df[
    df["월"] == selected_month
].copy()

month_data = month_data.sort_values("연도")

# 같은 연도에 중복 데이터가 있다면 평균 계산
month_data = (
    month_data.groupby("연도", as_index=False)
    ["평균기온(℃)"].mean()
)

if len(month_data) < 2:

    st.warning(
        "선택한 월의 데이터가 2개 이상 있어야 예측할 수 있습니다."
    )
    st.stop()


# =====================================
# 8. 선형회귀 알고리즘
# =====================================

# X: 연도
# y: 평균기온

X = month_data[["연도"]]
y = month_data["평균기온(℃)"]

# 모델 생성
model = LinearRegression()

# 과거 데이터 학습
model.fit(X, y)

# 미래 기온 예측
future_data = pd.DataFrame({
    "연도": [forecast_year]
})

predicted_temp = model.predict(future_data)[0]

# 회귀식 계산
slope = model.coef_[0]
intercept = model.intercept_

# 결정계수
r2 = model.score(X, y)


# =====================================
# 9. 회귀선 생성
# =====================================

start_year = min(
    int(month_data["연도"].min()),
    forecast_year
)

end_year = max(
    int(month_data["연도"].max()),
    forecast_year
)

line_years = np.linspace(
    start_year,
    end_year,
    300
)

line_temps = model.predict(
    pd.DataFrame({"연도": line_years})
)


# =====================================
# 10. 예측 결과
# =====================================
st.divider()

st.subheader(
    f"🌡️ {forecast_year}년 {selected_month}월 평균기온 예측"
)

col1, col2, col3 = st.columns(3)

with col1:

    st.metric(
        "예측 평균기온",
        f"{predicted_temp:.2f} ℃"
    )

with col2:

    st.metric(
        "과거 평균기온",
        f"{month_data['평균기온(℃)'].mean():.2f} ℃"
    )

with col3:

    st.metric(
        "결정계수 (R²)",
        f"{r2:.3f}"
    )


# =====================================
# 11. 그래프 생성
# =====================================

fig = go.Figure()

# 실제 기온 데이터
fig.add_trace(
    go.Scatter(
        x=month_data["연도"],
        y=month_data["평균기온(℃)"],
        mode="markers",
        name="실제 평균기온",
        marker=dict(
            color="#82B8E8",
            size=9
        ),
        hovertemplate=
        "%{x}년<br>실제 기온: %{y:.2f}℃<extra></extra>"
    )
)

# 실제 데이터와 회귀선 사이의 오차
for _, row in month_data.iterrows():

    estimated = model.predict(
        pd.DataFrame({
            "연도": [row["연도"]]
        })
    )[0]

    fig.add_trace(
        go.Scatter(
            x=[row["연도"], row["연도"]],
            y=[row["평균기온(℃)"], estimated],
            mode="lines",
            line=dict(
                color="rgba(170,170,170,0.5)",
                width=1,
                dash="dot"
            ),
            showlegend=False,
            hoverinfo="skip"
        )
    )


# 선형회귀 추세선
fig.add_trace(
    go.Scatter(
        x=line_years,
        y=line_temps,
        mode="lines",
        name="선형회귀 추세선",
        line=dict(
            color="#E88B8B",
            width=3
        ),
        hovertemplate=
        "회귀선<br>%{x:.1f}년<br>%{y:.2f}℃<extra></extra>"
    )
)


# 미래 예측 지점
fig.add_trace(
    go.Scatter(
        x=[forecast_year],
        y=[predicted_temp],
        mode="markers+text",
        name="미래 예측 기온",
        marker=dict(
            color="#F2BC50",
            size=18,
            symbol="star"
        ),
        text=[f"{predicted_temp:.2f}℃"],
        textposition="top center",
        textfont=dict(
            color="#B7791F",
            size=14
        ),
        hovertemplate=
        "%{x}년 예측 기온: %{y:.2f}℃<extra></extra>"
    )
)


# 그래프 레이아웃
fig.update_layout(

    title=dict(
        text=f"{selected_month}월 연도별 평균기온 분석 및 예측",
        x=0.5,
        font=dict(
            size=21,
            color="#555555"
        )
    ),

    xaxis_title="연도",
    yaxis_title="평균기온 (℃)",

    plot_bgcolor="#FFFFFF",
    paper_bgcolor="#FFF9F5",

    height=600,

    hovermode="closest",

    legend=dict(
        orientation="h",
        yanchor="bottom",
        y=1.02,
        xanchor="center",
        x=0.5
    ),

    xaxis=dict(
        showgrid=True,
        gridcolor="#EEEEEE",
        dtick=5
    ),

    yaxis=dict(
        showgrid=True,
        gridcolor="#EEEEEE",
        zeroline=True,
        zerolinecolor="#BBBBBB"
    )
)

st.plotly_chart(
    fig,
    use_container_width=True
)


# =====================================
# 12. 선형회귀 알고리즘 설명
# =====================================
st.divider()

st.subheader("📖 선형회귀 알고리즘 알아보기")

st.write("""
선형회귀는 과거의 데이터에서 일정한 관계를 찾아
가장 적합한 직선을 만들고, 그 직선을 이용하여
미래의 값을 예측하는 머신러닝 알고리즘입니다.

이 프로그램은 과거의 연도별 평균기온을 학습하여
미래의 평균기온을 예측합니다.
""")

# 1단계
st.markdown("### ① 데이터 학습")

st.write("""
과거의 연도를 X값으로 사용하고,
각 연도의 평균기온을 Y값으로 사용합니다.

이 두 데이터의 관계를 분석하여
가장 적합한 직선을 찾습니다.
""")

st.latex(r"y = ax + b")

st.write("""
- x: 연도
- y: 평균기온
- a: 기울기
- b: y절편
""")

# 2단계
st.markdown("### ② 가장 적합한 직선 찾기")

st.write("""
실제 데이터의 점들과 직선 사이의 오차를 계산합니다.

선형회귀는 이 오차들의 제곱합이 최소가 되도록
기울기와 절편을 결정합니다.

그래프에서 빨간색 직선은 이렇게 계산된 회귀선이며,
회색 점선은 실제 기온과 회귀선 사이의 차이를 보여줍니다.
""")

st.latex(
    r"\min \sum_{i=1}^{n}(y_i-\hat{y}_i)^2"
)

# 3단계
st.markdown("### ③ 실제 분석에 사용된 회귀식")

st.write(
    "이번 분석에서 계산된 기울기와 절편은 다음과 같습니다."
)

st.latex(
    rf"y = {slope:.4f}x + ({intercept:.4f})"
)

st.write(f"""
- 기울기: {slope:.4f}
- 절편: {intercept:.4f}
- 결정계수(R²): {r2:.4f}
""")

if slope > 0:

    st.info(
        f"{selected_month}월 평균기온은 과거 데이터에서 "
        "전반적으로 상승하는 선형 경향을 보입니다."
    )

elif slope < 0:

    st.info(
        f"{selected_month}월 평균기온은 과거 데이터에서 "
        "전반적으로 하락하는 선형 경향을 보입니다."
    )

else:

    st.info(
        "평균기온에서 뚜렷한 선형 변화가 나타나지 않습니다."
    )


# 4단계
st.markdown("### ④ 미래 평균기온 예측")

st.write(
    f"학습한 회귀식에 {forecast_year}년을 대입합니다."
)

st.latex(
    rf"y = {slope:.4f} \times {forecast_year} + ({intercept:.4f})"
)

st.success(
    f"{forecast_year}년 {selected_month}월 "
    f"예측 평균기온은 {predicted_temp:.2f}℃입니다."
)


# 5단계
st.markdown("### ⑤ 결정계수(R²) 이해하기")

st.write("""
결정계수는 회귀 모델이 실제 데이터의 변화 경향을
얼마나 설명하는지 나타내는 지표입니다.

- 1에 가까울수록 데이터의 변화 경향을 잘 설명합니다.
- 0에 가까울수록 직선으로 설명하는 정도가 낮습니다.

결정계수가 높더라도 미래의 기온을 정확하게 맞힌다는
의미는 아닙니다.
""")

st.caption(
    "※ 선형회귀는 과거의 선형적인 변화 경향을 바탕으로 "
    "예측합니다. 실제 미래 기온은 기후 변화, 이상기후 등 "
    "여러 요인에 따라 달라질 수 있습니다."
)


# =====================================
# 13. 실제 데이터 확인
# =====================================
with st.expander("📊 분석에 사용된 실제 데이터 확인"):

    display_data = month_data[
        ["연도", "평균기온(℃)"]
    ].sort_values(
        "연도",
        ascending=False
    )

    st.dataframe(
        display_data,
        use_container_width=True,
        hide_index=True
    )

