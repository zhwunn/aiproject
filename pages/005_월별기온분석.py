    # 연도와 월 추출
    df["연도"] = df["일시"].dt.year
    df["월"] = df["일시"].dt.month

    return df.sort_values("일시")


# 데이터 불러오기
try:
    df = load_data()

except FileNotFoundError:
    st.error(
        "temperature.csv 파일을 찾을 수 없습니다. "
        "app.py와 같은 폴더에 업로드해 주세요."
    )
    st.stop()

except Exception as e:
    st.error(f"데이터를 불러오는 중 오류가 발생했습니다: {e}")
    st.stop()


# 월 선택
month_names = {
    1: "1월", 2: "2월", 3: "3월",
    4: "4월", 5: "5월", 6: "6월",
    7: "7월", 8: "8월", 9: "9월",
    10: "10월", 11: "11월", 12: "12월"
}

selected_month_name = st.selectbox(
    "분석할 월을 선택하세요",
    list(month_names.values())
)

selected_month = [
    month for month, name in month_names.items()
    if name == selected_month_name
][0]


# 선택한 월 데이터 추출
chart_data = df[df["월"] == selected_month].copy()
chart_data = chart_data.sort_values("연도")

chart_data = chart_data.dropna(
    subset=["최고기온(℃)", "최저기온(℃)"],
    how="all"
)

if chart_data.empty:
    st.warning("선택한 월의 데이터가 없습니다.")
    st.stop()


# 그래프 생성
fig = go.Figure()

# 최고기온
fig.add_trace(
    go.Scatter(
        x=chart_data["연도"],
        y=chart_data["최고기온(℃)"],
        mode="lines+markers",
        name="최고기온",
        line=dict(color="#F2A3A3", width=3),
        marker=dict(color="#F2A3A3", size=7)
    )
)

# 최저기온
fig.add_trace(
    go.Scatter(
        x=chart_data["연도"],
        y=chart_data["최저기온(℃)"],
        mode="lines+markers",
        name="최저기온",
        line=dict(color="#9CC9F5", width=3),
        marker=dict(color="#9CC9F5", size=7)
    )
)


# 그래프 디자인
fig.update_layout(
    title={
        "text": "월별 기온분석",
        "x": 0.5,
        "xanchor": "center"
    },
    xaxis_title="연도",
    yaxis_title="온도(℃)",
    legend=dict(
        title="기온 구분",
        orientation="h",
        y=1.02,
        x=1,
        xanchor="right"
    ),
    template="plotly_white",
    hovermode="x unified",
    height=550
)

fig.update_xaxes(
    showgrid=True,
    gridcolor="#EEEEEE"
)

fig.update_yaxes(
    showgrid=True,
    gridcolor="#EEEEEE"
)

st.plotly_chart(
    fig,
    use_container_width=True
)


# 데이터 표
with st.expander("연도별 기온 데이터 보기"):

    display_data = chart_data[
        ["연도", "최고기온(℃)", "최저기온(℃)"]
    ].copy()

    display_data = display_data.round(1)

    st.dataframe(
        display_data,
        use_container_width=True,
        hide_index=True
    )

st.caption(
    "자료: temperature.csv | 결측 기온 값은 그래프에서 표시되지 않습니다."
)
