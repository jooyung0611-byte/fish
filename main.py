import streamlit as st
import random
import math
import json
import os
import time
import base64
from pathlib import Path

import streamlit.components.v1 as components


# ============================================================
# 페이지 설정
# ============================================================

st.set_page_config(
    page_title="3D 낚시 게임",
    page_icon="🎣",
    layout="wide",
    initial_sidebar_state="collapsed"
)


# ============================================================
# 기본 데이터
# ============================================================

RARITY_DATA = {
    "일반": {
        "color": "#BFC7D5",
        "multiplier": 1,
        "weight_range": (0.3, 3.0)
    },
    "희귀": {
        "color": "#4DA6FF",
        "multiplier": 2,
        "weight_range": (1.0, 6.0)
    },
    "레어": {
        "color": "#9B59FF",
        "multiplier": 5,
        "weight_range": (2.0, 12.0)
    },
    "전설": {
        "color": "#FFB020",
        "multiplier": 15,
        "weight_range": (5.0, 25.0)
    },
    "신화": {
        "color": "#FF4D8D",
        "multiplier": 40,
        "weight_range": (10.0, 50.0)
    },
    "고대": {
        "color": "#FF6B35",
        "multiplier": 100,
        "weight_range": (20.0, 100.0)
    },
    "천상": {
        "color": "#E8F7FF",
        "multiplier": 500,
        "weight_range": (50.0, 250.0)
    },
    "차원": {
        "color": "#D900FF",
        "multiplier": 2500,
        "weight_range": (100.0, 1000.0)
    }
}


# ============================================================
# 특성 데이터
# ============================================================

TRAIT_DATA = {
    "없음": {
        "chance": 0.82,
        "multiplier": 1,
        "color": "#FFFFFF"
    },
    "실버": {
        "chance": 0.10,
        "multiplier": 25,
        "color": "#D8E1EA"
    },
    "골드": {
        "chance": 0.05,
        "multiplier": 100,
        "color": "#FFD700"
    },
    "무지개": {
        "chance": 0.02,
        "multiplier": 625,
        "color": "#FF4DFF"
    },
    "차원": {
        "chance": 0.01,
        "multiplier": 2500,
        "color": "#9B00FF"
    }
}


# ============================================================
# 낚싯대 20종
# ============================================================

RODS = [
    {
        "name": "나무 낚싯대",
        "price": 0,
        "power": 1,
        "luck": 0.00,
        "speed": 1.00,
        "color": "#8B5A2B",
        "shape": "wood"
    },
    {
        "name": "대나무 낚싯대",
        "price": 100,
        "power": 2,
        "luck": 0.01,
        "speed": 1.05,
        "color": "#C9A227",
        "shape": "bamboo"
    },
    {
        "name": "초보자 낚싯대",
        "price": 250,
        "power": 3,
        "luck": 0.02,
        "speed": 1.10,
        "color": "#4A90E2",
        "shape": "basic"
    },
    {
        "name": "강철 낚싯대",
        "price": 600,
        "power": 5,
        "luck": 0.03,
        "speed": 1.15,
        "color": "#AAB2BD",
        "shape": "steel"
    },
    {
        "name": "은빛 낚싯대",
        "price": 1200,
        "power": 7,
        "luck": 0.05,
        "speed": 1.20,
        "color": "#DDE6F0",
        "shape": "silver"
    },
    {
        "name": "황금 낚싯대",
        "price": 3000,
        "power": 10,
        "luck": 0.07,
        "speed": 1.25,
        "color": "#FFD700",
        "shape": "gold"
    },
    {
        "name": "다이아 낚싯대",
        "price": 7000,
        "power": 15,
        "luck": 0.10,
        "speed": 1.30,
        "color": "#7FDBFF",
        "shape": "diamond"
    },
    {
        "name": "화염 낚싯대",
        "price": 15000,
        "power": 20,
        "luck": 0.12,
        "speed": 1.35,
        "color": "#FF4B20",
        "shape": "fire"
    },
    {
        "name": "빙결 낚싯대",
        "price": 25000,
        "power": 25,
        "luck": 0.15,
        "speed": 1.40,
        "color": "#66DDFF",
        "shape": "ice"
    },
    {
        "name": "번개 낚싯대",
        "price": 40000,
        "power": 32,
        "luck": 0.18,
        "speed": 1.45,
        "color": "#FFFF66",
        "shape": "lightning"
    },
    {
        "name": "심해 낚싯대",
        "price": 65000,
        "power": 40,
        "luck": 0.20,
        "speed": 1.50,
        "color": "#154C79",
        "shape": "deep"
    },
    {
        "name": "용의 낚싯대",
        "price": 100000,
        "power": 50,
        "luck": 0.23,
        "speed": 1.55,
        "color": "#E63946",
        "shape": "dragon"
    },
    {
        "name": "천상의 낚싯대",
        "price": 180000,
        "power": 65,
        "luck": 0.27,
        "speed": 1.60,
        "color": "#FFFFFF",
        "shape": "heaven"
    },
    {
        "name": "고대의 낚싯대",
        "price": 300000,
        "power": 80,
        "luck": 0.30,
        "speed": 1.65,
        "color": "#B87333",
        "shape": "ancient"
    },
    {
        "name": "신화의 낚싯대",
        "price": 500000,
        "power": 100,
        "luck": 0.35,
        "speed": 1.70,
        "color": "#FF4DFF",
        "shape": "mythic"
    },
    {
        "name": "공허의 낚싯대",
        "price": 800000,
        "power": 130,
        "luck": 0.40,
        "speed": 1.80,
        "color": "#7A00FF",
        "shape": "void"
    },
    {
        "name": "차원의 낚싯대",
        "price": 1500000,
        "power": 170,
        "luck": 0.45,
        "speed": 1.90,
        "color": "#FF00FF",
        "shape": "dimension"
    },
    {
        "name": "무한의 낚싯대",
        "price": 3000000,
        "power": 220,
        "luck": 0.50,
        "speed": 2.00,
        "color": "#00FFFF",
        "shape": "infinity"
    },
    {
        "name": "신의 낚싯대",
        "price": 7000000,
        "power": 300,
        "luck": 0.60,
        "speed": 2.20,
        "color": "#FFF5AA",
        "shape": "god"
    },
    {
        "name": "창조주의 낚싯대",
        "price": 15000000,
        "power": 500,
        "luck": 0.75,
        "speed": 2.50,
        "color": "#FFFFFF",
        "shape": "creator"
    }
]


