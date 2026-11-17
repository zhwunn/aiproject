
import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go

from pathlib import Path
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.neighbors import KNeighborsClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.svm import SVC


# ==========================================
# 1. 페이지 설정
# ==========================================

st.set_page_config(
    page_title="봄날의 아이리스",
    page_icon="🌸",
    layout="wide"
)


# ==========================================
# 2. 디자인 및 벚꽃 애니메이션
# ==========================================

st.markdown("""
<style>

@import url('https://fonts.googleapis.com/css2?family=Gowun+Dodum&display=swap');

.stApp {
    background: linear-gradient(
        180deg,
        #F9FFF7 0%,
        #FFF9FC 50%,
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

h1, h2, h3 {
    color: #718B70 !important;
}

p, label {
    color: #687B68;
}

.stButton > button {
    background: linear-gradient(
        120deg,
        #E9D8F7,
        #F8DCE9
    );
    color: #755E83;
    border: 1px solid #EBD9F1;
    border-radius: 18px;
    height: 3.2rem;
    font-size: 16px;
    font-weight: bold;
}

.stButton > button:hover {
    background: #DCC8EE;
    color: white;
}

div[data-testid="stMetric"] {
    background: rgba(255,255,255,0.85);
    padding: 18px;
    border-radius: 18px;
    border: 1px solid #E9EDE2;
}

div[data-testid="stTabs"] button {
    color: #788B72;
    font-size: 16px;
}

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
    opacity: 0.7;
    animation: falling linear infinite;
}

@keyframes falling {
    0% {
        transform: translate3d(0,-10vh,0) rotate(0deg);
    }
    25% {
        transform: translate3d(45px,25vh,0) rotate(100deg);
    }
    50% {
        transform: translate3d(-35px,55vh,0) rotate(200deg);
    }
    75% {
        transform: translate3d(45px,80vh,0) rotate(280deg);
    }
    100% {
        transform: translate3d(-20px,115vh,0) rotate(360deg);
    }
}

</style>
""", unsafe_allow_html=True)


# 벚꽃잎 생성

petals = [
    (3, 0, 14), (10, 3, 17), (17, 6, 12),
    (24, 2, 16), (31, 8, 13), (38, 1, 18),
    (45, 5, 15), (52, 0, 12), (59, 7, 17),
    (66, 3, 14), (73, 9, 18), (80, 2, 13),
    (87, 6, 16), (94, 1, 12), (15, 10, 20),
    (35, 12, 19), (55, 11, 21), (76, 13, 18),
    (90, 15, 20), (5, 18, 22)
]

petal_html = "".join(
    f'<span class="petal" style="left:{x}%;'
    f'animation-delay:-{delay}s;'
    f'animation-duration:{duration}s;"></span>'
    for x, delay, duration in petals
)

st.markdown(
    f'<div class="petal-container">{petal_html}</div>',
    unsafe_allow_html=True
)


# ==========================================
# 3. 데이터 불러오기
# ==========================================

@st.cache_data
def load_data():

    # pages 폴더의 상위 폴더에서 CSV 불러오기
    file_path = (
        Path(__file__).resolve().parent.parent
        / "Iris.csv"
    )

    if not file_path.exists():
        raise FileNotFoundError(
            "상위 폴더에 Iris.csv 파일이 없습니다."
        )

    data = pd.read_csv(
        file_path,
        encoding="cp949"
    )

    # CSV의 실제 컬럼명 오타 보정
    data = data.rename(
        columns={
            "꽃발침 길이": "꽃받침 길이"
        }
    )

    required = [
        "꽃받침 길이",
        "꽃받침 너비",
        "꽃잎 길이",
        "꽃잎 너비",
        "품종"
    ]

    for col in required:
        if col not in data.columns:
            raise ValueError(
                f"CSV에 {col} 컬럼이 없습니다."
            )

    data = data.dropna(subset=required)

    for col in required[:4]:
        data[col] = pd.to_numeric(
            data[col],
            errors="coerce"
        )

    data = data.dropna(subset=required)

    return data


