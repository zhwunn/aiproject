
import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go

from pathlib import Path
from sklearn.neighbors import KNeighborsClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline


# --------------------------------
# 1. 페이지 설정
# --------------------------------

st.set_page_config(
    page_title="아이리스 품종 예측",
    page_icon="🌸",
    layout="wide"
)


# --------------------------------
# 2. 배경 및 디자인
# --------------------------------

st.markdown("""
<style>
.stApp {
    background-color: #F8FFF5;
}

section[data-testid="stSidebar"] {
    background-color: #F0F8EA;
}

h1, h2, h3 {
    color: #536B4E;
}

p, label, div {
    color: #52644D;
}

.stButton > button {
    background-color: #DCCAF5;
    color: #51416B;
    border-radius: 12px;
    border: none;
    font-weight: bold;
}

.stButton > button:hover {
    background-color: #CBB2EA;
    color: white;
}

div[data-testid="stMetric"] {
    background-color: #FFFFFF;
    padding: 18px;
    border-radius: 15px;
    border: 1px solid #E5EEDD;
}
</style>
""", unsafe_allow_html=True)


# --------------------------------
# 3. 데이터 불러오기
# --------------------------------

@st.cache_data
def load_data():

    file_path = Path(__file__).resolve().parent / "Iris.csv"

    if not file_path.exists():
        raise FileNotFoundError(
            "Iris.csv 파일을 app.py와 같은 폴더에 넣어주세요."
        )

    for encoding in ["utf-8-sig", "cp949", "euc-kr"]:
        try:
            data = pd.read_csv(file_path, encoding=encoding)
            break
        except UnicodeDecodeError:
            continue
    else:
        raise ValueError("CSV 파일의 인코딩을 확인해주세요.")

    required_columns = ["꽃잎 길이", "꽃잎 너비", "품종"]

    for column in required_columns:
        if column not in data.columns:
            raise ValueError(
                f"CSV 파일에 '{column}' 컬럼이 없습니다."
            )

    return data


try:
    df = load_data()

except Exception as e:
    st.error(str(e))
    st.stop()


# --------------------------------
# 4. 데이터 전처리
# --------------------------------

X = df[["꽃잎 길이", "꽃잎 너비"]]
y = df["품종"]


# --------------------------------
# 5. 머신러닝 모델 생성
# --------------------------------

model = Pipeline([
    ("scaler", StandardScaler()),
    ("knn", KNeighborsClassifier(n_neighbors=5))
])

model.fit(X, y)


# --------------------------------
# 6. 제목
# --------------------------------

st.title("🌸 아이리스 붓꽃 품종 예측")
st.write(
    "꽃잎의 길이와 너비를 입력하면 "
    "인공지능이 붓꽃의 품종을 예측합니다."
)

st.divider()


# --------------------------------
# 7. 입력 범위 설정
# --------------------------------

petal_length_min = float(df["꽃잎 길이"].min())
petal_length_max = float(df["꽃잎 길이"].max())

petal_width_min = float(df["꽃잎 너비"].min())
petal_width_max = float(df["꽃잎 너비"].max())


# --------------------------------
# 8. 사용자 입력
# --------------------------------

st.subheader("🌿 붓꽃 크기 입력하기")

col1, col2 = st.columns(2)

with col1:

    st.markdown("### 🌷 꽃잎 길이")

    petal_length = st.number_input(
        "꽃잎 길이 (cm)",
        min_value=petal_length_min,
        max_value=petal_length_max,
        value=3.0,
        step=0.1,
        format="%.1f"
    )

    st.caption(
        f"입력 가능 범위: {petal_length_min} ~ "
        f"{petal_length_max} cm"
    )


with col2:

    st.markdown("### 🌷 꽃잎 너비")

    petal_width = st.number_input(
        "꽃잎 너비 (cm)",
        min_value=petal_width_min,
        max_value=petal_width_max,
        value=1.0,
        step=0.1,
        format="%.1f"
    )

    st.caption(
        f"입력 가능 범위: {petal_width_min} ~ "
        f"{petal_width_max} cm"
    )


st.divider()


# --------------------------------
# 9. 품종 예측
# --------------------------------

st.subheader("🔍 품종 예측 결과")