# ============================================================
# 물고기 30종
# ============================================================

FISH = [
    {
        "name": "멸치",
        "rarity": "일반",
        "base_price": 20,
        "min_weight": 0.1,
        "max_weight": 0.5,
        "size": "소형"
    },
    {
        "name": "정어리",
        "rarity": "일반",
        "base_price": 30,
        "min_weight": 0.2,
        "max_weight": 0.8,
        "size": "소형"
    },
    {
        "name": "고등어",
        "rarity": "일반",
        "base_price": 45,
        "min_weight": 0.5,
        "max_weight": 2.0,
        "size": "중형"
    },
    {
        "name": "전갱이",
        "rarity": "일반",
        "base_price": 50,
        "min_weight": 0.5,
        "max_weight": 2.5,
        "size": "중형"
    },
    {
        "name": "갈치",
        "rarity": "희귀",
        "base_price": 100,
        "min_weight": 1.0,
        "max_weight": 5.0,
        "size": "중형"
    },
    {
        "name": "광어",
        "rarity": "희귀",
        "base_price": 120,
        "min_weight": 1.0,
        "max_weight": 7.0,
        "size": "중형"
    },
    {
        "name": "우럭",
        "rarity": "희귀",
        "base_price": 130,
        "min_weight": 1.0,
        "max_weight": 6.0,
        "size": "중형"
    },
    {
        "name": "도미",
        "rarity": "희귀",
        "base_price": 150,
        "min_weight": 1.5,
        "max_weight": 8.0,
        "size": "중형"
    },
    {
        "name": "농어",
        "rarity": "레어",
        "base_price": 250,
        "min_weight": 2.0,
        "max_weight": 12.0,
        "size": "대형"
    },
    {
        "name": "참치",
        "rarity": "레어",
        "base_price": 400,
        "min_weight": 5.0,
        "max_weight": 30.0,
        "size": "대형"
    },
    {
        "name": "연어",
        "rarity": "레어",
        "base_price": 350,
        "min_weight": 3.0,
        "max_weight": 20.0,
        "size": "대형"
    },
    {
        "name": "복어",
        "rarity": "레어",
        "base_price": 450,
        "min_weight": 1.0,
        "max_weight": 10.0,
        "size": "중형"
    },
    {
        "name": "상어",
        "rarity": "전설",
        "base_price": 1000,
        "min_weight": 20.0,
        "max_weight": 150.0,
        "size": "초대형"
    },
    {
        "name": "청새치",
        "rarity": "전설",
        "base_price": 1500,
        "min_weight": 30.0,
        "max_weight": 200.0,
        "size": "초대형"
    },
    {
        "name": "황새치",
        "rarity": "전설",
        "base_price": 1800,
        "min_weight": 40.0,
        "max_weight": 250.0,
        "size": "초대형"
    },
    {
        "name": "범고래",
        "rarity": "신화",
        "base_price": 5000,
        "min_weight": 100.0,
        "max_weight": 800.0,
        "size": "거대"
    },
    {
        "name": "대왕오징어",
        "rarity": "신화",
        "base_price": 7000,
        "min_weight": 100.0,
        "max_weight": 1000.0,
        "size": "거대"
    },
    {
        "name": "고래상어",
        "rarity": "신화",
        "base_price": 10000,
        "min_weight": 300.0,
        "max_weight": 2000.0,
        "size": "거대"
    },
    {
        "name": "고대어",
        "rarity": "고대",
        "base_price": 20000,
        "min_weight": 50.0,
        "max_weight": 500.0,
        "size": "거대"
    },
    {
        "name": "고대 상어",
        "rarity": "고대",
        "base_price": 30000,
        "min_weight": 200.0,
        "max_weight": 1200.0,
        "size": "거대"
    },
    {
        "name": "화염어",
        "rarity": "고대",
        "base_price": 40000,
        "min_weight": 30.0,
        "max_weight": 300.0,
        "size": "대형"
    },
    {
        "name": "빙결어",
        "rarity": "천상",
        "base_price": 100000,
        "min_weight": 100.0,
        "max_weight": 700.0,
        "size": "거대"
    },
    {
        "name": "천상의 잉어",
        "rarity": "천상",
        "base_price": 150000,
        "min_weight": 50.0,
        "max_weight": 500.0,
        "size": "대형"
    },
    {
        "name": "신성한 물고기",
        "rarity": "천상",
        "base_price": 250000,
        "min_weight": 100.0,
        "max_weight": 1000.0,
        "size": "거대"
    },
    {
        "name": "차원어",
        "rarity": "차원",
        "base_price": 1000000,
        "min_weight": 100.0,
        "max_weight": 3000.0,
        "size": "거대"
    },
    {
        "name": "차원 고래",
        "rarity": "차원",
        "base_price": 3000000,
        "min_weight": 500.0,
        "max_weight": 10000.0,
        "size": "초거대"
    },
    {
        "name": "공허의 물고기",
        "rarity": "차원",
        "base_price": 5000000,
        "min_weight": 200.0,
        "max_weight": 5000.0,
        "size": "초거대"
    },
    {
        "name": "무한어",
        "rarity": "차원",
        "base_price": 10000000,
        "min_weight": 1000.0,
        "max_weight": 20000.0,
        "size": "초거대"
    },
    {
        "name": "창조어",
        "rarity": "차원",
        "base_price": 50000000,
        "min_weight": 5000.0,
        "max_weight": 100000.0,
        "size": "초거대"
    },
    {
        "name": "세계의 물고기",
        "rarity": "차원",
        "base_price": 100000000,
        "min_weight": 10000.0,
        "max_weight": 200000.0,
        "size": "초거대"
    }
]


# ============================================================
# 보스 물고기
# ============================================================