try:
    df = load_data()

except Exception as e:
    st.error(f"데이터 오류: {e}")
    st.stop()


# ==========================================
# 4. 공통 설정
# ==========================================

FEATURES = [
    "꽃받침 길이",
    "꽃받침 너비",
    "꽃잎 길이",
    "꽃잎 너비"
]

ALGORITHMS = [
    "KNN",
    "Random Forest",
    "SVM"
]

SPECIES_NAMES = {
    "Iris-setosa": "세토사 (Setosa)",
    "Iris-versicolor": "버시컬러 (Versicolor)",
    "Iris-virginica": "버지니카 (Virginica)"
}

SPECIES_COLORS = {
    "Iris-setosa": "#C7DDBB",
    "Iris-versicolor": "#A9CFC4",
    "Iris-virginica": "#E7C9D8"
}


# ==========================================
# 5. 알고리즘 생성 함수
# ==========================================

def create_model(algorithm):

    if algorithm == "KNN":

        classifier = KNeighborsClassifier(
            n_neighbors=5
        )

    elif algorithm == "Random Forest":

        classifier = RandomForestClassifier(
            n_estimators=200,
            random_state=42
        )

    else:

        classifier = SVC(
            kernel="rbf",
            C=1.0,
            gamma="scale",
            probability=True,
            random_state=42
        )

    model = Pipeline([
        ("scaler", StandardScaler()),
        ("classifier", classifier)
    ])

    return model


# ==========================================
# 6. 예측 및 결과 출력 함수
# ==========================================

def predict_species(features, values, algorithm):

    X = df[features]
    y = df["품종"]

    model = create_model(algorithm)

    model.fit(X, y)

    input_data = pd.DataFrame(
        [values],
        columns=features
    )

    prediction = model.predict(input_data)[0]

    probabilities = model.predict_proba(
        input_data
    )[0]

    confidence = probabilities[
        list(model.classes_).index(prediction)
    ] * 100

    return prediction, confidence


# ==========================================
# 7. 그래프 생성 함수
# ==========================================

