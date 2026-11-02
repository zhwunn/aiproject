```python
# -------------------------------
# 예쁜 배경 SVG
# 풀뱅 + 안경 + 긴 머리 여자아이
# -------------------------------
background_svg = """
<svg width="1000" height="1200" xmlns="http://www.w3.org/2000/svg">

    <!-- 전체 파스텔 배경 -->
    <rect width="100%" height="100%" fill="#FFF8F4"/>

    <!-- 배경 장식용 큰 원 -->
    <circle cx="80" cy="180" r="120" fill="#FCE4EC" opacity="0.6"/>
    <circle cx="920" cy="350" r="150" fill="#E3F2FD" opacity="0.7"/>
    <circle cx="100" cy="950" r="130" fill="#FFF3CD" opacity="0.6"/>
    <circle cx="880" cy="1000" r="130" fill="#E8F5E9" opacity="0.7"/>

    <!-- 구름 -->
    <g fill="#FFFFFF" opacity="0.9">
        <circle cx="110" cy="120" r="25"/>
        <circle cx="145" cy="105" r="35"/>
        <circle cx="185" cy="120" r="25"/>

        <circle cx="800" cy="180" r="25"/>
        <circle cx="835" cy="160" r="35"/>
        <circle cx="875" cy="180" r="25"/>
    </g>

    <!-- 별 -->
    <text x="70" y="400" font-size="45">✨</text>
    <text x="880" y="480" font-size="40">⭐</text>
    <text x="150" y="720" font-size="35">💫</text>
    <text x="810" y="750" font-size="35">✨</text>

    <!-- 하트 -->
    <text x="100" y="550" font-size="35">💗</text>
    <text x="860" y="650" font-size="35">🩷</text>
    <text x="210" y="280" font-size="30">♡</text>
    <text x="750" y="320" font-size="35">♡</text>

    <!-- 책과 영화 장식 -->
    <text x="80" y="850" font-size="42">📚</text>
    <text x="850" y="900" font-size="42">🎬</text>
    <text x="180" y="1050" font-size="35">🎀</text>
    <text x="760" y="1080" font-size="35">🍿</text>

    <!-- 여자아이 긴 머리 -->
    <!-- 뒷머리 -->
    <path d="
        M350 600
        Q330 400 500 330
        Q670 400 650 600
        L680 970
        Q610 1030 500 1000
        Q390 1030 320 970
        Z
    " fill="#40312F"/>

    <!-- 긴 머리 양쪽 -->
    <path d="
        M365 520
        Q315 650 340 950
        Q360 1020 420 980
        L430 570 Z
    " fill="#40312F"/>

    <path d="
        M635 520
        Q685 650 660 950
        Q640 1020 580 980
        L570 570 Z
    " fill="#40312F"/>

    <!-- 얼굴 -->
    <ellipse cx="500" cy="530" rx="130" ry="150"
             fill="#FFE1CF"/>

    <!-- 풀뱅 -->
    <path d="
        M370 450
        Q380 320 500 320
        Q620 320 630 450
        Q600 410 570 445
        Q545 405 520 445
        Q500 400 480 445
        Q455 405 430 445
        Q400 410 370 450
        Z
    " fill="#40312F"/>

    <!-- 안경 -->
    <circle cx="445" cy="525" r="48"
            fill="none" stroke="#4B3B38" stroke-width="8"/>
    <circle cx="555" cy="525" r="48"
            fill="none" stroke="#4B3B38" stroke-width="8"/>

    <line x1="493" y1="525" x2="507" y2="525"
          stroke="#4B3B38" stroke-width="8"/>

    <!-- 눈 -->
    <circle cx="445" cy="530" r="7" fill="#40312F"/>
    <circle cx="555" cy="530" r="7" fill="#40312F"/>

    <!-- 볼 -->
    <ellipse cx="405" cy="590" rx="22" ry="11"
             fill="#F7AFC0" opacity="0.8"/>
    <ellipse cx="595" cy="590" rx="22" ry="11"
             fill="#F7AFC0" opacity="0.8"/>

    <!-- 입 -->
    <path d="M480 615 Q500 632 520 615"
          fill="none"
          stroke="#C96F7E"
          stroke-width="5"
          stroke-linecap="round"/>

    <!-- 몸 / 옷 -->
    <path d="
        M380 760
        Q500 690 620 760
        L680 1100
        L320 1100 Z
    " fill="#BFDDF2"/>

    <!-- 옷 깃 -->
    <path d="M440 735 L500 810 L560 735"
          fill="#FFFFFF"/>

    <!-- 리본 -->
    <path d="
        M500 810
        L455 780
        L440 830
        L485 835
        Z
    " fill="#F6B6C8"/>

    <path d="
        M500 810
        L545 780
        L560 830
        L515 835
        Z
    " fill="#F6B6C8"/>

    <circle cx="500" cy="812" r="13" fill="#F19BB5"/>

    <!-- 들고 있는 책 -->
    <rect x="410" y="880" width="180" height="115"
          rx="12" fill="#FFD6A5"/>

    <rect x="420" y="890" width="70" height="95"
          rx="5" fill="#FFE7C7"/>

    <rect x="510" y="890" width="70" height="95"
          rx="5" fill="#FFE7C7"/>

    <line x1="500" y1="885" x2="500" y2="995"
          stroke="#E5B984" stroke-width="5"/>

    <!-- 책 위 작은 하트 -->
    <text x="475" y="955" font-size="25">♡</text>

    <!-- 머리 주변 작은 장식 -->
    <text x="300" y="450" font-size="30">✦</text>
    <text x="670" y="430" font-size="30">✦</text>

</svg>
"""
```
