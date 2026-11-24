    if uploaded_file is None:
        st.info(
            "CSV 파일을 Streamlit 메인 파일(.py)이 있는 폴더에 두거나, "
            "pages 폴더에 이 코드를 저장했다면 한 단계 위 폴더에 넣어 주세요."
        )
        st.stop()
    try:
        df_raw = pd.read_csv(uploaded_file, encoding="utf-8-sig")
    except UnicodeDecodeError:
        uploaded_file.seek(0)
        df_raw = pd.read_csv(uploaded_file, encoding="cp949")
    data_path = uploaded_file.name

try:
    df = clean_data(df_raw)
except ValueError as error:
    st.error(str(error))
    st.stop()

# -----------------------------
# 필터 영역
# -----------------------------
st.markdown("## 🎀 나만의 식품 데이터 고르기")
filter1, filter2, filter3 = st.columns(3)

with filter1:
    gender_options = ["전체", "남자", "여자"]
    selected_gender = st.selectbox("👧 성별", gender_options, index=0)

with filter2:
    food_groups = sorted(df["식품군"].dropna().unique().tolist())
    selected_group = st.selectbox("🍰 식품군", food_groups)

with filter3:
    years = sorted(df["연도"].dropna().unique().tolist())
    selected_year = st.selectbox("📅 조사 연도", years, index=len(years) - 1)

# 성별 기준 자료만 선택
filtered = df[
    (df["분석기준"] == "성별") &
    (df["기준값"] == selected_gender) &
    (df["식품군"] == selected_group) &
    (df["연도"] == selected_year)
].copy()

filtered = filtered.sort_values("평균", ascending=False)

st.markdown("---")

if filtered.empty:
    st.warning("선택한 조건에 해당하는 자료가 없어요. 다른 조건을 선택해 주세요.")
    st.stop()

# -----------------------------
# 핵심 수치
# -----------------------------
top_row = filtered.iloc[0]
mean_value = filtered["평균"].mean()
food_count = filtered["식품"].nunique()

m1, m2, m3 = st.columns(3)
m1.metric("🍓 가장 높은 평균값", f"{top_row['평균']:.2f}", help=f"식품: {top_row['식품']}")
m2.metric("🧁 해당 식품 수", f"{food_count}개")
m3.metric("🌷 선택한 연도", f"{selected_year}년")

st.markdown(
    f"<div class='note'>💡 <b>{selected_year}년 · {selected_gender} · {selected_group}</b> 조건의 식품별 평균값을 보여주고 있어요. "
    f"가장 높은 평균값을 보인 식품은 <b>{top_row['식품']}</b>이에요.</div>",
    unsafe_allow_html=True
)

# -----------------------------
# 그래프와 표
# -----------------------------
left, right = st.columns([1.15, 1])

with left:
    st.markdown("### 📊 식품별 평균값 그래프")
    chart_data = filtered[["식품", "평균"]].set_index("식품")
    st.bar_chart(chart_data, color="#E9AFC2", height=430)
    st.caption("막대가 길수록 해당 식품의 평균값이 높아요.")

with right:
    st.markdown("### 🍬 자세한 데이터")
    display_df = filtered[["식품", "평균", "표준오차"]].rename(
        columns={"식품": "식품명", "평균": "평균값", "표준오차": "표준오차"}
    )
    st.dataframe(
        display_df.style.format({"평균값": "{:.2f}", "표준오차": "{:.2f}"}),
        use_container_width=True,
        height=430,
        hide_index=True
    )

# -----------------------------
# 식품 하나 자세히 보기
# -----------------------------
st.markdown("---")
st.markdown("## 🔎 식품 하나 더 자세히 보기")

food_options = filtered["식품"].dropna().sort_values().unique().tolist()
selected_food = st.selectbox("궁금한 식품을 선택해 주세요.", food_options)

food_detail = filtered[filtered["식품"] == selected_food].iloc[0]
d1, d2 = st.columns(2)
d1.metric(f"🍡 {selected_food} 평균값", f"{food_detail['평균']:.2f}")
d2.metric("📐 표준오차", f"{food_detail['표준오차']:.2f}")

# -----------------------------
# 자료 설명
# -----------------------------
with st.expander("📚 데이터와 분석 기준 알아보기"):
    st.write("""
    - 자료: 한국보건산업진흥원 국민영양통계 식품별 평균섭취량
    - 분석 기준: 성별
    - 성별 선택: 전체, 남자, 여자
    - 식품군: 원본 CSV에 들어 있는 식품군 분류를 그대로 사용
    - 평균값과 표준오차: 원본 데이터의 값을 그대로 표시
    - 연도: 2020~2023년 자료 중 선택
    """)
    st.caption(f"불러온 파일: {data_path}")
    st.caption(
        "참고: 이 화면은 식품별 평균값을 비교하는 기능이며, "
        "개인의 선호도나 특정 식품을 좋아하는 정도를 나타내지는 않아요."
    )

st.markdown(
    "<div class='footer'>🍓 오늘도 맛있고 건강한 데이터 탐험! · Snack Data Lab 🍓</div>",