BOSS_FISH = [
    {
        "name": "해신 레비아탄",
        "rarity": "차원",
        "base_price": 500000000,
        "min_weight": 10000,
        "max_weight": 500000,
        "size": "보스"
    },
    {
        "name": "심해의 군주",
        "rarity": "차원",
        "base_price": 1000000000,
        "min_weight": 50000,
        "max_weight": 1000000,
        "size": "보스"
    },
    {
        "name": "차원의 고래왕",
        "rarity": "차원",
        "base_price": 5000000000,
        "min_weight": 100000,
        "max_weight": 5000000,
        "size": "보스"
    }
]


# ============================================================
# 세션 상태 초기화
# ============================================================

if "money" not in st.session_state:
    st.session_state.money = 1000

if "level" not in st.session_state:
    st.session_state.level = 1

if "xp" not in st.session_state:
    st.session_state.xp = 0

if "total_catches" not in st.session_state:
    st.session_state.total_catches = 0

if "best_price" not in st.session_state:
    st.session_state.best_price = 0

if "caught_fish" not in st.session_state:
    st.session_state.caught_fish = []

if "codex" not in st.session_state:
    st.session_state.codex = {}

if "owned_rods" not in st.session_state:
    st.session_state.owned_rods = [0]

if "equipped_rod" not in st.session_state:
    st.session_state.equipped_rod = 0

if "fishing" not in st.session_state:
    st.session_state.fishing = False

if "last_catch" not in st.session_state:
    st.session_state.last_catch = None

if "message" not in st.session_state:
    st.session_state.message = ""

if "game_started" not in st.session_state:
    st.session_state.game_started = True


# ============================================================
# 함수
# ============================================================

def get_level_required_xp(level):
    return int(100 * (level ** 1.5))


def add_xp(amount):
    st.session_state.xp += amount

    while st.session_state.xp >= get_level_required_xp(
        st.session_state.level
    ):
        st.session_state.xp -= get_level_required_xp(
            st.session_state.level
        )

        st.session_state.level += 1

        st.session_state.message = (
            f"🎉 레벨 업! 현재 레벨: "
            f"{st.session_state.level}"
        )


def choose_trait(rod_luck=0.0):
    """
    기본 확률
    차원 1%
    무지개 2%
    골드 5%
    실버 10%

    낚싯대 행운 능력치에 따라 희귀 특성 확률 보정
    """

    roll = random.random()

    bonus = rod_luck * 0.20

    dimension = 0.01 + bonus * 0.20
    rainbow = 0.02 + bonus * 0.30
    gold = 0.05 + bonus * 0.50
    silver = 0.10 + bonus * 0.80

    if roll < dimension:
        return "차원"

    roll -= dimension

    if roll < rainbow:
        return "무지개"

    roll -= rainbow

    if roll < gold:
        return "골드"

    roll -= gold

    if roll < silver:
        return "실버"

    return "없음"


def choose_rarity(rod_power=1):
    """
    낚싯대 파워가 높을수록 높은 등급이 조금 더 잘 나오도록 구성
    """

    power_bonus = min(rod_power / 1000, 0.5)

    roll = random.random()

    weights = {
        "일반": 55,
        "희귀": 22,
        "레어": 12,
        "전설": 6,
        "신화": 3,
        "고대": 1.5,
        "천상": 0.4,
        "차원": 0.1
    }

    weights["희귀"] += power_bonus * 5
    weights["레어"] += power_bonus * 4
    weights["전설"] += power_bonus * 3
    weights["신화"] += power_bonus * 2
    weights["고대"] += power_bonus
    weights["천상"] += power_bonus * 0.3
    weights["차원"] += power_bonus * 0.1

    total = sum(weights.values())

    value = roll * total

    current = 0

    for rarity, weight in weights.items():
        current += weight

        if value <= current:
            return rarity

    return "일반"


def choose_fish(rod_power=1):
    rarity = choose_rarity(rod_power)

    possible = [
        fish for fish in FISH
        if fish["rarity"] == rarity
    ]

    if not possible:
        possible = [
            fish for fish in FISH
            if fish["rarity"] == "일반"
        ]

    return random.choice(possible)


def calculate_price(fish, weight, trait):
    """
    가격 = 기본가격 × 무게 보정 × 특성 배율 × 희귀도 배율
    """

    rarity_multiplier = RARITY_DATA[
        fish["rarity"]
    ]["multiplier"]

    trait_multiplier = TRAIT_DATA[
        trait
    ]["multiplier"]

    weight_multiplier = max(
        0.1,
        weight
    )

    price = (
        fish["base_price"]
        * weight_multiplier
        * rarity_multiplier
        * trait_multiplier
    )

    return int(price)


def catch_fish():
    rod = RODS[
        st.session_state.equipped_rod
    ]

    fish = choose_fish(
        rod["power"]
    )

    weight = random.uniform(
        fish["min_weight"],
        fish["max_weight"]
    )

    trait = choose_trait(
        rod["luck"]
    )

    price = calculate_price(
        fish,
        weight,
        trait
    )

    xp = max(
        10,
        int(price / 100)
    )

    caught = {
        "name": fish["name"],
        "rarity": fish["rarity"],
        "trait": trait,
        "weight": round(weight, 2),
        "price": price,
        "time": time.strftime(
            "%Y-%m-%d %H:%M:%S"
        )
    }

    st.session_state.caught_fish.append(
        caught
    )

    st.session_state.last_catch = caught

    st.session_state.total_catches += 1

    st.session_state.best_price = max(
        st.session_state.best_price,
        price
    )

    key = fish["name"]

    if key not in st.session_state.codex:
        st.session_state.codex[key] = {
            "name": fish["name"],
            "rarity": fish["rarity"],
            "count": 1,
            "best_weight": round(
                weight,
                2
            ),
            "best_price": price
        }
    else:
        st.session_state.codex[key]["count"] += 1

        if weight > st.session_state.codex[key]["best_weight"]:
            st.session_state.codex[key]["best_weight"] = round(
                weight,
                2
            )

        if price > st.session_state.codex[key]["best_price"]:
            st.session_state.codex[key]["best_price"] = price

    add_xp(xp)

    return caught


