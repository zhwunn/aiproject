import streamlit as st
import base64

# ========================================
# 1. 페이지 설정
# ========================================
st.set_page_config(
    page_title="MBTI 취향 추천소 🎀",
    page_icon="📚",
    layout="centered"
)


# ========================================
# 2. 긴 머리 + 안경 여자아이 배경 만들기
# ========================================
background_svg = """
<svg xmlns="http://www.w3.org/2000/svg" width="1000" height="1200">

    <!-- 파스텔 배경 -->
    <rect width="100%" height="100%" fill="#FFF8F5"/>

    <!-- 큰 파스텔 장식 -->
    <circle cx="100" cy="150" r="130" fill="#FBE2EA" opacity="0.7"/>
    <circle cx="900" cy="280" r="150" fill="#DDEEFF" opacity="0.7"/>
    <circle cx="80" cy="900" r="150" fill="#FFF0C9" opacity="0.7"/>
    <circle cx="900" cy="1000" r="160" fill="#E2F3E5" opacity="0.7"/>

    <!-- 구름 -->
    <g fill="white" opacity="0.9">
        <circle cx="100" cy="180" r="30"/>
        <circle cx="140" cy="160" r="40"/>
        <circle cx="185" cy="180" r="30"/>

        <circle cx="800" cy="150" r="30"/>
        <circle cx="840" cy="130" r="40"/>
        <circle cx="885" cy="150" r="30"/>
    </g>

    <!-- 귀여운 배경 장식 -->
    <text x="80" y="400" font-size="45">✨</text>
    <text x="850" y="420" font-size="45">⭐</text>
    <text x="120" y="650" font-size="40">🩷</text>
    <text x="830" y="700" font-size="40">💗</text>
    <text x="100" y="850" font-size="45">📚</text>
    <text x="830" y="900" font-size="45">🎬</text>
    <text x="200" y="300" font-size="35">♡</text>
    <text x="730" y="300" font-size="35">✦</text>

    <!-- 긴 머리 뒷부분 -->
    <path d="
        M350 560
        Q320 370 500 300
        Q680 370 650 560
        L690 970
        Q620 1030 500 1000
        Q380 1030 310 970
        Z
    " fill="#40312F"/>

    <!-- 얼굴 -->
    <ellipse cx="500" cy="500" rx="130" ry="150" fill="#FFE1CF"/>

    <!-- 풀뱅 -->
    <path d="
        M370 440
        Q380 320 500 320
        Q620 320 630 440
        L600 420
        L575 450
        L550 415
        L525 450
        L500 415
        L475 450
        L450 415
        L425 450
        L400 420
        Z
    " fill="#40312F"/>

    <!-- 긴 머리 왼쪽 -->
    <path d="
        M380 500
        Q320 650 350 1000
        Q390 1040 440 990
        L440 560
        Z
    " fill="#40312F"/>

    <!-- 긴 머리 오른쪽 -->
    <path d="
        M620 500
        Q680 650 650 1000
        Q610 1040 560 990
        L560 560
        Z
    " fill="#40312F"/>

    <!-- 안경 -->
    <circle cx="445" cy="520" r="45"
        fill="none" stroke="#4A3937" stroke-width="8"/>

    <circle cx="555" cy="520" r="45"
        fill="none" stroke="#4A3937" stroke-width="8"/>

    <line x1="490" y1="520" x2="510" y2="520"
        stroke="#4A3937" stroke-width="8"/>

    <!-- 눈 -->
    <circle cx="445" cy="525" r="7" fill="#40312F"/>
    <circle cx="555" cy="525" r="7" fill="#40312F"/>

    <!-- 볼 -->
    <ellipse cx="405" cy="580" rx="20" ry="10" fill="#F5AFC0"/>
    <ellipse cx="595" cy="580" rx="20" ry="10" fill="#F5AFC0"/>

    <!-- 입 -->
    <path d="M480 610 Q500 625 520 610"
        fill="none"
        stroke="#C96F7E"
        stroke-width="5"
        stroke-linecap="round"/>

    <!-- 옷 -->
    <path d="
        M380 760
        Q500 690 620 760
        L680 1150
        L320 1150
        Z
    " fill="#BFDDF2"/>

    <!-- 흰색 옷깃 -->
    <path d="M440 735 L500 810 L560 735"
        fill="#FFFFFF"/>

    <!-- 핑크 리본 -->
    <path d="M500 810 L450 780 L440 830 L490 835 Z"
        fill="#F6B6C8"/>

    <path d="M500 810 L550 780 L560 830 L510 835 Z"
        fill="#F6B6C8"/>

    <circle cx="500" cy="812" r="13" fill="#EF9DB5"/>

    <!-- 들고 있는 책 -->
    <rect x="410" y="900" width="180" height="120"
        rx="12" fill="#FFD6A5"/>

    <line x1="500" y1="900" x2="500" y2="1020"
        stroke="#E2B580" stroke-width="5"/>

    <text x="470" y="975" font-size="35">♡</text>

</svg>
"""

