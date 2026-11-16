
# ==========================================
# 6-1. 3가지 알고리즘 비교 함수
# ==========================================

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

        probabilities = model.predict_proba(
            input_data
        )[0]

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

    # 가장 많이 예측된 품종
    majority = result_df["원본 품종"].value_counts()

    best_prediction = majority.index[0]

    agreement = (
        result_df["원본 품종"].nunique() == 1
    )

    return result_df, best_prediction, agreement


# ==========================================
# 6-2. 비교 결과 시각화 함수
# ==========================================

def show_comparison(features, values):

    result_df, best_prediction, agreement = (
        compare_algorithms(features, values)
    )

    st.markdown("### 🌸 알고리즘별 예측 결과")

    display_df = result_df[
        ["알고리즘", "예측 품종", "예측 확률 (%)"]
    ]

    st.dataframe(
        display_df,
        use_container_width=True,
        hide_index=True
    )

    st.markdown("### 📊 알고리즘별 예측 확률")

    fig = go.Figure()

    bar_colors = [
        "#C9A7E8",
        "#B9D9B0",
        "#E9BDD1"
    ]

    fig.add_trace(
        go.Bar(
            x=result_df["알고리즘"],
            y=result_df["예측 확률 (%)"],
            marker_color=bar_colors,
            text=[
                f"{v:.1f}%"
                for v in result_df["예측 확률 (%)"]
            ],
            textposition="outside"
        )
    )

    fig.update_layout(
        title="3가지 알고리즘의 예측 확률 비교",
        yaxis_title="예측 확률 (%)",
        xaxis_title="분류 알고리즘",
        yaxis=dict(
            range=[0, 115],
            gridcolor="#EAEFE5"
        ),
        plot_bgcolor="#FCFFF9",
        paper_bgcolor="#FFFFFF",
        font=dict(color="#75836F"),
        height=400,
        showlegend=False
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

    st.markdown("### 🏆 최종 비교 결과")

    counts = result_df["원본 품종"].value_counts()

    if agreement:

        st.success(
            "세 가지 알고리즘이 모두 같은 품종으로 예측했습니다!"
        )

    else:

        st.info(
            "알고리즘마다 예측 결과에 차이가 있습니다."
        )

    st.markdown(
        f"""
        <div style="
            background:linear-gradient(
                120deg,#FFF5FA,#F5F8FF,#F5FFF1
            );
            padding:22px;
            border-radius:20px;
            text-align:center;
            border:1px solid #EADDEB;
        ">
            <h3 style="color:#9673AE;">
                가장 많이 예측된 품종
            </h3>
            <h1 style="color:#9673AE;">
                {SPECIES_NAMES.get(best_prediction, best_prediction)}
            </h1>
            <p style="color:#82917A;">
                {int(counts.iloc[0])}개 알고리즘이 선택한 품종
                / 전체 3개 알고리즘
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )

    return result_df
