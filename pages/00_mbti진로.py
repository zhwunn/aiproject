
import streamlit as st
import html

st.set_page_config(
    page_title="MBTI 진로 탐험소",
    page_icon="🧭",
    layout="wide"
)

# ── 진로 데이터 ──────────────────────────────
# 연봉은 공식 통계의 확정 평균이 아닌 대략적인 참고 범위입니다.
CAREERS = {
    "ISTJ": ("꼼꼼한 현실주의자", [
        ("회계사", "기업의 재무 자료를 분석하고 회계·세무 업무를 수행해.", "회계학과, 경영학과, 세무학과", "꼼꼼하고 숫자와 규칙을 잘 다루는 사람", "약 4,000만~7,000만 원"),
        ("기록물관리 전문가", "문서와 기록을 분류하고 안전하게 보존해.", "문헌정보학과, 기록관리 관련 전공", "체계적이고 정리하는 걸 좋아하는 사람", "약 2,800만~4,000만 원"),
    ]),
    "ISFJ": ("다정한 수호자", [
        ("간호사", "환자의 상태를 확인하고 치료와 회복을 도와.", "간호학과", "책임감 있고 세심하게 사람을 돌보는 사람", "약 3,000만~4,500만 원"),
        ("초등교사", "초등학생에게 여러 과목을 가르치고 성장을 도와.", "교육대학교, 초등교육과", "인내심이 있고 차근차근 설명하는 사람", "약 3,000만~4,500만 원"),
    ]),
    "INFJ": ("의미를 찾는 조언자", [
        ("상담심리 전문가", "상담과 심리 평가 등을 통해 사람들의 고민 해결을 도와.", "심리학과, 상담학과, 상담심리 관련 대학원", "공감 능력이 있고 다른 사람의 이야기를 잘 듣는 사람", "약 2,800만~4,500만 원"),
        ("환경공학자", "오염을 줄이는 기술을 연구하고 환경 문제 해결 방법을 찾아.", "환경공학과, 환경과학과, 토목공학과", "책임감이 있고 분석과 문제 해결을 좋아하는 사람", "약 3,500만~6,000만 원"),
    ]),
    "INTJ": ("전략을 세우는 설계자", [
        ("소프트웨어 개발자", "프로그램과 앱을 설계하고 코드를 작성해.", "컴퓨터공학과, 소프트웨어학과", "논리적이고 문제의 원인을 찾는 걸 좋아하는 사람", "약 3,500만~6,000만 원"),
        ("건축가", "건물의 공간과 구조, 기능과 디자인을 계획해.", "건축학과", "계획적이고 공간을 상상하는 걸 좋아하는 사람", "약 3,000만~5,000만 원"),
    ]),
    "ISTP": ("실용적인 탐구가", [
        ("기계 엔지니어", "기계와 장비를 설계하고 성능을 개선해.", "기계공학과, 메카트로닉스공학과", "원리를 파악하고 직접 문제를 해결하는 사람", "약 3,200만~5,000만 원"),
        ("항공정비사", "항공기의 상태를 점검하고 안전하게 정비해.", "항공정비학과, 항공기계 관련 학과", "침착하고 안전 수칙을 꼼꼼히 지키는 사람", "약 3,000만~4,800만 원"),
    ]),
    "ISFP": ("감각적인 예술가", [
        ("제품 디자이너", "물건의 모양과 기능, 사용하기 편한 정도를 설계해.", "산업디자인학과, 제품디자인학과", "감각적이고 사용자의 입장을 생각하는 사람", "약 2,800만~4,500만 원"),
        ("플로리스트", "꽃과 식물로 꽃다발과 공간 장식을 만들어.", "원예학과, 화훼 관련 학과", "색 조합을 좋아하고 손으로 만드는 걸 즐기는 사람", "약 2,500만~3,500만 원"),
    ]),
    "INFP": ("상상력이 풍부한 이야기꾼", [
        ("콘텐츠 작가", "글과 이야기를 기획하고 사람들에게 메시지를 전달해.", "문예창작학과, 국어국문학과, 미디어학과", "상상력이 풍부하고 글로 표현하는 걸 좋아하는 사람", "약 2,800만~4,500만 원"),
        ("일러스트레이터", "책이나 광고, 온라인 콘텐츠에 들어가는 그림을 그려.", "시각디자인학과, 일러스트레이션 관련 전공", "그림과 색감에 관심이 있고 꾸준히 작업하는 사람", "약 2,800만~4,500만 원"),
    ]),
    "INTP": ("원리를 파고드는 분석가", [
        ("데이터 분석가", "데이터를 분석해 패턴을 찾고 의사결정에 필요한 정보를 제공해.", "통계학과, 데이터사이언스학과, 산업공학과", "호기심이 많고 논리적으로 분석하는 사람", "약 3,300만~5,500만 원"),
        ("연구원", "실험과 조사로 질문에 대한 답을 찾고 새로운 지식을 만들어.", "관심 분야의 자연과학·공학·사회과학 관련 학과", "탐구심이 강하고 한 가지 문제를 깊이 파고드는 사람", "약 3,000만~5,000만 원"),
    ]),
    "ESTP": ("현장에서 빛나는 실행가", [
        ("행사 기획자", "행사 일정과 장소, 프로그램을 계획하고 현장을 관리해.", "광고홍보학과, 관광학과, 경영학과", "순발력이 있고 사람들과 소통하는 걸 좋아하는 사람", "약 2,800만~4,200만 원"),
        ("영업 담당자", "고객의 필요를 파악하고 제품이나 서비스를 소개해.", "경영학과, 유통학과 등", "적극적이고 대화와 협상에 흥미가 있는 사람", "약 3,000만~5,000만 원"),
    ]),
    "ESFP": ("분위기를 살리는 표현가", [
        ("영상 콘텐츠 제작자", "영상의 기획·촬영·편집을 통해 콘텐츠를 만들어.", "영상학과, 미디어학과, 방송영상학과", "표현력이 있고 사람들의 반응에 관심이 많은 사람", "약 2,800만~4,500만 원"),
        ("호텔 서비스 매니저", "고객 서비스를 관리하고 직원들과 운영 업무를 조율해.", "호텔경영학과, 관광학과", "친화력이 있고 상황에 맞게 대응하는 사람", "약 2,800만~4,200만 원"),
    ]),
    "ENFP": ("아이디어가 넘치는 탐험가", [
        ("광고 기획자", "브랜드를 알릴 광고 아이디어와 캠페인을 기획해.", "광고홍보학과, 미디어학과, 경영학과", "창의적이고 새로운 아이디어를 내는 걸 좋아하는 사람", "약 3,000만~4,800만 원"),
        ("진로 상담 전문가", "학생이나 구직자가 흥미와 강점을 발견하도록 도와.", "상담학과, 심리학과, 교육학과", "공감 능력이 있고 다른 사람의 가능성을 발견하는 사람", "약 2,800만~4,200만 원"),
    ]),
    "ENTP": ("새로운 판을 짜는 발명가", [
        ("창업가", "아이디어를 사업으로 발전시키고 제품이나 서비스를 운영해.", "경영학과, 창업 관련 전공 등", "도전적이고 새로운 방법을 실험하는 사람", "수입 편차가 매우 커서 일률적인 평균 제시가 어려움"),
        ("브랜드 기획자", "시장과 고객을 분석해 브랜드의 이미지와 전략을 만들어.", "경영학과, 광고홍보학과, 마케팅 관련 학과", "변화를 좋아하고 아이디어를 전략으로 연결하는 사람", "약 3,200만~5,000만 원"),
    ]),
    "ESTJ": ("계획을 실행하는 관리자", [
        ("프로젝트 매니저", "일정과 예산, 업무 분담을 조율해 프로젝트를 진행해.", "경영학과, 산업공학과, 정보시스템 관련 학과", "조직적이고 목표를 세워 추진하는 사람", "약 3,500만~5,500만 원"),
        ("물류 관리자", "상품의 재고와 보관, 배송 과정을 효율적으로 관리해.", "물류학과, 유통학과, 산업공학과", "체계적이고 일정과 자원을 관리하는 사람", "약 3,000만~4,800만 원"),
    ]),
    "ESFJ": ("사람을 연결하는 협력가", [
        ("인사 담당자", "채용과 직원 교육, 조직문화 관련 업무를 맡아.", "경영학과, 심리학과, 행정학과", "배려심이 있고 사람들과 협력하는 걸 좋아하는 사람", "약 3,000만~4,800만 원"),
        ("이벤트 플래너", "행사의 콘셉트와 일정, 준비 과정을 조율해.", "관광학과, 이벤트 관련 학과, 광고홍보학과", "세심하고 사람들을 위해 준비하는 걸 좋아하는 사람", "약 2,800만~4,200만 원"),
    ]),
    "ENFJ": ("사람을 이끄는 응원단장", [
        ("교사", "학생에게 지식을 전달하고 학습과 성장을 지원해.", "사범대학 또는 희망 교과 관련 학과·교직 과정", "설명을 잘하고 다른 사람의 성장을 돕는 사람", "약 3,000만~4,500만 원"),
        ("홍보 전문가", "조직의 소식과 메시지를 대중에게 효과적으로 전달해.", "광고홍보학과, 미디어커뮤니케이션학과", "소통 능력이 좋고 핵심 내용을 정리하는 사람", "약 3,000만~4,800만 원"),
    ]),
    "ENTJ": ("큰 그림을 그리는 리더", [
        ("경영 컨설턴트", "기업의 문제를 분석하고 개선 방안을 제안해.", "경영학과, 경제학과, 산업공학과 등", "분석적이고 목표를 세워 해결책을 찾는 사람", "약 4,000만~7,000만 원"),
        ("사업 기획자", "시장과 고객을 분석해 사업 목표와 실행 계획을 세워.", "경영학과, 경제학과, 산업공학과", "추진력이 있고 장기적인 계획을 좋아하는 사람", "약 3,300만~5,500만 원"),
    ]),
}

