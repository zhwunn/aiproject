import streamlit as st

# 페이지 설정
st.set_page_config(
    page_title="MBTI 취향 추천소",
    page_icon="🎠",
    layout="centered"
)

# 제목
st.title("🎠 MBTI 취향 추천소")
st.write("### 내 MBTI로 만화책 📚과 디즈니 영화 🎬를 추천받아 보자!")
st.divider()

# MBTI별 추천 데이터
recommendations = {
    "INTJ": {
        "comics": ["데스노트 📓", "진격의 거인 ⚔️"],
        "movies": ["닥터 스트레인지 🌀", "빅 히어로 🤖"],
        "comment": "혼자 깊게 생각하는 거 좋아하지? 이런 이야기쯤은 봐줘야지. 😏"
    },
    "INTP": {
        "comics": ["스파이 패밀리 🕵️", "닥터 스톤 🧪"],
        "movies": ["월-E 🤖", "소울 🎹"],
        "comment": "생각이 너무 많아도 괜찮아. 이건 재밌게 볼 수 있을 거야. 아마도. 🤓"
    },
    "ENTJ": {
        "comics": ["하이큐!! 🏐", "원피스 ☠️"],
        "movies": ["라이온 킹 🦁", "뮬란 ⚔️"],
        "comment": "목표 정했으면 끝까지 가는 타입이니까, 이런 주인공들이 잘 맞을걸. 👑"
    },
    "ENTP": {
        "comics": ["괴수 8호 🦖", "나의 히어로 아카데미아 🦸"],
        "movies": ["알라딘 🧞", "주토피아 🦊"],
        "comment": "새롭고 정신없는 이야기가 딱이지. 지루한 건 못 참잖아. 🙃"
    },
    "INFJ": {
        "comics": ["너의 이름은. 📖", "프루츠 바스켓 🌸"],
        "movies": ["코코 🎸", "인사이드 아웃 🌈"],
        "comment": "감정선 깊은 이야기 좋아할 것 같아서 골라봤어. 울어도 내가 책임 안 져. 🥲"
    },
    "INFP": {
        "comics": ["카드캡터 체리 🌸", "나츠메 우인장 🐱"],
        "movies": ["라따뚜이 🐭", "루카 🌊"],
        "comment": "따뜻하고 상상력 가득한 이야기가 잘 어울려. 완전 예상했어. ☁️"
    },
    "ENFJ": {
        "comics": ["하이큐!! 🏐", "너에게 닿기를 💌"],
        "movies": ["엔칸토 🦋", "모아나 🌊"],
        "comment": "사람들과 함께 성장하는 이야기를 좋아할 것 같았어. 역시 그렇지? 😌"
    },
    "ENFP": {
        "comics": ["원피스 ☠️", "스파이 패밀리 🕵️"],
        "movies": ["라푼젤 🌼", "겨울왕국 ❄️"],
        "comment": "재미있고 신나는 거 좋아하는 사람에게 딱이야. 일단 믿고 봐봐. ✨"
    },
    "ISTJ": {
        "comics": ["명탐정 코난 🔍", "강철의 연금술사 ⚙️"],
        "movies": ["뮬란 ⚔️", "라이온 킹 🦁"],
        "comment": "탄탄한 이야기와 책임감 있는 주인공들로 골랐어. 무난하지만 좋은 선택이야. 📚"
    },
    "ISFJ": {
        "comics": ["너에게 닿기를 💌", "나츠메 우인장 🐱"],
        "movies": ["곰돌이 푸 🍯", "인사이드 아웃 🌈"],
        "comment": "편안하고 따뜻한 이야기가 잘 맞을 것 같아. 마음 편하게 봐. 🍀"
    },
    "ESTJ": {
        "comics": ["하이큐!! 🏐", "귀멸의 칼날 🔥"],
        "movies": ["주토피아 🦊", "빅 히어로 🤖"],
        "comment": "에너지 넘치고 목표가 뚜렷한 이야기로 준비했어. 마음에 안 들면... 어쩔 수 없고. 😎"
    },
    "ESFJ": {
        "comics": ["프루츠 바스켓 🌸", "스파이 패밀리 🕵️"],
        "movies": ["미녀와 야수 🌹", "엔칸토 🦋"],
        "comment": "사람 사이의 관계가 따뜻한 작품들이야. 혼자 보기 아까울 수도 있겠네. 🫶"
    },
    "ISTP": {
        "comics": ["원펀맨 💥", "괴수 8호 🦖"],
        "movies": ["빅 히어로 🤖", "몬스터 주식회사 👾"],
        "comment": "복잡한 설명보다 재밌고 시원한 게 최고지. 이건 꽤 괜찮을 거야. 🔥"
    },
    "ISFP": {
        "comics": ["카드캡터 체리 🌸", "너의 이름은. 🌠"],
        "movies": ["루카 🌊", "라푼젤 🌼"],
        "comment": "예쁘고 감성적인 이야기를 골라봤어. 그냥 분위기에 푹 빠져봐. 🎨"
    },
    "ESTP": {
        "comics": ["괴수 8호 🦖", "원펀맨 💥"],
        "movies": ["알라딘 🧞", "주토피아 🦊"],
        "comment": "빠르고 신나는 이야기가 최고잖아. 지루할 틈은 없을 거야. ⚡"
    },
    "ESFP": {
        "comics": ["스파이 패밀리 🕵️", "하이큐!! 🏐"],
        "movies": ["라푼젤 🌼", "모아나 🌊"],
        "comment": "재미있고 밝은 작품들로 골랐어. 기분 전환하기 딱 좋겠네. 🎉"
    }
}

# MBTI 선택
mbti_list = list(recommendations.keys())

selected_mbti = st.selectbox(
    "🧩 당신의 MBTI를 선택하세요!",
    mbti_list
)

# 추천 버튼
if st.button("✨ 취향 추천받기"):
    result = recommendations[selected_mbti]

    st.balloons()

    st.subheader(f"🔮 {selected_mbti}님을 위한 추천 결과")

    st.write("## 📚 추천 만화책")
    st.write(f"**① {result['comics'][0]}**")
    st.write(f"**② {result['comics'][1]}**")

    st.divider()

    st.write("## 🎬 추천 디즈니 영화")
    st.write(f"**① {result['movies'][0]}**")
    st.write(f"**② {result['movies'][1]}**")

    st.divider()

    st.info(f"💬 추천 한마디: {result['comment']}")

    st.caption("🎠 취향은 참고만 해. 결국 네가 재밌으면 그게 정답이니까.")
