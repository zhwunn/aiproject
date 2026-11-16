
import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go

from pathlib import Path
from sklearn.neighbors import KNeighborsClassifier
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler


# ==========================================
# 1. 페이지 설정
# ==========================================

st.set_page_config(
    page_title="봄날의 아이리스 🌸",
    page_icon="🌸",
    layout="wide"
)


# ==========================================
# 2. 벚꽃 애니메이션 및 디자인
# ==========================================

st.markdown("""
<style>

@import url('https://fonts.googleapis.com/css2?family=Gowun+Dodum&display=swap');

.stApp {
    background:
        linear-gradient(
            180deg,
            #F9FFF7 0%,
            #FFF9FC 45%,
            #F5FFF2 100%
        );
    font-family: 'Gowun Dodum', sans-serif;
}

header[data-testid="stHeader"] {
    background: transparent;
}

.block-container {
    padding-top: 2rem;
    padding-bottom: 4rem;
    max-width: 1100px;
}

/* 제목 */

h1 {
    color: #657D65 !important;
    font-size: 42px !important;
    font-weight: 700 !important;
}

h2, h3 {
    color: #718C70 !important;
}

/* 일반 글씨 */

p, label {
    color: #687B68;
}

/* 입력창 */

div[data-baseweb="input"] {
    background-color: #FFFFFF;
    border-radius: 14px;
}

div[data-baseweb="select"] {
    border-radius: 14px;
}

/* 버튼 */

.stButton > button {
    background: linear-gradient(
        120deg,
        #E9D8F7,
        #F8DCE9
    );
    color: #755E83;
    border: 1px solid #EBD9F1;
    border-radius: 18px;
    height: 3.3rem;
    font-size: 17px;
    font-weight: bold;
    transition: 0.3s;
}

.stButton > button:hover {
    background: #DCC8EE;
    color: #FFFFFF;
    transform: translateY(-2px);
}

/* 카드 */

div[data-testid="stMetric"] {
    background: rgba(255,255,255,0.85);
    padding: 20px;
    border-radius: 20px;
    border: 1px solid #E9EDE2;
    box-shadow: 0 5px 18px rgba(130,150,120,0.07);
}

/* 구분선 */

hr {
    border-color: #E7EDE1;
}

/* 벚꽃잎 애니메이션 */

.petal-container {
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    overflow: hidden;
    pointer-events: none;
    z-index: 9999;
}

.petal {
    position: absolute;
    top: -10%;
    width: 15px;
    height: 21px;
    border-radius: 2px 100% 2px 100%;
    background: linear-gradient(
        135deg,
        #FFFFFF,
        #F7CDE0,
        #EAC5ED
    );
    opacity: 0.75;
    animation: falling linear infinite;
    box-shadow: 0 1px 5px rgba(222,170,200,0.15);
}

@keyframes falling {
    0% {
        transform: translate3d(0, -10vh, 0) rotate(0deg);
    }

    25% {
        transform: translate3d(45px, 25vh, 0) rotate(100deg);
    }

    50% {
        transform: translate3d(-35px, 55vh, 0) rotate(200deg);
    }

    75% {
        transform: translate3d(45px, 80vh, 0) rotate(280deg);
    }

    100% {
        transform: translate3d(-20px, 115vh, 0) rotate(360deg);
    }
}

</style>
""", unsafe_allow_html=True)


# 벚꽃잎 생성

petal_positions = [
    (3, 0, 14), (10, 3, 17), (17, 6, 12),
    (24, 2, 16), (31, 8, 13), (38, 1, 18),
    (45, 5, 15), (52, 0, 12), (59, 7, 17),
    (66, 3, 14), (73, 9, 18), (80, 2, 13),
    (87, 6, 16), (94, 1, 12), (15, 10, 20),
    (35, 12, 19), (55, 11, 21), (76, 13, 18),
    (90, 15, 20), (5, 18, 22)
]

petal_html = "".join(
    f'<span class="petal" style="left:{left}%;'
    f'animation-delay:-{delay}s;'
    f'animation-duration:{duration}s;"></span>'
    for left, delay, duration in petal_positions
)

st.markdown(
    f'<div class="petal-container">{petal_html}</div>',
    unsafe_allow_html=True
)


# ==========================================
# 3. CSV 파일 불러오기
# ==========================================

