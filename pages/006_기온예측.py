
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
    "세 가지 회귀 알고리즘을 이용하여 "
    "과거 기온을 분석하고 미래 기온을 예측합니다."
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
        raise ValueError("날짜 형식을 확인해주세요. 예: Oct-07")

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
# 5. 데이터 불러오기
# =====================================

try:

    if not CSV_PATH.exists():
        st.error(
            "temperature.csv 파일을 찾을 수 없습니다."
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
# 7. 선택한 월 데이터 추출
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


X = month_data[["연도"]]
y = month_data["평균기온(℃)"]


# =====================================
# 8. 세 가지 회귀 알고리즘 생성
# =====================================

models = {

    "선형회귀": LinearRegression(),

    "랜덤 포레스트": RandomForestRegressor(
        n_estimators=200,
        max_depth=5,
        min_samples_leaf=2,
        random_state=42
    ),

    "의사결정나무": DecisionTreeRegressor(
        max_depth=3,
        min_samples_leaf=2,
        random_state=42
    )
}


# =====================================
# 9. 알고리즘별 학습 및 예측
# =====================================

results = []

for name, model in models.items():

    # 학습
    model.fit(X, y)

    # 미래 기온 예측
    future_data = pd.DataFrame({
        "연도": [forecast_year]
    })

    prediction = model.predict(future_data)[0]

    # 학습 데이터 결정계수
    r2 = model.score(X, y)

    results.append({
        "알고리즘": name,
        "예측 평균기온(℃)": prediction,
        "결정계수(R²)": r2
    })


result_df = pd.DataFrame(results)


# =====================================
# 10. 알고리즘 선택
# =====================================

st.divider()

st.subheader("🤖 회귀 알고리즘 선택")

selected_algorithm = st.selectbox(
    "자세히 확인할 알고리즘을 선택하세요.",
    [
        "선형회귀",
        "랜덤 포레스트",
        "의사결정나무"
    ]
)

selected_model = models[selected_algorithm]

selected_result = result_df[
    result_df["알고리즘"] == selected_algorithm
].iloc[0]

selected_prediction = selected_result["예측 평균기온(℃)"]
selected_r2 = selected_result["결정계수(R²)"]


# =====================================
# 11. 선택한 알고리즘의 결과
# =====================================

st.divider()

st.subheader(
    f"🌡️ {forecast_year}년 {selected_month}월 예측 결과"
)

col1, col2, col3 = st.columns(3)

with col1:

    st.metric(
        "선택한 알고리즘의 예측 기온",
        f"{selected_prediction:.2f} ℃"
    )

with col2:

    st.metric(
        "과거 평균기온",
        f"{y.mean():.2f} ℃"
    )

with col3:

    st.metric(
        "학습 결정계수 (R²)",
        f"{selected_r2:.3f}"
    )


# =====================================
# 12. 세 알고리즘 예측값 비교
# =====================================

st.divider()

st.subheader("📊 세 가지 알고리즘 예측 결과 비교")

st.write(
    "같은 월과 같은 예측 연도를 사용하여 "
    "세 가지 알고리즘이 계산한 결과입니다."
)

# 결과 표
comparison_table = result_df.copy()

comparison_table["예측 평균기온(℃)"] = (
    comparison_table["예측 평균기온(℃)"].round(2)
)

comparison_table["결정계수(R²)"] = (
    comparison_table["결정계수(R²)"].round(3)
)

st.dataframe(
    comparison_table,
    use_container_width=True,
    hide_index=True
)


# =====================================
# 13. 알고리즘별 예측 기온 차이 그래프
# =====================================

colors = [
    "#E88B8B",
    "#82B8E8",
    "#A6CFA8"
]

bar_fig = go.Figure()

bar_fig.add_trace(
    go.Bar(
        x=result_df["알고리즘"],
        y=result_df["예측 평균기온(℃)"],
        marker_color=colors,
        text=[
            f"{v:.2f}℃"
            for v in result_df["예측 평균기온(℃)"]
        ],
        textposition="outside",
        hovertemplate=
        "%{x}<br>예측 기온: %{y:.2f}℃<extra></extra>"
    )
)

bar_fig.update_layout(
    title=dict(
        text=f"{forecast_year}년 {selected_month}월 알고리즘별 예측 기온 비교",
        x=0.5
    ),
    xaxis_title="회귀 알고리즘",
    yaxis_title="예측 평균기온 (℃)",
    plot_bgcolor="#FFFFFF",
    paper_bgcolor="#FFF9F5",
    height=430,
    showlegend=False
)

st.plotly_chart(
    bar_fig,
    use_container_width=True
)


# 알고리즘 간 예측 차이
max_temp = result_df["예측 평균기온(℃)"].max()
min_temp = result_df["예측 평균기온(℃)"].min()
difference = max_temp - min_temp

st.info(
    f"세 알고리즘의 예측 기온 차이는 "
    f"최대 {difference:.2f}℃입니다."
)


# =====================================
# 14. 세 알고리즘의 변화 추세 비교
# =====================================

st.divider()

st.subheader("📈 세 가지 알고리즘의 예측 추세 비교")

start_year = int(month_data["연도"].min())

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

fig = go.Figure()

# 실제 데이터
fig.add_trace(
    go.Scatter(
        x=month_data["연도"],
        y=month_data["평균기온(℃)"],
        mode="markers",
        name="실제 평균기온",
        marker=dict(
            color="#333333",
            size=9,
            symbol="circle"
        )
    )
)


# 알고리즘별 추세선
algorithm_colors = {
    "선형회귀": "#E88B8B",
    "랜덤 포레스트": "#82B8E8",
    "의사결정나무": "#A6CFA8"
}

for name, model in models.items():

    line_predictions = model.predict(line_data)

    future_prediction = model.predict(
        pd.DataFrame({
            "연도": [forecast_year]
        })
    )[0]

    fig.add_trace(
        go.Scatter(
            x=line_years,
            y=line_predictions,
            mode="lines",
            name=name,
            line=dict(
                color=algorithm_colors[name],
                width=3
            )
        )
    )

    # 미래 예측 지점
    fig.add_trace(
        go.Scatter(
            x=[forecast_year],
            y=[future_prediction],
            mode="markers+text",
            name=f"{name} 예측값",
            marker=dict(
                color=algorithm_colors[name],
                size=14,
                symbol="star"
            ),
            text=[f"{future_prediction:.2f}℃"],
            textposition="top center",
            showlegend=True
        )
    )


fig.update_layout(
    title=dict(
        text=f"{selected_month}월 실제 기온과 세 알고리즘의 예측 비교",
        x=0.5
    ),
    xaxis_title="연도",
    yaxis_title="평균기온 (℃)",
    plot_bgcolor="#FFFFFF",
    paper_bgcolor="#FFF9F5",
    height=650,
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
# 15. 선택한 알고리즘 설명
# =====================================

st.divider()

st.subheader(
    f"📖 {selected_algorithm} 알고리즘 알아보기"
)


if selected_algorithm == "선형회귀":

    st.write("""
    선형회귀는 과거 데이터의 전체적인 변화 경향을
    하나의 직선으로 나타내는 알고리즘입니다.
    """)

    slope = selected_model.coef_[0]
    intercept = selected_model.intercept_

    st.markdown("### 작동 원리")

    st.latex(r"y = ax + b")

    st.write("""
    - x: 연도
    - y: 평균기온
    - a: 기울기
    - b: 절편
    """)

    st.markdown("### 이번 분석의 회귀식")

    st.latex(
        rf"y = {slope:.4f}x + ({intercept:.4f})"
    )

    st.write(f"""
    기울기: {slope:.4f}

    절편: {intercept:.4f}
    """)

    st.markdown("### 미래 기온 계산")

    st.latex(
        rf"y = {slope:.4f} \times {forecast_year} + ({intercept:.4f})"
    )


elif selected_algorithm == "랜덤 포레스트":

    st.write("""
    랜덤 포레스트는 여러 개의 의사결정나무를 만들고
    각각의 예측 결과를 평균 내는 알고리즘입니다.
    """)

    st.markdown("### 작동 원리")

    st.markdown("""
    1. 과거 데이터를 이용하여 여러 학습 데이터를 구성합니다.
    2. 여러 개의 의사결정나무를 학습합니다.
    3. 각각의 나무가 미래 기온을 예측합니다.
    4. 예측 결과의 평균을 최종값으로 사용합니다.
    """)

    st.latex(
        r"\hat{y} = \frac{1}{N}\sum_{i=1}^{N}T_i(x)"
    )

    st.write("""
    이번 프로그램에서는 200개의 의사결정나무를 사용합니다.

    각 나무의 예측값을 평균 내어 최종 기온을 계산합니다.
    """)

    st.markdown("### 주요 설정")

    st.write("""
    - 의사결정나무 개수: 200개
    - 최대 깊이: 5
    - 최소 리프 노드 데이터 수: 2개
    """)


else:

    st.write("""
    의사결정나무는 데이터를 여러 구간으로 나누고
    각 구간에 속한 데이터의 평균기온으로 예측합니다.
    """)

    st.markdown("### 작동 원리")

    st.markdown("""
    1. 과거 기온 데이터를 확인합니다.
    2. 데이터를 여러 구간으로 나눕니다.
    3. 각 구간의 평균기온을 계산합니다.
    4. 새로운 연도가 입력되면 해당 구간의 평균값을 예측합니다.
    """)

    st.latex(
        r"\hat{y}_j = \frac{1}{n_j}\sum_{i \in R_j}y_i"
    )

    st.markdown("### 주요 설정")

    st.write("""
    - 최대 깊이: 3
    - 최소 리프 노드 데이터 수: 2개
    """)


# =====================================
# 16. 결정계수 설명
# =====================================

st.divider()

st.subheader("📊 결정계수(R²)란?")

st.write("""
결정계수는 학습된 알고리즘이 실제 데이터의 변화 경향을
얼마나 설명하는지 나타내는 지표입니다.

- 1에 가까울수록 학습 데이터의 변화 경향을 잘 설명합니다.
- 0에 가까울수록 설명하는 정도가 낮습니다.
- 음수라면 학습 데이터의 평균값을 사용하는 것보다
  예측 성능이 낮을 수 있습니다.

결정계수가 높다고 해서 미래 예측이 반드시 정확한 것은 아닙니다.
""")

st.caption(
    "※ 표시된 결정계수는 학습에 사용한 데이터에 대한 값이며, "
    "미래 예측 정확도를 직접 나타내는 값은 아닙니다."
)


# =====================================
# 17. 실제 데이터 확인
# =====================================

with st.expander("📋 분석에 사용된 실제 데이터 확인하기"):

    st.dataframe(
        month_data.sort_values(
            "연도",
            ascending=False
        ),
        use_container_width=True,
        hide_index=True
    )


# =====================================
# 18. 주의사항
# =====================================

st.caption("""
이 프로그램은 과거의 월별 평균기온을 학습하는 교육용 예측 프로그램입니다.
실제 미래 기온은 기후 변화와 다양한 기상 요인에 따라 달라질 수 있습니다.
""")