def sell_all_fish():
    total = sum(
        fish["price"]
        for fish in st.session_state.caught_fish
    )

    st.session_state.money += total

    st.session_state.caught_fish = []

    return total


def buy_rod(index):
    rod = RODS[index]

    if index in st.session_state.owned_rods:
        st.session_state.equipped_rod = index
        return True, f"🎣 {rod['name']} 장착!"

    if st.session_state.money < rod["price"]:
        return False, "💰 돈이 부족합니다."

    st.session_state.money -= rod["price"]

    st.session_state.owned_rods.append(index)

    st.session_state.equipped_rod = index

    return True, f"🎣 {rod['name']} 구매 및 장착 완료!"


def save_game():
    data = {
        "money": st.session_state.money,
        "level": st.session_state.level,
        "xp": st.session_state.xp,
        "total_catches": st.session_state.total_catches,
        "best_price": st.session_state.best_price,
        "caught_fish": st.session_state.caught_fish,
        "codex": st.session_state.codex,
        "owned_rods": st.session_state.owned_rods,
        "equipped_rod": st.session_state.equipped_rod
    }

    return json.dumps(
        data,
        ensure_ascii=False,
        indent=2
    )


def load_game(data):
    try:
        obj = json.loads(data)

        st.session_state.money = obj.get(
            "money",
            1000
        )

        st.session_state.level = obj.get(
            "level",
            1
        )

        st.session_state.xp = obj.get(
            "xp",
            0
        )

        st.session_state.total_catches = obj.get(
            "total_catches",
            0
        )

        st.session_state.best_price = obj.get(
            "best_price",
            0
        )

        st.session_state.caught_fish = obj.get(
            "caught_fish",
            []
        )

        st.session_state.codex = obj.get(
            "codex",
            {}
        )

        st.session_state.owned_rods = obj.get(
            "owned_rods",
            [0]
        )

        st.session_state.equipped_rod = obj.get(
            "equipped_rod",
            0
        )

        return True

    except Exception:
        return False


# ============================================================
# CSS
# ============================================================

st.markdown(
    """
<style>

html, body, [class*="css"] {
    font-family:
        -apple-system,
        BlinkMacSystemFont,
        "Segoe UI",
        sans-serif;
}

.stApp {
    background:
        radial-gradient(
            circle at top,
            #18395c 0%,
            #081522 45%,
            #03070c 100%
        );
}

.block-container {
    max-width: 1500px;
    padding-top: 1rem;
}

.game-title {
    font-size: 42px;
    font-weight: 900;
    text-align: center;
    color: white;
    text-shadow:
        0 0 10px #00bfff,
        0 0 30px #0077ff;
    margin-bottom: 10px;
}

.stat-card {
    background:
        linear-gradient(
            135deg,
            rgba(255,255,255,0.08),
            rgba(255,255,255,0.025)
        );
    border: 1px solid rgba(255,255,255,0.15);
    border-radius: 15px;
    padding: 15px;
    text-align: center;
    box-shadow:
        0 10px 30px rgba(0,0,0,0.25);
}

.stat-value {
    font-size: 25px;
    font-weight: 900;
    color: white;
}

.stat-label {
    color: #9fb4c8;
    font-size: 13px;
}

.rod-card {
    background:
        linear-gradient(
            135deg,
            rgba(255,255,255,0.08),
            rgba(255,255,255,0.02)
        );
    border: 1px solid rgba(255,255,255,0.12);
    border-radius: 15px;
    padding: 15px;
    margin-bottom: 10px;
}

.fish-card {
    background:
        linear-gradient(
            135deg,
            rgba(255,255,255,0.08),
            rgba(255,255,255,0.025)
        );
    border-radius: 15px;
    padding: 15px;
    margin-bottom: 10px;
    border: 1px solid rgba(255,255,255,0.12);
}

.big-result {
    background:
        radial-gradient(
            circle,
            rgba(0,191,255,0.18),
            rgba(0,0,0,0.15)
        );
    border: 2px solid rgba(0,191,255,0.5);
    border-radius: 20px;
    padding: 25px;
    text-align: center;
    margin-top: 15px;
}

.big-result-name {
    font-size: 35px;
    font-weight: 900;
    color: white;
}

.big-result-price {
    font-size: 27px;
    font-weight: 900;
    color: #ffe66d;
}

.rarity {
    font-weight: 900;
}

</style>
""",
    unsafe_allow_html=True
)


# ============================================================
# 제목
# ============================================================

st.markdown(
    '<div class="game-title">🎣 3D FISHING WORLD</div>',
    unsafe_allow_html=True
)


# ============================================================
# 상단 스탯
# ============================================================

current_rod = RODS[
    st.session_state.equipped_rod
]

xp_required = get_level_required_xp(
    st.session_state.level
)

c1, c2, c3, c4, c5 = st.columns(5)

with c1:
    st.markdown(
        f"""
        <div class="stat-card">
            <div class="stat-label">💰 보유 골드</div>
            <div class="stat-value">
                {st.session_state.money:,}
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

with c2:
    st.markdown(
        f"""
        <div class="stat-card">
            <div class="stat-label">⭐ 레벨</div>
            <div class="stat-value">
                {st.session_state.level}
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

with c3:
    st.markdown(
        f"""
        <div class="stat-card">
            <div class="stat-label">✨ 경험치</div>
            <div class="stat-value">
                {st.session_state.xp:,}
                /
                {xp_required:,}
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

with c4:
    st.markdown(
        f"""
        <div class="stat-card">
            <div class="stat-label">🐟 낚은 물고기</div>
            <div class="stat-value">
                {st.session_state.total_catches:,}
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

with c5:
    st.markdown(
        f"""
        <div class="stat-card">
            <div class="stat-label">🎣 현재 낚싯대</div>
            <div class="stat-value">
                {current_rod["name"]}
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )


# ============================================================
# 3D 게임 화면
# ============================================================

def render_3d_ocean_view(
    rod_color,
    rod_shape,
    rod_power,
    last_result=None
):

    result_name = ""

    if last_result:
        result_name = last_result["name"]

    html_code = f"""
<!DOCTYPE html>
<html>
<head>

<meta charset="UTF-8">

<style>

html, body {{
    margin: 0;
    padding: 0;
    overflow: hidden;
    width: 100%;
    height: 100%;
    background: #02070d;
}}

#game {{
    width: 100%;
    height: 100%;
}}

#hud {{
    position: absolute;
    top: 15px;
    left: 15px;
    z-index: 10;
    color: white;
    font-family: Arial, sans-serif;
    pointer-events: none;
}}

