chart_data = pd.DataFrame({
    "나이": ages,
    "인구수(명)": population
})

# 그래프 눈금 50단위를 보기 쉽게 유지하기 위해
# 세로축은 백 명 단위로 표시 (50 = 5,000명)
chart_data["인구수(백 명)"] = chart_data["인구수(명)"] / 100


# ---------------------------------------------------------
# 요약 정보
# ---------------------------------------------------------
total_population = int(sum(population))

metric1, metric2, metric3 = st.columns(3)
metric1.metric("선택한 행정구역", selected_region)
metric2.metric("선택한 성별", selected_gender_label)
metric3.metric("연령별 인구 합계", f"{total_population:,}명")


# ---------------------------------------------------------
# 꺾은선 그래프
# ---------------------------------------------------------
fig = go.Figure()

fig.add_trace(
    go.Scatter(
        x=chart_data["나이"],
        y=chart_data["인구수(백 명)"],
        mode="lines+markers",
        name="인구수",
        line=dict(color="#E98EAD", width=4),
        marker=dict(
            color="#F3AFC4",
            size=9,
            line=dict(color="#FFFFFF", width=1.5)
        ),
        customdata=chart_data[["인구수(명)"]],
        hovertemplate=(
            "나이: %{x}<br>"
            "인구수: %{customdata[0]:,.0f}명"
            "<extra></extra>"
        )
    )
)

fig.update_layout(
    title=dict(
        text=f"{selected_region} · {selected_gender_label} · {selected_year}년 연령별 인구",
        x=0.5,
        xanchor="center",
        font=dict(size=20, color="#51434A")
    ),
    xaxis=dict(
        title="나이",
        type="category",
        tickmode="array",
        tickvals=ages,
        ticktext=ages,
        tickangle=0,
        showgrid=True,
        gridcolor="#F1DFA8",
        gridwidth=1,
        linecolor="#D8C99A"
    ),
    yaxis=dict(
        title="인구수 (백 명 단위)",
        rangemode="tozero",
        dtick=50,
        showgrid=True,
        gridcolor="#EADBAA",
        gridwidth=1,
        zeroline=True,
        zerolinecolor="#D8C99A"
    ),
    plot_bgcolor="#FFFDF3",
    paper_bgcolor="#FFF9D9",
    font=dict(
        family="Malgun Gothic, AppleGothic, NanumGothic, sans-serif",
        color="#51434A",
        size=12
    ),
    hoverlabel=dict(
        bgcolor="#FFF0F5",
        font=dict(color="#51434A")
    ),
    margin=dict(l=30, r=30, t=75, b=50),
    height=560
)

st.plotly_chart(fig, use_container_width=True)

st.caption(
    "※ 연령은 0~4세, 5~9세처럼 5세 단위로 구분됩니다. "
    "세로축은 백 명 단위이며 눈금 간격 50은 실제 인구 5,000명을 뜻합니다. "
    "그래프의 점에 마우스를 올리면 실제 인구수를 확인할 수 있습니다."
)


# ---------------------------------------------------------
# 데이터 표 및 다운로드
# ---------------------------------------------------------
with st.expander("연령별 인구 데이터 표 보기"):
    display_data = chart_data[["나이", "인구수(명)"]].copy()
    display_data["인구수(명)"] = display_data["인구수(명)"].map(
        lambda value: f"{int(value):,}"
    )
    st.dataframe(display_data, use_container_width=True, hide_index=True)

    csv_data = chart_data[["나이", "인구수(명)"]].to_csv(
        index=False,
        encoding="utf-8-sig"
    )
    st.download_button(
        label="분석 데이터 CSV 다운로드",
        data=csv_data,
        file_name=f"{selected_region}_{selected_gender_label}_{selected_year}_인구분석.csv",
        mime="text/csv"
    )

st.markdown("---")
st.caption("데이터 출처: 업로드된 population.csv")
