import streamlit as st
import random
import time
import math

# ============================================================
# 🎣 FISHING LEGENDS
# Streamlit Fishing RPG
# ============================================================

st.set_page_config(
    page_title="Fishing Legends",
    page_icon="🎣",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ============================================================
# CSS
# ============================================================

st.markdown("""
<style>

@import url('https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@400;500;600;700;800;900&display=swap');

* {
    font-family: 'Noto Sans KR', sans-serif;
}

html, body, [class*="css"] {
    font-family: 'Noto Sans KR', sans-serif;
}

.stApp {
    background:
        radial-gradient(
            circle at 15% 10%,
            rgba(38, 130, 255, 0.16),
            transparent 28%
        ),
        radial-gradient(
            circle at 85% 15%,
            rgba(0, 220, 255, 0.10),
            transparent 25%
        ),
        linear-gradient(
            135deg,
            #050d18 0%,
            #081a30 45%,
            #06101d 100%
        );
    color: #ffffff;
}

.block-container {
    max-width: 1500px;
    padding-top: 18px;
    padding-bottom: 60px;
}

h1, h2, h3 {
    letter-spacing: -1px;
}

button {
    font-family: 'Noto Sans KR', sans-serif !important;
}

div.stButton > button {
    border-radius: 12px;
    min-height: 44px;
    font-weight: 800;
    border: 1px solid rgba(120,180,255,0.22);
    background: rgba(14,30,50,0.80);
}

div.stButton > button:hover {
    border: 1px solid rgba(100,210,255,0.65);
    transform: translateY(-1px);
}

.game-title {
    font-size: 46px;
    line-height: 1.0;
    font-weight: 900;
    letter-spacing: -3px;
}

.game-subtitle {
    color: #7891ad;
    margin-top: 8px;
    font-size: 14px;
}

.topbar {
    background:
        linear-gradient(
            135deg,
            rgba(12,30,52,0.92),
            rgba(8,20,37,0.92)
        );
    border: 1px solid rgba(110,170,235,0.20);
    border-radius: 20px;
    padding: 14px;
    box-shadow: 0 15px 45px rgba(0,0,0,0.22);
}

.top-stat {
    text-align: center;
    padding: 8px;
}

.top-stat-label {
    color: #7790ab;
    font-size: 11px;
    font-weight: 700;
}

.top-stat-value {
    font-size: 19px;
    font-weight: 900;
    margin-top: 2px;
}

.card {
    background:
        linear-gradient(
            145deg,
            rgba(12,29,49,0.94),
            rgba(7,20,36,0.94)
        );
    border: 1px solid rgba(100,165,225,0.18);
    border-radius: 22px;
    padding: 22px;
    margin-bottom: 18px;
    box-shadow:
        0 15px 50px rgba(0,0,0,0.24),
        inset 0 1px rgba(255,255,255,0.02);
}

.water {
    position: relative;
    min-height: 500px;
    overflow: hidden;
    border-radius: 24px;
    background:
        radial-gradient(
            circle at 50% 10%,
            rgba(95,220,255,0.20),
            transparent 30%
        ),
        linear-gradient(
            180deg,
            #0a789e 0%,
            #075d87 38%,
            #06486f 72%,
            #043858 100%
        );
    border: 1px solid rgba(110,220,255,0.30);
    box-shadow:
        inset 0 0 80px rgba(0,0,0,0.18),
        0 20px 60px rgba(0,0,0,0.25);
}

.water::before {
    content: "";
    position: absolute;
    left: -10%;
    top: 34%;
    width: 120%;
    height: 100px;
    border-top: 2px solid rgba(190,245,255,0.16);
    border-radius: 50%;
    transform: rotate(-2deg);
}

.water::after {
    content: "";
    position: absolute;
    left: -10%;
    top: 60%;
    width: 120%;
    height: 100px;
    border-top: 2px solid rgba(190,245,255,0.12);
    border-radius: 50%;
    transform: rotate(2deg);
}

.water-location {
    position: relative;
    z-index: 3;
    padding-top: 24px;
    text-align: center;
    font-size: 28px;
    font-weight: 900;
}

.water-description {
    position: relative;
    z-index: 3;
    text-align: center;
    color: #b7e8f8;
    font-size: 13px;
}

.rod-display {
    position: relative;
    z-index: 3;
    text-align: center;
    font-size: 100px;
    margin-top: 75px;
    filter:
        drop-shadow(0 12px 12px rgba(0,0,0,0.25));
    transform: rotate(-10deg);
}

.line {
    position: absolute;
    z-index: 2;
    width: 2px;
    height: 150px;
    background: rgba(230,250,255,0.65);
    left: 54%;
    top: 55%;
    transform: rotate(12deg);
}

.float {
    position: absolute;
    z-index: 4;
    left: 53%;
    top: 81%;
    font-size: 25px;
}

.water-info {
    position: absolute;
    z-index: 4;
    left: 20px;
    bottom: 20px;
    color: rgba(225,250,255,0.75);
    font-size: 12px;
}

.status-card {
    background: rgba(4,15,27,0.72);
    border: 1px solid rgba(100,170,230,0.18);
    border-radius: 16px;
    padding: 15px;
}

.status-label {
    color: #7189a5;
    font-size: 11px;
}

.status-value {
    font-size: 22px;
    font-weight: 900;
}

.rod-card {
    background:
        linear-gradient(
            145deg,
            rgba(10,25,43,0.94),
            rgba(6,17,30,0.94)
        );
    border: 1px solid rgba(100,160,220,0.18);
    border-radius: 18px;
    padding: 18px;
    margin-bottom: 14px;
}

.rod-icon {
    font-size: 58px;
    text-align: center;
}

.rod-name {
    font-size: 19px;
    font-weight: 900;
}

.rod-grade {
    color: #89b4df;
    font-size: 12px;
    font-weight: 700;
}

.fish-card {
    background:
        linear-gradient(
            145deg,
            rgba(10,26,44,0.95),
            rgba(6,18,31,0.95)
        );
    border: 1px solid rgba(90,160,220,0.17);
    border-radius: 18px;
    padding: 17px;
    margin-bottom: 14px;
    min-height: 190px;
}

.fish-icon {
    font-size: 50px;
}

.fish-name {
    font-size: 18px;
    font-weight: 900;
}

.fish-detail {
    color: #91a8c0;
    font-size: 12px;
    line-height: 1.8;
}

.catch-result {
    background:
        radial-gradient(
            circle at center,
            rgba(50,160,255,0.16),
            transparent 60%
        ),
        rgba(6,20,36,0.96);
    border: 1px solid rgba(100,200,255,0.30);
    border-radius: 24px;
    padding: 35px;
    text-align: center;
    box-shadow: 0 0 70px rgba(20,150,255,0.12);
}

.catch-icon {
    font-size: 100px;
}

.catch-name {
    font-size: 32px;
    font-weight: 900;
}

.catch-price {
    color: #ffd86a;
    font-size: 25px;
    font-weight: 900;
}

.trait {
    display: inline-block;
    padding: 5px 10px;
    margin: 3px;
    border-radius: 10px;
    background: rgba(255,255,255,0.07);
    font-size: 12px;
    font-weight: 800;
}

.event {
    background:
        linear-gradient(
            135deg,
            rgba(122,73,255,0.18),
            rgba(25,164,255,0.14)
        );
    border: 1px solid rgba(140,120,255,0.35);
    border-radius: 20px;
    padding: 18px;
    text-align: center;
    margin: 15px 0;
}

.event-title {
    font-size: 22px;
    font-weight: 900;
}

.event-text {
    color: #b4c9df;
    font-size: 13px;
    line-height: 1.7;
}

.inventory-slot {
    background: rgba(5,15,27,0.85);
    border: 1px solid rgba(105,165,220,0.18);
    border-radius: 15px;
    padding: 12px;
    min-height: 145px;
    text-align: center;
    margin-bottom: 8px;
}

.empty-slot {
    color: #526981;
    padding-top: 42px;
    font-size: 12px;
}

.inventory-icon {
    font-size: 42px;
}

.inventory-name {
    font-size: 13px;
    font-weight: 900;
}

.inventory-price {
    color: #ffd36a;
    font-size: 12px;
}

.title-card {
    background:
        linear-gradient(
            145deg,
            rgba(24,37,59,0.96),
            rgba(9,20,35,0.96)
        );
    border: 1px solid rgba(130,175,235,0.18);
    border-radius: 20px;
    padding: 18px;
    margin-bottom: 13px;
}

.title-name {
    font-size: 20px;
    font-weight: 900;
}

.title-condition {
    color: #8ca5c0;
    font-size: 12px;
    margin-top: 5px;
}

.title-effect {
    color: #9fdcff;
    font-size: 13px;
    margin-top: 8px;
}

.shop-price {
    color: #ffd76a;
    font-size: 17px;
    font-weight: 900;
}

.big-number {
    font-size: 34px;
    font-weight: 900;
}

.muted {
    color: #7189a4;
    font-size: 12px;
}

.section-title {
    font-size: 25px;
    font-weight: 900;
    margin-bottom: 15px;
}

</style>
""", unsafe_allow_html=True)


# ============================================================
# 낚싯대
# ============================================================

RODS = [
    {
        "name": "나뭇가지 낚싯대",
        "emoji": "🪵",
        "grade": "일반",
        "price": 0,
        "power": 5,
        "luck": 1,
        "bite": 1,
        "pull": 5
    },
    {
        "name": "초보자 낚싯대",
        "emoji": "🎣",
        "grade": "일반",
        "price": 100,
        "power": 10,
        "luck": 3,
        "bite": 3,
        "pull": 10
    },
    {
        "name": "대나무 낚싯대",
        "emoji": "🎋",
        "grade": "일반",
        "price": 300,
        "power": 17,
        "luck": 5,
        "bite": 5,
        "pull": 17
    },
    {
        "name": "철제 낚싯대",
        "emoji": "🛠️",
        "grade": "고급",
        "price": 800,
        "power": 28,
        "luck": 8,
        "bite": 8,
        "pull": 28
    },
    {
        "name": "강철 낚싯대",
        "emoji": "⚙️",
        "grade": "고급",
        "price": 2000,
        "power": 42,
        "luck": 13,
        "bite": 13,
        "pull": 42
    },
    {
        "name": "은빛 낚싯대",
        "emoji": "🥈",
        "grade": "희귀",
        "price": 5000,
        "power": 65,
        "luck": 20,
        "bite": 20,
        "pull": 65
    },
    {
        "name": "황금 낚싯대",
        "emoji": "🥇",
        "grade": "희귀",
        "price": 12000,
        "power": 90,
        "luck": 30,
        "bite": 30,
        "pull": 90
    },
    {
        "name": "수정 낚싯대",
        "emoji": "💎",
        "grade": "희귀",
        "price": 25000,
        "power": 120,
        "luck": 42,
        "bite": 38,
        "pull": 120
    },
    {
        "name": "사파이어 낚싯대",
        "emoji": "🔷",
        "grade": "영웅",
        "price": 50000,
        "power": 165,
        "luck": 58,
        "bite": 50,
        "pull": 165
    },
    {
        "name": "루비 낚싯대",
        "emoji": "🔶",
        "grade": "영웅",
        "price": 100000,
        "power": 220,
        "luck": 78,
        "bite": 65,
        "pull": 220
    },
    {
        "name": "다이아몬드 낚싯대",
        "emoji": "💠",
        "grade": "영웅",
        "price": 250000,
        "power": 300,
        "luck": 110,
        "bite": 85,
        "pull": 300
    },
    {
        "name": "별빛 낚싯대",
        "emoji": "🌌",
        "grade": "전설",
        "price": 500000,
        "power": 400,
        "luck": 150,
        "bite": 110,
        "pull": 400
    },
    {
        "name": "달빛 낚싯대",
        "emoji": "🌙",
        "grade": "전설",
        "price": 1000000,
        "power": 540,
        "luck": 210,
        "bite": 145,
        "pull": 540
    },
    {
        "name": "태양 낚싯대",
        "emoji": "☀️",
        "grade": "전설",
        "price": 2500000,
        "power": 720,
        "luck": 290,
        "bite": 190,
        "pull": 720
    },
    {
        "name": "해신의 낚싯대",
        "emoji": "🌊",
        "grade": "신화",
        "price": 5000000,
        "power": 950,
        "luck": 390,
        "bite": 250,
        "pull": 950
    },
    {
        "name": "번개의 낚싯대",
        "emoji": "⚡",
        "grade": "신화",
        "price": 10000000,
        "power": 1250,
        "luck": 520,
        "bite": 330,
        "pull": 1250
    },
    {
        "name": "용의 낚싯대",
        "emoji": "🔥",
        "grade": "신화",
        "price": 25000000,
        "power": 1650,
        "luck": 700,
        "bite": 450,
        "pull": 1650
    },
    {
        "name": "은하 낚싯대",
        "emoji": "🌠",
        "grade": "초월",
        "price": 60000000,
        "power": 2200,
        "luck": 950,
        "bite": 600,
        "pull": 2200
    },
    {
        "name": "차원의 낚싯대",
        "emoji": "🌀",
        "grade": "초월",
        "price": 150000000,
        "power": 3000,
        "luck": 1400,
        "bite": 850,
        "pull": 3000
    },
    {
        "name": "신의 낚싯대",
        "emoji": "👑",
        "grade": "초월",
        "price": 500000000,
        "power": 4500,
        "luck": 2200,
        "bite": 1300,
        "pull": 4500
    }
]


# ============================================================
# 물고기 80종
# ============================================================

fish_names = [
    "피라미",
    "송사리",
    "붕어",
    "잉어",
    "은어",
    "전어",
    "고등어",
    "멸치",
    "정어리",
    "꽁치",
    "청어",
    "숭어",
    "갈치",
    "가자미",
    "농어",
    "우럭",
    "망둥어",
    "쥐치",
    "보리멸",
    "도미",

    "참돔",
    "광어",
    "쏘가리",
    "메기",
    "장어",
    "송어",
    "연어",
    "방어",
    "삼치",
    "복어",
    "민어",
    "감성돔",
    "벵에돔",
    "전갱이",
    "대구",
    "황어",
    "빙어",
    "철갑상어",
    "가물치",
    "가오리",

    "대왕잉어",
    "대형연어",
    "황금송어",
    "황금도미",
    "청새치",
    "참치",
    "다랑어",
    "대왕오징어",
    "대왕문어",
    "전기뱀장어",
    "대형농어",
    "거대메기",
    "왕연어",
    "거대복어",
    "흑참치",

    "황금잉어",
    "황금참치",
    "심해아귀",
    "거대상어",
    "백상아리",
    "범고래",
    "거대가오리",
    "심해용",
    "대왕참치",
    "고대상어",
    "빙하상어",
    "폭풍참치",
    "심해문어",
    "고대철갑상어",
    "유령고래",

    "해룡",
    "크라켄",
    "고대고래",
    "황금고래",
    "차원의 물고기",
    "천공의 용어",
    "심연의 상어",
    "시간의 물고기",
    "우주의 고래",
    "창조의 물고기"
]


fish_grades = (
    ["일반"] * 20 +
    ["희귀"] * 20 +
    ["영웅"] * 15 +
    ["전설"] * 15 +
    ["신화"] * 10
)

grade_base_price = {
    "일반": 100,
    "희귀": 1000,
    "영웅": 8000,
    "전설": 50000,
    "신화": 300000
}

grade_weight = {
    "일반": (0.05, 8),
    "희귀": (1, 30),
    "영웅": (10, 150),
    "전설": (50, 1000),
    "신화": (300, 10000)
}

fish_emojis = [
    "🐟",
    "🐠",
    "🐡",
    "🦈",
    "🐋",
    "🐙",
    "🦑",
    "🐬"
]

FISH = []

for i in range(80):

    grade = fish_grades[i]

    min_w, max_w = grade_weight[grade]

    base = grade_base_price[grade]

    rarity_multiplier = 1 + (
        (i % 20) * 0.08
    )

    FISH.append({
        "id": i,
        "name": fish_names[i],
        "grade": grade,
        "emoji": fish_emojis[i % len(fish_emojis)],
        "base_price": int(base * rarity_multiplier),
        "min_weight": min_w,
        "max_weight": max_w,
        "min_size": round(
            max(0.08, min_w ** (1/3) * 0.55),
            2
        ),
        "max_size": round(
            max(0.20, max_w ** (1/3) * 0.85),
            2
        )
    })


# ============================================================
# 타이틀
# ============================================================

TITLES = [
    {
        "name": "초보 낚시꾼",
        "condition": "게임 시작",
        "effect": "기본 타이틀",
        "stat": {}
    },
    {
        "name": "첫 물고기",
        "condition": "물고기 1마리 낚기",
        "effect": "행운 +1%",
        "stat": {"luck": 0.01}
    },
    {
        "name": "숙련 낚시꾼",
        "condition": "물고기 100마리 낚기",
        "effect": "입질 속도 +3%",
        "stat": {"bite": 0.03}
    },
    {
        "name": "대어 사냥꾼",
        "condition": "50kg 이상 물고기 낚기",
        "effect": "끌어올리기 +5%",
        "stat": {"pull": 0.05}
    },
    {
        "name": "황금 손",
        "condition": "총 판매액 100,000G",
        "effect": "판매가격 +5%",
        "stat": {"sell": 0.05}
    },
    {
        "name": "물고기 수집가",
        "condition": "물고기 30종 발견",
        "effect": "행운 +5%",
        "stat": {"luck": 0.05}
    },
    {
        "name": "전설의 낚시꾼",
        "condition": "물고기 50종 발견",
        "effect": "행운 +10%",
        "stat": {"luck": 0.10}
    },
    {
        "name": "강화의 달인",
        "condition": "강화 20회 성공",
        "effect": "강화 성공률 +2%p",
        "stat": {"enhance": 2}
    },
    {
        "name": "무지개의 낚시꾼",
        "condition": "무지개 물고기 10마리",
        "effect": "무지개 특성 확률 +1%p",
        "stat": {"rainbow": 0.01}
    },
    {
        "name": "차원의 낚시꾼",
        "condition": "차원 물고기 3마리",
        "effect": "차원 특성 확률 +0.5%p",
        "stat": {"dimension": 0.005}
    },
    {
        "name": "낚시왕",
        "condition": "80종 모두 발견",
        "effect": "전체 스탯 +10%",
        "stat": {"all": 0.10}
    },
    {
        "name": "신의 낚시꾼",
        "condition": "+100 강화 달성",
        "effect": "전체 스탯 +15%",
        "stat": {"all": 0.15}
    }
]


# ============================================================
# 초기화
# ============================================================

def initialize_game():

    st.session_state.gold = 5000

    st.session_state.inventory = []

    st.session_state.inventory_capacity = 10

    st.session_state.owned_rods = [0]

    st.session_state.equipped_rod = 0

    st.session_state.rod_levels = {
        0: 0
    }

    st.session_state.protection_tickets = 0

    st.session_state.discovered = set()

    st.session_state.titles = [
        "초보 낚시꾼"
    ]

    st.session_state.equipped_title = "초보 낚시꾼"

    st.session_state.total_catches = 0

    st.session_state.total_sold = 0

    st.session_state.max_weight = 0

    st.session_state.enhancement_successes = 0

    st.session_state.dimension_catches = 0

    st.session_state.rainbow_catches = 0

    st.session_state.silver_catches = 0

    st.session_state.gold_catches = 0

    st.session_state.page = "낚시"

    st.session_state.last_catch = None

    st.session_state.event_active = False

    st.session_state.event_end = 0

    st.session_state.location = "푸른 바다"

    st.session_state.catching = False


if "gold" not in st.session_state:
    initialize_game()


# ============================================================
# 유틸
# ============================================================

def fmt(value):
    return f"{int(value):,} G"


def current_rod():
    return RODS[
        st.session_state.equipped_rod
    ]


def rod_level():
    return st.session_state.rod_levels.get(
        st.session_state.equipped_rod,
        0
    )


def title_data():

    for title in TITLES:

        if title["name"] == st.session_state.equipped_title:

            return title

    return TITLES[0]


def get_title_stat(stat):

    data = title_data()

    return data["stat"].get(stat, 0)


def get_rod_stats(index):

    rod = RODS[index]

    level = st.session_state.rod_levels.get(
        index,
        0
    )

    multiplier = 1.02 ** level

    all_bonus = get_title_stat("all")

    return {
        "power": rod["power"] * multiplier * (1 + all_bonus),
        "luck": rod["luck"] * multiplier * (1 + all_bonus),
        "bite": rod["bite"] * multiplier * (1 + all_bonus),
        "pull": rod["pull"] * multiplier * (1 + all_bonus)
    }


# ============================================================
# 강화 비용
# ============================================================

def enhancement_cost(level, rod_index):

    rod_price = RODS[rod_index]["price"]

    if rod_price <= 0:
        rod_price = 100

    base_cost = max(
        100,
        int(rod_price * 0.08)
    )

    return int(
        base_cost *
        (1.18 ** level)
    )


def enhancement_success_rate(level):

    # +0 = 100%
    # +1 = 99%
    # ...
    # +99 = 1%
    # +100부터 1%
    return max(
        1,
        100 - level
    )


# ============================================================
# 이벤트
# ============================================================

def check_event():

    now = time.time()

    if st.session_state.event_active:

        if now >= st.session_state.event_end:

            st.session_state.event_active = False

            st.session_state.event_end = 0

    else:

        if random.random() < 0.025:

            st.session_state.event_active = True

            duration = random.randint(
                90,
                240
            )

            st.session_state.event_end = (
                now + duration
            )


def event_bonus():

    if st.session_state.event_active:
        return 0.05

    return 0


def event_remaining():

    if not st.session_state.event_active:
        return 0

    return max(
        0,
        int(
            st.session_state.event_end
            - time.time()
        )
    )


check_event()


# ============================================================
# 특성
# ============================================================

def roll_traits():

    event = event_bonus()

    silver_chance = 0.08 + event

    gold_chance = 0.04 + event

    rainbow_chance = (
        0.02
        + event
        + get_title_stat("rainbow")
    )

    dimension_chance = (
        0.009
        + event
        + get_title_stat("dimension")
    )

    traits = []

    # 각각 독립 판정
    if random.random() < silver_chance:

        traits.append({
            "name": "실버",
            "emoji": "🥈",
            "bonus": 0.10
        })

        st.session_state.silver_catches += 1

    if random.random() < gold_chance:

        traits.append({
            "name": "골드",
            "emoji": "🥇",
            "bonus": 0.20
        })

        st.session_state.gold_catches += 1

    if random.random() < rainbow_chance:

        traits.append({
            "name": "무지개",
            "emoji": "🌈",
            "bonus": 0.50
        })

        st.session_state.rainbow_catches += 1

    if random.random() < dimension_chance:

        traits.append({
            "name": "차원",
            "emoji": "🌀",
            "bonus": 1.00
        })

        st.session_state.dimension_catches += 1

    return traits


# ============================================================
# 물고기 가격
# ============================================================

def calculate_price(
    fish,
    weight,
    size,
    traits
):

    price = fish["base_price"]

    average_weight = (
        fish["min_weight"]
        + fish["max_weight"]
    ) / 2

    average_size = (
        fish["min_size"]
        + fish["max_size"]
    ) / 2

    weight_multiplier = (
        weight / average_weight
    )

    size_multiplier = (
        size / average_size
    )

    # 무게와 크기의 영향
    price *= (
        0.55
        + weight_multiplier * 0.45
    )

    price *= (
        0.60
        + size_multiplier * 0.40
    )

    # 특성
    for trait in traits:

        price *= (
            1 + trait["bonus"]
        )

    # 타이틀 판매 보너스
    sell_bonus = get_title_stat("sell")

    price *= (
        1 + sell_bonus
    )

    return max(
        1,
        int(price)
    )


# ============================================================
# 물고기 낚기
# ============================================================

def catch_fish():

    if len(
        st.session_state.inventory
    ) >= st.session_state.inventory_capacity:

        st.error(
            "🎒 인벤토리가 가득 찼습니다!"
        )

        return False

    index = st.session_state.equipped_rod

    stats = get_rod_stats(index)

    luck = stats["luck"]

    grade_weights = {

        "일반":
            max(
                10,
                1000 - luck * 1.5
            ),

        "희귀":
            180 + luck * 0.45,

        "영웅":
            45 + luck * 0.13,

        "전설":
            10 + luck * 0.04,

        "신화":
            1 + luck * 0.012
    }

    grades = list(
        grade_weights.keys()
    )

    weights = list(
        grade_weights.values()
    )

    grade = random.choices(
        grades,
        weights=weights,
        k=1
    )[0]

    candidates = [
        fish
        for fish in FISH
        if fish["grade"] == grade
    ]

    fish = random.choice(
        candidates
    )

    weight = random.uniform(
        fish["min_weight"],
        fish["max_weight"]
    )

    size = random.uniform(
        fish["min_size"],
        fish["max_size"]
    )

    traits = roll_traits()

    price = calculate_price(
        fish,
        weight,
        size,
        traits
    )

    result = {
        "fish_id": fish["id"],
        "name": fish["name"],
        "grade": fish["grade"],
        "emoji": fish["emoji"],
        "weight": weight,
        "size": size,
        "traits": traits,
        "price": price,
        "base_price": fish["base_price"]
    }

    st.session_state.inventory.append(
        result
    )

    st.session_state.discovered.add(
        fish["id"]
    )

    st.session_state.total_catches += 1

    st.session_state.max_weight = max(
        st.session_state.max_weight,
        weight
    )

    st.session_state.last_catch = result

    check_titles()

    return True


# ============================================================
# 타이틀 체크
# ============================================================

def unlock_title(name):

    if name not in st.session_state.titles:

        st.session_state.titles.append(
            name
        )

        return True

    return False


def check_titles():

    if st.session_state.total_catches >= 1:

        unlock_title(
            "첫 물고기"
        )

    if st.session_state.total_catches >= 100:

        unlock_title(
            "숙련 낚시꾼"
        )

    if st.session_state.max_weight >= 50:

        unlock_title(
            "대어 사냥꾼"
        )

    if st.session_state.total_sold >= 100000:

        unlock_title(
            "황금 손"
        )

    if len(
        st.session_state.discovered
    ) >= 30:

        unlock_title(
            "물고기 수집가"
        )

    if len(
        st.session_state.discovered
    ) >= 50:

        unlock_title(
            "전설의 낚시꾼"
        )

    if st.session_state.enhancement_successes >= 20:

        unlock_title(
            "강화의 달인"
        )

    if st.session_state.rainbow_catches >= 10:

        unlock_title(
            "무지개의 낚시꾼"
        )

    if st.session_state.dimension_catches >= 3:

        unlock_title(
            "차원의 낚시꾼"
        )

    if len(
        st.session_state.discovered
    ) >= 80:

        unlock_title(
            "낚시왕"
        )

    if rod_level() >= 100:

        unlock_title(
            "신의 낚시꾼"
        )


# ============================================================
# 판매
# ============================================================

def sell_one(index):

    if index >= len(
        st.session_state.inventory
    ):

        return

    fish = st.session_state.inventory.pop(
        index
    )

    st.session_state.gold += fish["price"]

    st.session_state.total_sold += fish["price"]

    check_titles()


def sell_all():

    total = sum(
        fish["price"]
        for fish in st.session_state.inventory
    )

    count = len(
        st.session_state.inventory
    )

    st.session_state.gold += total

    st.session_state.total_sold += total

    st.session_state.inventory = []

    check_titles()

    return count, total


# ============================================================
# 낚싯대 구매
# ============================================================

def buy_rod(index):

    rod = RODS[index]

    if index in st.session_state.owned_rods:

        return

    if st.session_state.gold < rod["price"]:

        st.error(
            "💰 골드가 부족합니다."
        )

        return

    st.session_state.gold -= rod["price"]

    st.session_state.owned_rods.append(
        index
    )

    st.session_state.rod_levels[index] = 0

    st.success(
        f"{rod['emoji']} {rod['name']} 구매 완료!"
    )


# ============================================================
# 낚싯대 강화
# ============================================================

def enhance_rod():

    index = st.session_state.equipped_rod

    level = st.session_state.rod_levels.get(
        index,
        0
    )

    cost = enhancement_cost(
        level,
        index
    )

    if st.session_state.gold < cost:

        st.error(
            "💰 골드가 부족합니다."
        )

        return

    st.session_state.gold -= cost

    rate = (
        enhancement_success_rate(
            level
        )
    )

    rate += get_title_stat(
        "enhance"
    )

    rate = min(
        100,
        rate
    )

    success = (
        random.random() * 100
        < rate
    )

    if success:

        st.session_state.rod_levels[index] = (
            level + 1
        )

        st.session_state.enhancement_successes += 1

        st.success(
            f"✨ 강화 성공! +{level + 1}"
        )

        check_titles()

    else:

        if st.session_state.protection_tickets > 0:

            st.session_state.protection_tickets -= 1

            st.warning(
                f"🛡️ 강화 실패방지권 발동!"
                f" +{level}을 유지했습니다."
            )

        else:

            st.session_state.rod_levels[index] = 0

            st.error(
                f"💥 강화 실패!"
                f" +{level} → +0"
            )


# ============================================================
# 인벤토리 업그레이드
# ============================================================

def inventory_upgrade_cost():

    current = (
        st.session_state.inventory_capacity
    )

    level = (
        current - 10
    ) // 5

    return int(
        1000 * (1.55 ** level)
    )


def upgrade_inventory():

    cost = inventory_upgrade_cost()

    if st.session_state.gold < cost:

        st.error(
            "💰 골드가 부족합니다."
        )

        return

    st.session_state.gold -= cost

    st.session_state.inventory_capacity += 5

    st.success(
        f"🎒 인벤토리 확장!"
        f" 현재 {st.session_state.inventory_capacity}칸"
    )


# ============================================================
# 실패방지권 가격
# ============================================================

PROTECTION_TICKET_PRICE = 1000000


def buy_protection_ticket():

    if st.session_state.gold < PROTECTION_TICKET_PRICE:

        st.error(
            "💰 골드가 부족합니다."
        )

        return

    st.session_state.gold -= (
        PROTECTION_TICKET_PRICE
    )

    st.session_state.protection_tickets += 1

    st.success(
        "🛡️ 강화 실패방지권을 구매했습니다!"
    )


# ============================================================
# 상단 제목
# ============================================================

st.markdown(
    '<div class="game-title">🎣 FISHING LEGENDS</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="game-subtitle">'
    '낚싯대를 강화하고 전설의 물고기를 수집하세요.'
    '</div>',
    unsafe_allow_html=True
)

st.write("")


# ============================================================
# 상단 스탯
# ============================================================

st.markdown(
    '<div class="topbar">',
    unsafe_allow_html=True
)

c1, c2, c3, c4, c5, c6 = st.columns(6)

with c1:

    st.markdown(
        f"""
        <div class="top-stat">
            <div class="top-stat-label">
                💰 GOLD
            </div>
            <div class="top-stat-value">
                {fmt(st.session_state.gold)}
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

with c2:

    st.markdown(
        f"""
        <div class="top-stat">
            <div class="top-stat-label">
                🎒 INVENTORY
            </div>
            <div class="top-stat-value">
                {len(st.session_state.inventory)}
                /
                {st.session_state.inventory_capacity}
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

with c3:

    st.markdown(
        f"""
        <div class="top-stat">
            <div class="top-stat-label">
                📖 COLLECTION
            </div>
            <div class="top-stat-value">
                {len(st.session_state.discovered)}
                / 80
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

with c4:

    st.markdown(
        f"""
        <div class="top-stat">
            <div class="top-stat-label">
                🎣 CATCHES
            </div>
            <div class="top-stat-value">
                {st.session_state.total_catches:,}
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

with c5:

    st.markdown(
        f"""
        <div class="top-stat">
            <div class="top-stat-label">
                🛡️ PROTECTION
            </div>
            <div class="top-stat-value">
                {st.session_state.protection_tickets}
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

with c6:

    st.markdown(
        f"""
        <div class="top-stat">
            <div class="top-stat-label">
                🏆 TITLE
            </div>
            <div class="top-stat-value">
                {st.session_state.equipped_title}
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

st.markdown(
    '</div>',
    unsafe_allow_html=True
)


# ============================================================
# 이벤트
# ============================================================

if st.session_state.event_active:

    remaining = event_remaining()

    minutes = remaining // 60
    seconds = remaining % 60

    st.markdown(
        f"""
        <div class="event">

            <div class="event-title">
                🌟 특성 확률 UP 이벤트
            </div>

            <div class="event-text">

                모든 특성 확률이
                <b>+5%p</b> 증가합니다!

                <br><br>

                🥈 실버 13%
                ·
                🥇 골드 9%
                ·
                🌈 무지개 7%
                ·
                🌀 차원 5.9%

                <br><br>

                ⏱️ 남은 시간
                <b>
                    {minutes:02d}:{seconds:02d}
                </b>

            </div>

        </div>
        """,
        unsafe_allow_html=True
    )


# ============================================================
# 메뉴
# ============================================================

m1, m2, m3, m4, m5, m6, m7 = st.columns(7)

with m1:

    if st.button(
        "🎣 낚시",
        use_container_width=True
    ):

        st.session_state.page = "낚시"

        st.rerun()

with m2:

    if st.button(
        "🎒 인벤토리",
        use_container_width=True
    ):

        st.session_state.page = "인벤토리"

        st.rerun()

with m3:

    if st.button(
        "🏪 상점",
        use_container_width=True
    ):

        st.session_state.page = "상점"

        st.rerun()

with m4:

    if st.button(
        "💰 판매",
        use_container_width=True
    ):

        st.session_state.page = "판매"

        st.rerun()

with m5:

    if st.button(
        "🔨 강화",
        use_container_width=True
    ):

        st.session_state.page = "강화"

        st.rerun()

with m6:

    if st.button(
        "🏆 타이틀",
        use_container_width=True
    ):

        st.session_state.page = "타이틀"

        st.rerun()

with m7:

    if st.button(
        "📖 도감",
        use_container_width=True
    ):

        st.session_state.page = "도감"

        st.rerun()


st.write("")


# ============================================================
# 🎣 낚시
# ============================================================

if st.session_state.page == "낚시":

    left, right = st.columns(
        [2.25, 1]
    )

    # --------------------------------------------------------
    # 낚시터
    # --------------------------------------------------------

    with left:

        st.markdown(
            f"""
            <div class="water">

                <div class="water-location">
                    🌊 {st.session_state.location}
                </div>

                <div class="water-description">
                    잔잔한 물결 아래에서
                    무언가 움직이고 있습니다...
                </div>

                <div class="rod-display">
                    {current_rod()["emoji"]}
                </div>

                <div class="line"></div>

                <div class="float">
                    🔴
                </div>

                <div class="water-info">
                    🎣 {current_rod()["name"]}
                    +{rod_level()}
                    &nbsp; · &nbsp;
                    ♾️ 내구도 무한
                </div>

            </div>
            """,
            unsafe_allow_html=True
        )

        st.write("")

        if len(
            st.session_state.inventory
        ) >= st.session_state.inventory_capacity:

            st.warning(
                "🎒 인벤토리가 가득 찼습니다."
            )

        else:

            if st.button(
                "🎣 낚싯대 던지기",
                use_container_width=True,
                type="primary"
            ):

                stats = get_rod_stats(
                    st.session_state.equipped_rod
                )

                bite_time = max(
                    0.5,
                    3.0 / (
                        1 + stats["bite"] / 100
                    )
                )

                with st.spinner(
                    f"🌊 입질을 기다리는 중..."
                ):

                    time.sleep(
                        min(
                            3,
                            bite_time
                        )
                    )

                # 끌어올리기 성공 확률
                pull_chance = (
                    stats["pull"]
                    /
                    (
                        stats["pull"]
                        + 100
                    )
                )

                # 기본 성공률 보정
                success_chance = min(
                    0.97,
                    0.45
                    + pull_chance * 0.55
                )

                if random.random() < success_chance:

                    if catch_fish():

                        st.success(
                            "🎣 입질 성공!"
                        )

                        st.rerun()

                else:

                    st.error(
                        "💦 물고기가 도망갔습니다!"
                    )

        # ----------------------------------------------------
        # 최근 물고기
        # ----------------------------------------------------

        if st.session_state.last_catch:

            fish = (
                st.session_state.last_catch
            )

            if fish["traits"]:

                trait_html = "".join(
                    f"""
                    <span class="trait">
                        {t["emoji"]}
                        {t["name"]}
                    </span>
                    """
                    for t in fish["traits"]
                )

            else:

                trait_html = """
                <span class="trait">
                    일반
                </span>
                """

            st.markdown(
                f"""
                <div class="catch-result">

                    <div class="catch-icon">
                        {fish["emoji"]}
                    </div>

                    <div class="catch-name">
                        {fish["name"]}
                    </div>

                    <div>
                        {fish["grade"]}
                    </div>

                    <br>

                    {trait_html}

                    <br><br>

                    📏 크기
                    <b>{fish["size"]:.2f} m</b>

                    &nbsp;&nbsp;

                    ⚖️ 무게
                    <b>{fish["weight"]:.2f} kg</b>

                    <br><br>

                    <div class="catch-price">
                        {fmt(fish["price"])}
                    </div>

                </div>
                """,
                unsafe_allow_html=True
            )

    # --------------------------------------------------------
    # 오른쪽 스탯
    # --------------------------------------------------------

    with right:

        rod = current_rod()

        stats = get_rod_stats(
            st.session_state.equipped_rod
        )

        st.markdown(
            '<div class="card">',
            unsafe_allow_html=True
        )

        st.markdown(
            f"""
            <div class="section-title">
                {rod["emoji"]}
                {rod["name"]}
            </div>

            <div class="muted">
                {rod["grade"]}
                · 강화 +{rod_level()}
            </div>

            <br>
            """,
            unsafe_allow_html=True
        )

        s1, s2 = st.columns(2)

        with s1:

            st.markdown(
                f"""
                <div class="status-card">
                    <div class="status-label">
                        💪 힘
                    </div>
                    <div class="status-value">
                        {stats["power"]:,.1f}
                    </div>
                </div>
                """,
                unsafe_allow_html=True
            )

        with s2:

            st.markdown(
                f"""
                <div class="status-card">
                    <div class="status-label">
                        🍀 행운
                    </div>
                    <div class="status-value">
                        {stats["luck"]:,.1f}
                    </div>
                </div>
                """,
                unsafe_allow_html=True
            )

        st.write("")

        s3, s4 = st.columns(2)

        with s3:

            st.markdown(
                f"""
                <div class="status-card">
                    <div class="status-label">
                        ⚡ 입질
                    </div>
                    <div class="status-value">
                        {stats["bite"]:,.1f}
                    </div>
                </div>
                """,
                unsafe_allow_html=True
            )

        with s4:

            st.markdown(
                f"""
                <div class="status-card">
                    <div class="status-label">
                        🌀 끌어올리기
                    </div>
                    <div class="status-value">
                        {stats["pull"]:,.1f}
                    </div>
                </div>
                """,
                unsafe_allow_html=True
            )

        st.write("")

        st.markdown(
            """
            <div class="muted">
                ♾️ 내구도: 무한
            </div>
            """,
            unsafe_allow_html=True
        )

        st.markdown(
            '</div>',
            unsafe_allow_html=True
        )

        # 낚시 특성 확률
        st.markdown(
            '<div class="card">',
            unsafe_allow_html=True
        )

        st.markdown(
            "### ✨ 특성 확률"
        )

        event = event_bonus()

        st.write(
            f"🥈 실버  **{8 + event * 100:.1f}%**"
        )

        st.write(
            f"🥇 골드  **{4 + event * 100:.1f}%**"
        )

        st.write(
            f"🌈 무지개  **{2 + event * 100 + get_title_stat('rainbow') * 100:.1f}%**"
        )

        st.write(
            f"🌀 차원  **{0.9 + event * 100 + get_title_stat('dimension') * 100:.1f}%**"
        )

        st.markdown(
            '</div>',
            unsafe_allow_html=True
        )


# ============================================================
# 🎒 인벤토리
# ============================================================

elif st.session_state.page == "인벤토리":

    st.markdown(
        '<div class="card">',
        unsafe_allow_html=True
    )

    st.markdown(
        "## 🎒 물고기 인벤토리"
    )

    st.write(
        f"보관 공간: "
        f"**{len(st.session_state.inventory)} / "
        f"{st.session_state.inventory_capacity}칸**"
    )

    st.markdown(
        '</div>',
        unsafe_allow_html=True
    )

    capacity = (
        st.session_state.inventory_capacity
    )

    columns = 5

    for start in range(
        0,
        capacity,
        columns
    ):

        cols = st.columns(columns)

        for j in range(columns):

            index = start + j

            with cols[j]:

                if index < len(
                    st.session_state.inventory
                ):

                    fish = (
                        st.session_state.inventory[
                            index
                        ]
                    )

                    traits = "일반"

                    if fish["traits"]:

                        traits = " ".join(
                            t["emoji"]
                            for t in fish["traits"]
                        )

                    st.markdown(
                        f"""
                        <div class="inventory-slot">

                            <div class="inventory-icon">
                                {fish["emoji"]}
                            </div>

                            <div class="inventory-name">
                                {traits}
                                {fish["name"]}
                            </div>

                            <div class="muted">
                                {fish["weight"]:.1f} kg
                            </div>

                            <div class="inventory-price">
                                {fmt(fish["price"])}
                            </div>

                        </div>
                        """,
                        unsafe_allow_html=True
                    )

                    if st.button(
                        "💰 판매",
                        key=f"inv_sell_{index}",
                        use_container_width=True
                    ):

                        sell_one(index)

                        st.rerun()

                else:

                    st.markdown(
                        """
                        <div class="inventory-slot">

                            <div class="empty-slot">
                                빈 슬롯
                            </div>

                        </div>
                        """,
                        unsafe_allow_html=True
                    )

    st.write("")

    st.markdown(
        '<div class="card">',
        unsafe_allow_html=True
    )

    st.markdown(
        "### 📦 인벤토리 확장"
    )

    cost = inventory_upgrade_cost()

    st.write(
        f"현재 "
        f"**{st.session_state.inventory_capacity}칸**"
        f" → "
        f"**{st.session_state.inventory_capacity + 5}칸**"
    )

    st.write(
        f"업그레이드 비용: "
        f"**{fmt(cost)}**"
    )

    if st.button(
        "📦 5칸 확장",
        use_container_width=True
    ):

        upgrade_inventory()

        st.rerun()

    st.markdown(
        '</div>',
        unsafe_allow_html=True
    )


# ============================================================
# 🏪 상점
# ============================================================

elif st.session_state.page == "상점":

    st.markdown(
        '<div class="card">',
        unsafe_allow_html=True
    )

    st.markdown(
        "## 🏪 낚싯대 상점"
    )

    st.write(
        f"보유 골드: "
        f"**{fmt(st.session_state.gold)}**"
    )

    st.markdown(
        '</div>',
        unsafe_allow_html=True
    )

    for i, rod in enumerate(RODS):

        cols = st.columns(
            [1, 3, 2, 1.4]
        )

        with cols[0]:

            st.markdown(
                f"""
                <div class="rod-card">
                    <div class="rod-icon">
                        {rod["emoji"]}
                    </div>
                </div>
                """,
                unsafe_allow_html=True
            )

        with cols[1]:

            st.markdown(
                f"""
                <div class="rod-card">

                    <div class="rod-name">
                        {rod["name"]}
                    </div>

                    <div class="rod-grade">
                        {rod["grade"]}
                    </div>

                    <br>

                    💪 힘
                    <b>{rod["power"]:,}</b>

                    &nbsp;

                    🍀 행운
                    <b>{rod["luck"]:,}</b>

                    <br>

                    ⚡ 입질
                    <b>{rod["bite"]:,}</b>

                    &nbsp;

                    🌀 끌어올리기
                    <b>{rod["pull"]:,}</b>

                    <br><br>

                    <div class="muted">
                        ♾️ 내구도 무한
                    </div>

                </div>
                """,
                unsafe_allow_html=True
            )

        with cols[2]:

            if i in st.session_state.owned_rods:

                st.success(
                    f"보유 중"
                )

                if (
                    st.session_state.equipped_rod
                    == i
                ):

                    st.info(
                        "🎣 장착 중"
                    )

                else:

                    if st.button(
                        "🎣 장착",
                        key=f"equip_{i}",
                        use_container_width=True
                    ):

                        st.session_state.equipped_rod = i

                        st.rerun()

            else:

                st.markdown(
                    f"""
                    <div class="shop-price">
                        {fmt(rod["price"])}
                    </div>
                    """,
                    unsafe_allow_html=True
                )

                if st.button(
                    "🛒 구매",
                    key=f"buy_{i}",
                    use_container_width=True
                ):

                    buy_rod(i)

                    st.rerun()

        with cols[3]:

            st.write("")


    # 실패방지권
    st.markdown(
        '<div class="card">',
        unsafe_allow_html=True
    )

    st.markdown(
        "## 🛡️ 강화 실패방지권"
    )

    st.write(
        "강화 실패 시 현재 강화 단계를 유지합니다."
    )

    st.write(
        f"현재 보유: "
        f"**{st.session_state.protection_tickets}장**"
    )

    st.markdown(
        f"""
        <div class="shop-price">
            {fmt(PROTECTION_TICKET_PRICE)}
        </div>
        """,
        unsafe_allow_html=True
    )

    if st.button(
        "🛡️ 실패방지권 구매",
        use_container_width=True
    ):

        buy_protection_ticket()

        st.rerun()

    st.markdown(
        '</div>',
        unsafe_allow_html=True
    )


# ============================================================
# 💰 판매
# ============================================================

elif st.session_state.page == "판매":

    st.markdown(
        '<div class="card">',
        unsafe_allow_html=True
    )

    st.markdown(
        "## 💰 물고기 판매"
    )

    total = sum(
        fish["price"]
        for fish in st.session_state.inventory
    )

    st.write(
        f"현재 판매 가능한 물고기: "
        f"**{len(st.session_state.inventory)}마리**"
    )

    st.markdown(
        f"""
        <div class="big-number">
            💰 {fmt(total)}
        </div>
        """,
        unsafe_allow_html=True
    )

    if st.session_state.inventory:

        if st.button(
            "💰 전부 판매",
            use_container_width=True,
            type="primary"
        ):

            count, value = sell_all()

            st.success(
                f"{count}마리를 판매하여 "
                f"{fmt(value)}를 획득했습니다!"
            )

            st.rerun()

    else:

        st.info(
            "🎒 판매할 물고기가 없습니다."
        )

    st.markdown(
        '</div>',
        unsafe_allow_html=True
    )

    for i, fish in enumerate(
        st.session_state.inventory
    ):

        cols = st.columns(
            [1, 4, 2, 1]
        )

        with cols[0]:

            st.markdown(
                f"""
                <div style="font-size:45px">
                    {fish["emoji"]}
                </div>
                """,
                unsafe_allow_html=True
            )

        with cols[1]:

            traits = "일반"

            if fish["traits"]:

                traits = " ".join(
                    t["emoji"]
                    for t in fish["traits"]
                )

            st.write(
                f"**{traits} {fish['name']}**"
            )

            st.caption(
                f"{fish['grade']} · "
                f"{fish['weight']:.2f}kg · "
                f"{fish['size']:.2f}m"
            )

        with cols[2]:

            st.markdown(
                f"### {fmt(fish['price'])}"
            )

        with cols[3]:

            if st.button(
                "판매",
                key=f"sell_{i}"
            ):

                sell_one(i)

                st.rerun()


# ============================================================
# 🔨 강화
# ============================================================

elif st.session_state.page == "강화":

    rod = current_rod()

    index = st.session_state.equipped_rod

    level = rod_level()

    stats = get_rod_stats(index)

    cost = enhancement_cost(
        level,
        index
    )

    success_rate = (
        enhancement_success_rate(level)
        + get_title_stat("enhance")
    )

    success_rate = min(
        100,
        success_rate
    )

    st.markdown(
        '<div class="card">',
        unsafe_allow_html=True
    )

    st.markdown(
        "## 🔨 낚싯대 강화"
    )

    st.markdown(
        f"""
        <div class="catch-result">

            <div class="catch-icon">
                {rod["emoji"]}
            </div>

            <div class="catch-name">
                {rod["name"]}
            </div>

            <div>
                {rod["grade"]}
            </div>

            <br>

            <div class="big-number">
                +{level}
            </div>

            <br>

            💪 {stats["power"]:,.2f}

            <br>

            🍀 {stats["luck"]:,.2f}

            <br>

            ⚡ {stats["bite"]:,.2f}

            <br>

            🌀 {stats["pull"]:,.2f}

            <br><br>

            ♾️ 내구도 무한

        </div>
        """,
        unsafe_allow_html=True
    )

    st.write("")

    c1, c2, c3, c4 = st.columns(4)

    with c1:

        st.metric(
            "강화",
            f"+{level}"
        )

    with c2:

        st.metric(
            "성공 확률",
            f"{success_rate:.1f}%"
        )

    with c3:

        st.metric(
            "비용",
            fmt(cost)
        )

    with c4:

        st.metric(
            "실패방지권",
            st.session_state.protection_tickets
        )

    st.write("")

    st.info(
        "✨ 강화 성공 시 모든 기본 스탯이 2%씩 증가합니다."
    )

    st.warning(
        "💥 강화 실패 시 +0으로 초기화됩니다."
        " 실패방지권이 있으면 현재 강화 단계가 유지됩니다."
    )

    if st.button(
        f"🔨 강화하기 · {fmt(cost)}",
        use_container_width=True,
        type="primary"
    ):

        enhance_rod()

        st.rerun()

    st.markdown(
        '</div>',
        unsafe_allow_html=True
    )


# ============================================================
# 🏆 타이틀
# ============================================================

elif st.session_state.page == "타이틀":

    st.markdown(
        '<div class="card">',
        unsafe_allow_html=True
    )

    st.markdown(
        "## 🏆 타이틀"
    )

    st.write(
        f"현재 타이틀: "
        f"**{st.session_state.equipped_title}**"
    )

    st.write(
        f"획득 타이틀: "
        f"**{len(st.session_state.titles)} / {len(TITLES)}**"
    )

    st.markdown(
        '</div>',
        unsafe_allow_html=True
    )

    for title in TITLES:

        unlocked = (
            title["name"]
            in st.session_state.titles
        )

        st.markdown(
            f"""
            <div class="title-card">

                <div class="title-name">
                    {"🏆" if unlocked else "🔒"}
                    {title["name"]}
                </div>

                <div class="title-condition">
                    조건: {title["condition"]}
                </div>

                <div class="title-effect">
                    ✨ 효과: {title["effect"]}
                </div>

            </div>
            """,
            unsafe_allow_html=True
        )

        if unlocked:

            if (
                st.session_state.equipped_title
                == title["name"]
            ):

                st.success(
                    "현재 장착 중"
                )

            else:

                if st.button(
                    "🏆 타이틀 장착",
                    key=f"title_{title['name']}",
                    use_container_width=True
                ):

                    st.session_state.equipped_title = (
                        title["name"]
                    )

                    st.success(
                        f"{title['name']} 장착!"
                    )

                    st.rerun()


# ============================================================
# 📖 도감
# ============================================================

elif st.session_state.page == "도감":

    st.markdown(
        '<div class="card">',
        unsafe_allow_html=True
    )

    st.markdown(
        "## 📖 물고기 도감"
    )

    discovered = len(
        st.session_state.discovered
    )

    st.progress(
        discovered / 80
    )

    st.write(
        f"발견: **{discovered} / 80**"
    )

    st.markdown(
        '</div>',
        unsafe_allow_html=True
    )

    selected_grade = st.selectbox(
        "등급 필터",
        [
            "전체",
            "일반",
            "희귀",
            "영웅",
            "전설",
            "신화"
        ]
    )

    filtered = FISH

    if selected_grade != "전체":

        filtered = [
            fish
            for fish in FISH
            if fish["grade"]
            == selected_grade
        ]

    cols = st.columns(4)

    for i, fish in enumerate(
        filtered
    ):

        with cols[i % 4]:

            if fish["id"] in st.session_state.discovered:

                st.markdown(
                    f"""
                    <div class="fish-card">

                        <div class="fish-icon">
                            {fish["emoji"]}
                        </div>

                        <div class="fish-name">
                            {fish["name"]}
                        </div>

                        <div class="fish-detail">

                            등급:
                            <b>{fish["grade"]}</b>

                            <br>

                            기본 가격:
                            {fmt(fish["base_price"])}

                            <br>

                            무게:
                            {fish["min_weight"]:.1f}
                            ~
                            {fish["max_weight"]:.1f} kg

                            <br>

                            크기:
                            {fish["min_size"]:.2f}
                            ~
                            {fish["max_size"]:.2f} m

                        </div>

                    </div>
                    """,
                    unsafe_allow_html=True
                )

            else:

                st.markdown(
                    """
                    <div class="fish-card">

                        <div class="fish-icon">
                            ❓
                        </div>

                        <div class="fish-name">
                            미발견
                        </div>

                        <div class="fish-detail">
                            아직 이 물고기를
                            낚지 못했습니다.
                        </div>

                    </div>
                    """,
                    unsafe_allow_html=True
                )


# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:

    st.markdown(
        "## 🎣 Fishing Legends"
    )

    st.divider()

    rod = current_rod()

    st.markdown(
        f"""
        ### {rod["emoji"]} {rod["name"]}

        **강화 +{rod_level()}**

        ♾️ 내구도 무한
        """
    )

    stats = get_rod_stats(
        st.session_state.equipped_rod
    )

    st.write(
        f"💪 힘: {stats['power']:,.1f}"
    )

    st.write(
        f"🍀 행운: {stats['luck']:,.1f}"
    )

    st.write(
        f"⚡ 입질: {stats['bite']:,.1f}"
    )

    st.write(
        f"🌀 끌어올리기: {stats['pull']:,.1f}"
    )

    st.divider()

    st.markdown(
        "### 🏆 타이틀"
    )

    st.write(
        st.session_state.equipped_title
    )

    st.divider()

    st.markdown(
        "### ✨ 특성"

    )

    st.write(
        "🥈 실버 · +10%"
    )

    st.write(
        "🥇 골드 · +20%"
    )

    st.write(
        "🌈 무지개 · +50%"
    )

    st.write(
        "🌀 차원 · +100%"
    )

    st.divider()

    st.markdown(
        "### 📊 기록"
    )

    st.write(
        f"🐟 낚은 물고기: "
        f"{st.session_state.total_catches:,}"
    )

    st.write(
        f"🏆 발견한 종류: "
        f"{len(st.session_state.discovered)}/80"
    )

    st.write(
        f"⚖️ 최대 무게: "
        f"{st.session_state.max_weight:.2f}kg"
    )

    st.write(
        f"💰 총 판매액: "
        f"{fmt(st.session_state.total_sold)}"
    )

    st.divider()

    if st.button(
        "🔄 게임 초기화",
        use_container_width=True
    ):

        initialize_game()

        st.rerun()