.hud-box {{
    background: rgba(0,0,0,0.35);
    border: 1px solid rgba(255,255,255,0.2);
    border-radius: 12px;
    padding: 10px 14px;
    backdrop-filter: blur(8px);
}}

#status {{
    position: absolute;
    bottom: 18px;
    left: 50%;
    transform: translateX(-50%);
    color: white;
    font-family: Arial, sans-serif;
    font-size: 18px;
    font-weight: bold;
    text-shadow: 0 2px 5px black;
    z-index: 10;
}}

</style>

</head>

<body>

<div id="game"></div>

<div id="hud">
    <div class="hud-box">
        🎣 {rod_shape.upper()} ROD
        <br>
        POWER {rod_power}
    </div>
</div>

<div id="status">
    물고기를 기다리는 중...
</div>

<script src="https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js"></script>

<script>

const container =
    document.getElementById("game");

const scene =
    new THREE.Scene();

scene.fog =
    new THREE.FogExp2(
        0x061421,
        0.018
    );

const camera =
    new THREE.PerspectiveCamera(
        48,
        window.innerWidth /
        window.innerHeight,
        0.1,
        500
    );

camera.position.set(
    0,
    5.5,
    10
);

camera.lookAt(
    0,
    1,
    -4
);

const renderer =
    new THREE.WebGLRenderer({
        antialias: true
    });

renderer.setSize(
    window.innerWidth,
    window.innerHeight
);

renderer.setPixelRatio(
    Math.min(
        window.devicePixelRatio,
        2
    )
);

renderer.shadowMap.enabled = true;

renderer.shadowMap.type =
    THREE.PCFSoftShadowMap;

renderer.outputEncoding =
    THREE.sRGBEncoding;

renderer.toneMapping =
    THREE.ACESFilmicToneMapping;

renderer.toneMappingExposure =
    1.15;

container.appendChild(
    renderer.domElement
);


// ========================================================
// 조명
// ========================================================

const hemi =
    new THREE.HemisphereLight(
        0x8fdcff,
        0x06101c,
        1.5
    );

scene.add(hemi);


const sun =
    new THREE.DirectionalLight(
        0xffffff,
        2.5
    );

sun.position.set(
    -10,
    20,
    10
);

sun.castShadow = true;

sun.shadow.mapSize.width =
    2048;

sun.shadow.mapSize.height =
    2048;

scene.add(sun);


const rodLight =
    new THREE.PointLight(
        {json.dumps(rod_color)},
        2.5,
        15
    );

rodLight.position.set(
    0,
    2,
    2
);

scene.add(rodLight);


// ========================================================
// 하늘
// ========================================================

const skyGeometry =
    new THREE.SphereGeometry(
        100,
        32,
        32
    );

const skyMaterial =
    new THREE.MeshBasicMaterial({
        color: 0x061827,
        side: THREE.BackSide
    });

const sky =
    new THREE.Mesh(
        skyGeometry,
        skyMaterial
    );

scene.add(sky);


// ========================================================
// 물
// ========================================================

const waterGeometry =
    new THREE.PlaneGeometry(
        100,
        100,
        100,
        100
    );

waterGeometry.rotateX(
    -Math.PI / 2
);

const waterMaterial =
    new THREE.MeshPhysicalMaterial({
        color: 0x087a9c,
        metalness: 0.05,
        roughness: 0.12,
        transparent: true,
        opacity: 0.88,
        clearcoat: 1,
        clearcoatRoughness: 0.08
    });

const water =
    new THREE.Mesh(
        waterGeometry,
        waterMaterial
    );

water.position.y = 0;

water.receiveShadow = true;

scene.add(water);


// ========================================================
// 바닥
// ========================================================

const seabedGeometry =
    new THREE.PlaneGeometry(
        100,
        100
    );

seabedGeometry.rotateX(
    -Math.PI / 2
);

const seabedMaterial =
    new THREE.MeshStandardMaterial({
        color: 0x092c3a,
        roughness: 1
    });

const seabed =
    new THREE.Mesh(
        seabedGeometry,
        seabedMaterial
    );

seabed.position.y = -4;

scene.add(seabed);


// ========================================================
// 부두
// ========================================================

function createBox(
    x,
    y,
    z,
    sx,
    sy,
    sz,
    color
) {{

    const geometry =
        new THREE.BoxGeometry(
            sx,
            sy,
            sz
        );

    const material =
        new THREE.MeshStandardMaterial({
            color: color,
            roughness: 0.55
        });

    const mesh =
        new THREE.Mesh(
            geometry,
            material
        );

    mesh.position.set(
        x,
        y,
        z
    );

    mesh.castShadow = true;

    mesh.receiveShadow = true;

    scene.add(mesh);

    return mesh;
}}


// 넓은 부두
createBox(
    0,
    -0.15,
    4,
    18,
    0.5,
    7,
    0x4b2d1d
);


// 나무 판자
for (
    let x = -8;
    x <= 8;
    x += 1
) {{

    createBox(
        x,
        0.14,
        4,
        0.08,
        0.06,
        6.8,
        0x7a4a2b
    );

}}


// 난간
for (
    let x = -8;
    x <= 8;
    x += 2
) {{

    createBox(
        x,
        1,
        0.8,
        0.15,
        2,
        0.15,
        0x4c2d1c
    );

    createBox(
        x,
        1,
        7.2,
        0.15,
        2,
        0.15,
        0x4c2d1c
    );
}}


// ========================================================
// 낚싯대
// ========================================================

const rodGroup =
    new THREE.Group();

rodGroup.position.set(
    0,
    1.1,
    3.0
);

