
import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go

from pathlib import Path
from datetime import datetime

from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor
from sklearn.tree import DecisionTreeRegressor


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

</style>
""", unsafe_allow_html=True)


st.title("🌤️ 월별 평균기온 예측")
st.write(
    "과거의 월별 평균기온 데이터를 분석하고 "
    "다양한 회귀 알고리즘으로 미래 기온을 예측합니다."
)

st.divider()


# =====================================
# 3. CSV 파일 경로
# =====================================

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

    if "일시" not in df.columns:
        raise ValueError("'일시' 열이 없습니다.")

    if "평균기온(℃)" not in df.columns:
        raise ValueError("'평균기온(℃)' 열이 없습니다.")

    # 날짜 처리
    date_parts = df["일시"].astype(str).str.strip().str.extract(
        r"^([A-Za-z]{3})-(\d{2})$"
    )

    month_map = {
        "Jan": 1, "Feb": 2, "Mar": 3,
        "Apr": 4, "May": 5, "Jun": 6,
        "Jul": 7, "Aug": 8, "Sep": 9,
        "Oct": 10, "Nov": 11, "Dec": 12
    }

    df["월"] = date_parts[0].str.title().map(month_map)

    df["두자리연도"] = pd.to_numeric(
        date_parts[1],
        errors="coerce"
    )

    if df["두자리연도"].isna().any() or df["월"].isna().any():
        raise ValueError("날짜 형식이 올바르지 않습니다. 예: Oct-07")

    # 마지막 연도를 기준으로 연도 계산
    last_yy = int(df["두자리연도"].iloc[-1])
    current_year = datetime.now().year

    last_year = (current_year // 100) * 100 + last_yy

    if last_year > current_year + 1:
        last_year -= 100

    years = [None] * len(df)
    years[-1] = last_year

    for i in range(len(df) - 2, -1, -1):

        years[i] = years[i + 1]

        if df["월"].iloc[i] > df["월"].iloc[i + 1]:
            years[i] -= 1

    df["연도"] = years

    df["평균기온(℃)"] = pd.to_numeric(
        df["평균기온(℃)"],
        errors="coerce"
    )

    df = df.dropna(
        subset=["연도", "월", "평균기온(℃)"]
    ).copy()

    df["연도"] = df["연도"].astype(int)
    df["월"] = df["월"].astype(int)

    return df


# =====================================
# 5. 데이터 오류 확인
# =====================================

try:

    if not CSV_PATH.exists():
        st.error(
            "temperature.csv 파일을 찾을 수 없습니다. "
            "프로젝트 상위 폴더에 CSV 파일이 있는지 확인해주세요."
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
# 7. 회귀 알고리즘 선택
# =====================================

st.subheader("🤖 회귀 알고리즘 선택")

algorithm = st.selectbox(
    "사용할 회귀 알고리즘을 선택하세요.",
    [
        "선형회귀 (Linear Regression)",
        "랜덤 포레스트 회귀 (Random Forest)",
        "의사결정나무 회귀 (Decision Tree)"
    ]
)


# =====================================
# 8. 선택한 월 데이터 추출
# =====================================

month_data = df[
    df["월"] == selected_month
].copy()

month_data = month_data.sort_values("연도")

month_data = (
    month_data.groupby("연도", as_index=False)
    ["평균기온(℃)"].mean()
)

if len(month_data) < 2:

    st.warning(
        "선택한 월의 데이터가 2개 이상 필요합니다."
    )
    st.stop()


# =====================================
# 9. 학습 데이터 설정
# =====================================

X = month_data[["연도"]]
y = month_data["평균기온(℃)"]


# =====================================
# 10. 알고리즘별 모델 생성
# =====================================

if algorithm == "선형회귀 (Linear Regression)":

    model = LinearRegression()

    algorithm_description = """
    선형회귀는 과거 데이터의 전체적인 변화 경향을
    하나의 직선으로 표현하는 알고리즘입니다.
    기울기와 절편을 계산하여 미래 기온을 예측합니다.
    """

elif algorithm == "랜덤 포레스트 회귀 (Random Forest)":

    model = RandomForestRegressor(
        n_estimators=200,
        max_depth=5,
        min_samples_leaf=2,
        random_state=42
    )

    algorithm_description = """
    랜덤 포레스트는 여러 개의 의사결정나무를 만들어
    각각 예측한 결과의 평균을 이용하는 알고리즘입니다.
    여러 나무의 결과를 결합하기 때문에 복잡한 데이터의
    비선형적인 관계도 학습할 수 있습니다.
    """

else:

    model = DecisionTreeRegressor(
        max_depth=3,
        min_samples_leaf=2,
        random_state=42
    )

    algorithm_description = """
    의사결정나무는 데이터를 여러 구간으로 나누고
    각 구간에 속한 데이터의 평균기온을 이용하여 예측합니다.
    데이터의 변화 패턴을 계단 형태의 그래프로 표현합니다.
    """


# =====================================
# 11. 모델 학습 및 예측
# =====================================

model.fit(X, y)

future_data = pd.DataFrame({
    "연도": [forecast_year]
})

predicted_temp = model.predict(future_data)[0]

# 학습 데이터에 대한 결정계수
r2 = model.score(X, y)


# =====================================
# 12. 그래프용 예측 데이터
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
    500
)

line_data = pd.DataFrame({
    "연도": line_years
})

line_temps = model.predict(line_data)


# =====================================
# 13. 예측 결과 출력
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

st.caption(f"현재 선택된 알고리즘: {algorithm}")


# =====================================
# 14. 그래프 생성
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
            size=10
        ),
        hovertemplate=
        "%{x}년<br>실제 평균기온: %{y:.2f}℃<extra></extra>"
    )
)


# 실제 기온과 학습 모델의 예측 차이
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


# 알고리즘이 학습한 예측 추세선
fig.add_trace(
    go.Scatter(
        x=line_years,
        y=line_temps,
        mode="lines",
        name="알고리즘 예측 추세선",
        line=dict(
            color="#E88B8B",
            width=3
        ),
        hovertemplate=
        "연도: %{x:.1f}<br>예측값: %{y:.2f}℃<extra></extra>"
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
            symbol="star",
            line=dict(
                color="white",
                width=2
            )
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
        text=f"{selected_month}월 평균기온 분석 및 예측",
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
        gridcolor="#EEEEEE"
    )
)

st.plotly_chart(
    fig,
    use_container_width=True
)


# =====================================
# 15. 알고리즘 설명
# =====================================

st.divider()

st.subheader("📖 선택한 회귀 알고리즘 알아보기")

st.write(algorithm_description)


# -------------------------------------
# 선형회귀 설명
# -------------------------------------

if algorithm == "선형회귀 (Linear Regression)":

    st.markdown("### ① 선형회귀의 작동 원리")

    st.latex(r"y = ax + b")

    st.write("""
    - x: 연도
    - y: 평균기온
    - a: 기울기
    - b: 절편

    과거 데이터와 직선 사이의 오차 제곱합이
    최소가 되도록 직선을 계산합니다.
    """)

    slope = model.coef_[0]
    intercept = model.intercept_

    st.markdown("### ② 이번 분석의 회귀식")

    st.latex(
        rf"y = {slope:.4f}x + ({intercept:.4f})"
    )

    st.write(f"""
    - 기울기: {slope:.4f}
    - 절편: {intercept:.4f}
    - 결정계수: {r2:.4f}
    """)

    if slope > 0:
        st.info("기울기가 양수이므로 전반적으로 상승하는 경향입니다.")
    elif slope < 0:
        st.info("기울기가 음수이므로 전반적으로 하락하는 경향입니다.")
    else:
        st.info("뚜렷한 선형 변화가 나타나지 않습니다.")

    st.markdown("### ③ 미래 기온 계산")

    st.latex(
        rf"y = {slope:.4f} \times {forecast_year} + ({intercept:.4f})"
    )


# -------------------------------------
# 랜덤 포레스트 설명
# -------------------------------------

elif algorithm == "랜덤 포레스트 회귀 (Random Forest)":

    st.markdown("### ① 랜덤 포레스트의 작동 원리")

    st.write("""
    랜덤 포레스트는 여러 개의 의사결정나무를 생성하여
    각각의 예측 결과를 평균 내는 알고리즘입니다.
    """)

    st.markdown("""
    **작동 과정**

    1. 과거 기온 데이터를 이용하여 여러 개의 학습용 데이터를 구성합니다.
    2. 각각의 데이터로 여러 의사결정나무를 학습합니다.
    3. 각각의 나무가 미래 기온을 예측합니다.
    4. 여러 나무의 예측값을 평균 내어 최종 결과를 만듭니다.
    """)

    st.latex(
        r"\hat{y} = \frac{1}{N}\sum_{i=1}^{N}T_i(x)"
    )

    st.write("""
    - N: 생성한 의사결정나무의 개수
    - Tᵢ(x): 각각의 나무가 예측한 기온
    - ŷ: 최종 예측 평균기온
    """)

    st.markdown("### ② 이번 분석의 설정")

    st.write("""
    - 생성한 의사결정나무: 200개
    - 최대 깊이: 5
    - 최소 리프 노드 데이터 수: 2개
    """)

    st.markdown("### ③ 그래프 해석")

    st.write("""
    빨간색 선은 200개 나무의 예측 결과를 평균 낸 값입니다.

    직선이 아닌 구간별 변화가 나타날 수 있으며,
    미래 연도가 과거 데이터 범위를 벗어나면
    마지막 구간의 예측값이 유지될 수 있습니다.
    """)


# -------------------------------------
# 의사결정나무 설명
# -------------------------------------

else:

    st.markdown("### ① 의사결정나무의 작동 원리")

    st.write("""
    의사결정나무는 데이터를 여러 구간으로 나누어
    각 구간의 특징을 학습하는 알고리즘입니다.
    """)

    st.markdown("""
    **작동 과정**

    1. 연도별 평균기온 데이터를 확인합니다.
    2. 기온의 차이를 기준으로 데이터를 여러 구간으로 나눕니다.
    3. 각 구간에 포함된 데이터의 평균기온을 계산합니다.
    4. 새로운 연도가 입력되면 해당 구간의 평균기온을 예측합니다.
    """)

    st.latex(
        r"\hat{y}_j = \frac{1}{n_j}\sum_{i \in R_j}y_i"
    )

    st.write("""
    - Rⱼ: 나누어진 데이터 구간
    - nⱼ: 해당 구간의 데이터 개수
    - ŷⱼ: 해당 구간의 예측 평균기온
    """)

    st.markdown("### ② 이번 분석의 설정")

    st.write("""
    - 최대 깊이: 3
    - 최소 리프 노드 데이터 수: 2개
    """)

    st.markdown("### ③ 그래프 해석")

    st.write("""
    빨간색 선이 계단 모양으로 나타날 수 있습니다.

    이는 연도별 데이터를 구간으로 나누고
    각 구간의 평균값으로 예측하기 때문입니다.

    학습 데이터의 마지막 연도 이후에는
    마지막 구간의 예측값이 유지될 수 있습니다.
    """)


# =====================================
# 16. 결정계수 설명
# =====================================

st.markdown("### 📊 결정계수(R²)란?")

st.write("""
결정계수는 학습된 회귀 모델이 실제 데이터의
변화를 얼마나 설명하는지 나타내는 지표입니다.

- 1에 가까울수록 실제 데이터의 변화 경향을 잘 설명합니다.
- 0에 가까울수록 설명하는 정도가 낮습니다.
- 음수라면 학습 데이터에 대한 평균값 예측보다 성능이 낮을 수 있습니다.

결정계수가 높다고 해서 미래 예측이 반드시 정확한 것은 아닙니다.
""")

st.metric(
    "현재 알고리즘의 결정계수",
    f"{r2:.4f}"
)


# =====================================
# 17. 실제 데이터 확인
# =====================================

with st.expander("📊 분석에 사용된 실제 데이터 확인하기"):

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


# =====================================
# 18. 주의사항
# =====================================

st.caption("""
※ 이 프로그램은 과거의 월별 평균기온을 학습하여
통계적으로 미래 기온을 예측하는 교육용 프로그램입니다.
실제 기상예보와는 차이가 있을 수 있습니다.
""")
