import streamlit as st
import random
import math
import time

# ============================================================
# 🎣 FISHING RPG - STREAMLIT
# ============================================================

st.set_page_config(
    page_title="🎣 낚시왕",
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

html, body, [class*="css"] {
    font-family: 'Noto Sans KR', sans-serif;
}

.stApp {
    background:
        radial-gradient(circle at 20% 10%, rgba(35,130,255,0.14), transparent 28%),
        radial-gradient(circle at 80% 20%, rgba(0,210,255,0.10), transparent 30%),
        linear-gradient(135deg, #07111f 0%, #0b1830 45%, #07101e 100%);
    color: white;
}

.block-container {
    padding-top: 1rem;
    padding-bottom: 3rem;
    max-width: 1500px;
}

.main-title {
    font-size: 42px;
    font-weight: 900;
    letter-spacing: -2px;
    margin-bottom: 0;
}

.subtitle {
    color: #91a7c3;
    font-size: 15px;
    margin-top: -5px;
}

.top-stat {
    background: rgba(16,31,53,0.82);
    border: 1px solid rgba(110,160,220,0.22);
    border-radius: 16px;
    padding: 14px 18px;
    text-align: center;
    box-shadow: 0 10px 35px rgba(0,0,0,0.2);
}

.top-stat-title {
    color: #8da4c2;
    font-size: 12px;
}

.top-stat-value {
    font-size: 21px;
    font-weight: 800;
}

.game-card {
    background: rgba(12,28,48,0.86);
    border: 1px solid rgba(95,145,205,0.22);
    border-radius: 22px;
    padding: 22px;
    margin-bottom: 18px;
    box-shadow: 0 14px 45px rgba(0,0,0,0.25);
}

.water {
    min-height: 390px;
    border-radius: 22px;
    position: relative;
    overflow: hidden;
    background:
        radial-gradient(circle at 50% 20%, rgba(82,210,255,0.20), transparent 30%),
        linear-gradient(180deg, #0c6c91 0%, #07517a 45%, #06395e 100%);
    border: 1px solid rgba(100,220,255,0.28);
}

.water:before,
.water:after {
    content: "";
    position: absolute;
    left: -10%;
    width: 120%;
    height: 80px;
    border-radius: 50%;
    border-top: 2px solid rgba(180,245,255,0.16);
}

.water:before {
    top: 35%;
    transform: rotate(-2deg);
}

.water:after {
    top: 60%;
    transform: rotate(2deg);
}

.water-title {
    position: relative;
    z-index: 2;
    text-align: center;
    padding-top: 25px;
    font-size: 27px;
    font-weight: 900;
}

.fishing-rod {
    position: relative;
    z-index: 3;
    text-align: center;
    font-size: 85px;
    margin-top: 55px;
    transform: rotate(-12deg);
    filter: drop-shadow(0 12px 15px rgba(0,0,0,0.3));
}

.fishing-status {
    position: relative;
    z-index: 3;
    text-align: center;
    font-size: 17px;
    font-weight: 700;
    margin-top: 25px;
}

.stat-box {
    background: rgba(6,16,29,0.72);
    border-radius: 15px;
    border: 1px solid rgba(100,160,220,0.18);
    padding: 13px;
    margin-bottom: 8px;
}

.stat-name {
    color: #8da7c5;
    font-size: 12px;
}

.stat-number {
    font-size: 20px;
    font-weight: 800;
}

.rod-card {
    background: rgba(9,22,38,0.92);
    border: 1px solid rgba(105,160,220,0.20);
    border-radius: 18px;
    padding: 18px;
    margin-bottom: 13px;
}

.rod-name {
    font-size: 20px;
    font-weight: 900;
}

.rod-grade {
    font-size: 12px;
    font-weight: 700;
    color: #94b9e8;
}

.fish-card {
    background: rgba(8,22,37,0.90);
    border: 1px solid rgba(95,155,215,0.18);
    border-radius: 17px;
    padding: 16px;
    min-height: 170px;
    margin-bottom: 12px;
}

.fish-icon {
    font-size: 42px;
}

.fish-name {
    font-size: 18px;
    font-weight: 900;
}

.fish-info {
    color: #9eb1c9;
    font-size: 13px;
    line-height: 1.7;
}

.catch-card {
    text-align: center;
    background:
        radial-gradient(circle at center, rgba(45,160,255,0.18), transparent 55%),
        rgba(8,22,40,0.95);
    border: 1px solid rgba(100,190,255,0.32);
    border-radius: 25px;
    padding: 35px;
    box-shadow: 0 0 60px rgba(20,140,255,0.15);
}

.catch-icon {
    font-size: 90px;
}

.catch-name {
    font-size: 32px;
    font-weight: 900;
}

.catch-special {
    font-size: 19px;
    font-weight: 800;
    margin: 12px 0;
}

.event-card {
    background: linear-gradient(
        135deg,
        rgba(130,80,255,0.18),
        rgba(20,160,255,0.12)
    );
    border: 1px solid rgba(150,120,255,0.38);
    border-radius: 20px;
    padding: 20px;
    text-align: center;
    margin-bottom: 18px;
}

.event-title {
    font-size: 24px;
    font-weight: 900;
}

.event-desc {
    color: #b7c8dd;
}

.inventory-slot {
    background: rgba(5,15,27,0.82);
    border: 1px solid rgba(110,160,220,0.20);
    border-radius: 14px;
    padding: 12px;
    min-height: 125px;
    text-align: center;
    margin-bottom: 10px;
}

.inventory-empty {
    color: #52677f;
    font-size: 13px;
    padding-top: 30px;
}

.inventory-fish {
    font-size: 35px;
}

.inventory-name {
    font-weight: 800;
    font-size: 13px;
}

.inventory-price {
    color: #ffd66b;
    font-size: 12px;
}

div.stButton > button {
    border-radius: 12px;
    border: 1px solid rgba(120,180,240,0.25);
    font-weight: 800;
    min-height: 45px;
}

div.stButton > button:hover {
    border-color: rgba(120,210,255,0.65);
    transform: translateY(-1px);
}

.small-muted {
    color: #8095ad;
    font-size: 12px;
}

.big-number {
    font-size: 30px;
    font-weight: 900;
}

</style>
""", unsafe_allow_html=True)


# ============================================================
# 낚싯대 데이터
# ============================================================

RODS = [
    {
        "name": "나뭇가지 낚싯대",
        "emoji": "🪵",
        "grade": "일반",
        "power": 5,
        "luck": 1,
        "bite": 1,
        "pull": 5,
        "price": 0,
        "description": "처음 낚시를 시작하는 사람이 사용하는 낚싯대."
    },
    {
        "name": "초보자 낚싯대",
        "emoji": "🎣",
        "grade": "일반",
        "power": 10,
        "luck": 3,
        "bite": 3,
        "pull": 10,
        "price": 100,
        "description": "기본적인 성능을 가진 입문용 낚싯대."
    },
    {
        "name": "대나무 낚싯대",
        "emoji": "🎋",
        "grade": "일반",
        "power": 15,
        "luck": 5,
        "bite": 5,
        "pull": 15,
        "price": 250,
        "description": "가볍고 부드러운 대나무 낚싯대."
    },
    {
        "name": "철제 낚싯대",
        "emoji": "🛠️",
        "grade": "고급",
        "power": 25,
        "luck": 8,
        "bite": 8,
        "pull": 25,
        "price": 500,
        "description": "철로 만들어져 강한 물고기도 상대할 수 있다."
    },
    {
        "name": "강철 낚싯대",
        "emoji": "⚙️",
        "grade": "고급",
        "power": 35,
        "luck": 12,
        "bite": 12,
        "pull": 35,
        "price": 1000,
        "description": "강철 합금으로 제작된 튼튼한 낚싯대."
    },
    {
        "name": "은빛 낚싯대",
        "emoji": "🥈",
        "grade": "희귀",
        "power": 50,
        "luck": 18,
        "bite": 18,
        "pull": 50,
        "price": 2500,
        "description": "은빛으로 빛나는 행운의 낚싯대."
    },
    {
        "name": "황금 낚싯대",
        "emoji": "🥇",
        "grade": "희귀",
        "power": 70,
        "luck": 25,
        "bite": 25,
        "pull": 70,
        "price": 5000,
        "description": "황금으로 장식된 고급 낚싯대."
    },
    {
        "name": "수정 낚싯대",
        "emoji": "💎",
        "grade": "희귀",
        "power": 90,
        "luck": 35,
        "bite": 32,
        "pull": 90,
        "price": 10000,
        "description": "투명한 수정이 빛나는 신비로운 낚싯대."
    },
    {
        "name": "사파이어 낚싯대",
        "emoji": "🔷",
        "grade": "영웅",
        "power": 120,
        "luck": 45,
        "bite": 40,
        "pull": 120,
        "price": 20000,
        "description": "푸른 사파이어의 힘이 깃든 낚싯대."
    },
    {
        "name": "루비 낚싯대",
        "emoji": "🔶",
        "grade": "영웅",
        "power": 150,
        "luck": 60,
        "bite": 50,
        "pull": 150,
        "price": 40000,
        "description": "붉은 루비 장식이 빛나는 강력한 낚싯대."
    },
    {
        "name": "다이아몬드 낚싯대",
        "emoji": "💠",
        "grade": "영웅",
        "power": 200,
        "luck": 80,
        "bite": 65,
        "pull": 200,
        "price": 80000,
        "description": "다이아몬드로 장식된 최고급 낚싯대."
    },
    {
        "name": "별빛 낚싯대",
        "emoji": "🌌",
        "grade": "전설",
        "power": 270,
        "luck": 110,
        "bite": 85,
        "pull": 270,
        "price": 150000,
        "description": "밤하늘의 별빛을 담은 전설의 낚싯대."
    },
    {
        "name": "달빛 낚싯대",
        "emoji": "🌙",
        "grade": "전설",
        "power": 350,
        "luck": 150,
        "bite": 110,
        "pull": 350,
        "price": 300000,
        "description": "달의 힘으로 희귀한 물고기를 유혹한다."
    },
    {
        "name": "태양 낚싯대",
        "emoji": "☀️",
        "grade": "전설",
        "power": 450,
        "luck": 200,
        "bite": 140,
        "pull": 450,
        "price": 600000,
        "description": "태양처럼 강렬한 힘을 가진 낚싯대."
    },
    {
        "name": "해신의 낚싯대",
        "emoji": "🌊",
        "grade": "신화",
        "power": 600,
        "luck": 280,
        "bite": 180,
        "pull": 600,
        "price": 1200000,
        "description": "바다의 신이 사용했다고 전해지는 낚싯대."
    },
    {
        "name": "번개의 낚싯대",
        "emoji": "⚡",
        "grade": "신화",
        "power": 800,
        "luck": 380,
        "bite": 250,
        "pull": 800,
        "price": 2500000,
        "description": "번개의 힘으로 입질을 빠르게 만든다."
    },
    {
        "name": "용의 낚싯대",
        "emoji": "🔥",
        "grade": "신화",
        "power": 1100,
        "luck": 500,
        "bite": 330,
        "pull": 1100,
        "price": 5000000,
        "description": "고대 용의 힘이 깃든 전설적인 낚싯대."
    },
    {
        "name": "은하 낚싯대",
        "emoji": "🌠",
        "grade": "신화",
        "power": 1500,
        "luck": 700,
        "bite": 450,
        "pull": 1500,
        "price": 10000000,
        "description": "은하의 에너지를 담은 초고급 낚싯대."
    },
    {
        "name": "차원의 낚싯대",
        "emoji": "🌀",
        "grade": "초월",
        "power": 2000,
        "luck": 1000,
        "bite": 600,
        "pull": 2000,
        "price": 50000000,
        "description": "공간과 차원을 뒤틀어 다른 세계의 물고기를 끌어낸다."
    },
    {
        "name": "신의 낚싯대",
        "emoji": "👑",
        "grade": "초월",
        "power": 3000,
        "luck": 1500,
        "bite": 1000,
        "pull": 3000,
        "price": 250000000,
        "description": "낚시의 끝에 도달한 자만 사용할 수 있는 전설의 낚싯대."
    }
]


# ============================================================
# 물고기 80종
# ============================================================

fish_groups = [
    (
        "일반",
        [
            "피라미", "송사리", "붕어", "잉어", "은어",
            "전어", "고등어", "멸치", "정어리", "꽁치",
            "청어", "숭어", "갈치", "가자미", "도미",
            "농어", "우럭", "망둥어", "쥐치", "보리멸"
        ],
        80,
        2.0,
        15.0
    ),
    (
        "희귀",
        [
            "참돔", "광어", "쏘가리", "메기", "장어",
            "송어", "연어", "방어", "삼치", "복어",
            "민어", "감성돔", "벵에돔", "전갱이", "가자미왕",
            "황어", "빙어", "철갑상어", "가물치", "대구"
        ],
        250,
        5.0,
        35.0
    ),
    (
        "영웅",
        [
            "대왕잉어", "대형연어", "황금송어", "황금도미",
            "청새치", "참치", "다랑어", "대왕오징어", "대왕문어",
            "전기뱀장어", "대형농어", "거대메기", "왕연어",
            "거대복어", "흑참치"
        ],
        1000,
        15.0,
        100.0
    ),
    (
        "전설",
        [
            "황금잉어", "황금참치", "심해아귀", "거대상어",
            "백상아리", "범고래", "거대가오리", "심해용",
            "대왕참치", "고대상어", "빙하상어", "폭풍참치",
            "심해문어", "고대철갑상어", "유령고래"
        ],
        5000,
        30.0,
        300.0
    ),
    (
        "신화",
        [
            "해룡", "크라켄", "고대고래", "신비한 황금고래",
            "차원의 물고기", "천공의 용어", "심연의 상어",
            "시간의 물고기", "우주의 고래", "창조의 물고기"
        ],
        30000,
        80.0,
        1000.0
    )
]


FISH = []

fish_emojis = ["🐟", "🐠", "🐡", "🦈", "🐋", "🐙", "🦑", "🐬"]

for grade, names, base_price, min_weight, max_weight in fish_groups:
    for index, name in enumerate(names):
        FISH.append({
            "id": len(FISH),
            "name": name,
            "grade": grade,
            "base_price": base_price + index * max(1, base_price * 0.08),
            "min_weight": min_weight,
            "max_weight": max_weight,
            "emoji": fish_emojis[len(FISH) % len(fish_emojis)]
        })


# ============================================================
# 게임 초기화
# ============================================================

def initialize_game():

    st.session_state.gold = 1000

    st.session_state.inventory = []

    st.session_state.inventory_capacity = 10

    st.session_state.owned_rods = [0]

    st.session_state.equipped_rod = 0

    st.session_state.rod_levels = {
        0: 0
    }

    st.session_state.discovered = set()

    st.session_state.total_catches = 0

    st.session_state.page = "낚시"

    st.session_state.event_active = False

    st.session_state.event_end = 0

    st.session_state.event_id = 0

    st.session_state.last_catch = None

    st.session_state.fishing = False


if "gold" not in st.session_state:
    initialize_game()


# ============================================================
# 유틸
# ============================================================

def format_gold(value):
    return f"{int(value):,} G"


def get_rod_level(rod_index):
    return st.session_state.rod_levels.get(rod_index, 0)


def get_rod_stats(rod_index):

    rod = RODS[rod_index]
    level = get_rod_level(rod_index)

    multiplier = 1.02 ** level

    return {
        "power": rod["power"] * multiplier,
        "luck": rod["luck"] * multiplier,
        "bite": rod["bite"] * multiplier,
        "pull": rod["pull"] * multiplier
    }


def enhancement_success_rate(level):
    return max(1, 100 - level)


def enhancement_cost(level, rod_index):

    base = RODS[rod_index]["price"]

    if base <= 0:
        base = 100

    return int(
        max(
            100,
            base * (1.18 ** level)
        )
    )


def get_trait():

    event_bonus = 5 if st.session_state.event_active else 0

    traits = []

    if random.random() < (0.08 + event_bonus / 100):
        traits.append({
            "name": "실버",
            "emoji": "🥈",
            "bonus": 0.10
        })

    if random.random() < (0.04 + event_bonus / 100):
        traits.append({
            "name": "골드",
            "emoji": "🥇",
            "bonus": 0.20
        })

    if random.random() < (0.02 + event_bonus / 100):
        traits.append({
            "name": "무지개",
            "emoji": "🌈",
            "bonus": 0.50
        })

    if random.random() < (0.009 + event_bonus / 100):
        traits.append({
            "name": "차원",
            "emoji": "🌀",
            "bonus": 1.00
        })

    return traits


def catch_fish():

    if len(st.session_state.inventory) >= st.session_state.inventory_capacity:
        st.error("🎒 인벤토리가 가득 찼습니다!")
        return

    rod_stats = get_rod_stats(st.session_state.equipped_rod)

    # 행운이 높을수록 상위 등급 가중치 상승
    luck = rod_stats["luck"]

    weights = {
        "일반": max(20, 1000 - luck * 1.2),
        "희귀": 150 + luck * 0.35,
        "영웅": 35 + luck * 0.10,
        "전설": 8 + luck * 0.035,
        "신화": 1 + luck * 0.008
    }

    selected_grade = random.choices(
        list(weights.keys()),
        weights=list(weights.values()),
        k=1
    )[0]

    candidates = [
        fish for fish in FISH
        if fish["grade"] == selected_grade
    ]

    fish = random.choice(candidates)

    weight = random.uniform(
        fish["min_weight"],
        fish["max_weight"]
    )

    # 무게 기반 크기
    size = max(
        0.15,
        (weight ** (1 / 3)) * random.uniform(0.65, 1.15)
    )

    # 크기와 무게 보정
    average_weight = (
        fish["min_weight"] +
        fish["max_weight"]
    ) / 2

    weight_multiplier = max(
        0.25,
        weight / average_weight
    )

    size_multiplier = max(
        0.5,
        size / 1.0
    )

    traits = get_trait()

    trait_multiplier = 1.0

    for trait in traits:
        trait_multiplier *= 1 + trait["bonus"]

    base_price = fish["base_price"]

    price = (
        base_price
        * weight_multiplier
        * size_multiplier
        * trait_multiplier
    )

    # 낚싯대 행운에 따른 소폭 가격 보너스
    luck_bonus = 1 + min(0.5, luck / 5000)

    price *= luck_bonus

    caught = {
        "fish_id": fish["id"],
        "name": fish["name"],
        "grade": fish["grade"],
        "emoji": fish["emoji"],
        "weight": weight,
        "size": size,
        "traits": traits,
        "price": int(price),
        "base_price": int(base_price)
    }

    st.session_state.inventory.append(caught)
    st.session_state.discovered.add(fish["id"])
    st.session_state.total_catches += 1
    st.session_state.last_catch = caught


def sell_fish(index):

    if index < 0 or index >= len(st.session_state.inventory):
        return

    fish = st.session_state.inventory.pop(index)

    st.session_state.gold += fish["price"]


def sell_all():

    if not st.session_state.inventory:
        return 0

    total = sum(
        fish["price"]
        for fish in st.session_state.inventory
    )

    st.session_state.gold += total

    count = len(st.session_state.inventory)

    st.session_state.inventory = []

    return count


def buy_rod(index):

    rod = RODS[index]

    if index in st.session_state.owned_rods:
        return

    if st.session_state.gold < rod["price"]:
        st.error("💰 골드가 부족합니다.")
        return

    st.session_state.gold -= rod["price"]

    st.session_state.owned_rods.append(index)

    st.session_state.rod_levels[index] = 0

    st.success(f"{rod['emoji']} {rod['name']} 구매 완료!")


def enhance_rod():

    index = st.session_state.equipped_rod

    level = get_rod_level(index)

    cost = enhancement_cost(level, index)

    if st.session_state.gold < cost:
        st.error("💰 골드가 부족합니다.")
        return

    st.session_state.gold -= cost

    rate = enhancement_success_rate(level)

    success = random.random() * 100 < rate

    if success:

        st.session_state.rod_levels[index] = level + 1

        st.success(
            f"✨ 강화 성공! +{level + 1}"
        )

    else:

        st.session_state.rod_levels[index] = 0

        st.error(
            f"💥 강화 실패! +{level} → +0"
        )

    st.rerun()


def upgrade_inventory():

    current = st.session_state.inventory_capacity

    # 업그레이드 가격
    upgrade_number = (current - 10) // 5

    cost = int(
        500 * (1.55 ** upgrade_number)
    )

    if st.session_state.gold < cost:
        st.error("💰 골드가 부족합니다.")
        return

    st.session_state.gold -= cost

    st.session_state.inventory_capacity += 5

    st.success(
        f"🎒 인벤토리가 {st.session_state.inventory_capacity}칸이 되었습니다!"
    )

    st.rerun()


def inventory_upgrade_cost():

    current = st.session_state.inventory_capacity

    upgrade_number = (current - 10) // 5

    return int(
        500 * (1.55 ** upgrade_number)
    )


def maybe_event():

    now = time.time()

    if st.session_state.event_active:

        if now >= st.session_state.event_end:
            st.session_state.event_active = False
            st.session_state.event_end = 0

    else:

        # 낚시할 때마다 낮은 확률로 이벤트 시작
        if random.random() < 0.025:

            st.session_state.event_active = True

            duration = random.randint(60, 180)

            st.session_state.event_end = now + duration

            st.session_state.event_id += 1


def event_remaining():

    if not st.session_state.event_active:
        return 0

    return max(
        0,
        int(st.session_state.event_end - time.time())
    )


# ============================================================
# 이벤트 체크
# ============================================================

maybe_event()


# ============================================================
# 상단 UI
# ============================================================

st.markdown(
    '<div class="main-title">🎣 낚시왕</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">최고의 낚싯대를 만들고 80종의 물고기를 모두 수집하세요.</div>',
    unsafe_allow_html=True
)

st.write("")

top1, top2, top3, top4, top5 = st.columns(5)

with top1:
    st.markdown(
        f"""
        <div class="top-stat">
            <div class="top-stat-title">💰 보유 골드</div>
            <div class="top-stat-value">{format_gold(st.session_state.gold)}</div>
        </div>
        """,
        unsafe_allow_html=True
    )

with top2:
    st.markdown(
        f"""
        <div class="top-stat">
            <div class="top-stat-title">🎒 인벤토리</div>
            <div class="top-stat-value">
            {len(st.session_state.inventory)} / {st.session_state.inventory_capacity}
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

with top3:
    st.markdown(
        f"""
        <div class="top-stat">
            <div class="top-stat-title">🐟 도감</div>
            <div class="top-stat-value">
            {len(st.session_state.discovered)} / 80
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

with top4:
    st.markdown(
        f"""
        <div class="top-stat">
            <div class="top-stat-title">🎣 총 낚은 수</div>
            <div class="top-stat-value">
            {st.session_state.total_catches:,}
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

with top5:
    rod = RODS[st.session_state.equipped_rod]
    level = get_rod_level(st.session_state.equipped_rod)

    st.markdown(
        f"""
        <div class="top-stat">
            <div class="top-stat-title">현재 낚싯대</div>
            <div class="top-stat-value">
            {rod["emoji"]} +{level}
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )


# ============================================================
# 이벤트 UI
# ============================================================

if st.session_state.event_active:

    remain = event_remaining()

    minutes = remain // 60
    seconds = remain % 60

    st.markdown(
        f"""
        <div class="event-card">
            <div class="event-title">🌟 특성 확률 UP 이벤트!</div>
            <div class="event-desc">
                지금 잡는 물고기의 특성 확률이 각각 <b>+5%p</b> 증가합니다.
                <br>
                🥈 실버 13% · 🥇 골드 9% · 🌈 무지개 7% · 🌀 차원 5.9%
                <br><br>
                ⏱️ 남은 시간: <b>{minutes:02d}:{seconds:02d}</b>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )


# ============================================================
# 메뉴
# ============================================================

menu1, menu2, menu3, menu4, menu5, menu6 = st.columns(6)

with menu1:
    if st.button("🎣 낚시", use_container_width=True):
        st.session_state.page = "낚시"
        st.rerun()

with menu2:
    if st.button("🎒 인벤토리", use_container_width=True):
        st.session_state.page = "인벤토리"
        st.rerun()

with menu3:
    if st.button("🏪 상점", use_container_width=True):
        st.session_state.page = "상점"
        st.rerun()

with menu4:
    if st.button("💰 판매", use_container_width=True):
        st.session_state.page = "판매"
        st.rerun()

with menu5:
    if st.button("🔨 강화", use_container_width=True):
        st.session_state.page = "강화"
        st.rerun()

with menu6:
    if st.button("📖 도감", use_container_width=True):
        st.session_state.page = "도감"
        st.rerun()


st.write("")


# ============================================================
# 낚시 페이지
# ============================================================

if st.session_state.page == "낚시":

    left, right = st.columns([2.2, 1])

    with left:

        st.markdown(
            """
            <div class="game-card">
                <div class="water">
                    <div class="water-title">🌊 푸른 바다 낚시터</div>
                    <div class="fishing-rod">🎣</div>
                    <div class="fishing-status">
                        깊은 바다에서 물고기를 기다리고 있습니다...
                    </div>
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

        if len(st.session_state.inventory) >= st.session_state.inventory_capacity:

            st.error(
                "🎒 인벤토리가 가득 찼습니다. 물고기를 판매하거나 인벤토리를 확장하세요."
            )

        else:

            if st.button(
                "🎣 낚시하기",
                use_container_width=True,
                type="primary"
            ):

                maybe_event()

                rod_stats = get_rod_stats(
                    st.session_state.equipped_rod
                )

                # 입질 속도가 높을수록 실제 대기시간 감소
                bite_time = max(
                    0.3,
                    2.8 / (1 + rod_stats["bite"] / 100)
                )

                with st.spinner(
                    f"🌊 물고기가 미끼를 물 때까지 기다리는 중... ({bite_time:.1f}초)"
                ):
                    time.sleep(
                        min(
                            2.5,
                            bite_time
                        )
                    )

                # 끌어올리기 판정
                pull_power = rod_stats["pull"]

                fish_result = random.random()

                required = random.uniform(
                    0.2,
                    0.8
                )

                if pull_power / (
                    pull_power + 100
                ) >= required * 0.55:

                    catch_fish()

                    maybe_event()

                    st.rerun()

                else:

                    st.warning(
                        "💦 물고기가 도망갔습니다! 더 강한 낚싯대가 필요할지도 몰라요."
                    )

        # 최근 획득
        if st.session_state.last_catch:

            fish = st.session_state.last_catch

            trait_text = "일반"

            if fish["traits"]:
                trait_text = " ".join(
                    f'{t["emoji"]} {t["name"]}'
                    for t in fish["traits"]
                )

            st.markdown(
                f"""
                <div class="catch-card">
                    <div class="catch-icon">{fish["emoji"]}</div>
                    <div class="catch-name">{fish["name"]}</div>
                    <div>{fish["grade"]}</div>
                    <div class="catch-special">{trait_text}</div>
                    <br>
                    📏 크기: <b>{fish["size"]:.2f} m</b>
                    &nbsp;&nbsp;
                    ⚖️ 무게: <b>{fish["weight"]:.2f} kg</b>
                    <br><br>
                    💰 예상 판매가격:
                    <b>{format_gold(fish["price"])}</b>
                </div>
                """,
                unsafe_allow_html=True
            )

    with right:

        rod_index = st.session_state.equipped_rod
        rod = RODS[rod_index]
        stats = get_rod_stats(rod_index)
        level = get_rod_level(rod_index)

        st.markdown(
            '<div class="game-card">',
            unsafe_allow_html=True
        )

        st.markdown(
            f"""
            <h2>
                {rod["emoji"]} {rod["name"]}
            </h2>
            <div class="small-muted">
                {rod["grade"]} · 강화 +{level}
            </div>
            """,
            unsafe_allow_html=True
        )

        st.write("")

        st.markdown(
            f"""
            <div class="stat-box">
                <div class="stat-name">💪 낚시 힘</div>
                <div class="stat-number">{stats["power"]:,.1f}</div>
            </div>

            <div class="stat-box">
                <div class="stat-name">🍀 행운</div>
                <div class="stat-number">{stats["luck"]:,.1f}</div>
            </div>

            <div class="stat-box">
                <div class="stat-name">⚡ 입질 속도</div>
                <div class="stat-number">{stats["bite"]:,.1f}</div>
            </div>

            <div class="stat-box">
                <div class="stat-name">🌀 끌어올리기</div>
                <div class="stat-number">{stats["pull"]:,.1f}</div>
            </div>

            <br>

            <div class="small-muted">
                ♾️ 내구도: 무한
            </div>
            """,
            unsafe_allow_html=True
        )

        st.markdown("</div>", unsafe_allow_html=True)

        st.info(
            "💡 낚싯대의 행운이 높을수록 높은 등급의 물고기를 만날 확률이 증가합니다."
        )


# ============================================================
# 인벤토리
# ============================================================

elif st.session_state.page == "인벤토리":

    st.markdown(
        '<div class="game-card"><h2>🎒 물고기 인벤토리</h2>',
        unsafe_allow_html=True
    )

    st.write(
        f"보관 공간: **{len(st.session_state.inventory)} / {st.session_state.inventory_capacity}칸**"
    )

    columns = 5

    for start in range(
        0,
        st.session_state.inventory_capacity,
        columns
    ):

        cols = st.columns(columns)

        for j in range(columns):

            index = start + j

            with cols[j]:

                if index < len(st.session_state.inventory):

                    fish = st.session_state.inventory[index]

                    trait_text = "일반"

                    if fish["traits"]:
                        trait_text = " ".join(
                            t["emoji"]
                            for t in fish["traits"]
                        )

                    st.markdown(
                        f"""
                        <div class="inventory-slot">
                            <div class="inventory-fish">{fish["emoji"]}</div>
                            <div class="inventory-name">
                                {trait_text} {fish["name"]}
                            </div>
                            <div class="small-muted">
                                {fish["weight"]:.1f} kg
                            </div>
                            <div class="inventory-price">
                                {format_gold(fish["price"])}
                            </div>
                        </div>
                        """,
                        unsafe_allow_html=True
                    )

                    if st.button(
                        "💰 판매",
                        key=f"inventory_sell_{index}",
                        use_container_width=True
                    ):

                        sell_fish(index)

                        st.rerun()

                else:

                    st.markdown(
                        """
                        <div class="inventory-slot">
                            <div class="inventory-empty">
                                빈 슬롯
                            </div>
                        </div>
                        """,
                        unsafe_allow_html=True
                    )

    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown(
        '<div class="game-card"><h2>📦 인벤토리 확장</h2>',
        unsafe_allow_html=True
    )

    cost = inventory_upgrade_cost()

    st.write(
        f"현재 **{st.session_state.inventory_capacity}칸** → "
        f"업그레이드 후 **{st.session_state.inventory_capacity + 5}칸**"
    )

    st.write(
        f"💰 업그레이드 비용: **{format_gold(cost)}**"
    )

    if st.button(
        "📦 5칸 확장하기",
        use_container_width=True
    ):

        upgrade_inventory()

    st.markdown("</div>", unsafe_allow_html=True)


# ============================================================
# 상점
# ============================================================

elif st.session_state.page == "상점":

    st.markdown(
        '<div class="game-card"><h2>🏪 낚싯대 상점</h2>',
        unsafe_allow_html=True
    )

    st.write(
        f"💰 보유 골드: **{format_gold(st.session_state.gold)}**"
    )

    st.markdown("</div>", unsafe_allow_html=True)

    for index, rod in enumerate(RODS):

        stats = get_rod_stats(index) if index in st.session_state.owned_rods else {
            "power": rod["power"],
            "luck": rod["luck"],
            "bite": rod["bite"],
            "pull": rod["pull"]
        }

        cols = st.columns([1.5, 3, 2, 1.5])

        with cols[0]:

            st.markdown(
                f"""
                <div class="rod-card">
                    <div style="font-size:50px;text-align:center;">
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

                    💪 {rod["power"]:,}
                    &nbsp; 🍀 {rod["luck"]:,}
                    <br>
                    ⚡ {rod["bite"]:,}
                    &nbsp; 🌀 {rod["pull"]:,}

                    <br><br>

                    <div class="small-muted">
                        {rod["description"]}
                    </div>
                </div>
                """,
                unsafe_allow_html=True
            )

        with cols[2]:

            if index in st.session_state.owned_rods:

                current_level = get_rod_level(index)

                st.success(
                    f"보유 중 · +{current_level}"
                )

                if st.session_state.equipped_rod == index:

                    st.info("현재 장착")

                else:

                    if st.button(
                        "🎣 장착",
                        key=f"equip_{index}",
                        use_container_width=True
                    ):

                        st.session_state.equipped_rod = index

                        st.rerun()

            else:

                st.write(
                    f"💰 **{format_gold(rod['price'])}**"
                )

                if st.button(
                    "🛒 구매",
                    key=f"buy_{index}",
                    use_container_width=True
                ):

                    buy_rod(index)

                    st.rerun()

        with cols[3]:

            st.write("")


# ============================================================
# 판매
# ============================================================

elif st.session_state.page == "판매":

    st.markdown(
        '<div class="game-card"><h2>💰 물고기 판매</h2>',
        unsafe_allow_html=True
    )

    total_value = sum(
        fish["price"]
        for fish in st.session_state.inventory
    )

    st.write(
        f"현재 물고기 {len(st.session_state.inventory)}마리"
    )

    st.markdown(
        f"""
        <div class="big-number">
            💰 {format_gold(total_value)}
        </div>
        """,
        unsafe_allow_html=True
    )

    st.write("")

    if st.session_state.inventory:

        if st.button(
            "💰 물고기 전부 판매",
            use_container_width=True,
            type="primary"
        ):

            count = sell_all()

            st.success(
                f"🐟 {count}마리를 판매했습니다!"
            )

            st.rerun()

        st.write("")

        for index, fish in enumerate(
            st.session_state.inventory
        ):

            cols = st.columns([1, 4, 2, 1])

            with cols[0]:

                st.markdown(
                    f"""
                    <div style="font-size:45px;">
                        {fish["emoji"]}
                    </div>
                    """,
                    unsafe_allow_html=True
                )

            with cols[1]:

                traits = "일반"

                if fish["traits"]:

                    traits = " ".join(
                        f'{t["emoji"]} {t["name"]}'
                        for t in fish["traits"]
                    )

                st.markdown(
                    f"""
                    **{fish["name"]}**

                    {fish["grade"]} · {traits}

                    📏 {fish["size"]:.2f} m
                    · ⚖️ {fish["weight"]:.2f} kg
                    """,
                )

            with cols[2]:

                st.markdown(
                    f"### {format_gold(fish['price'])}"
                )

            with cols[3]:

                if st.button(
                    "판매",
                    key=f"sell_page_{index}"
                ):

                    sell_fish(index)

                    st.rerun()

    else:

        st.info(
            "🎒 판매할 물고기가 없습니다."
        )

    st.markdown("</div>", unsafe_allow_html=True)


# ============================================================
# 강화
# ============================================================

elif st.session_state.page == "강화":

    rod_index = st.session_state.equipped_rod

    rod = RODS[rod_index]

    level = get_rod_level(rod_index)

    stats = get_rod_stats(rod_index)

    success_rate = enhancement_success_rate(level)

    cost = enhancement_cost(level, rod_index)

    st.markdown(
        '<div class="game-card"><h2>🔨 낚싯대 강화</h2>',
        unsafe_allow_html=True
    )

    st.markdown(
        f"""
        <div class="catch-card">

            <div class="catch-icon">
                {rod["emoji"]}
            </div>

            <div class="catch-name">
                {rod["name"]} +{level}
            </div>

            <div>
                {rod["grade"]}
            </div>

            <br>

            💪 낚시 힘:
            <b>{stats["power"]:,.2f}</b>

            <br>

            🍀 행운:
            <b>{stats["luck"]:,.2f}</b>

            <br>

            ⚡ 입질 속도:
            <b>{stats["bite"]:,.2f}</b>

            <br>

            🌀 끌어올리기:
            <b>{stats["pull"]:,.2f}</b>

            <br><br>

            ♾️ 내구도: <b>무한</b>

        </div>
        """,
        unsafe_allow_html=True
    )

    st.write("")

    c1, c2, c3 = st.columns(3)

    with c1:

        st.metric(
            "🔨 현재 강화",
            f"+{level}"
        )

    with c2:

        st.metric(
            "🎯 성공 확률",
            f"{success_rate}%"
        )

    with c3:

        st.metric(
            "💰 강화 비용",
            format_gold(cost)
        )

    st.write("")

    st.info(
        "✨ 강화 성공: 모든 스탯 +2%  |  "
        "💥 강화 실패: 강화 단계와 강화 스탯이 +0으로 초기화"
    )

    if st.button(
        f"🔨 강화하기 · {format_gold(cost)}",
        use_container_width=True,
        type="primary"
    ):

        enhance_rod()

    st.markdown("</div>", unsafe_allow_html=True)


# ============================================================
# 도감
# ============================================================

elif st.session_state.page == "도감":

    st.markdown(
        '<div class="game-card"><h2>📖 물고기 도감</h2>',
        unsafe_allow_html=True
    )

    progress = len(
        st.session_state.discovered
    ) / 80

    st.progress(
        progress
    )

    st.write(
        f"발견한 물고기: **{len(st.session_state.discovered)} / 80**"
    )

    st.markdown("</div>", unsafe_allow_html=True)

    grade_filter = st.selectbox(
        "등급 선택",
        ["전체", "일반", "희귀", "영웅", "전설", "신화"]
    )

    filtered = FISH

    if grade_filter != "전체":

        filtered = [
            fish
            for fish in FISH
            if fish["grade"] == grade_filter
        ]

    cols = st.columns(4)

    for index, fish in enumerate(filtered):

        with cols[index % 4]:

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

                        <div class="fish-info">

                            등급: {fish["grade"]}<br>

                            기본 가격:
                            {format_gold(fish["base_price"])}<br>

                            무게:
                            {fish["min_weight"]:.1f}
                            ~
                            {fish["max_weight"]:.1f} kg

                        </div>

                    </div>
                    """,
                    unsafe_allow_html=True
                )

            else:

                st.markdown(
                    f"""
                    <div class="fish-card">

                        <div class="fish-icon">
                            ❓
                        </div>

                        <div class="fish-name">
                            ???
                        </div>

                        <div class="fish-info">
                            아직 발견하지 못한 물고기입니다.
                        </div>

                    </div>
                    """,
                    unsafe_allow_html=True
                )


# ============================================================
# 사이드바 정보
# ============================================================

with st.sidebar:

    st.title("🎣 낚시왕")

    st.write(
        f"💰 {format_gold(st.session_state.gold)}"
    )

    st.write(
        f"🎒 {len(st.session_state.inventory)} / "
        f"{st.session_state.inventory_capacity}"
    )

    st.divider()

    rod = RODS[st.session_state.equipped_rod]
    level = get_rod_level(
        st.session_state.equipped_rod
    )

    st.subheader("현재 낚싯대")

    st.write(
        f"{rod['emoji']} **{rod['name']} +{level}**"
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

    st.write("♾️ 내구도: 무한")

    st.divider()

    st.subheader("✨ 특성 확률")

    st.write("🥈 실버 — 8%")
    st.write("🥇 골드 — 4%")
    st.write("🌈 무지개 — 2%")
    st.write("🌀 차원 — 0.9%")

    st.divider()

    st.subheader("💰 특성 가격 보너스")

    st.write("🥈 실버 — +10%")
    st.write("🥇 골드 — +20%")
    st.write("🌈 무지개 — +50%")
    st.write("🌀 차원 — +100%")

    st.divider()

    if st.button(
        "🔄 게임 초기화",
        use_container_width=True
    ):

        initialize_game()

        st.rerun()
