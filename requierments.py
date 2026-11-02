
import streamlit as st

# =====================================
# 1. 기본 설정
# =====================================
st.set_page_config(
    page_title="서울 관광 지도 🗺️",
    page_icon="🇰🇷",
    layout="wide"
)

# =====================================
# 2. 디자인
# =====================================
st.markdown("""
<style>
.stApp {
    background-color: #F2F7FF;
}

.block-container {
    max-width: 1100px;
    padding-top: 2rem;
}

.title {
    background: white;
    padding: 25px;
    border-radius: 22px;
    text-align: center;
    margin-bottom: 20px;
}

.talk {
    background: #FFF0CE;
    padding: 17px;
    border-radius: 16px;
    margin: 15px 0;
    color: #604D39;
    font-size: 16px;
}

.place {
    background: white;
    border-radius: 16px;
    padding: 17px;
    margin-bottom: 12px;
    border-left: 5px solid #83B9E8;
}

</style>
""", unsafe_allow_html=True)

# =====================================
# 3. 관광지 데이터
# =====================================
places = [
    {
        "name": "경복궁",
        "lat": 37.5796,
        "lon": 126.9770,
        "description": "조선 왕조의 대표 궁궐. 한복 체험과 한국 전통문화를 즐기기 좋은 곳.",
        "emoji": "🏯"
    },
    {
        "name": "북촌한옥마을",
        "lat": 37.5826,
        "lon": 126.9830,
        "description": "전통 한옥이 모여 있는 아름다운 마을.",
        "emoji": "🏘️"
    },
    {
        "name": "인사동",
        "lat": 37.5742,
        "lon": 126.9855,
        "description": "전통 공예품과 기념품, 한국적인 카페를 만날 수 있는 거리.",
        "emoji": "🎨"
    },
    {
        "name": "명동",
        "lat": 37.5636,
        "lon": 126.9869,
        "description": "쇼핑과 K-뷰티, 길거리 음식으로 유명한 관광 거리.",
        "emoji": "🛍️"
    },
    {
        "name": "남산서울타워",
        "lat": 37.5512,
        "lon": 126.9882,
        "description": "서울의 멋진 전망과 야경을 감상할 수 있는 명소.",
        "emoji": "🗼"
    },
    {
        "name": "홍대",
        "lat": 37.5563,
        "lon": 126.9236,
        "description": "거리 공연과 개성 있는 카페, 젊은 문화를 즐길 수 있는 곳.",
        "emoji": "🎸"
    },
    {
        "name": "강남",
        "lat": 37.4979,
        "lon": 127.0276,
        "description": "세련된 쇼핑 공간과 맛집이 많은 서울의 번화가.",
        "emoji": "🌃"
    },
    {
        "name": "코엑스 별마당도서관",
        "lat": 37.5116,
        "lon": 127.0592,
        "description": "웅장한 책장으로 유명한 실내 문화 공간.",
        "emoji": "📚"
    },
    {
        "name": "롯데월드",
        "lat": 37.5111,
        "lon": 127.0982,
        "description": "다양한 놀이기구와 볼거리를 즐기는 테마파크.",
        "emoji": "🎢"
    },
    {
        "name": "청계천",
        "lat": 37.5692,
        "lon": 126.9788,
        "description": "서울 도심을 따라 흐르는 아름다운 산책 공간.",
        "emoji": "🌊"
    }
]

# =====================================
# 4. 제목
# =====================================
st.markdown("""
<div class="title">
    <h1>🇰🇷 SEOUL TRAVEL MAP 🗺️</h1>
    <h3>외국인 관광객을 위한 서울 명소 10곳</h3>
    <p>서울 여행이 처음이라고? 걱정 마. 내가 알려줄 테니까. ✈️</p>
</div>
""", unsafe_allow_html=True)

st.markdown("""
<div class="talk">
💬 <b>서울 여행 도우미:</b>
서울에 왔으면 유명한 곳은 좀 가봐야지.
아래 지도에 위치 표시해 뒀으니까 잘 찾아봐. 😏
</div>
""", unsafe_allow_html=True)

# =====================================
# 5. 실제 서울 지도 표시
# =====================================
st.subheader("📍 서울 관광지 위치 지도")

# 지도에 표시할 위도와 경도
map_data = [
    {"lat": place["lat"], "lon": place["lon"]}
    for place in places
]

st.map(
    map_data,
    latitude="lat",
    longitude="lon",
    zoom=11,
    use_container_width=True
)

st.caption("📌 지도에 표시된 점들은 아래 관광지 10곳의 위치야.")

# =====================================
# 6. 관광지 선택 및 설명
# =====================================
st.divider()

st.subheader("🎀 서울 관광지 알아보기")

selected = st.selectbox(
    "어디가 궁금한데?",
    [place["name"] for place in places]
)

for place in places:
    if place["name"] == selected:
        st.markdown(f"""
        <div class="place">
            <h3>{place['emoji']} {place['name']}</h3>
            <p>{place['description']}</p>
            <p>📍 위도: {place['lat']} / 경도: {place['lon']}</p>
        </div>
        """, unsafe_allow_html=True)

        st.link_button(
            "🧭 구글 지도에서 위치 확인하기",
            f"https://www.google.com/maps/search/?api=1&query={place['lat']},{place['lon']}"
        )

# =====================================
# 7. 전체 관광지 설명
# =====================================
st.divider()
st.subheader("✨ 서울 관광지 TOP 10")

col1, col2 = st.columns(2)

for i, place in enumerate(places):
    with (col1 if i % 2 == 0 else col2):
        st.markdown(f"""
        <div class="place">
            <b>{i+1}. {place['emoji']} {place['name']}</b>
            <p>{place['description']}</p>
        </div>
        """, unsafe_allow_html=True)

# =====================================
# 8. 마무리
# =====================================
st.markdown("""
<div class="talk">
💬 <b>서울 여행 도우미:</b>
자, 이제 지도까지 보여줬으니까 길 잃으면 안 된다?
즐거운 서울 여행 하고 와! 🧳🇰🇷
</div>
""", unsafe_allow_html=True)

st.caption("Seoul Travel Guide | Made with ❤️")
