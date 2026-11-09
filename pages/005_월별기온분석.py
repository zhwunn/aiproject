    df["연도"] = df["일시"].dt.year
    df["월"] = df["일시"].dt.month

    return df.sort_values("일시")


try:
    df = load_data()
except FileNotFoundError:
    st.error(
        "temperature.csv 파일을 찾을 수 없습니다. "
        "app.py와 같은 GitHub 저장소 폴더에 temperature.csv를 업로드해 주세요."
    )
    st.stop()
except Exception as e:
    st.error(f"데이터를 불러오는 중 오류가 발생했습니다: {e}")
    st.stop()

# --------------------------------------------------
# 월 선택
# --------------------------------------------------
month_names = {
    1: "1월", 2: "2월", 3: "3월", 4: "4월",
    5: "5월", 6: "6월", 7: "7월", 8: "8월",
    9: "9월", 10: "10월", 11: "11월", 12: "12월"
}

selected_month_name = st.selectbox(
    "분석할 월을 선택하세요",
    options=list(month_names.values()),
    index=0
)

selected_month = [
    month for month, name in month_names.items()
    if name == selected_month_name
][0]

# 선택한 월의 데이터만 추출
chart_data = df[df["월"] == selected_month].copy()
chart_data = chart_data.sort_values("연도")

# 최고기온과 최저기온 중 하나라도 값이 있는 연도 표시
chart_data = chart_data.dropna(
    subset=["최고기온(℃)", "최저기온(℃)"],
    how="all"
)

if chart_data.empty:
    st.warning(f"{selected_month_name} 데이터가 없습니다.")
    st.stop()

# --------------------------------------------------
# 꺾은선 그래프
# --------------------------------------------------
fig = go.Figure()

# 최고기온: 파스텔 빨간색
fig.add_trace(
    go.Scatter(
        x=chart_data["연도"],
        y=chart_data["최고기온(℃)"],
        mode="lines+markers",
        name="최고기온",
        line=dict(color="#F2A3A3", width=3),
        marker=dict(color="#F2A3A3", size=7),
        connectgaps=False,
        hovertemplate="%{x}년<br>최고기온: %{y:.1f}℃<extra></extra>"
    )
)

# 최저기온: 파스텔 파란색
fig.add_trace(
    go.Scatter(
        x=chart_data["연도"],
        y=chart_data["최저기온(℃)"],
        mode="lines+markers",
        name="최저기온",
        line=dict(color="#9CC9F5", width=3),
        marker=dict(color="#9CC9F5", size=7),
        connectgaps=False,
        hovertemplate="%{x}년<br>최저기온: %{y:.1f}℃<extra></extra>"
    )
)

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
        yanchor="bottom",
        y=1.02,
        xanchor="right",
        x=1
    ),
    template="plotly_white",
    hovermode="x unified",
    height=550,
    margin=dict(l=40, r=30, t=100, b=50)
)

fig.update_xaxes(
    dtick=1,
    tickformat="d",
    showgrid=True,
    gridcolor="#EEEEEE"
)
fig.update_yaxes(
    showgrid=True,
    gridcolor="#EEEEEE",
    zeroline=True,
    zerolinecolor="#BBBBBB"
)

st.plotly_chart(fig, use_container_width=True)

# --------------------------------------------------
# 선택 월 데이터 표
# --------------------------------------------------
with st.expander(f"{selected_month_name} 연도별 기온 데이터 보기"):
    display_data = chart_data[
        ["연도", "최고기온(℃)", "최저기온(℃)"]
    ].copy()

    display_data["최고기온(℃)"] = display_data["최고기온(℃)"].round(1)
    display_data["최저기온(℃)"] = display_data["최저기온(℃)"].round(1)

    st.dataframe(
        display_data,
        use_container_width=True,
        hide_index=True
    )

st.caption("자료: 업로드한 temperature.csv | 결측 기온 값은 그래프에서 자동으로 건너뜁니다.")