# ── 디자인 ───────────────────────────────────
st.markdown("""
<style>
.stApp {
    background: #fffaf0;
    color: #283653;
}
.block-container {
    max-width: 1120px;
    padding-top: 2rem;
}
h1, h2, h3 { color: #26365b !important; }
.stSelectbox > div > div {
    border: 2px solid #b9d9fa;
    border-radius: 15px;
    background: white;
}
.stButton > button {
    border: 2px solid #26365b;
    border-radius: 15px;
    background: #dceaff;
    color: #26365b;
    font-weight: bold;
    box-shadow: 3px 3px 0 #26365b;
}
.stButton > button:hover {
    background: #ffedb5;
    color: #26365b;
    border-color: #26365b;
}
.doodle {
    background: #fff1c9;
    border: 2px solid #373b50;
    border-radius: 23px 17px 25px 19px;
    padding: 18px;
    margin: 8px 0 18px 0;
    box-shadow: 4px 4px 0 #373b50;
}
.career {
    background: #ffffff;
    border: 2px solid #c9b6f5;
    border-radius: 22px 17px 25px 19px;
    padding: 18px;
    margin-bottom: 12px;
    min-height: 370px;
}
.career.green { border-color: #a8d9d2; }
.label {
    display: inline-block;
    background: #fff0c5;
    border-radius: 10px;
    padding: 5px 9px;
    font-weight: bold;
    margin: 6px 0;
}
.small-note { color: #666; font-size: 0.88rem; }
</style>
""", unsafe_allow_html=True)

