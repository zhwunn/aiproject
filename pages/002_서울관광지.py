        "name": "코엑스 별마당도서관",
        "lat": 37.5116, "lon": 127.0592,
        "emoji": "📚",
        "description": "높은 서가와 개방감 있는 공간이 인상적인 대형 실내 도서관이에요.",
        "tip": "코엑스 쇼핑몰과 함께 둘러보면 동선을 짜기 편해요."
    }
]

# ---------- 제목 ----------
st.markdown("""
<div class="hero">
    <h1>🗺️ SEOUL TRAVEL MAP</h1>
    <p>서울의 인기 관광 명소 10곳을 한눈에 살펴보자!</p>
</div>
""", unsafe_allow_html=True)

st.markdown("""
<div class="intro">
    <b>서울에 왔으면 유명한 곳은 좀 가봐야지.</b><br>
    내가 외국인 여행객에게 잘 알려진 대표 명소들을 지도에 표시해 뒀으니까,
    어디부터 갈지 잘 골라 봐.
</div>
""", unsafe_allow_html=True)

# ---------- 지도 ----------
st.subheader("📍 서울 주요 관광지 지도")
st.caption("지도 위의 분홍색 점이 아래 목록의 관광지 위치를 나타내요.")

# st.map은 Streamlit에 내장된 지도 기능이므로 별도 지도 패키지가 필요하지 않음.
map_points = [
    {"lat": place["lat"], "lon": place["lon"]}
    for place in places
]

st.map(
    map_points,
    latitude="lat",
    longitude="lon",
    color="#E98EAB",
    size=180,
    zoom=10,
    use_container_width=True
)

st.markdown(
    '<p class="small-note">※ 지도에는 위치 점으로 표시되며, 각 번호와 장소 이름은 아래 목록에서 확인할 수 있어요.</p>',
    unsafe_allow_html=True
)

# ---------- 장소 선택 및 설명 ----------
st.divider()
st.subheader("✨ 관광지 자세히 보기")

place_names = [
    f"{i + 1}. {place['emoji']} {place['name']}"
    for i, place in enumerate(places)
]

selected_label = st.selectbox(
    "궁금한 장소를 골라 봐.",
    place_names
)

selected_index = place_names.index(selected_label)
selected_place = places[selected_index]

st.markdown(
    f"""
    <div class="place-card">
        <h4>{selected_place['emoji']} {selected_place['name']}</h4>
        <p>{selected_place['description']}</p>
        <p style="margin-top:8px;"><b>여행 팁:</b> {selected_place['tip']}</p>
    </div>
    """,
    unsafe_allow_html=True
)

# Google Maps 길찾기/장소 검색 링크 (추가 라이브러리 불필요)
google_maps_url = (
    "https://www.google.com/maps/search/?api=1&query="
    + str(selected_place["lat"])
    + ","
    + str(selected_place["lon"])
)

st.link_button("📍 Google 지도에서 위치 보기", google_maps_url)

# ---------- 전체 관광지 목록 ----------
st.divider()
st.subheader("🎒 서울 관광지 TOP 10")

st.caption(
    "아래는 외국인 여행객에게 잘 알려진 서울의 대표 관광 명소를 모은 목록이에요. "
    "공식적인 방문객 수 순위는 아니며, 순서는 앱에서 보기 편하도록 정리했어요."
)

for i, place in enumerate(places, start=1):
    st.markdown(
        f"""
        <div class="place-card">
            <h4>{i:02d} · {place['emoji']} {place['name']}</h4>
            <p>{place['description']}</p>
        </div>
        """,
        unsafe_allow_html=True
    )

st.markdown("---")
st.markdown(
    """
    <div style="text-align:center; color:#A69A94; font-size:13px; padding:10px;">
        💗 SEOUL TRAVEL MAP<br>
        지도까지 보여줬으니까 길 잃으면 안 된다? 즐거운 여행 하고 와!
    </div>
    """,
    unsafe_allow_html=True
)
