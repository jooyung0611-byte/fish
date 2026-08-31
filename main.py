import streamlit as st
import random
import time
import math

# ============================================================
# 🎣 FISHING GAME
# Streamlit Single File Version
# ============================================================

st.set_page_config(
    page_title="LEGEND FISHING",
    page_icon="🎣",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================================
# CSS
# ============================================================

st.markdown("""
<style>

html, body, [class*="css"] {
    font-family: Arial, sans-serif;
}

.main {
    background: #07111f;
}

.block-container {
    padding-top: 1rem;
    padding-bottom: 2rem;
}

.game-title {
    text-align: center;
    font-size: 42px;
    font-weight: 900;
    color: #ffffff;
    margin-bottom: 5px;
    text-shadow: 0 0 20px #00aaff;
}

.game-subtitle {
    text-align: center;
    color: #8fa8c7;
    margin-bottom: 25px;
}

.top-stat {
    background: linear-gradient(135deg, #10253c, #081522);
    border: 1px solid #234b6c;
    border-radius: 15px;
    padding: 14px;
    text-align: center;
    box-shadow: 0 5px 20px rgba(0,0,0,0.3);
}

.top-stat-title {
    color: #8fa8c7;
    font-size: 13px;
}

.top-stat-value {
    color: white;
    font-size: 22px;
    font-weight: bold;
}

.panel {
    background: linear-gradient(145deg, #102238, #07121f);
    border: 1px solid #244966;
    border-radius: 18px;
    padding: 20px;
    margin-bottom: 15px;
    box-shadow: 0 8px 25px rgba(0,0,0,0.35);
}

.panel-title {
    color: white;
    font-size: 22px;
    font-weight: bold;
    margin-bottom: 15px;
}

.fishing-water {
    height: 390px;
    border-radius: 25px;
    background:
        radial-gradient(circle at 30% 30%, rgba(50,180,255,0.18), transparent 20%),
        radial-gradient(circle at 70% 60%, rgba(0,100,255,0.18), transparent 25%),
        linear-gradient(180deg, #075985, #062f4f 45%, #041b30);
    border: 2px solid #1c83b5;
    position: relative;
    overflow: hidden;
    text-align: center;
    padding-top: 35px;
    box-shadow: inset 0 0 50px rgba(0,0,0,0.5);
}

.water-title {
    font-size: 30px;
    font-weight: bold;
    color: white;
}

.water-fish {
    font-size: 100px;
    margin-top: 50px;
    animation: swim 3s infinite ease-in-out;
}

@keyframes swim {
    0% { transform: translateX(-20px); }
    50% { transform: translateX(20px); }
    100% { transform: translateX(-20px); }
}

.status-box {
    background: #091a2b;
    border-radius: 12px;
    padding: 12px;
    margin: 7px 0;
    border: 1px solid #1c405b;
}

.stat-label {
    color: #7f9bb5;
}

.stat-value {
    color: white;
    font-weight: bold;
}

.fish-card {
    background: linear-gradient(145deg, #102840, #071421);
    border: 1px solid #275674;
    border-radius: 15px;
    padding: 15px;
    margin-bottom: 10px;
}

.common {
    border-left: 5px solid #b9c2ca;
}

.silver {
    border-left: 5px solid #c7d1dc;
    box-shadow: 0 0 10px rgba(200,210,220,0.15);
}

.gold {
    border-left: 5px solid #ffd700;
    box-shadow: 0 0 15px rgba(255,215,0,0.2);
}

.rainbow {
    border-left: 5px solid #ff4fd8;
    box-shadow: 0 0 20px rgba(255,79,216,0.3);
}

.dimension {
    border-left: 5px solid #7b5cff;
    box-shadow: 0 0 25px rgba(123,92,255,0.4);
}

.big-number {
    font-size: 32px;
    font-weight: 900;
    color: white;
}

.event-box {
    background: linear-gradient(135deg, #30185c, #14294c);
    border: 1px solid #7655c9;
    border-radius: 15px;
    padding: 16px;
    text-align: center;
    margin-bottom: 15px;
}

.event-title {
    color: #d4c2ff;
    font-size: 18px;
    font-weight: bold;
}

.event-value {
    color: white;
    font-size: 25px;
    font-weight: bold;
}

.title-box {
    background: linear-gradient(135deg, #291c4d, #10213a);
    border: 1px solid #7555b8;
    border-radius: 15px;
    padding: 15px;
    margin-bottom: 10px;
}

</style>
""", unsafe_allow_html=True)

# ============================================================
# DATA
# ============================================================

RODS = [
    {"name":"나무 낚싯대","price":0,"luck":1.00,"bite":1.00,"pull":1.00},
    {"name":"대나무 낚싯대","price":500,"luck":1.05,"bite":1.05,"pull":1.05},
    {"name":"강철 낚싯대","price":1500,"luck":1.12,"bite":1.10,"pull":1.15},
    {"name":"은빛 낚싯대","price":3500,"luck":1.20,"bite":1.16,"pull":1.25},
    {"name":"황금 낚싯대","price":7000,"luck":1.30,"bite":1.22,"pull":1.38},
    {"name":"플래티넘 낚싯대","price":12000,"luck":1.42,"bite":1.30,"pull":1.52},
    {"name":"크리스탈 낚싯대","price":20000,"luck":1.55,"bite":1.38,"pull":1.68},
    {"name":"다이아몬드 낚싯대","price":35000,"luck":1.70,"bite":1.48,"pull":1.85},
    {"name":"화염 낚싯대","price":55000,"luck":1.88,"bite":1.58,"pull":2.05},
    {"name":"얼음 낚싯대","price":80000,"luck":2.05,"bite":1.68,"pull":2.25},
    {"name":"번개 낚싯대","price":120000,"luck":2.25,"bite":1.82,"pull":2.45},
    {"name":"심해 낚싯대","price":180000,"luck":2.50,"bite":1.95,"pull":2.70},
    {"name":"천공 낚싯대","price":260000,"luck":2.80,"bite":2.10,"pull":3.00},
    {"name":"마계 낚싯대","price":380000,"luck":3.10,"bite":2.28,"pull":3.35},
    {"name":"신성 낚싯대","price":550000,"luck":3.45,"bite":2.48,"pull":3.75},
    {"name":"시간의 낚싯대","price":800000,"luck":3.85,"bite":2.70,"pull":4.20},
    {"name":"공허의 낚싯대","price":1200000,"luck":4.30,"bite":2.95,"pull":4.75},
    {"name":"차원의 낚싯대","price":1800000,"luck":4.85,"bite":3.25,"pull":5.40},
    {"name":"무한의 낚싯대","price":3000000,"luck":5.50,"bite":3.60,"pull":6.20},
    {"name":"창조주의 낚싯대","price":10000000,"luck":7.00,"bite":4.00,"pull":8.00},
]

FISH_NAMES = [
    "피라미","붕어","잉어","송사리","메기","가물치","미꾸라지","갈치",
    "고등어","전갱이","참돔","감성돔","농어","광어","우럭","도미",
    "연어","송어","무지개송어","참치","방어","삼치","복어","장어",
    "청어","정어리","오징어","문어","갑오징어","꽃게","대게","새우",
    "랍스터","해마","복어왕","황금붕어","황금잉어","황금송어","황금참치",
    "심해메기","심해상어","청새치","돛새치","범고래","상어","백상아리",
    "귀상어","망치상어","고래상어","대왕오징어","고대어","화석어",
    "용어","불꽃잉어","얼음송어","번개장어","천공어","마계어","신성어",
    "시간어","공허어","차원어","무한어","별빛물고기","달빛물고기",
    "태양물고기","혜성어","은하어","성운어","블랙홀피쉬","창조어",
    "신의물고기","전설의 잉어","심연의 왕","세계수의 물고기",
    "태초의 물고기","미지의 물고기","차원포식자","시간의 고래"
]

# 80종 확인
FISH = []

for i, name in enumerate(FISH_NAMES[:80]):
    tier = i // 10
    base_price = 30 + (i * 35) + (tier * 120)

    FISH.append({
        "name": name,
        "base_price": base_price,
        "min_size": round(10 + i * 0.7, 1),
        "max_size": round(35 + i * 1.8, 1),
        "min_weight": round(0.2 + i * 0.08, 2),
        "max_weight": round(2.0 + i * 0.35, 2)
    })

TRAITS = {
    "실버": {
        "chance": 0.08,
        "multiplier": 1.10,
        "emoji": "🥈"
    },
    "골드": {
        "chance": 0.04,
        "multiplier": 1.20,
        "emoji": "🥇"
    },
    "무지개": {
        "chance": 0.02,
        "multiplier": 1.50,
        "emoji": "🌈"
    },
    "차원": {
        "chance": 0.009,
        "multiplier": 2.00,
        "emoji": "🌀"
    }
}

TITLES = [
    {"name":"🐟 초보 낚시꾼","require":0,"bonus":1.00},
    {"name":"🎣 낚시꾼","require":10,"bonus":1.02},
    {"name":"🌊 바다의 친구","require":50,"bonus":1.05},
    {"name":"🐠 숙련 낚시꾼","require":100,"bonus":1.08},
    {"name":"💎 낚시 전문가","require":250,"bonus":1.12},
    {"name":"👑 낚시 마스터","require":500,"bonus":1.18},
    {"name":"🌌 심해의 지배자","require":1000,"bonus":1.25},
    {"name":"🌀 차원의 낚시꾼","require":2500,"bonus":1.35},
    {"name":"⭐ 전설의 낚시꾼","require":5000,"bonus":1.50},
]

# ============================================================
# SESSION INITIALIZATION
# ============================================================

def init_game():

    if "money" not in st.session_state:
        st.session_state.money = 1000

    if "rod_index" not in st.session_state:
        st.session_state.rod_index = 0

    if "rod_level" not in st.session_state:
        st.session_state.rod_level = 0

    if "inventory" not in st.session_state:
        st.session_state.inventory = []

    if "inventory_size" not in st.session_state:
        st.session_state.inventory_size = 10

    if "failsafe" not in st.session_state:
        st.session_state.failsafe = 0

    if "caught" not in st.session_state:
        st.session_state.caught = 0

    if "fish_total_sold" not in st.session_state:
        st.session_state.fish_total_sold = 0

    if "screen" not in st.session_state:
        st.session_state.screen = "fishing"

    if "event_active" not in st.session_state:
        st.session_state.event_active = False

    if "event_name" not in st.session_state:
        st.session_state.event_name = ""

    if "event_bonus" not in st.session_state:
        st.session_state.event_bonus = 0

    if "last_catch" not in st.session_state:
        st.session_state.last_catch = None

    if "message" not in st.session_state:
        st.session_state.message = ""

init_game()

# ============================================================
# FUNCTIONS
# ============================================================

def current_rod():
    return RODS[st.session_state.rod_index]

def upgraded_stat(base, level):
    return base * (1.02 ** level)

def rod_stats():
    rod = current_rod()

    return {
        "luck": upgraded_stat(rod["luck"], st.session_state.rod_level),
        "bite": upgraded_stat(rod["bite"], st.session_state.rod_level),
        "pull": upgraded_stat(rod["pull"], st.session_state.rod_level)
    }

def upgrade_cost():
    rod = current_rod()

    base = max(100, int(rod["price"] * 0.12))

    multiplier = 1 + (st.session_state.rod_level * 0.35)

    return int(base * multiplier)

def upgrade_success_rate():
    level = st.session_state.rod_level

    # 기본 성공률
    rate = 95 - (level * 4)

    # 최소 5%
    return max(5, rate)

def failsafe_cost():
    rod = current_rod()

    return max(500, int(rod["price"] * 0.25))

def get_title():

    caught = st.session_state.caught

    selected = TITLES[0]

    for title in TITLES:
        if caught >= title["require"]:
            selected = title

    return selected

def title_bonus():
    return get_title()["bonus"]

def inventory_full():
    return len(st.session_state.inventory) >= st.session_state.inventory_size

def generate_trait():

    bonus = st.session_state.event_bonus if st.session_state.event_active else 0

    # 각각 독립적으로 판정
    # 이벤트가 발생하면 각 특성 확률에 +5%p
    for trait_name in ["차원", "무지개", "골드", "실버"]:

        chance = TRAITS[trait_name]["chance"] + bonus

        if random.random() < chance:
            return trait_name

    return "일반"

def catch_fish():

    if inventory_full():
        st.warning("🎒 인벤토리가 가득 찼습니다!")
        return

    stats = rod_stats()

    # 행운에 따른 고급 물고기 등장 확률
    weights = []

    for i in range(len(FISH)):
        rarity_factor = 1 + (stats["luck"] - 1) * (i / len(FISH))
        weights.append(rarity_factor)

    fish = random.choices(FISH, weights=weights, k=1)[0]

    size = round(
        random.uniform(
            fish["min_size"],
            fish["max_size"]
        ),
        1
    )

    weight = round(
        random.uniform(
            fish["min_weight"],
            fish["max_weight"]
        ),
        2
    )

    trait = generate_trait()

    # 기본 가격
    price = fish["base_price"]

    # 크기 보정
    average_size = (fish["min_size"] + fish["max_size"]) / 2
    size_multiplier = size / average_size

    # 무게 보정
    average_weight = (fish["min_weight"] + fish["max_weight"]) / 2
    weight_multiplier = weight / average_weight

    price *= (size_multiplier * 0.55 + weight_multiplier * 0.45)

    # 특성 가격 보정
    if trait != "일반":
        price *= TRAITS[trait]["multiplier"]

    # 타이틀 보정
    price *= title_bonus()

    price = int(max(1, price))

    fish_data = {
        "name": fish["name"],
        "size": size,
        "weight": weight,
        "trait": trait,
        "price": price
    }

    st.session_state.inventory.append(fish_data)
    st.session_state.caught += 1
    st.session_state.last_catch = fish_data

def start_random_event():

    # 이벤트가 이미 진행 중이면 실행하지 않음
    if st.session_state.event_active:
        return

    if random.random() < 0.18:

        st.session_state.event_active = True
        st.session_state.event_bonus = 0.05

        events = [
            "✨ 행운의 파도",
            "🌈 무지개 바다 이벤트",
            "🌀 차원 균열 발생",
            "🥇 황금 물결 이벤트",
            "🌌 심해 축제"
        ]

        st.session_state.event_name = random.choice(events)

def fishing_minigame():

    stats = rod_stats()

    # 입질 시간
    base_wait = random.uniform(2.5, 5.5)

    wait_time = base_wait / stats["bite"]

    wait_time = max(1.2, min(wait_time, 6.0))

    # 입질
    with st.spinner("🎣 물고기를 기다리는 중..."):

        time.sleep(wait_time)

    st.success("🐟 입질이 왔습니다!")

    # 힘겨루기
    max_fish_strength = random.uniform(60, 130)

    # 끌어오기 스탯으로 난이도 완화
    difficulty = max_fish_strength / stats["pull"]

    # 너무 쉽게 도망가지 않도록 기본 탈출 시간 증가
    fight_time = max(2.5, min(9.0, difficulty * 0.75))

    progress = 0.0

    start = time.time()

    placeholder = st.empty()

    # 버튼 클릭 방식의 단순화된 힘겨루기
    # Streamlit 특성상 실시간 게임보다는 턴 방식으로 구성
    while progress < 100 and time.time() - start < fight_time:

        placeholder.markdown(
            f"""
            <div class="panel">
                <div class="panel-title">🐟 물고기와 힘겨루기</div>
                <div style="font-size:20px;color:white;">
                    물고기가 도망가기 전에 끌어오세요!
                </div>
                <div style="
                    background:#17283a;
                    border-radius:20px;
                    height:28px;
                    margin-top:15px;
                    overflow:hidden;
                ">
                    <div style="
                        background:linear-gradient(90deg,#00c6ff,#00ff9d);
                        width:{min(progress,100)}%;
                        height:100%;
                    "></div>
                </div>
                <div style="text-align:center;color:white;margin-top:8px;">
                    {int(progress)}%
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

        # Streamlit은 한 실행 중 버튼 입력을 반복적으로 받을 수 없기 때문에
        # 자동 전투 방식으로 구현
        gain = random.uniform(4.0, 8.0) * stats["pull"]
        loss = random.uniform(0.5, 2.0)

        progress += gain - loss

        time.sleep(0.15)

    if progress >= 100:

        catch_fish()

        placeholder.empty()

        st.balloons()
        st.success("🎉 물고기를 낚았습니다!")

        # 이벤트 종료
        if st.session_state.event_active:
            if random.random() < 0.35:
                st.session_state.event_active = False
                st.session_state.event_bonus = 0
                st.session_state.event_name = ""

    else:

        placeholder.empty()

        # 도망 확률을 낮춤
        # 여기서는 대부분의 경우 재시도 기회를 제공
        if random.random() < 0.70:

            st.warning("🐟 물고기가 힘을 뿌리쳤지만 다시 입질을 기다릴 수 있습니다.")

        else:

            st.error("🐟 물고기가 도망갔습니다.")

# ============================================================
# HEADER
# ============================================================

st.markdown(
    '<div class="game-title">🎣 LEGEND FISHING</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="game-subtitle">최고의 낚싯대를 만들고 전설의 물고기를 잡아보세요!</div>',
    unsafe_allow_html=True
)

rod = current_rod()
stats = rod_stats()
title = get_title()

# ============================================================
# TOP STATUS
# ============================================================

c1, c2, c3, c4, c5 = st.columns(5)

with c1:
    st.markdown(
        f"""
        <div class="top-stat">
            <div class="top-stat-title">💰 골드</div>
            <div class="top-stat-value">{st.session_state.money:,}</div>
        </div>
        """,
        unsafe_allow_html=True
    )

with c2:
    st.markdown(
        f"""
        <div class="top-stat">
            <div class="top-stat-title">🎣 낚싯대</div>
            <div class="top-stat-value">{rod["name"]}</div>
        </div>
        """,
        unsafe_allow_html=True
    )

with c3:
    st.markdown(
        f"""
        <div class="top-stat">
            <div class="top-stat-title">🔨 강화</div>
            <div class="top-stat-value">+{st.session_state.rod_level}</div>
        </div>
        """,
        unsafe_allow_html=True
    )

with c4:
    st.markdown(
        f"""
        <div class="top-stat">
            <div class="top-stat-title">🎒 인벤토리</div>
            <div class="top-stat-value">{len(st.session_state.inventory)} / {st.session_state.inventory_size}</div>
        </div>
        """,
        unsafe_allow_html=True
    )

with c5:
    st.markdown(
        f"""
        <div class="top-stat">
            <div class="top-stat-title">🏆 타이틀</div>
            <div class="top-stat-value">{title["name"]}</div>
        </div>
        """,
        unsafe_allow_html=True
    )

st.write("")

# ============================================================
# EVENT
# ============================================================

start_random_event()

if st.session_state.event_active:

    st.markdown(
        f"""
        <div class="event-box">
            <div class="event-title">🎉 현재 이벤트</div>
            <div class="event-value">{st.session_state.event_name}</div>
            <div style="color:#b8c9e0;">
                모든 특성 등장 확률 +5%p
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:

    st.markdown("## 🎮 메뉴")

    if st.button("🎣 낚시", use_container_width=True):
        st.session_state.screen = "fishing"

    if st.button("🎒 인벤토리", use_container_width=True):
        st.session_state.screen = "inventory"

    if st.button("🏪 상점", use_container_width=True):
        st.session_state.screen = "shop"

    if st.button("🔨 낚싯대 강화", use_container_width=True):
        st.session_state.screen = "upgrade"

    if st.button("🎣 낚싯대", use_container_width=True):
        st.session_state.screen = "rods"

    if st.button("🏆 타이틀", use_container_width=True):
        st.session_state.screen = "titles"

    st.divider()

    st.markdown("### 📊 현재 능력치")

    st.write(f"🍀 행운: **{stats['luck']:.2f}**")
    st.write(f"⚡ 입질 속도: **{stats['bite']:.2f}**")
    st.write(f"💪 끌어오기: **{stats['pull']:.2f}**")

    st.divider()

    st.markdown("### 🏆 기록")
    st.write(f"🐟 잡은 물고기: **{st.session_state.caught:,}마리**")
    st.write(f"💰 총 판매 금액: **{st.session_state.fish_total_sold:,}G**")

# ============================================================
# FISHING SCREEN
# ============================================================

if st.session_state.screen == "fishing":

    left, right = st.columns([2.1, 1])

    with left:

        st.markdown(
            """
            <div class="fishing-water">
                <div class="water-title">🌊 낚시터</div>
                <div class="water-fish">🐟</div>
                <div style="color:#b7dcf3;">
                    잔잔한 바다에 낚싯줄을 던져보세요.
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

        st.write("")

        if st.button(
            "🎣 낚싯줄 던지기",
            use_container_width=True,
            type="primary"
        ):

            fishing_minigame()

        if st.session_state.last_catch:

            fish = st.session_state.last_catch

            trait = fish["trait"]

            if trait == "일반":
                emoji = "🐟"
                css = "common"
                trait_text = "일반"
            else:
                emoji = TRAITS[trait]["emoji"]
                css = trait.lower()
                trait_text = trait

            st.markdown(
                f"""
                <div class="fish-card {css}">
                    <div style="font-size:25px;font-weight:bold;color:white;">
                        {emoji} {fish["name"]}
                    </div>
                    <div style="color:#a9bfd3;margin-top:8px;">
                        특성: <b>{trait_text}</b><br>
                        크기: <b>{fish["size"]} cm</b><br>
                        무게: <b>{fish["weight"]} kg</b><br>
                        판매 가격: <b>{fish["price"]:,} G</b>
                    </div>
                </div>
                """,
                unsafe_allow_html=True
            )

    with right:

        st.markdown(
            """
            <div class="panel">
                <div class="panel-title">🎣 낚싯대 정보</div>
            """,
            unsafe_allow_html=True
        )

        st.write(f"### {rod['name']}")
        st.write(f"🔨 강화 단계: **+{st.session_state.rod_level}**")

        st.progress(
            min(
                st.session_state.rod_level / 20,
                1.0
            )
        )

        st.markdown(
            f"""
            <div class="status-box">
                <span class="stat-label">🍀 행운</span><br>
                <span class="stat-value">{stats["luck"]:.2f}</span>
            </div>

            <div class="status-box">
                <span class="stat-label">⚡ 입질 속도</span><br>
                <span class="stat-value">{stats["bite"]:.2f}x</span>
            </div>

            <div class="status-box">
                <span class="stat-label">💪 끌어오기</span><br>
                <span class="stat-value">{stats["pull"]:.2f}x</span>
            </div>
            """,
            unsafe_allow_html=True
        )

        st.markdown("</div>", unsafe_allow_html=True)

        st.markdown("### ✨ 특성 확률")

        event_bonus = st.session_state.event_bonus

        st.write(
            f"🥈 실버: **{(0.08 + event_bonus)*100:.1f}%**"
        )

        st.write(
            f"🥇 골드: **{(0.04 + event_bonus)*100:.1f}%**"
        )

        st.write(
            f"🌈 무지개: **{(0.02 + event_bonus)*100:.1f}%**"
        )

        st.write(
            f"🌀 차원: **{(0.009 + event_bonus)*100:.1f}%**"
        )

# ============================================================
# INVENTORY
# ============================================================

elif st.session_state.screen == "inventory":

    st.header("🎒 물고기 인벤토리")

    st.write(
        f"보관 공간: **{len(st.session_state.inventory)} / "
        f"{st.session_state.inventory_size}칸**"
    )

    if st.button("➕ 인벤토리 5칸 확장"):

        cost = int(500 * (st.session_state.inventory_size / 10))

        if st.session_state.money >= cost:

            st.session_state.money -= cost
            st.session_state.inventory_size += 5

            st.success(
                f"인벤토리가 5칸 증가했습니다! (-{cost:,}G)"
            )

        else:

            st.error("골드가 부족합니다.")

    st.divider()

    if not st.session_state.inventory:

        st.info("🎣 아직 잡은 물고기가 없습니다.")

    else:

        for index, fish in enumerate(st.session_state.inventory):

            trait = fish["trait"]

            if trait == "일반":
                emoji = "🐟"
                css = "common"
            else:
                emoji = TRAITS[trait]["emoji"]
                css = trait.lower()

            c1, c2 = st.columns([5, 1])

            with c1:

                st.markdown(
                    f"""
                    <div class="fish-card {css}">
                        <b style="font-size:20px;">
                            {emoji} {fish["name"]}
                        </b><br>
                        특성: {trait}<br>
                        크기: {fish["size"]} cm<br>
                        무게: {fish["weight"]} kg<br>
                        가격: <b>{fish["price"]:,} G</b>
                    </div>
                    """,
                    unsafe_allow_html=True
                )

            with c2:

                if st.button(
                    "💰 판매",
                    key=f"sell_{index}"
                ):

                    st.session_state.money += fish["price"]
                    st.session_state.fish_total_sold += fish["price"]

                    st.session_state.inventory.pop(index)

                    st.rerun()

# ============================================================
# SHOP
# ============================================================

elif st.session_state.screen == "shop":

    st.header("🏪 낚시 상점")

    tab1, tab2, tab3 = st.tabs([
        "🎣 낚싯대",
        "🛡️ 실패방지권",
        "🎒 인벤토리"
    ])

    with tab1:

        st.subheader("🎣 낚싯대 상점")

        for i, r in enumerate(RODS):

            c1, c2 = st.columns([4, 1])

            with c1:

                owned = i == st.session_state.rod_index

                status = "현재 사용 중" if owned else ""

                st.markdown(
                    f"""
                    <div class="panel">
                        <div class="panel-title">
                            🎣 {r["name"]}
                        </div>
                        <div style="color:#a9bfd3;">
                            🍀 행운: {r["luck"]:.2f}<br>
                            ⚡ 입질 속도: {r["bite"]:.2f}<br>
                            💪 끌어오기: {r["pull"]:.2f}<br>
                            💰 가격: {r["price"]:,}G
                        </div>
                    </div>
                    """,
                    unsafe_allow_html=True
                )

            with c2:

                if i == 0:

                    st.success("기본 지급")

                elif i <= st.session_state.rod_index:

                    if st.button(
                        "장착",
                        key=f"equip_{i}",
                        use_container_width=True
                    ):

                        st.session_state.rod_index = i
                        st.session_state.rod_level = 0
                        st.success("낚싯대를 장착했습니다.")
                        st.rerun()

                else:

                    if st.button(
                        "구매",
                        key=f"buy_{i}",
                        use_container_width=True
                    ):

                        if st.session_state.money >= r["price"]:

                            st.session_state.money -= r["price"]

                            st.session_state.rod_index = i
                            st.session_state.rod_level = 0

                            st.success(
                                f"{r['name']} 구매 완료!"
                            )

                            st.rerun()

                        else:

                            st.error("골드 부족")

    with tab2:

        st.subheader("🛡️ 강화 실패방지권")

        cost = failsafe_cost()

        st.markdown(
            f"""
            <div class="panel">
                <div class="panel-title">🛡️ 강화 실패방지권</div>
                <div style="color:#a9bfd3;">
                    강화 실패 시 강화 단계와 능력치가 초기화되는 것을
                    한 번 막아줍니다.
                    <br><br>
                    보유 수량: <b>{st.session_state.failsafe}장</b><br>
                    가격: <b>{cost:,}G</b>
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

        if st.button(
            f"🛡️ 실패방지권 구매 ({cost:,}G)",
            use_container_width=True
        ):

            if st.session_state.money >= cost:

                st.session_state.money -= cost
                st.session_state.failsafe += 1

                st.success("실패방지권을 구매했습니다!")

            else:

                st.error("골드가 부족합니다.")

    with tab3:

        st.subheader("🎒 인벤토리 확장")

        cost = int(
            500 *
            (st.session_state.inventory_size / 10)
        )

        st.write(
            f"현재 인벤토리: "
            f"**{st.session_state.inventory_size}칸**"
        )

        st.write(
            f"다음 확장: **+5칸**"
        )

        st.write(
            f"비용: **{cost:,}G**"
        )

        if st.button(
            "➕ 5칸 확장",
            use_container_width=True
        ):

            if st.session_state.money >= cost:

                st.session_state.money -= cost
                st.session_state.inventory_size += 5

                st.success("인벤토리가 확장되었습니다!")

                st.rerun()

            else:

                st.error("골드가 부족합니다.")

# ============================================================
# UPGRADE
# ============================================================

elif st.session_state.screen == "upgrade":

    st.header("🔨 낚싯대 강화")

    rod = current_rod()
    stats = rod_stats()

    left, right = st.columns([1.5, 1])

    with left:

        st.markdown(
            f"""
            <div class="panel">
                <div class="panel-title">
                    🎣 {rod["name"]} +{st.session_state.rod_level}
                </div>

                <div class="status-box">
                    🍀 행운<br>
                    <span class="big-number">
                        {stats["luck"]:.2f}
                    </span>
                </div>

                <div class="status-box">
                    ⚡ 입질 속도<br>
                    <span class="big-number">
                        {stats["bite"]:.2f}
                    </span>
                </div>

                <div class="status-box">
                    💪 끌어오기<br>
                    <span class="big-number">
                        {stats["pull"]:.2f}
                    </span>
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

    with right:

        cost = upgrade_cost()
        success = upgrade_success_rate()

        st.markdown(
            f"""
            <div class="panel">
                <div class="panel-title">🔨 강화 정보</div>
                <div style="color:#a9bfd3;">
                    강화 비용<br>
                    <span class="big-number">
                        {cost:,} G
                    </span>
                    <br><br>

                    성공 확률<br>
                    <span class="big-number">
                        {success}%
                    </span>
                    <br><br>

                    성공 시<br>
                    모든 능력치 <b>+2%</b>
                    <br><br>

                    실패 시<br>
                    강화 단계 및 능력치 초기화
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

        st.write(
            f"🛡️ 실패방지권 보유: "
            f"**{st.session_state.failsafe}장**"
        )

        if st.button(
            f"🔨 강화하기 ({cost:,}G)",
            use_container_width=True,
            type="primary"
        ):

            if st.session_state.money < cost:

                st.error("골드가 부족합니다.")

            else:

                st.session_state.money -= cost

                success_roll = random.random() < (
                    success / 100
                )

                if success_roll:

                    st.session_state.rod_level += 1

                    st.success(
                        f"🎉 강화 성공! "
                        f"+{st.session_state.rod_level}"
                    )

                    st.rerun()

                else:

                    if st.session_state.failsafe > 0:

                        st.session_state.failsafe -= 1

                        st.warning(
                            "🛡️ 강화 실패방지권이 발동했습니다!"
                        )

                        st.rerun()

                    else:

                        st.session_state.rod_level = 0

                        st.error(
                            "💥 강화 실패! "
                            "강화 단계와 능력치가 초기화되었습니다."
                        )

                        st.rerun()

# ============================================================
# RODS
# ============================================================

elif st.session_state.screen == "rods":

    st.header("🎣 낚싯대 목록")

    for i, r in enumerate(RODS):

        equipped = (
            i == st.session_state.rod_index
        )

        st.markdown(
            f"""
            <div class="panel">
                <div class="panel-title">
                    {"⭐ " if equipped else ""}
                    {r["name"]}
                </div>

                <div style="color:#a9bfd3;">
                    가격: {r["price"]:,} G<br>
                    🍀 행운: {r["luck"]:.2f}<br>
                    ⚡ 입질 속도: {r["bite"]:.2f}<br>
                    💪 끌어오기: {r["pull"]:.2f}
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

# ============================================================
# TITLES
# ============================================================

elif st.session_state.screen == "titles":

    st.header("🏆 타이틀")

    st.write(
        f"현재 잡은 물고기: "
        f"**{st.session_state.caught:,}마리**"
    )

    for t in TITLES:

        unlocked = (
            st.session_state.caught >= t["require"]
        )

        if unlocked:

            st.markdown(
                f"""
                <div class="title-box">
                    <div style="font-size:23px;font-weight:bold;color:white;">
                        {t["name"]}
                    </div>

                    <div style="color:#a9bfd3;margin-top:7px;">
                        필요 물고기: {t["require"]:,}마리<br>
                        판매 가격 보너스: +{int((t["bonus"]-1)*100)}%
                    </div>

                    <div style="color:#7dffb2;margin-top:8px;">
                        ✅ 획득 완료
                    </div>
                </div>
                """,
                unsafe_allow_html=True
            )

        else:

            st.markdown(
                f"""
                <div class="title-box" style="opacity:0.5;">
                    <div style="font-size:23px;font-weight:bold;color:white;">
                        🔒 ??? 타이틀
                    </div>

                    <div style="color:#a9bfd3;margin-top:7px;">
                        필요 물고기: {t["require"]:,}마리
                    </div>
                </div>
                """,
                unsafe_allow_html=True
            )

# ============================================================
# FOOTER
# ============================================================

st.divider()

st.markdown(
    """
    <div style="
        text-align:center;
        color:#607d96;
        padding:20px;
    ">
        🎣 LEGEND FISHING<br>
        낚싯대를 강화하고 전설의 물고기를 찾아보세요!
    </div>
    """,
    unsafe_allow_html=True
)
```
