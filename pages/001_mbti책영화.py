import streamlit as st
import base64

# -------------------------------
# 페이지 기본 설정
# -------------------------------
st.set_page_config(
    page_title="MBTI 취향 추천소",
    page_icon="🎀",
    layout="centered"
)

# -------------------------------
# 배경 이미지 설정
# 풀뱅 + 안경 쓴 귀여운 여자아이 느낌
# -------------------------------
background_svg = """
<svg width="1000" height="1000" xmlns="http://www.w3.org/2000/svg">

    <!-- 배경 -->
    <rect width="100%" height="100%" fill="#FFF9F2"/>

    <!-- 구름 -->
    <circle cx="120" cy="100" r="35" fill="#DDEEFF"/>
    <circle cx="160" cy="85" r="45" fill="#DDEEFF"/>
    <circle cx="205" cy="105" r="32" fill="#DDEEFF"/>

    <circle cx="820" cy="160" r="30" fill="#FFE4EF"/>
    <circle cx="860" cy="145" r="42" fill="#FFE4EF"/>
    <circle cx="900" cy="165" r="30" fill="#FFE4EF"/>

    <!-- 별과 하트 장식 -->
    <text x="80" y="300" font-size="45">⭐</text>
    <text x="880" y="350" font-size="40">💗</text>
    <text x="100" y="750" font-size="40">📚</text>
    <text x="850" y="800" font-size="40">🎬</text>
    <text x="750" y="100" font-size="35">✨</text>
    <text x="170" y="500" font-size="35">🫧</text>

    <!-- 여자아이 머리 -->
    <circle cx="500" cy="450" r="155" fill="#3D302E"/>

    <!-- 얼굴 -->
    <circle cx="500" cy="480" r="125" fill="#FFE0CC"/>

    <!-- 풀뱅 -->
    <path d="
        M375 420
        Q390 300 500 300
        Q610 300 625 420
        L600 395
        L575 425
        L550 390
        L525 425
        L500 390
        L475 425
        L450 390
        L425 425
        L400 395 Z
    " fill="#3D302E"/>

    <!-- 안경 -->
    <circle cx="450" cy="470" r="42"
        fill="none" stroke="#4A3B39" stroke-width="8"/>
    <circle cx="550" cy="470" r="42"
        fill="none" stroke="#4A3B39" stroke-width="8"/>
    <line x1="492" y1="470" x2="508" y2="470"
        stroke="#4A3B39" stroke-width="8"/>

    <!-- 눈 -->
    <circle cx="450" cy="475" r="7" fill="#3D302E"/>
    <circle cx="550" cy="475" r="7" fill="#3D302E"/>

    <!-- 볼 -->
    <ellipse cx="415" cy="520" rx="18" ry="9" fill="#F7AFC0"/>
    <ellipse cx="585" cy="520" rx="18" ry="9" fill="#F7AFC0"/>

    <!-- 입 -->
    <path d="M480 540 Q500 555 520 540"
        fill="none" stroke="#C76B7B"
        stroke-width="5" stroke-linecap="round"/>

    <!-- 몸 -->
    <path d="
        M390 650
        Q500 590 610 650
        L650 850
        L350 850 Z
    " fill="#BFDDF2"/>

    <!-- 책 -->
    <rect x="420" y="700" width="160" height="100"
        rx="10" fill="#FFD6A5"/>
    <line x1="500" y1="700" x2="500" y2="800"
        stroke="#FFFFFF" stroke-width="5"/>

    <!-- 리본 -->
    <path d="M380 650 L330 620 L350 690 Z"
        fill="#F6B6C8"/>
    <path d="M620 650 L670 620 L650 690 Z"
        fill="#F6B6C8"/>

</svg>
"""

# SVG를 Base64로 변환
background_base64 = base64.b64encode(
    background_svg.encode("utf-8")
).decode()

# CSS 적용
st.markdown(
    f"""
    <style>

    /* 전체 배경 */
    .stApp {{
        background-color: #FFF9F2;
        background-image: url("data:image/svg+xml;base64,{background_base64}");
        background-repeat: no-repeat;
        background-position: center bottom;
        background-size: 420px;
        background-attachment: fixed;
    }}

    /* 제목 */
    h1 {{
        text-align: center;
        color: #5B4B49;
        padding-top: 15px;
    }}

    /* 설명 글 */
    h3 {{
        text-align: center;
        color: #8A6F6A;
    }}

    /* 추천 결과 박스 */
    .stAlert {{
        border-radius: 15px;
    }}

    /* 버튼 */
    .stButton > button {{
        width: 100%;
        border-radius: 15px;
        border: none;
        padding: 12px;
        font-size: 17px;
        font-weight: bold;
        background-color: #F6B6C8;
        color: #4A3B39;
    }}

    .stButton > button:hover {{
        background-color: #EFA4BA;
        color: white;
    }}

    /* 선택 상자 */
    div[data-baseweb="select"] {{
        border-radius: 12px;
    }}

    </style>
    """,
    unsafe_allow_html=True
)