rodGroup.rotation.x =
    -0.35;

scene.add(rodGroup);


// 손잡이
const handleGeometry =
    new THREE.CylinderGeometry(
        0.16,
        0.22,
        1.8,
        16
    );

const handleMaterial =
    new THREE.MeshStandardMaterial({
        color: 0x3a2417,
        roughness: 0.7
    });

const handle =
    new THREE.Mesh(
        handleGeometry,
        handleMaterial
    );

handle.rotation.z =
    Math.PI / 2;

handle.position.x =
    -0.7;

rodGroup.add(handle);


// 손잡이 링
for (
    let i = 0;
    i < 6;
    i++
) {{

    const ringGeometry =
        new THREE.TorusGeometry(
            0.18,
            0.025,
            8,
            20
        );

    const ringMaterial =
        new THREE.MeshStandardMaterial({
            color: 0x222222,
            metalness: 0.8,
            roughness: 0.25
        });

    const ring =
        new THREE.Mesh(
            ringGeometry,
            ringMaterial
        );

    ring.rotation.y =
        Math.PI / 2;

    ring.position.x =
        -1.45 +
        i * 0.25;

    rodGroup.add(ring);
}}


// 낚싯대 본체
const rodGeometry =
    new THREE.CylinderGeometry(
        0.035,
        0.10,
        7.5,
        14
    );

const rodMaterial =
    new THREE.MeshPhysicalMaterial({
        color: {json.dumps(rod_color)},
        metalness: 0.35,
        roughness: 0.22,
        clearcoat: 1
    });

const rod =
    new THREE.Mesh(
        rodGeometry,
        rodMaterial
    );

rod.rotation.z =
    -Math.PI / 2;

rod.position.x =
    2.6;

rod.castShadow = true;

rodGroup.add(rod);


// 낚싯대 가이드
for (
    let i = 0;
    i < 7;
    i++
) {{

    const guideGeometry =
        new THREE.TorusGeometry(
            0.13 - i * 0.01,
            0.018,
            8,
            16
        );

    const guideMaterial =
        new THREE.MeshStandardMaterial({
            color: 0x222222,
            metalness: 0.9,
            roughness: 0.2
        });

    const guide =
        new THREE.Mesh(
            guideGeometry,
            guideMaterial
        );

    guide.rotation.y =
        Math.PI / 2;

    guide.position.x =
        0.0 +
        i * 0.85;

    guide.position.y =
        0.08;

    rodGroup.add(guide);
}}


// ========================================================
// 릴
// ========================================================

const reelGroup =
    new THREE.Group();

reelGroup.position.set(
    -0.2,
    0.25,
    0
);

rodGroup.add(reelGroup);


const spoolGeometry =
    new THREE.CylinderGeometry(
        0.35,
        0.35,
        0.18,
        24
    );

const spoolMaterial =
    new THREE.MeshStandardMaterial({
        color: 0x20242a,
        metalness: 0.9,
        roughness: 0.18
    });

const spool =
    new THREE.Mesh(
        spoolGeometry,
        spoolMaterial
    );

spool.rotation.z =
    Math.PI / 2;

reelGroup.add(spool);


const reelDiskGeometry =
    new THREE.CylinderGeometry(
        0.42,
        0.42,
        0.06,
        24
    );

const reelDiskMaterial =
    new THREE.MeshStandardMaterial({
        color: {json.dumps(rod_color)},
        metalness: 0.8,
        roughness: 0.2
    });

const reelDisk =
    new THREE.Mesh(
        reelDiskGeometry,
        reelDiskMaterial
    );

reelDisk.rotation.z =
    Math.PI / 2;

reelGroup.add(
    reelDisk
);


// ========================================================
// 찌
// ========================================================

const bobberGroup =
    new THREE.Group();

bobberGroup.position.set(
    0,
    0.5,
    -5
);

scene.add(
    bobberGroup
);


const bobberGeometry =
    new THREE.SphereGeometry(
        0.18,
        16,
        16
    );

const bobberMaterial =
    new THREE.MeshPhysicalMaterial({
        color: 0xff3d3d,
        roughness: 0.2,
        clearcoat: 1
    });

const bobber =
    new THREE.Mesh(
        bobberGeometry,
        bobberMaterial
    );

bobberGroup.add(
    bobber
);


const tipGeometry =
    new THREE.CylinderGeometry(
        0.04,
        0.04,
        0.6,
        10
    );

const tipMaterial =
    new THREE.MeshStandardMaterial({
        color: 0xffffff
    });

const tip =
    new THREE.Mesh(
        tipGeometry,
        tipMaterial
    );

tip.position.y =
    0.3;

bobberGroup.add(
    tip
);


// ========================================================
// 낚싯줄
// ========================================================

const lineMaterial =
    new THREE.LineBasicMaterial({
        color: 0xe9f7ff,
        transparent: true,
        opacity: 0.75
    });

const lineGeometry =
    new THREE.BufferGeometry();

const line =
    new THREE.Line(
        lineGeometry,
        lineMaterial
    );

scene.add(line);


// ========================================================
// 물고기
// ========================================================

const fishGroup =
    new THREE.Group();

fishGroup.position.set(
    0,
    -1.2,
    -5
);

scene.add(
    fishGroup
);


const fishBodyGeometry =
    new THREE.SphereGeometry(
        0.45,
        20,
        14
    );

const fishBodyMaterial =
    new THREE.MeshPhysicalMaterial({
        color: 0xff8844,
        metalness: 0.15,
        roughness: 0.3,
        clearcoat: 0.8
    });

const fishBody =
    new THREE.Mesh(
        fishBodyGeometry,
        fishBodyMaterial
    );

fishBody.scale.set(
    1.7,
    0.8,
    0.65
);

fishGroup.add(
    fishBody
);


// 꼬리
const tailGeometry =
    new THREE.ConeGeometry(
        0.4,
        0.8,
        3
    );

const tailMaterial =
    new THREE.MeshStandardMaterial({
        color: 0xff6644
    });

const tail =
    new THREE.Mesh(
        tailGeometry,
        tailMaterial
    );

tail.rotation.z =
    Math.PI / 2;