@st.cache_data
def load_data():

    # pages 폴더의 상위 폴더에서 CSV 찾기
    file_path = (
        Path(__file__).resolve().parent.parent
        / "Iris.csv"
    )

    if not file_path.exists():
        raise FileNotFoundError(
            "상위 폴더에 Iris.csv 파일이 있는지 확인해주세요."
        )

    data = pd.read_csv(
        file_path,
        encoding="cp949"
    )

    required_columns = [
        "꽃잎 길이",
        "꽃잎 너비",
        "품종"
    ]

    for col in required_columns:
        if col not in data.columns:
            raise ValueError(
                f"CSV 파일에 {col} 컬럼이 없습니다."
            )

    data = data.dropna(
        subset=required_columns
    )

    return data


try:
    df = load_data()

except Exception as e:
    st.error(f"데이터 불러오기 오류: {e}")
    st.stop()


# ==========================================
# 4. 머신러닝 모델 생성
# ==========================================

X = df[["꽃잎 길이", "꽃잎 너비"]]
y = df["품종"]

model = Pipeline([
    ("scaler", StandardScaler()),
    ("knn", KNeighborsClassifier(n_neighbors=5))
])

model.fit(X, y)


# ==========================================
# 5. 화면 제목
# ==========================================

st.markdown(
    """
    <div style="
        text-align:center;
        padding:25px 10px 15px 10px;
    ">
        <div style="
            font-size:48px;
            margin-bottom:5px;
        ">
            🌸 🌿 🌸
        </div>

        <h1 style="
            font-size:42px;
            color:#718B70;
            margin-bottom:8px;
        ">
            A Spring Day with Iris
        </h1>

        <p style="
            font-size:17px;
            color:#A18CA6;
        ">
            봄바람을 따라 피어나는 아름다운 붓꽃 이야기
        </p>

        <p style="
            font-size:13px;
            color:#9BAA91;
        ">
            Discover the beauty of Iris flowers
        </p>
    </div>
    """,
    unsafe_allow_html=True
)

st.divider()


# ==========================================
# 6. 데이터 입력 범위
# ==========================================

length_min = float(df["꽃잎 길이"].min())
length_max = float(df["꽃잎 길이"].max())

width_min = float(df["꽃잎 너비"].min())
width_max = float(df["꽃잎 너비"].max())


st.markdown("## 🌷 나만의 붓꽃을 만나보세요")

st.write(
    "꽃잎의 길이와 너비를 입력하면 "
    "어떤 품종인지 알아볼 수 있어요."
)

col1, col2 = st.columns(2)

with col1:

    st.markdown("### 🌸 Petal Length")

    petal_length = st.number_input(
        "꽃잎 길이 (cm)",
        min_value=length_min,
        max_value=length_max,
        value=3.0,
        step=0.1,
        format="%.1f"
    )

    st.caption(
        f"측정 범위: {length_min} ~ {length_max} cm"
    )


with col2:

    st.markdown("### 🌸 Petal Width")

    petal_width = st.number_input(
        "꽃잎 너비 (cm)",
        min_value=width_min,
        max_value=width_max,
        value=1.0,
        step=0.1,
        format="%.1f"
    )

    st.caption(
        f"측정 범위: {width_min} ~ {width_max} cm"
    )


st.markdown(
    """
    <div style="
        background:rgba(255,255,255,0.75);
        border:1px solid #E9EBDD;
        border-radius:15px;
        padding:15px;
        text-align:center;
        color:#82937B;
        margin:15px 0;
    ">
        🍃 실제 Iris 데이터의 측정 범위를 기준으로 입력해주세요.
    </div>
    """,
    unsafe_allow_html=True
)


# ==========================================
# 7. 품종 예측
# ==========================================

st.markdown("## 🦋 붓꽃 품종 예측")