def draw_graph(features, values, title):

    x_feature = features[0]
    y_feature = features[1]

    fig = go.Figure()

    # 기존 품종별 데이터
    for species in df["품종"].unique():

        subset = df[df["품종"] == species]

        fig.add_trace(
            go.Scatter(
                x=subset[x_feature],
                y=subset[y_feature],
                mode="markers",
                name=SPECIES_NAMES.get(
                    species, species
                ),
                marker=dict(
                    size=10,
                    color=SPECIES_COLORS.get(
                        species, "#CCCCCC"
                    ),
                    opacity=0.75,
                    line=dict(
                        color="white",
                        width=1
                    )
                )
            )
        )

    # 사용자가 입력한 값
    fig.add_trace(
        go.Scatter(
            x=[values[0]],
            y=[values[1]],
            mode="markers",
            name="내가 입력한 값",
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

    x_min = df[x_feature].min()
    x_max = df[x_feature].max()

    y_min = df[y_feature].min()
    y_max = df[y_feature].max()

    x_margin = max((x_max - x_min) * 0.08, 0.1)
    y_margin = max((y_max - y_min) * 0.08, 0.1)

    fig.update_layout(
        title=dict(
            text=title,
            x=0.5,
            font=dict(
                size=22,
                color="#788C76"
            )
        ),

        xaxis_title=f"{x_feature} (cm)",
        yaxis_title=f"{y_feature} (cm)",

        plot_bgcolor="#FCFFF9",
        paper_bgcolor="#FFFFFF",

        font=dict(
            color="#75836F"
        ),

        height=550,

        xaxis=dict(
            range=[
                x_min - x_margin,
                x_max + x_margin
            ],
            gridcolor="#EAEFE5"
        ),

        yaxis=dict(
            range=[
                max(0, y_min - y_margin),
                y_max + y_margin
            ],
            gridcolor="#EAEFE5"
        ),

        legend=dict(
            orientation="h",
            y=-0.2,
            x=0.5,
            xanchor="center"
        )
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )


# ==========================================
# 8. 알고리즘 작동 원리 설명 함수
# ==========================================

def show_algorithm_info():

    st.markdown("### 📚 분류 알고리즘 작동 원리")

    with st.expander("① KNN - K최근접 이웃", expanded=False):

        st.write("""
        **핵심 원리: 가까운 데이터의 다수결**

        1. 새로운 꽃의 측정값을 입력합니다.
        2. 기존 데이터와의 거리를 계산합니다.
        3. 가장 가까운 데이터 5개를 선택합니다.
        4. 5개 중 가장 많이 등장한 품종으로 예측합니다.

        **특징**

        - 원리가 간단하고 이해하기 쉽습니다.
        - 주변 데이터의 영향을 많이 받습니다.
        - 데이터의 크기와 거리 계산이 중요합니다.
        """)

    with st.expander("② Random Forest - 랜덤 포레스트"):

        st.write("""
        **핵심 원리: 여러 결정 트리의 투표**

        1. 기존 데이터에서 서로 다른 학습용 표본을 만듭니다.
        2. 여러 개의 결정 트리를 학습시킵니다.
        3. 각 트리가 새로운 꽃의 품종을 예측합니다.
        4. 가장 많은 표를 받은 품종을 최종 결과로 선택합니다.

        **특징**

        - 여러 트리의 결과를 종합합니다.
        - 복잡한 데이터 관계를 학습할 수 있습니다.
        - 개별 결정 트리보다 안정적인 예측에 유리합니다.
        """)

    with st.expander("③ SVM - 서포트 벡터 머신"):

        st.write("""
        **핵심 원리: 품종을 구분하는 최적의 경계 찾기**

        1. 각 품종의 데이터 분포를 확인합니다.
        2. 품종을 구분하는 결정 경계를 학습합니다.
        3. 경계 주변의 중요한 데이터들을 활용합니다.
        4. 새로운 데이터가 어느 영역에 속하는지 판단합니다.

        **특징**

        - 데이터의 분류 경계를 학습합니다.
        - 커널을 활용하여 비선형적인 관계도 학습할 수 있습니다.
        - 데이터 표준화가 중요합니다.
        """)


# ==========================================
# 9. 제목
# ==========================================

st.markdown(
    """
    <div style="text-align:center;padding:25px 10px;">

        <div style="font-size:45px;">
            🌸 🌿 🌸
        </div>

        <h1 style="font-size:40px;color:#718B70;">
            A Spring Day with Iris
        </h1>

        <p style="color:#A18CA6;font-size:17px;">
            봄바람을 따라 피어나는 아름다운 붓꽃 이야기
        </p>

        <p style="color:#9BAA91;font-size:13px;">
            Discover the beauty of Iris flowers
        </p>

    </div>
    """,
    unsafe_allow_html=True
)

st.divider()


# ==========================================
# 10. 두 개의 예측 탭
# ==========================================

tab1, tab2 = st.tabs([
    "🌸 꽃잎으로 품종 예측",
    "🌿 원하는 속성으로 예측"
])


# ==========================================
# TAB 1
# 꽃잎 길이 + 꽃잎 너비
# ==========================================

with tab1:

    st.markdown("## 🌷 꽃잎으로 품종 예측하기")

    st.write(
        "꽃잎의 길이와 너비를 입력하여 "
        "붓꽃의 품종을 예측해 보세요."
    )

    features1 = [
        "꽃잎 길이",
        "꽃잎 너비"
    ]

    col1, col2 = st.columns(2)

    with col1:

        st.markdown("### 🌸 꽃잎 길이")

        length_value = st.number_input(
            "꽃잎 길이 (cm)",
            min_value=float(df["꽃잎 길이"].min()),
            max_value=float(df["꽃잎 길이"].max()),
            value=3.0,
            step=0.1,
            format="%.1f",
            key="petal_length"
        )

        st.caption(
            f"입력 범위: {df['꽃잎 길이'].min()} ~ "
            f"{df['꽃잎 길이'].max()} cm"
        )

    with col2:

        st.markdown("### 🌸 꽃잎 너비")

        width_value = st.number_input(
            "꽃잎 너비 (cm)",
            min_value=float(df["꽃잎 너비"].min()),
            max_value=float(df["꽃잎 너비"].max()),
            value=1.0,
            step=0.1,
            format="%.1f",
            key="petal_width"
        )

        st.caption(
            f"입력 범위: {df['꽃잎 너비'].min()} ~ "
            f"{df['꽃잎 너비'].max()} cm"
        )

    st.divider()

    st.markdown("### 🤖 분류 알고리즘 선택")

    algorithm1 = st.selectbox(
        "사용할 알고리즘을 선택하세요.",
        ALGORITHMS,
        key="algorithm1"
    )

    if st.button(
        "🌸 꽃잎 품종 예측하기",
        key="predict1",
        use_container_width=True
    ):

        values1 = [
            length_value,
            width_value
        ]

        prediction, confidence = predict_species(
            features1,
            values1,
            algorithm1
        )

        st.session_state["result1"] = (
            prediction,
            confidence,
            values1,
            algorithm1
        )

    if "result1" in st.session_state:

        prediction, confidence, values1, used_algorithm = (
            st.session_state["result1"]
        )

        result_name = SPECIES_NAMES.get(
            prediction, prediction
        )

        st.markdown(
            f"""
            <div style="
                background:linear-gradient(
                    120deg,#FFF5FA,#F5F8FF,#F5FFF1
                );
                padding:25px;
                border-radius:22px;
                border:1px solid #EADDEB;
                text-align:center;
            ">
                <div style="font-size:35px;">🌸 ✨ 🌸</div>
                <h3 style="color:#A17CB6;">
                    예측된 붓꽃 품종
                </h3>
                <h1 style="color:#9673AE;">
                    {result_name}
                </h1>
                <p>사용 알고리즘: {used_algorithm}</p>
                <h3 style="color:#A17CB6;">
                    모델 투표 비율: {confidence:.1f}%
                </h3>
            </div>
            """,
            unsafe_allow_html=True
        )

        st.caption(
            "※ 모델 투표 비율은 KNN의 이웃 투표 비율, "
            "Random Forest의 트리 투표 비율, "
            "SVM의 확률 추정값입니다. "
            "실제 정확도와는 다릅니다."
        )

    st.divider()

    st.markdown("## 📊 꽃잎 크기 그래프")

    if "result1" in st.session_state:
        graph_values1 = st.session_state["result1"][2]
    else:
        graph_values1 = [
            length_value,
            width_value
        ]

    draw_graph(
        features1,
        graph_values1,
        "Petal Length & Width"
    )

    # 그래프 바로 아래 작동 원리
    show_algorithm_info()


# ==========================================
# TAB 2
# 사용자가 원하는 속성 2개 선택
# ==========================================

with tab2:

    st.markdown("## 🌿 원하는 속성으로 품종 예측하기")

    st.write(
        "이번에는 꽃잎뿐만 아니라 꽃받침의 크기도 "
        "활용할 수 있어요."
    )

    st.markdown("### 🍃 사용할 속성 2개 선택하기")

    feature_col1, feature_col2 = st.columns(2)

    with feature_col1:

        feature1 = st.selectbox(
            "첫 번째 속성",
            FEATURES,
            index=0,
            key="feature1"
        )

    second_options = [
        f for f in FEATURES
        if f != feature1
    ]

    with feature_col2:

        default_second = (
            "꽃받침 너비"
            if "꽃받침 너비" in second_options
            else second_options[0]
        )

        feature2 = st.selectbox(
            "두 번째 속성",
            second_options,
            index=second_options.index(default_second),
            key="feature2"
        )

    selected_features = [
        feature1,
        feature2
    ]

    st.success(
        f"선택된 속성: {feature1} + {feature2}"
    )

    st.divider()

    st.markdown("### 🌷 선택한 속성의 측정값 입력")

    input_col1, input_col2 = st.columns(2)

    with input_col1:

        st.markdown(f"#### {feature1}")

        value1 = st.number_input(
            f"{feature1} (cm)",
            min_value=float(df[feature1].min()),
            max_value=float(df[feature1].max()),
            value=float(
                round(df[feature1].mean(), 1)
            ),
            step=0.1,
            format="%.1f",
            key="custom_value1"
        )

        st.caption(
            f"입력 범위: {df[feature1].min()} ~ "
            f"{df[feature1].max()} cm"
        )

    with input_col2:

        st.markdown(f"#### {feature2}")

        value2 = st.number_input(
            f"{feature2} (cm)",
            min_value=float(df[feature2].min()),
            max_value=float(df[feature2].max()),
            value=float(
                round(df[feature2].mean(), 1)
            ),
            step=0.1,
            format="%.1f",
            key="custom_value2"
        )

        st.caption(
            f"입력 범위: {df[feature2].min()} ~ "
            f"{df[feature2].max()} cm"
        )

    st.divider()

    st.markdown("### 🤖 분류 알고리즘 선택")

    algorithm2 = st.selectbox(
        "사용할 알고리즘을 선택하세요.",
        ALGORITHMS,
        key="algorithm2"
    )

    if st.button(
        "🌸 선택한 속성으로 품종 예측하기",
        key="predict2",
        use_container_width=True
    ):

        values2 = [
            value1,
            value2
        ]

        prediction2, confidence2 = predict_species(
            selected_features,
            values2,
            algorithm2
        )

        st.session_state["result2"] = (
            prediction2,
            confidence2,
            selected_features,
            values2,
            algorithm2
        )

    if "result2" in st.session_state:

        (
            prediction2,
            confidence2,
            saved_features,
            saved_values,
            used_algorithm2
        ) = st.session_state["result2"]

        result_name2 = SPECIES_NAMES.get(
            prediction2, prediction2
        )

        st.markdown(
            f"""
            <div style="
                background:linear-gradient(
                    120deg,#FFF5FA,#F5F8FF,#F5FFF1
                );
                padding:25px;
                border-radius:22px;
                border:1px solid #EADDEB;
                text-align:center;
            ">
                <div style="font-size:35px;">🌸 ✨ 🌸</div>
                <h3 style="color:#A17CB6;">
                    예측된 붓꽃 품종
                </h3>
                <h1 style="color:#9673AE;">
                    {result_name2}
                </h1>
                <p>사용 속성: {saved_features[0]} + {saved_features[1]}</p>
                <p>사용 알고리즘: {used_algorithm2}</p>
                <h3 style="color:#A17CB6;">
                    모델 투표 비율: {confidence2:.1f}%
                </h3>
            </div>
            """,
            unsafe_allow_html=True
        )

        st.caption(
            "※ 모델 투표 비율은 알고리즘의 예측 확률이며 "
            "실제 정확도와는 다릅니다."
        )

    st.divider()

    st.markdown("## 📊 선택한 속성의 그래프")

    if "result2" in st.session_state:
        saved_result = st.session_state["result2"]

        graph_features2 = saved_result[2]
        graph_values2 = saved_result[3]

    else:
        graph_features2 = selected_features
        graph_values2 = [value1, value2]

    draw_graph(
        graph_features2,
        graph_values2,
        f"{graph_features2[0]} & {graph_features2[1]}"
    )

    show_algorithm_info()


# ==========================================
# 11. 하단 안내
# ==========================================

st.divider()

st.markdown(
    """
    <div style="
        text-align:center;
        padding:30px 10px;
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