tail.position.x =
    -0.95;

fishGroup.add(
    tail
);


// 지느러미
const finGeometry =
    new THREE.ConeGeometry(
        0.25,
        0.6,
        3
    );

const finMaterial =
    new THREE.MeshStandardMaterial({
        color: 0xff7744
    });

const finTop =
    new THREE.Mesh(
        finGeometry,
        finMaterial
    );

finTop.position.y =
    0.4;

finTop.rotation.z =
    Math.PI;

fishGroup.add(
    finTop
);


// 눈
function createEye(x, z) {{

    const eyeGeometry =
        new THREE.SphereGeometry(
            0.08,
            12,
            12
        );

    const eyeMaterial =
        new THREE.MeshStandardMaterial({
            color: 0xffffff
        });

    const eye =
        new THREE.Mesh(
            eyeGeometry,
            eyeMaterial
        );

    eye.position.set(
        x,
        0.2,
        z
    );

    fishGroup.add(eye);


    const pupilGeometry =
        new THREE.SphereGeometry(
            0.035,
            8,
            8
        );

    const pupilMaterial =
        new THREE.MeshStandardMaterial({
            color: 0x000000
        });

    const pupil =
        new THREE.Mesh(
            pupilGeometry,
            pupilMaterial
        );

    pupil.position.set(
        x + 0.06,
        0.2,
        z
    );

    fishGroup.add(
        pupil
    );
}}

createEye(
    0.55,
    0.28
);

createEye(
    0.55,
    -0.28
);


// ========================================================
// 파티클
// ========================================================

const particleCount =
    500;

const particlePositions =
    new Float32Array(
        particleCount * 3
    );

for (
    let i = 0;
    i < particleCount;
    i++
) {{

    particlePositions[
        i * 3
    ] =
        (Math.random() - 0.5) * 40;

    particlePositions[
        i * 3 + 1
    ] =
        Math.random() * 8 - 3;

    particlePositions[
        i * 3 + 2
    ] =
        (Math.random() - 0.5) * 40;
}}

const particleGeometry =
    new THREE.BufferGeometry();

particleGeometry.setAttribute(
    "position",
    new THREE.BufferAttribute(
        particlePositions,
        3
    )
);

const particleMaterial =
    new THREE.PointsMaterial({
        color: 0x8eeaff,
        size: 0.035,
        transparent: true,
        opacity: 0.7
    });

const particles =
    new THREE.Points(
        particleGeometry,
        particleMaterial
    );

scene.add(
    particles
);


// ========================================================
// 애니메이션
// ========================================================

const clock =
    new THREE.Clock();

let elapsed = 0;

function animate() {{

    requestAnimationFrame(
        animate
    );

    const delta =
        clock.getDelta();

    elapsed += delta;


    // 물결
    const positions =
        waterGeometry.attributes.position;

    for (
        let i = 0;
        i < positions.count;
        i++
    ) {{

        const x =
            positions.getX(i);

        const z =
            positions.getZ(i);

        const y =
            Math.sin(
                x * 0.16 +
                elapsed * 1.5
            ) * 0.12
            +
            Math.cos(
                z * 0.13 +
                elapsed * 1.1
            ) * 0.08;

        positions.setY(
            i,
            y
        );
    }}

    positions.needsUpdate = true;


    // 찌 움직임
    bobberGroup.position.y =
        0.5 +
        Math.sin(
            elapsed * 2.5
        ) * 0.08;


    // 물고기 움직임
    fishGroup.position.x =
        Math.sin(
            elapsed * 0.6
        ) * 2.5;

    fishGroup.position.y =
        -1.2 +
        Math.sin(
            elapsed * 1.7
        ) * 0.25;

    fishGroup.rotation.y =
        Math.sin(
            elapsed * 0.5
        ) * 0.4;


    // 릴 회전
    spool.rotation.x =
        elapsed * 3;


    // 파티클
    particles.rotation.y =
        elapsed * 0.025;


    // 낚싯줄
    const lineStart =
        new THREE.Vector3(
            5.9,
            1.1,
            3
        );

    const lineEnd =
        bobberGroup.position.clone();

    const mid =
        new THREE.Vector3(
            2,
            0.4,
            -1
        );

    const curve =
        new THREE.CatmullRomCurve3([
            lineStart,
            mid,
            lineEnd
        ]);

    line.geometry.dispose();

    line.geometry =
        new THREE.BufferGeometry().setFromPoints(
            curve.getPoints(30)
        );


    renderer.render(
        scene,
        camera
    );
}}

animate();


// ========================================================
// 화면 크기 변경
// ========================================================

window.addEventListener(
    "resize",
    () => {{

        camera.aspect =
            window.innerWidth /
            window.innerHeight;

        camera.updateProjectionMatrix();

        renderer.setSize(
            window.innerWidth,
            window.innerHeight
        );
    }}
);

</script>