if st.button("🌸 품종 예측하기", use_container_width=True):

    input_data = pd.DataFrame(
        [[petal_length, petal_width]],
        columns=["꽃잎 길이", "꽃잎 너비"]
    )

    prediction = model.predict(input_data)[0]

    probability = model.predict_proba(input_data)[0]

    korean_names = {
        "Iris-setosa": "세토사 (Setosa)",
        "Iris-versicolor": "버시컬러 (Versicolor)",
        "Iris-virginica": "버지니카 (Virginica)"
    }

    result_name = korean_names.get(
        prediction, prediction
    )

    confidence = probability[
        list(model.classes_).index(prediction)
    ] * 100

    st.success(
        f"예측된 붓꽃 품종은 🌸 {result_name} 입니다!"
    )

    result_col1, result_col2 = st.columns(2)

    with result_col1:
        st.metric(
            "예측 품종",
            result_name
        )

    with result_col2:
        st.metric(
            "예측 품종의 모델 확률",
            f"{confidence:.1f}%"
        )

    st.caption(
        "※ 모델 확률은 KNN의 이웃 투표 비율이며, "
        "실제 예측의 정확도를 의미하지는 않습니다."
    )


# --------------------------------
# 10. 그래프 시각화
# --------------------------------

st.divider()

st.subheader("📊 꽃잎 길이와 너비 그래프")

st.write(
    "기존 붓꽃 데이터와 사용자가 입력한 값을 "
    "산점도로 비교할 수 있습니다."
)

fig = go.Figure()


# 기존 데이터 표시
species_colors = {
    "Iris-setosa": "#B9D9B0",
    "Iris-versicolor": "#A9CFC4",
    "Iris-virginica": "#D9D0B9"
}

for species in df["품종"].unique():

    species_data = df[df["품종"] == species]

    fig.add_trace(
        go.Scatter(
            x=species_data["꽃잎 길이"],
            y=species_data["꽃잎 너비"],
            mode="markers",
            name=species,
            marker=dict(
                size=8,
                color=species_colors.get(
                    species, "#C8D9C0"
                ),
                opacity=0.65
            )
        )
    )


# 사용자 입력값 표시
fig.add_trace(
    go.Scatter(
        x=[petal_length],
        y=[petal_width],
        mode="markers",
        name="내가 입력한 값",
        marker=dict(
            size=23,
            color="#C9A7EB",
            symbol="star",
            line=dict(
                color="#9271BD",
                width=2
            )
        )
    )
)


# 그래프 디자인
fig.update_layout(
    title="🌸 아이리스 꽃잎 크기 비교",
    xaxis_title="꽃잎 길이 (cm)",
    yaxis_title="꽃잎 너비 (cm)",

    plot_bgcolor="#F8FFF5",
    paper_bgcolor="#F8FFF5",

    font=dict(
        family="Malgun Gothic",
        color="#52644D"
    ),

    legend_title="붓꽃 품종",
    height=550,

    xaxis=dict(
        range=[
            petal_length_min - 0.2,
            petal_length_max + 0.2
        ],
        gridcolor="#E4EEDD"
    ),

    yaxis=dict(
        range=[
            max(0, petal_width_min - 0.1),
            petal_width_max + 0.2
        ],
        gridcolor="#E4EEDD"
    )
)

st.plotly_chart(
    fig,
    use_container_width=True
)


# --------------------------------
# 11. 데이터 안내
# --------------------------------

with st.expander("🌱 데이터 및 알고리즘 정보"):

    st.write("**사용 데이터:** Iris.csv")
    st.write("**전체 데이터 수:**", len(df))
    st.write("**사용 알고리즘:** K-최근접 이웃 (KNN)")
    st.write("**이웃 수:** 5")
    st.write("**전처리:** StandardScaler")
    st.write("**분석 변수:** 꽃잎 길이, 꽃잎 너비")
    st.write("**예측 대상:** 붓꽃 품종")

    st.write("### 품종별 데이터 개수")

    st.dataframe(
        df["품종"].value_counts().rename("데이터 개수"),
        use_container_width=True
    )

st.divider()

st.caption(
    "🌿 Iris Flower Prediction | "
    "Pandas & Scikit-learn & Streamlit"
)
