```python
import streamlit as st

# ==========================================
# 기본 설정
# ==========================================
st.set_page_config(
    page_title="서울 관광지 TOP 10 🗺️",
    page_icon="🗺️",
    layout="wide"
)

# ==========================================
# 디자인
# ==========================================
st.markdown("""
<style>
    .stApp {
        background: linear-gradient(180deg, #EAF6FF 0%, #FFF9F2 100%);
    }

    .block-container {
        max-width: 1100px;
        padding-top: 2rem;
        padding-bottom: 3rem;
    }

    .title-box {
        text-align: center;
        background-color: rgba(255, 255, 255, 0.85);
        padding: 25px;
        border-radius: 25px;
        margin-bottom: 25px;
    }

    .title-box h1 {
        color: #34495E;
        margin-bottom: 8px;
    }

    .character-talk {
        background-color: #FFF3C9;
        padding: 16px 20px;
        border-radius: 18px;
        font-size: 17px;
        margin-bottom: 25px;
        border: 2px solid #F3D77B;
    }

    .map-box {
        background-color: white;
        padding: 20px;
        border-radius: 25px;
        box-shadow: 0px 4px 15px rgba(0,0,0,0.08);
        margin-bottom: 30px;
    }

    .place-card {
        background-color: rgba(255, 255, 255, 0.95);
        padding: 18px;
        margin-bottom: 15px;
        border-radius: 18px;
        border-left: 6px solid #79B8E8;
        box-shadow: 0px 3px 10px rgba(0,0,0,0.06);
    }

    .place-title {
        font-size: 19px;
        font-weight: bold;
        color: #34495E;
        margin-bottom: 8px;
    }

    .place-description {
        color: #5D6D7E;
        line-height: 1.6;
    }
</style>
""", unsafe_allow_html=True)


# ==========================================
# 서울 관광지 데이터
# ==========================================
places = [
    {
        "number": 1,
        "emoji": "🏯",
        "name": "경복궁",
        "description": "조선 시대를 대표하는 궁궐이에요. 한복을 입고 아름다운 전통 건축을 구경하기 좋아요."
    },
    {
        "number": 2,
        "emoji": "🏘️",
        "name": "북촌한옥마을",
        "description": "전통 한옥이 모여 있는 마을이에요. 서울 속에서 한국의 옛 모습을 느껴볼 수 있어요."
    },
    {
        "number": 3,
        "emoji": "🎨",
        "name": "인사동",
        "description": "전통 기념품과 공예품, 한식과 다양한 카페를 만날 수 있는 한국적인 거리예요."
    },
    {
        "number": 4,
        "emoji": "🛍️",
        "name": "명동",
        "description": "쇼핑과 맛있는 길거리 음식으로 유명한 서울의 대표적인 관광 거리예요."
    },
    {
        "number": 5,
        "emoji": "🗼",
        "name": "남산서울타워",
        "description": "서울의 전경을 한눈에 볼 수 있는 전망 명소예요. 특히 반짝이는 야경이 유명해요."
    },
    {
        "number": 6,
        "emoji": "🎸",
        "name": "홍대",
        "description": "개성 있는 카페와 맛집, 거리 공연 등 젊고 활기찬 문화를 즐길 수 있는 곳이에요."
    },
    {
        "number": 7,
        "emoji": "🌃",
        "name": "강남",
        "description": "세련된 쇼핑 공간과 맛집, 다양한 문화 공간이 모여 있는 서울의 대표적인 번화가예요."
    },
    {
        "number": 8,
        "emoji": "📚",
        "name": "코엑스 & 별마당 도서관",
        "description": "대형 쇼핑몰과 높은 책장이 인상적인 별마당 도서관을 함께 즐길 수 있어요."
    },
    {
        "number": 9,
        "emoji": "🎢",
        "name": "롯데월드",
        "description": "다양한 놀이기구와 볼거리를 즐길 수 있는 서울의 대표적인 테마파크예요."
    },
    {
        "number": 10,
        "emoji": "🌊",
        "name": "청계천",
        "description": "서울 도심을 흐르는 산책 공간이에요. 관광하다가 잠시 쉬어가기에도 좋아요."
    }
]


# ==========================================
# 앱 제목과 캐릭터 말투
# ==========================================
st.markdown("""
<div class="title-box">
    <h1>🗺️ 외국인이 좋아하는 서울 관광지 TOP 10</h1>
    <p>🇰🇷 서울 여행, 어디부터 가야 할지 모르겠다고? 내가 알려줄게. ✈️</p>
</div>
""", unsafe_allow_html=True)

st.markdown("""
<div class="character-talk">
    💬 <b>서울 여행 도우미:</b> 서울에 볼 게 얼마나 많은데 아무 데나 갈 거야?
    내가 외국인들에게 인기 있는 관광지 10곳을 골라놨으니까 지도부터 봐. 😏🗺️
</div>
""", unsafe_allow_html=True)


# ==========================================
# 서울 관광 안내 지도
# ==========================================
seoul_map = """
<svg viewBox="0 0 1000 650" xmlns="http://www.w3.org/2000/svg"
     style="width:100%; height:auto; display:block;">

    <!-- 지도 배경 -->
    <rect width="1000" height="650" rx="25" fill="#EEF8FF"/>

    <!-- 서울 지역 -->
    <path d="
        M120 150
        Q220 80 350 125
        Q450 70 560 130
        Q700 90 830 165
        Q910 250 850 340
        Q920 430 830 530
        Q710 600 590 550
        Q470 615 350 560
        Q210 590 120 490
        Q70 400 130 305
        Q70 220 120 150 Z
    "
    fill="#DFF0DD"
    stroke="#8CBF9B"
    stroke-width="5"/>

    <!-- 한강 -->
    <path d="
        M80 350
        Q180 300 280 345
        Q390 395 490 350
        Q590 305 690 355
        Q790 405 900 350
    "
    fill="none"
    stroke="#7CC6E8"
    stroke-width="35"
    stroke-linecap="round"
    opacity="0.8"/>

    <!-- 지도 제목 -->
    <text x="500" y="70"
          text-anchor="middle"
          font-size="25"
          font-weight="bold"
          fill="#425B6B">
        📍 SEOUL TOP 10
    </text>

    <!-- 관광지 표시 -->
    <g font-family="Arial">

        <circle cx="400" cy="235" r="23" fill="#FF6B6B"/>
        <text x="400" y="243" text-anchor="middle"
              font-size="17" fill="white" font-weight="bold">1</text>

        <circle cx="460" cy="215" r="23" fill="#FF9F43"/>
        <text x="460" y="223" text-anchor="middle"
              font-size="17" fill="white" font-weight="bold">2</text>

        <circle cx="485" cy="270" r="23" fill="#F6C85F"/>
        <text x="485" y="278" text-anchor="middle"
              font-size="17" fill="white" font-weight="bold">3</text>

        <circle cx="530" cy="320" r="23" fill="#45B7D1"/>
        <text x="530" y="328" text-anchor="middle"
              font-size="17" fill="white" font-weight="bold">4</text>

        <circle cx="490" cy="380" r="23" fill="#6BCB77"/>
        <text x="490" y="388" text-anchor="middle"
              font-size="17" fill="white" font-weight="bold">5</text>

        <circle cx="300" cy="330" r="23" fill="#9B5DE5"/>
        <text x="300" y="338" text-anchor="middle"
              font-size="17" fill="white" font-weight="bold">6</text>

        <circle cx="650" cy="445" r="23" fill="#F15BB5"/>
        <text x="650" y="453" text-anchor="middle"
              font-size="17" fill="white" font-weight="bold">7</text>

        <circle cx="705" cy="410" r="23" fill="#00B4D8"/>
        <text x="705" y="418" text-anchor="middle"
              font-size="17" fill="white" font-weight="bold">8</text>

        <circle cx="775" cy="460" r="23" fill="#FF70A6"/>
        <text x="775" y="468" text-anchor="middle"
              font-size="17" fill="white" font-weight="bold">9</text>

        <circle cx="555" cy="270" r="23" fill="#577590"/>
        <text x="555" y="278" text-anchor="middle"
              font-size="17" fill="white" font-weight="bold">10</text>

    </g>

    <!-- 안내 문구 -->
    <rect x="120" y="555" width="760" height="55"
          rx="20" fill="white" opacity="0.9"/>

    <text x="500" y="590"
          text-anchor="middle"
          font-size="17"
          fill="#566573">
        지도 속 번호와 아래 관광지 설명을 확인해 보세요!
    </text>

</svg>
"""

st.markdown('<div class="map-box">', unsafe_allow_html=True)
st.markdown(seoul_map, unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)


# ==========================================
# 캐릭터 말투 안내
# ==========================================
st.markdown("""
<div class="character-talk">
    💬 <b>서울 여행 도우미:</b> 지도만 보고 끝낼 생각은 아니겠지?
    아래에 어디가 어떤 곳인지 간단하게 적어뒀으니까 하나씩 확인해 봐. 친절하지? 😌✨
</div>
""", unsafe_allow_html=True)


# ==========================================
# 관광지 설명
# ==========================================
st.subheader("📌 관광지 간단 설명")

col1, col2 = st.columns(2)

for index, place in enumerate(places):

    card = f"""
    <div class="place-card">
        <div class="place-title">
            {place['number']}. {place['emoji']} {place['name']}
        </div>
        <div class="place-description">
            {place['description']}
        </div>
    </div>
    """

    if index % 2 == 0:
        with col1:
            st.markdown(card, unsafe_allow_html=True)
    else:
        with col2:
            st.markdown(card, unsafe_allow_html=True)


# ==========================================
# 마무리 캐릭터 멘트
# ==========================================
st.markdown("""
<div class="character-talk">
    💬 <b>서울 여행 도우미:</b> 자, 이제 어디 갈지는 정했어?
    관광지끼리 가까운 곳을 묶어서 가면 덜 힘들어. 이것까지 알려줘야 하냐고...
    그래도 즐거운 서울 여행 하고 와. 🧳🇰🇷✨
</div>
""", unsafe_allow_html=True)

st.caption("🗺️ 서울 여행 도우미가 열심히 골라준 관광지 목록입니다!")
```
