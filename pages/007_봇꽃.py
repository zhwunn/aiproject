
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

from pathlib import Path
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.neighbors import KNeighborsClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.svm import SVC


# =======================================
# 1. 페이지 설정
# =======================================

st.set_page_config(
    page_title="붓꽃 품종 예측",
    page_icon="🌸",
    layout="wide"
)


# =======================================
# 2. 디자인 CSS
# =======================================

st.markdown("""
<style>

.stApp {
    background: linear-gradient(
        135deg,
        #fffdfd 0%,
        #f8fff8 50%,
        #fffaff 100%
    );
}

h1, h2, h3 {
    color: #718B70;
}

.stButton > button {
    background-color: #E8DDF0;
    color: #6F5C78;
    border-radius: 15px;
    border: none;
    padding: 10px 20px;
    font-weight: bold;
}

.stButton > button:hover {
    background-color: #D9C8E5;
    color: #594765;
}

.stTabs [data-baseweb="tab"] {
    color: #718B70;
    font-weight: bold;
}

.stTabs [aria-selected="true"] {
    color: #A18CA6;
}

div[data-testid="stMetric"] {
    background-color: #FFFFFF;
    border: 1px solid #E9E2EA;
    padding: 15px;
    border-radius: 15px;
}

.flower {
    position: fixed;
    top: -30px;
    z-index: 999;
    pointer-events: none;
    animation: fall 12s linear infinite;
    font-size: 20px;
    opacity: 0.65;
}

.flower:nth-child(1) {
    left: 10%;
    animation-delay: 0s;
}

.flower:nth-child(2) {
    left: 30%;
    animation-delay: 3s;
}

.flower:nth-child(3) {
    left: 55%;
    animation-delay: 5s;
}

.flower:nth-child(4) {
    left: 75%;
    animation-delay: 1s;
}

.flower:nth-child(5) {
    left: 90%;
    animation-delay: 7s;
}

@keyframes fall {
    0% {
        transform: translateY(-30px) rotate(0deg);
    }

    100% {
        transform: translateY(110vh) rotate(360deg);
    }
}

</style>
""", unsafe_allow_html=True)


# =======================================
# 3. 벚꽃 애니메이션
# =======================================

st.markdown("""
<div class="flower">🌸</div>
<div class="flower">🌸</div>
<div class="flower">🌸</div>
<div class="flower">🌸</div>
<div class="flower">🌸</div>
""", unsafe_allow_html=True)


# =======================================
# 4. 데이터 불러오기
# =======================================

@st.cache_data
def load_data():

    file_path = (
        Path(__file__).resolve().parent.parent / "Iris.csv"
    )

    if not file_path.exists():
        raise FileNotFoundError(
            f"Iris.csv 파일을 찾을 수 없습니다: {file_path}"
        )

    try:
        data = pd.read_csv(
            file_path,
            encoding="utf-8-sig"
        )

    except UnicodeDecodeError:
        data = pd.read_csv(
            file_path,
            encoding="cp949"
        )

    data.columns = data.columns.str.strip()

    data = data.rename(columns={
        "꽃발침 길이": "꽃받침 길이",
        "꽃받침길이": "꽃받침 길이",
        "꽃받침너비": "꽃받침 너비",
        "꽃잎길이": "꽃잎 길이",
        "꽃잎너비": "꽃잎 너비"
    })

    return data


try:
    df = load_data()

except Exception as e:
    st.error(f"데이터를 불러오는 중 오류가 발생했습니다: {e}")
    st.stop()


# =======================================
# 5. 데이터 정리
# =======================================

FEATURES = [
    "꽃받침 길이",
    "꽃받침 너비",
    "꽃잎 길이",
    "꽃잎 너비"
]

if not all(feature in df.columns for feature in FEATURES):
    st.error(
        "CSV 파일의 열 이름을 확인해주세요. "
        "꽃받침 길이, 꽃받침 너비, 꽃잎 길이, 꽃잎 너비가 필요합니다."
    )
    st.stop()

if "품종" not in df.columns:
    st.error("CSV 파일에 '품종' 열이 필요합니다.")
    st.stop()

df = df.dropna(
    subset=FEATURES + ["품종"]
).copy()

for feature in FEATURES:
    df[feature] = pd.to_numeric(
        df[feature],
        errors="coerce"
    )

df = df.dropna(subset=FEATURES)