if st.button(
    "🌸 나의 붓꽃 품종 알아보기",
    use_container_width=True
):

    input_data = pd.DataFrame(
        [[petal_length, petal_width]],
        columns=["꽃잎 길이", "꽃잎 너비"]
    )

    prediction = model.predict(input_data)[0]

    probabilities = model.predict_proba(input_data)[0]

    confidence = probabilities[
        list(model.classes_).index(prediction)
    ] * 100

    korean_names = {
        "Iris-setosa": "세토사 (Setosa)",
        "Iris-versicolor": "버시컬러 (Versicolor)",
        "Iris-virginica": "버지니카 (Virginica)"
    }

    result = korean_names.get(
        prediction, prediction
    )

    st.markdown(
        f"""
        <div style="
            background:linear-gradient(
                120deg,
                #FFF5FA,
                #F5F8FF,
                #F5FFF1
            );
            padding:30px;
            border-radius:23px;
            border:1px solid #EADDEB;
            text-align:center;
            margin-top:20px;
        ">
            <div style="font-size:40px;">
                🌸 ✨ 🌸
            </div>

            <h2 style="color:#8C719B;">
                당신의 붓꽃은...
            </h2>

            <h1 style="
                color:#A17CB6;
                font-size:32px;
            ">
                {result}
            </h1>

            <p style="color:#899A82;">
                KNN 알고리즘의 예측 결과입니다.
            </p>

            <h3 style="color:#A17CB6;">
                모델 투표 비율 {confidence:.1f}%
            </h3>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.caption(
        "※ 투표 비율은 가장 가까운 5개 데이터의 "
        "품종 투표 결과이며 실제 정확도와는 다릅니다."
    )


# ==========================================
# 8. 그래프
# ==========================================

st.divider()

st.markdown("## 🌿 꽃잎 크기 관찰하기")

st.write(
    "그래프에서 다른 품종의 꽃잎 크기를 비교하고 "
    "내가 입력한 위치를 확인할 수 있어요."
)

fig = go.Figure()

colors = {
    "Iris-setosa": "#C7DDBB",
    "Iris-versicolor": "#A9CFC4",
    "Iris-virginica": "#E7C9D8"
}

for species in df["품종"].unique():

    subset = df[df["품종"] == species]

    korean_names = {
        "Iris-setosa": "세토사",
        "Iris-versicolor": "버시컬러",
        "Iris-virginica": "버지니카"
    }

    fig.add_trace(
        go.Scatter(
            x=subset["꽃잎 길이"],
            y=subset["꽃잎 너비"],
            mode="markers",
            name=korean_names.get(species, species),

            marker=dict(
                size=10,
                color=colors.get(
                    species, "#D8D8D8"
                ),
                opacity=0.75,
                line=dict(
                    color="white",
                    width=1
                )
            )
        )
    )


# 사용자 입력값

fig.add_trace(
    go.Scatter(
        x=[petal_length],
        y=[petal_width],

        mode="markers",
        name="내가 입력한 꽃잎",

        marker=dict(
            size=25,
            color="#C7A4E8",
            symbol="star",
            line=dict(
                color="#9670B9",
                width=2
            )
        )
    )
)


fig.update_layout(

    title=dict(
        text="🌸 Petal Length & Width",
        font=dict(
            size=23,
            color="#788C76"
        ),
        x=0.5
    ),

    xaxis_title="꽃잎 길이 (cm)",
    yaxis_title="꽃잎 너비 (cm)",

    plot_bgcolor="#FCFFF9",
    paper_bgcolor="#FFFFFF",

    font=dict(
        family="Malgun Gothic",
        color="#75836F"
    ),

    height=560,

    margin=dict(
        l=30,
        r=30,
        t=80,
        b=40
    ),

    xaxis=dict(
        range=[
            length_min - 0.3,
            length_max + 0.3
        ],
        gridcolor="#EAEFE5",
        zeroline=False
    ),

    yaxis=dict(
        range=[
            max(0, width_min - 0.2),
            width_max + 0.3
        ],
        gridcolor="#EAEFE5",
        zeroline=False
    ),

    legend=dict(
        orientation="h",
        y=-0.2,
        x=0.5,
        xanchor="center"
    ),

    hovermode="closest"
)

st.plotly_chart(
    fig,
    use_container_width=True
)


# ==========================================
# 9. 데이터 정보
# ==========================================

with st.expander("🌼 아이리스 데이터 알아보기"):

    st.write("**데이터 출처:** Iris.csv")
    st.write("**전체 데이터:**", len(df), "개")
    st.write("**분류 알고리즘:** KNN")
    st.write("**이웃 수:** 5")
    st.write("**데이터 전처리:** StandardScaler")

    st.write("### 품종별 데이터 개수")

    st.dataframe(
        df["품종"].value_counts(),
        use_container_width=True
    )


# ==========================================
# 10. 마무리 문구
# ==========================================

st.markdown(
    """
    <div style="
        text-align:center;
        padding:35px 10px;
        color:#A18DA5;
    ">
        <div style="font-size:30px;">
            🌸 🦋 🌸
        </div>

        <p style="font-size:16px;">
            Every flower blooms in its own time.
        </p>

        <p style="font-size:12px;color:#A5B39C;">
            A little spring garden made with data.
        </p>
    </div>
    """,
    unsafe_allow_html=True
)