def girl():
    # 외부 이미지 없이 SVG로 직접 그린 간단한 애니메이션풍 캐릭터
    return """
    <svg width="150" height="135" viewBox="0 0 150 135"
         xmlns="http://www.w3.org/2000/svg">
      <ellipse cx="75" cy="126" rx="43" ry="5" fill="#eadfcf"/>
      <path d="M29 61 Q18 12 69 10 Q126 5 121 62 L119 112
               Q106 132 75 125 Q42 132 30 110 Z"
            fill="#493b3b" stroke="#302d3b" stroke-width="3"/>
      <ellipse cx="75" cy="61" rx="38" ry="43"
               fill="#ffe0d5" stroke="#302d3b" stroke-width="2.5"/>
      <path d="M37 54 Q35 12 74 16 Q116 12 113 53
               L103 40 L91 47 L80 38 L66 48 L54 40 Z"
            fill="#493b3b" stroke="#302d3b" stroke-width="2"/>
      <path d="M40 45 L41 65 M51 38 L53 53 M64 36 L65 52
               M78 35 L78 51 M92 37 L91 52 M105 42 L102 62"
            stroke="#493b3b" stroke-width="5" stroke-linecap="round"/>
      <ellipse cx="60" cy="65" rx="13" ry="12"
               fill="none" stroke="#30334b" stroke-width="3"/>
      <ellipse cx="91" cy="65" rx="13" ry="12"
               fill="none" stroke="#30334b" stroke-width="3"/>
      <path d="M73 64 L78 64" stroke="#30334b" stroke-width="3"/>
      <ellipse cx="61" cy="66" rx="4" ry="6" fill="#30334b"/>
      <ellipse cx="91" cy="66" rx="4" ry="6" fill="#30334b"/>
      <circle cx="63" cy="64" r="1.7" fill="white"/>
      <circle cx="93" cy="64" r="1.7" fill="white"/>
      <ellipse cx="48" cy="79" rx="7" ry="4" fill="#f5a5a9" opacity=".8"/>
      <ellipse cx="101" cy="79" rx="7" ry="4" fill="#f5a5a9" opacity=".8"/>
      <path d="M70 84 Q77 90 84 83" fill="none"
            stroke="#8c515b" stroke-width="2.5" stroke-linecap="round"/>
      <path d="M38 103 Q75 91 112 103 L119 126 L31 126 Z"
            fill="#b9d7f6" stroke="#302d3b" stroke-width="2.5"/>
      <path d="M75 100 L68 110 L76 119 L83 110 Z" fill="white"/>
      <path d="M24 25 l4 9 l9 1 l-7 6 l2 9 l-8 -5 l-8 5 l2 -9 l-7 -6 l9 -1 Z"
            fill="#ffd76c" stroke="#d2a83e" stroke-width="1.5"/>
      <path d="M124 24 l3 6 l7 1 l-5 5 l1 7 l-6 -3 l-6 3 l1 -7 l-5 -5 l7 -1 Z"
            fill="#ffd76c" stroke="#d2a83e" stroke-width="1.5"/>
    </svg>
    """