if df.empty:
    st.error("분석할 수 있는 데이터가 없습니다.")
    st.stop()


SPECIES_NAMES = {
    "Iris-setosa": "세토사 (Setosa)",
    "Iris-versicolor": "버시컬러 (Versicolor)",
    "Iris-virginica": "버지니카 (Virginica)"
}

SPECIES_COLORS = {
    "Iris-setosa": "#E7B7D7",
    "Iris-versicolor": "#A9C8A5",
    "Iris-virginica": "#B8A9D6"
}

ALGORITHMS = [
    "KNN",
    "Random Forest",
    "SVM"
]


# =======================================
# 6. 알고리즘 생성
# =======================================

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


# =======================================
# 7. 품종 예측 함수
# =======================================

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

    probabilities = model.predict_proba(input_data)[0]

    confidence = probabilities[
        list(model.classes_).index(prediction)
    ] * 100

    return prediction, confidence


# =======================================
# 8. 세 가지 알고리즘 비교
# =======================================

def compare_algorithms(features, values):

    results = []

    X = df[features]
    y = df["품종"]

    input_data = pd.DataFrame(
        [values],
        columns=features
    )

    for algorithm in ALGORITHMS:

        model = create_model(algorithm)
        model.fit(X, y)

        prediction = model.predict(input_data)[0]

        probabilities = model.predict_proba(input_data)[0]

        confidence = probabilities[
            list(model.classes_).index(prediction)
        ] * 100

        results.append({
            "알고리즘": algorithm,
            "예측 품종": SPECIES_NAMES.get(
                prediction, prediction
            ),
            "예측 확률 (%)": round(confidence, 1),
            "원본 품종": prediction
        })

    result_df = pd.DataFrame(results)

    vote_counts = result_df[
        "원본 품종"
    ].value_counts()

    max_votes = vote_counts.max()

    majority_species = vote_counts[
        vote_counts == max_votes
    ].index.tolist()

    return result_df, majority_species, max_votes


# =======================================
# 9. 비교 결과 출력
# =======================================