# -------------------------------
# MBTI별 추천 데이터
# -------------------------------
recommendations = {
    "INTJ": {
        "comics": ["데스노트 📓", "진격의 거인 ⚔️"],
        "movies": ["빅 히어로 🤖", "닥터 스트레인지 🌀"],
        "comment": "생각 많은 너한테 어울리는 걸로 골랐어. 마음에 들 거야. 아마도. 😏"
    },
    "INTP": {
        "comics": ["닥터 스톤 🧪", "스파이 패밀리 🕵️"],
        "movies": ["월-E 🤖", "소울 🎹"],
        "comment": "혼자 생각하는 시간 좋아하잖아. 이런 작품이면 꽤 재밌게 볼걸. 🤓"
    },
    "ENTJ": {
        "comics": ["하이큐!! 🏐", "원피스 ☠️"],
        "movies": ["라이온 킹 🦁", "뮬란 ⚔️"],
        "comment": "목표를 향해 달려가는 주인공들로 골랐어. 너랑 좀 닮았네. 👑"
    },
    "ENTP": {
        "comics": ["괴수 8호 🦖", "나의 히어로 아카데미아 🦸"],
        "movies": ["알라딘 🧞", "주토피아 🦊"],
        "comment": "뻔하고 조용한 건 재미없지. 그래서 좀 신나는 걸로 골랐어. 🙃"
    },
    "INFJ": {
        "comics": ["프루츠 바스켓 🌸", "나츠메 우인장 🐱"],
        "movies": ["코코 🎸", "인사이드 아웃 🌈"],
        "comment": "감정선 깊은 이야기 좋아할 것 같아서 골랐어. 울어도 난 몰라. 🥲"
    },
    "INFP": {
        "comics": ["카드캡터 체리 🌸", "너의 이름은. 🌠"],
        "movies": ["라따뚜이 🐭", "루카 🌊"],
        "comment": "따뜻하고 상상력 넘치는 이야기야. 그냥 편하게 즐겨. ☁️"
    },
    "ENFJ": {
        "comics": ["하이큐!! 🏐", "너에게 닿기를 💌"],
        "movies": ["엔칸토 🦋", "모아나 🌊"],
        "comment": "사람들과 함께 성장하는 이야기가 잘 어울릴 것 같았어. 😌"
    },
    "ENFP": {
        "comics": ["원피스 ☠️", "스파이 패밀리 🕵️"],
        "movies": ["라푼젤 🌼", "겨울왕국 ❄️"],
        "comment": "재미있고 밝은 작품들로 준비했어. 너라면 좋아할걸. ✨"
    },
    "ISTJ": {
        "comics": ["명탐정 코난 🔍", "강철의 연금술사 ⚙️"],
        "movies": ["뮬란 ⚔️", "라이온 킹 🦁"],
        "comment": "탄탄한 스토리가 있는 작품들이야. 무난하지만 실패는 없지. 📚"
    },
    "ISFJ": {
        "comics": ["너에게 닿기를 💌", "나츠메 우인장 🐱"],
        "movies": ["곰돌이 푸 🍯", "인사이드 아웃 🌈"],
        "comment": "따뜻하고 편안한 이야기가 딱이야. 마음 편하게 봐. 🍀"
    },
    "ESTJ": {
        "comics": ["하이큐!! 🏐", "귀멸의 칼날 🔥"],
        "movies": ["주토피아 🦊", "빅 히어로 🤖"],
        "comment": "에너지 넘치는 작품들로 골랐어. 꽤 괜찮은 선택이니까 믿어봐. 😎"
    },
    "ESFJ": {
        "comics": ["프루츠 바스켓 🌸", "스파이 패밀리 🕵️"],
        "movies": ["미녀와 야수 🌹", "엔칸토 🦋"],
        "comment": "사람 사이의 따뜻한 관계가 담긴 이야기들이야. 🫶"
    },
    "ISTP": {
        "comics": ["원펀맨 💥", "괴수 8호 🦖"],
        "movies": ["빅 히어로 🤖", "몬스터 주식회사 👾"],
        "comment": "복잡한 것보다 재밌고 시원한 게 좋지? 이걸로 봐. 🔥"
    },
    "ISFP": {
        "comics": ["카드캡터 체리 🌸", "너의 이름은. 🌠"],
        "movies": ["루카 🌊", "라푼젤 🌼"],
        "comment": "예쁘고 감성적인 작품들로 골랐어. 분위기 즐기면 돼. 🎨"
    },
    "ESTP": {
        "comics": ["괴수 8호 🦖", "원펀맨 💥"],
        "movies": ["알라딘 🧞", "주토피아 🦊"],
        "comment": "빠르고 신나는 작품들이야. 지루할 틈 없을걸. ⚡"
    },
    "ESFP": {
        "comics": ["스파이 패밀리 🕵️", "하이큐!! 🏐"],
        "movies": ["라푼젤 🌼", "모아나 🌊"],
        "comment": "밝고 재미있는 걸로 골랐어. 기분 전환하기 딱이네. 🎉"
    }
}


# -------------------------------
# 화면 구성
# -------------------------------
st.title("🎀 MBTI 취향 추천소")
st.write("### 📚 내 MBTI에 어울리는 만화책과 🎬 디즈니 영화를 찾아보자!")
st.divider()

mbti_list = list(recommendations.keys())

selected_mbti = st.selectbox(
    "🧩 당신의 MBTI를 선택하세요!",
    mbti_list
)

if st.button("✨ 내 취향 추천받기"):
    result = recommendations[selected_mbti]

    st.balloons()

    st.subheader(f"🔮 {selected_mbti}에게 추천하는 작품!")

    st.markdown("## 📚 추천 만화책")
    st.success(f"**① {result['comics'][0]}**")
    st.success(f"**② {result['comics'][1]}**")

    st.divider()

    st.markdown("## 🎬 추천 디즈니 영화")
    st.info(f"**① {result['movies'][0]}**")
    st.info(f"**② {result['movies'][1]}**")

    st.divider()

    st.warning(f"💬 한마디: {result['comment']}")

    st.caption("🎀 취향은 참고만 해. 재밌으면 그게 네 취향인 거니까.")