</body>
</html>
"""

    components.html(
        html_code,
        height=620,
        scrolling=False
    )


# ============================================================
# 3D 화면 출력
# ============================================================

render_3d_ocean_view(
    current_rod["color"],
    current_rod["shape"],
    current_rod["power"],
    st.session_state.last_catch
)


# ============================================================
# 낚시 버튼
# ============================================================

st.markdown("## 🎣 낚시")

col1, col2, col3 = st.columns(3)

with col1:
    if st.button(
        "🎣 낚싯줄 던지기",
        use_container_width=True
    ):
        st.session_state.fishing = True
        st.session_state.message = (
            "🌊 낚싯줄을 던졌습니다!"
        )
        st.rerun()

with col2:
    if st.button(
        "🐟 물고기 낚기",
        use_container_width=True
    ):
        result = catch_fish()

        st.session_state.fishing = False

        st.rerun()

with col3:
    if st.button(
        "💰 물고기 전부 판매",
        use_container_width=True
    ):
        earned = sell_all_fish()

        st.session_state.message = (
            f"💰 {earned:,} 골드를 획득했습니다!"
        )

        st.rerun()


# ============================================================
# 메시지
# ============================================================

if st.session_state.message:
    st.info(
        st.session_state.message
    )


# ============================================================
# 최근 낚은 물고기
# ============================================================

if st.session_state.last_catch:

    fish = st.session_state.last_catch

    rarity_color = RARITY_DATA[
        fish["rarity"]
    ]["color"]

    trait_color = TRAIT_DATA[
        fish["trait"]
    ]["color"]

    st.markdown(
        f"""
        <div class="big-result">

            <div class="big-result-name">
                🐟 {fish["name"]}
            </div>

            <div
                class="rarity"
                style="color:{rarity_color};"
            >
                {fish["rarity"]}
            </div>

            <div
                class="rarity"
                style="color:{trait_color};"
            >
                ✨ {fish["trait"]}
            </div>

            <br>

            ⚖️ 무게:
            <b>{fish["weight"]:,} kg</b>

            <br><br>

            <div class="big-result-price">
                💰 {fish["price"]:,} G
            </div>

        </div>
        """,
        unsafe_allow_html=True
    )


# ============================================================
# 메뉴
# ============================================================

st.markdown("---")

menu1, menu2, menu3, menu4 = st.tabs(
    [
        "🎣 낚싯대 상점",
        "📖 물고기 도감",
        "🐟 잡은 물고기",
        "💾 저장 / 불러오기"
    ]
)


# ============================================================
# 낚싯대 상점
# ============================================================

with menu1:

    st.markdown(
        "## 🎣 낚싯대 상점"
    )

    for index, rod in enumerate(RODS):

        owned = (
            index
            in st.session_state.owned_rods
        )

        col1, col2 = st.columns(
            [4, 1]
        )

        with col1:

            st.markdown(
                f"""
                <div class="rod-card">

                    <h3>
                        🎣 {rod["name"]}
                    </h3>

                    💰 가격:
                    <b>{rod["price"]:,} G</b>

                    <br>

                    ⚡ 파워:
                    <b>{rod["power"]}</b>

                    <br>

                    🍀 행운:
                    <b>{rod["luck"] * 100:.1f}%</b>

                    <br>

                    ⏱️ 속도:
                    <b>{rod["speed"]:.2f}x</b>

                </div>
                """,
                unsafe_allow_html=True
            )

        with col2:

            if owned:

                if (
                    st.session_state.equipped_rod
                    == index
                ):
                    st.success(
                        "장착 중"
                    )

                else:

                    if st.button(
                        "장착",
                        key=f"equip_{index}",
                        use_container_width=True
                    ):
                        st.session_state.equipped_rod = index
                        st.rerun()

            else:

                if st.button(
                    f"{rod['price']:,} G",
                    key=f"buy_{index}",
                    use_container_width=True
                ):

                    success, message = buy_rod(
                        index
                    )

                    if success:
                        st.success(
                            message
                        )
                    else:
                        st.error(
                            message
                        )

                    st.rerun()


# ============================================================
# 물고기 도감
# ============================================================

with menu2:

    st.markdown(
        "## 📖 물고기 도감"
    )

    st.write(
        f"발견한 물고기: "
        f"{len(st.session_state.codex)} / {len(FISH)}"
    )

    for fish in FISH:

        discovered = (
            fish["name"]
            in st.session_state.codex
        )

        if discovered:

            data = st.session_state.codex[
                fish["name"]
            ]

            st.markdown(
                f"""
                <div class="fish-card">

                    <h3>
                        🐟 {fish["name"]}
                    </h3>

                    등급:
                    <b>
                        {fish["rarity"]}
                    </b>

                    <br>

                    잡은 횟수:
                    <b>
                        {data["count"]}
                    </b>

                    <br>

                    최고 무게:
                    <b>
                        {data["best_weight"]:,} kg
                    </b>

                    <br>

                    최고 가격:
                    <b>
                        {data["best_price"]:,} G
                    </b>

                </div>
                """,
                unsafe_allow_html=True
            )

        else:

            st.markdown(
                f"""
                <div class="fish-card">

                    <h3>
                        ❓ 미발견 물고기
                    </h3>

                    등급:
                    {fish["rarity"]}

                </div>
                """,
                unsafe_allow_html=True
            )


# ============================================================
# 잡은 물고기
# ============================================================

with menu3:

    st.markdown(
        "## 🐟 보관 중인 물고기"
    )

    if not st.session_state.caught_fish:

        st.info(
            "현재 보관 중인 물고기가 없습니다."
        )

    else:

        total_value = sum(
            fish["price"]
            for fish
            in st.session_state.caught_fish
        )

        st.metric(
            "전체 판매 가격",
            f"{total_value:,} G"
        )

        for fish in reversed(
            st.session_state.caught_fish
        ):

            st.markdown(
                f"""
                <div class="fish-card">

                    🐟
                    <b>
                        {fish["name"]}
                    </b>

                    · {fish["rarity"]}

                    · {fish["trait"]}

                    · {fish["weight"]:,} kg

                    · 💰 {fish["price"]:,} G

                </div>
                """,
                unsafe_allow_html=True
            )


# ============================================================
# 저장 / 불러오기
# ============================================================

with menu4:

    st.markdown(
        "## 💾 저장 / 불러오기"
    )

    save_data = save_game()

    st.download_button(
        label="💾 게임 저장",
        data=save_data,
        file_name="fishing_save.json",
        mime="application/json",
        use_container_width=True
    )

    st.markdown(
        "### 📂 저장 데이터 불러오기"
    )

    uploaded = st.file_uploader(
        "저장 파일 선택",
        type=["json"]
    )

    if uploaded:

        text = uploaded.read().decode(
            "utf-8"
        )

        if st.button(
            "📥 불러오기",
            use_container_width=True
        ):

            if load_game(text):

                st.success(
                    "게임을 불러왔습니다!"
                )

                st.rerun()

            else:

                st.error(
                    "저장 파일을 읽을 수 없습니다."
                )


# ============================================================
# 하단 정보
# ============================================================

st.markdown("---")

st.caption(
    "🎣 3D Fishing World · "
    "20종 낚싯대 · 30종 물고기 · "
    "희귀도 · 특성 · 무게 · 가격 · "
    "도감 · 레벨 · 저장 시스템"
)