# SVG를 안전하게 Base64로 변환
background_base64 = base64.b64encode(
    background_svg.encode("utf-8")
).decode("utf-8")


# ========================================
# 3. 디자인 적용
# ========================================
st.markdown(
    f"""
    <style>

    /* 전체 앱 배경 */
    .stApp {{
        background-color: #FFF8F5;
        background-image: url("data:image/svg+xml;base64,{background_base64}");
        background-repeat: no-repeat;
        background-position: center bottom;
        background-size: 430px auto;
        background-attachment: fixed;
    }}

    /* 메인 내용 영역 */
    .block-container {{
        background-color: rgba(255, 255, 255, 0.88);
        border-radius: 25px;
        padding: 2rem;
        margin-top: 2rem;
        margin-bottom: 18rem;
        box-shadow: 0 4px 15px rgba(100, 80, 80, 0.08);
    }}

    /* 제목 */
    h1 {{
        text-align: center;
        color: #5C4A48;
    }}

    h3 {{
        text-align: center;
        color: #8C7370;
    }}

    /* 버튼 */
    .stButton > button {{
        width: 100%;
        border: none;
        border-radius: 18px;
        padding: 13px;
        background-color: #F5B6C8;
        color: #513F3D;
        font-size: 17px;
        font-weight: bold;
    }}

    .stButton > button:hover {{
        background-color: #EFA2BA;
        color: white;
    }}

    /* 알림 박스 둥글게 */
    .stAlert {{
        border-radius: 18px;
    }}

    </style>
    """,
    unsafe_allow_html=True
)