st.markdown(
    "<h1>🧭 MBTI 진로 탐험소</h1>",
    unsafe_allow_html=True
)

left, right = st.columns([1, 3])

with left:
    st.markdown(
        '<div class="doodle" style="text-align:center;">'
        + girl() +
        '<h3>MBTI 진로 탐험소</h3>'
        '<p>🎨 네 성격으로 진로를 찾아줄게!</p>'
        '<p>빨리 골라 봐. 내가 다 골라 줄 순 없잖아. 🙄</p>'
        '</div>',
        unsafe_allow_html=True
    )
    st.caption("✏️ 오늘의 잔소리: 꿈만 꾸지 말고 조금씩 알아보자고.")

with right:
    st.markdown(
        '<div class="doodle">'
        '<h2>💬 너의 MBTI는 뭐야?</h2>'
        '<p>16가지 중 하나를 골라. 진로 두 개를 추천해 줄게!</p>'
        '<p>물론 MBTI가 네 미래를 다 알려 주는 건 아니거든. 흥.</p>'
        '</div>',
        unsafe_allow_html=True
    )

    mbti = st.selectbox(
        "🧩 MBTI 유형 선택",
        list(CAREERS.keys()),
        index=2,
        format_func=lambda x: f"{x} · {CAREERS[x][0]}"
    )

    if st.button("🔎 내 진로 추천받기", use_container_width=True):
        st.session_state["chosen_mbti"] = mbti

    selected = st.session_state.get("chosen_mbti")

    if selected:
        title, jobs = CAREERS[selected]

        st.markdown(
            f'<div class="doodle">'
            f'<h2>⭐ {selected} · {html.escape(title)}</h2>'
            f'<p>너한테 어울릴 수 있는 진로 두 가지야. '
            f'대충 보지 말고 잘 읽어 봐. 🙄</p>'
            f'</div>',
            unsafe_allow_html=True
        )

        col1, col2 = st.columns(2)

        for i, (job, duty, major, personality, salary) in enumerate(jobs):
            target = col1 if i == 0 else col2
            style = "" if i == 0 else " green"

            with target:
                st.markdown(
                    f'<div class="career{style}">'
                    f'<h2>{"🌷" if i == 0 else "🌱"} {i+1}. '
                    f'{html.escape(job)}</h2>'
                    f'<p><span class="label">🛠️ 주요 업무</span><br>'
                    f'{html.escape(duty)}</p>'
                    f'<p><span class="label">🎓 관련 학과</span><br>'
                    f'{html.escape(major)}</p>'
                    f'<p><span class="label">🧠 어울리는 성격</span><br>'
                    f'{html.escape(personality)}</p>'
                    f'<p><span class="label">💰 연봉 참고 범위</span><br>'
                    f'<b>{html.escape(salary)}</b></p>'
                    f'</div>',
                    unsafe_allow_html=True
                )

                if i == 0:
                    st.markdown(
                        '<div style="text-align:center;">'
                        + girl() +
                        '<p>사람 마음을 돌보는 일, 생각보다 어렵거든. '
                        '그래도 관심 있다면 알아봐!</p></div>',
                        unsafe_allow_html=True
                    )
                else:
                    st.markdown(
                        '<div style="text-align:center;">'
                        + girl() +
                        '<p>세상을 바꾸고 싶다고? 말만 하지 말고 '
                        '뭐라도 찾아보라고!</p></div>',
                        unsafe_allow_html=True
                    )

        st.info(
            "📌 연봉은 국내 직업의 대략적인 참고 범위이며 공식 통계의 "
            "단일 평균값이 아닙니다. 회사, 지역, 경력, 자격 및 고용형태에 "
            "따라 달라질 수 있어요. 최신 자료는 고용24와 한국직업정보에서 확인하세요."
        )

        st.markdown(
            '<div class="doodle">'
            '<h3>📝 마지막으로 한마디</h3>'
            '<p>MBTI만 보고 진로를 정하진 마. '
            '네가 좋아하는 것, 잘하는 것, 원하는 생활도 중요하거든.</p>'
            '<p>조급해하지 말고 하나씩 알아봐. 할 수 있겠지? ✨</p>'
            '</div>',
            unsafe_allow_html=True
        )

st.divider()
st.caption("🖍️ MBTI 진로 탐험소 · 성격 유형은 진로 탐색을 위한 참고 자료입니다.")