def show_comparison(features, values):

    st.markdown(
        "### 🌷 3가지 알고리즘 예측 결과 비교"
    )

    result_df, majority_species, max_votes = compare_algorithms(
        features,
        values
    )

    st.dataframe(
        result_df[
            ["알고리즘", "예측 품종", "예측 확률 (%)"]
        ],
        use_container_width=True,
        hide_index=True
    )

    st.markdown("#### 📊 알고리즘별 예측 확률")

    fig = px.bar(
        result_df,
        x="알고리즘",
        y="예측 확률 (%)",
        color="알고리즘",
        text="예측 확률 (%)",
        color_discrete_sequence=[
            "#D9B9D8",
            "#B8D2B2",
            "#BDB0DC"
        ]
    )

    fig.update_traces(
        texttemplate="%{text:.1f}%",
        textposition="outside"
    )

    fig.update_layout(
        plot_bgcolor="rgba(255,255,255,0)",
        paper_bgcolor="rgba(255,255,255,0)",
        yaxis=dict(
            range=[0, 115],
            title="예측 확률 (%)"
        ),
        xaxis_title="알고리즘",
        showlegend=False
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

    st.markdown("#### 🌼 예측 결과 종합")

    if len(majority_species) == 1:

        species_name = SPECIES_NAMES.get(
            majority_species[0],
            majority_species[0]
        )

        if max_votes == 3:
            st.success(
                f"세 가지 알고리즘 모두 "
                f"**{species_name}**으로 예측했습니다!"
            )

        else:
            st.info(
                f"가장 많은 알고리즘이 "
                f"**{species_name}**으로 예측했습니다. "
                f"({max_votes}/3)"
            )

    else:
        st.warning(
            "세 알고리즘의 예측 결과가 동률입니다."
        )

    st.caption(
        "※ 예측 확률은 각 모델이 계산한 확률이며, "
        "실제 정확도나 알고리즘 간 성능 순위를 의미하지 않습니다."
    )


# =======================================
# 10. 붓꽃 데이터 그래프
# =======================================

def draw_graph(features, values, title):

    st.markdown("### 🌿 붓꽃 데이터 분포")

    fig = go.Figure()

    for species in df["품종"].unique():

        species_data = df[
            df["품종"] == species
        ]

        fig.add_trace(
            go.Scatter(
                x=species_data[features[0]],
                y=species_data[features[1]],
                mode="markers",
                name=SPECIES_NAMES.get(
                    species, species
                ),
                marker=dict(
                    size=9,
                    color=SPECIES_COLORS.get(
                        species, "#B8B8B8"
                    ),
                    opacity=0.75
                )
            )
        )

    fig.add_trace(
        go.Scatter(
            x=[values[0]],
            y=[values[1]],
            mode="markers",
            name="입력한 붓꽃",
            marker=dict(
                size=23,
                color="#B69ACF",
                symbol="star",
                line=dict(
                    color="#FFFFFF",
                    width=2
                )
            )
        )
    )

    fig.update_layout(
        title=title,
        xaxis_title=features[0],
        yaxis_title=features[1],
        plot_bgcolor="rgba(255,255,255,0.8)",
        paper_bgcolor="rgba(255,255,255,0)",
        font=dict(color="#718B70"),
        legend_title="붓꽃 품종",
        height=500
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )


# =======================================
# 11. 알고리즘 설명
# =======================================

def show_algorithm_info():

    st.markdown("### 📚 알고리즘 작동 원리")

    with st.expander("🌸 KNN (K-최근접 이웃)"):

        st.write("""
        KNN은 새로운 데이터와 가까운 기존 데이터 K개를 찾아
        가장 많이 나타나는 품종으로 분류하는 알고리즘입니다.

        **작동 원리**

        1. 새로운 붓꽃의 특징을 입력합니다.
        2. 기존 붓꽃 데이터와의 거리를 계산합니다.
        3. 가장 가까운 5개의 데이터를 선택합니다.
        4. 가장 많이 등장한 품종을 예측합니다.
        """)

    with st.expander("🌿 Random Forest (랜덤 포레스트)"):

        st.write("""
        랜덤 포레스트는 여러 개의 결정 트리를 만들어
        각각의 예측 결과를 종합하는 알고리즘입니다.

        **작동 원리**

        1. 여러 개의 학습용 데이터 집합을 구성합니다.
        2. 각각의 데이터로 여러 결정 트리를 만듭니다.
        3. 각 결정 트리가 붓꽃의 품종을 예측합니다.
        4. 여러 트리의 결과를 종합하여 최종 품종을 결정합니다.
        """)

    with st.expander("💜 SVM (서포트 벡터 머신)"):

        st.write("""
        SVM은 데이터를 가장 잘 구분할 수 있는 경계선을 찾아
        새로운 데이터가 어느 품종에 속하는지 분류하는 알고리즘입니다.

        **작동 원리**

        1. 붓꽃 데이터를 특징에 따라 배치합니다.
        2. 품종을 구분하는 경계를 찾습니다.
        3. 새로운 데이터가 경계의 어느 쪽에 있는지 확인합니다.
        4. 해당 위치를 바탕으로 품종을 예측합니다.

        이번 앱에서는 RBF 커널을 사용합니다.
        """)


# =======================================
# 12. 탭 구성
# =======================================

tab1, tab2 = st.tabs([
    "🌸 꽃잎으로 품종 예측",
    "🌿 원하는 속성으로 품종 예측"
])


# =======================================
# TAB 1. 꽃잎 길이와 너비
# =======================================

with tab1:

    st.markdown("## 🌸 꽃잎으로 붓꽃 품종 알아보기")

    st.write(
        "꽃잎의 길이와 너비를 입력하면 "
        "붓꽃의 품종을 예측할 수 있어요."
    )

    feature1 = "꽃잎 길이"
    feature2 = "꽃잎 너비"

    col1, col2 = st.columns(2)

    min1 = float(df[feature1].min())
    max1 = float(df[feature1].max())

    min2 = float(df[feature2].min())
    max2 = float(df[feature2].max())

    with col1:

        length_value = st.number_input(
            "🌷 꽃잎 길이 (cm)",
            min_value=min1,
            max_value=max1,
            value=float(df[feature1].median()),
            step=0.1,
            key="petal_length"
        )

    with col2:

        width_value = st.number_input(
            "🌷 꽃잎 너비 (cm)",
            min_value=min2,
            max_value=max2,
            value=float(df[feature2].median()),
            step=0.1,
            key="petal_width"
        )

    selected_algorithm = st.selectbox(
        "사용할 예측 알고리즘을 선택하세요.",
        ALGORITHMS,
        key="algorithm1"
    )

    if st.button(
        "🌸 붓꽃 품종 예측하기",
        key="predict1",
        use_container_width=True
    ):

        prediction, confidence = predict_species(
            [feature1, feature2],
            [length_value, width_value],
            selected_algorithm
        )

        st.markdown("### 🌼 예측 결과")

        st.success(
            f"예측된 품종은 "
            f"**{SPECIES_NAMES.get(prediction, prediction)}**입니다!"
        )

        col1, col2 = st.columns(2)

        with col1:
            st.metric(
                "예측 알고리즘",
                selected_algorithm
            )

        with col2:
            st.metric(
                "예측 확률",
                f"{confidence:.1f}%"
            )

    draw_graph(
        [feature1, feature2],
        [length_value, width_value],
        "Petal Length & Petal Width"
    )

    st.markdown("### 🌸 세 가지 알고리즘 결과 비교")

    if st.button(
        "🌷 3가지 알고리즘 예측 결과 비교하기",
        key="compare1",
        use_container_width=True
    ):

        st.session_state["comparison1"] = (
            length_value,
            width_value
        )

    if "comparison1" in st.session_state:

        saved_values = st.session_state["comparison1"]

        show_comparison(
            [feature1, feature2],
            list(saved_values)
        )

    show_algorithm_info()


# =======================================
# TAB 2. 원하는 속성 두 가지 선택
# =======================================

with tab2:

    st.markdown("## 🌿 원하는 속성으로 붓꽃 품종 알아보기")

    st.write(
        "네 가지 붓꽃의 특징 중 두 가지를 선택하고 "
        "값을 입력해 보세요."
    )

    col1, col2 = st.columns(2)

    with col1:
        selected_feature1 = st.selectbox(
            "첫 번째 속성 선택",
            FEATURES,
            index=0,
            key="feature1"
        )

    second_options = [
        feature for feature in FEATURES
        if feature != selected_feature1
    ]

    with col2:
        selected_feature2 = st.selectbox(
            "두 번째 속성 선택",
            second_options,
            key="feature2"
        )

    col1, col2 = st.columns(2)

    min1 = float(df[selected_feature1].min())
    max1 = float(df[selected_feature1].max())

    min2 = float(df[selected_feature2].min())
    max2 = float(df[selected_feature2].max())

    with col1:
        value1 = st.number_input(
            f"🌷 {selected_feature1} (cm)",
            min_value=min1,
            max_value=max1,
            value=float(df[selected_feature1].median()),
            step=0.1,
            key="value1"
        )

    with col2:
        value2 = st.number_input(
            f"🌷 {selected_feature2} (cm)",
            min_value=min2,
            max_value=max2,
            value=float(df[selected_feature2].median()),
            step=0.1,
            key="value2"
        )

    selected_algorithm2 = st.selectbox(
        "사용할 예측 알고리즘을 선택하세요.",
        ALGORITHMS,
        key="algorithm2"
    )

    if st.button(
        "🌸 선택한 속성으로 품종 예측하기",
        key="predict2",
        use_container_width=True
    ):

        prediction, confidence = predict_species(
            [selected_feature1, selected_feature2],
            [value1, value2],
            selected_algorithm2
        )

        st.markdown("### 🌼 예측 결과")

        st.success(
            f"예측된 품종은 "
            f"**{SPECIES_NAMES.get(prediction, prediction)}**입니다!"
        )

        col1, col2 = st.columns(2)

        with col1:
            st.metric(
                "예측 알고리즘",
                selected_algorithm2
            )

        with col2:
            st.metric(
                "예측 확률",
                f"{confidence:.1f}%"
            )

    draw_graph(
        [selected_feature1, selected_feature2],
        [value1, value2],
        f"{selected_feature1} & {selected_feature2}"
    )

    st.markdown("### 🌸 세 가지 알고리즘 결과 비교")

    if st.button(
        "🌷 선택한 속성으로 3가지 알고리즘 비교하기",
        key="compare2",
        use_container_width=True
    ):

        st.session_state["comparison2"] = (
            selected_feature1,
            selected_feature2,
            value1,
            value2
        )

    if "comparison2" in st.session_state:

        saved = st.session_state["comparison2"]

        show_comparison(
            [saved[0], saved[1]],
            [saved[2], saved[3]]
        )

    show_algorithm_info()