# ========================================
# 4. MBTI 추천 데이터
# ========================================
recommendations = {
    "INTJ": {
        "comics": ["데스노트 📓", "진격의 거인 ⚔️"],
        "movies": ["빅 히어로 🤖", "닥터 스트레인지 🌀"],
        "comment": "생각 많은 너한테 어울리는 걸로 골랐어. 마음에 들 거야. 아마도. 😏"
    },
    "INTP": {
        "comics": ["닥터 스톤 🧪", "스파이 패밀리 🕵️"],
        "movies": ["월-E 🤖", "소울 🎹"],
        "comment": "생각할 거 많은 이야기로 골랐어. 너 이런 거 좋아할 것 같았거든. 🤓"
    },
    "ENTJ": {
        "comics": ["하이큐!! 🏐", "원피스 ☠️"],
        "movies": ["라이온 킹 🦁", "뮬란 ⚔️"],
        "comment": "목표를 향해 달려가는 주인공들로 골랐어. 꽤 잘 맞을걸. 👑"
    },
    "ENTP": {
        "comics": ["괴수 8호 🦖", "나의 히어로 아카데미아 🦸"],
        "movies": ["알라딘 🧞", "주토피아 🦊"],
        "comment": "뻔한 건 재미없잖아. 그래서 좀 신나는 걸로 골랐어. 🙃"
    },
    "INFJ": {
        "comics": ["프루츠 바스켓 🌸", "나츠메 우인장 🐱"],
        "movies": ["코코 🎸", "인사이드 아웃 🌈"],
        "comment": "감정선 깊은 이야기들이야. 울어도 내가 책임지진 않아. 🥲"
    },
    "INFP": {
        "comics": ["카드캡터 체리 🌸", "나츠메 우인장 🐱"],
        "movies": ["라따뚜이 🐭", "루카 🌊"],
        "comment": "따뜻하고 상상력 가득한 이야기로 골랐어. 편하게 즐겨. ☁️"
    },
    "ENFJ": {
        "comics": ["하이큐!! 🏐", "너에게 닿기를 💌"],
        "movies": ["엔칸토 🦋", "모아나 🌊"],
        "comment": "사람들과 함께 성장하는 이야기가 잘 어울릴 것 같았어. 😌"
    },
    "ENFP": {
        "comics": ["원피스 ☠️", "스파이 패밀리 🕵️"],
        "movies": ["라푼젤 🌼", "겨울왕국 ❄️"],
        "comment": "밝고 재미있는 작품들로 골랐어. 일단 믿고 봐봐. ✨"
    },
    "ISTJ": {
        "comics": ["명탐정 코난 🔍", "강철의 연금술사 ⚙️"],
        "movies": ["뮬란 ⚔️", "라이온 킹 🦁"],
        "comment": "탄탄한 스토리를 좋아한다면 이 정도는 괜찮을 거야. 📚"
    },
    "ISFJ": {
        "comics": ["너에게 닿기를 💌", "나츠메 우인장 🐱"],
        "movies": ["곰돌이 푸 🍯", "인사이드 아웃 🌈"],
        "comment": "따뜻하고 편안한 이야기야. 마음 편하게 봐. 🍀"
    },
    "ESTJ": {
        "comics": ["하이큐!! 🏐", "귀멸의 칼날 🔥"],
        "movies": ["주토피아 🦊", "빅 히어로 🤖"],
        "comment": "에너지 넘치는 작품들이야. 실패 없는 선택이니까 믿어. 😎"
    },
    "ESFJ": {
        "comics": ["프루츠 바스켓 🌸", "스파이 패밀리 🕵️"],
        "movies": ["미녀와 야수 🌹", "엔칸토 🦋"],
        "comment": "사람 사이의 따뜻한 관계가 담긴 이야기들이야. 너랑 잘 맞을걸. 🫶"
    },
    "ISTP": {
        "comics": ["원펀맨 💥", "괴수 8호 🦖"],
        "movies": ["빅 히어로 🤖", "몬스터 주식회사 👾"],
        "comment": "복잡한 것보다 재밌고 시원한 게 좋지? 이걸로 봐. 🔥"
    },
    "ISFP": {
        "comics": ["카드캡터 체리 🌸", "너의 이름은. 🌠"],
        "movies": ["루카 🌊", "라푼젤 🌼"],
        "comment": "예쁘고 감성적인 작품들로 골랐어. 분위기에 푹 빠져봐. 🎨"
    },
    "ESTP": {
        "comics": ["괴수 8호 🦖", "원펀맨 💥"],
        "movies": ["알라딘 🧞", "주토피아 🦊"],
        "comment": "빠르고 신나는 작품들이야. 지루할 틈은 없을걸. ⚡"
    },
    "ESFP": {
        "comics": ["스파이 패밀리 🕵️", "하이큐!! 🏐"],
        "movies": ["라푼젤 🌼", "모아나 🌊"],
        "comment": "밝고 신나는 걸로 골랐어. 기분 전환하기 딱이네. 🎉"
    }
}


# ========================================
# 5. 화면
# ========================================
st.title("🎀 MBTI 취향 추천소")
st.write("### 📚 나에게 어울리는 만화책과 🎬 디즈니 영화를 찾아보자!")
st.divider()

selected_mbti = st.selectbox(
    "🧩 당신의 MBTI를 선택하세요!",
    list(recommendations.keys())
)

if st.button("✨ 내 취향 추천받기"):
    result = recommendations[selected_mbti]

    st.balloons()

    st.subheader(f"🔮 {selected_mbti}에게 추천하는 작품!")

    st.markdown("## 📚 추천 만화책")
    st.success(f"① {result['comics'][0]}")
    st.success(f"② {result['comics'][1]}")

    st.markdown("## 🎬 추천 디즈니 영화")
    st.info(f"① {result['movies'][0]}")
    st.info(f"② {result['movies'][1]}")

    st.warning(f"💬 {result['comment']}")

    st.caption("🎀 취향은 참고만 해. 결국 네가 재밌으면 그게 정답이니까.")
