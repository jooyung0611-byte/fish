import streamlit as st
import random
import json

# -----------------------------------------------------------------------------
# 1. 초기 데이터 및 세션 상태 설정
# -----------------------------------------------------------------------------
st.set_page_config(page_title="방치형 웹 낚시 게임", page_icon="🎣", layout="wide")

FISH_BOOK_TEMPLATE = {
    "피라미": {"rarity": "Common", "min_w": 0.1, "max_w": 0.5, "base_p": 10, "xp": 15},
    "붕어": {"rarity": "Common", "min_w": 0.5, "max_w": 2.0, "base_p": 25, "xp": 25},
    "배스": {"rarity": "Uncommon", "min_w": 1.0, "max_w": 4.0, "base_p": 60, "xp": 50},
    "비단잉어": {"rarity": "Rare", "min_w": 3.0, "max_w": 8.0, "base_p": 150, "xp": 120},
    "황금 잉어": {"rarity": "Epic", "min_w": 5.0, "max_w": 12.0, "base_p": 500, "xp": 350},
    "심해의 크라켄": {"rarity": "Boss", "min_w": 500.0, "max_w": 1500.0, "base_p": 5000, "xp": 2000},
    "천공의 고래": {"rarity": "Boss", "min_w": 1000.0, "max_w": 3000.0, "base_p": 12000, "xp": 5000},
    "차원의 레비아탄": {"rarity": "Boss", "min_w": 2500.0, "max_w": 8000.0, "base_p": 30000, "xp": 10000}
}

TRAITS = [
    {"name": "일반", "mult": 1.0},
    {"name": "반짝이는", "mult": 1.5},
    {"name": "거대한", "mult": 1.8},
    {"name": "전설의", "mult": 3.0}
]

SHOP_ITEMS = {
    "초강력 미끼": {"price": 100, "desc": "대형 물고기 등장 확률 증가"},
    "행운의 미끼": {"price": 150, "desc": "희귀 등급 물고기 등장 확률 증가"},
    "황금 미끼": {"price": 300, "desc": "판매 가격 상승 효과"},
    "보스 미끼": {"price": 1000, "desc": "보스 물고기 출현 확률 대폭 증가"}
}

def init_game():
    if "level" not in st.session_state:
        st.session_state.level = 1
        st.session_state.xp = 0
        st.session_state.max_xp = 100
        st.session_state.gold = 0
        st.session_state.inventory = []
        st.session_state.baits = {
            "일반 미끼": float('inf'),
            "초강력 미끼": 0,
            "행운의 미끼": 0,
            "황금 미끼": 0,
            "보스 미끼": 0
        }
        st.session_state.records = {name: 0 for name in FISH_BOOK_TEMPLATE.keys()}

init_game()

# -----------------------------------------------------------------------------
# 2. 핵심 로직 함수
# -----------------------------------------------------------------------------
def add_xp(amount):
    st.session_state.xp += amount
    while st.session_state.xp >= st.session_state.max_xp:
        st.session_state.xp -= st.session_state.max_xp
        st.session_state.level += 1
        st.session_state.max_xp = int(st.session_state.max_xp * 1.5)
        st.toast(f"🎉 레벨업! 현재 레벨: Lv.{st.session_state.level}", icon="⭐")

def catch_fish(selected_bait):
    if st.session_state.baits[selected_bait] <= 0:
        st.error("미끼가 부족합니다!")
        return

    if selected_bait != "일반 미끼":
        st.session_state.baits[selected_bait] -= 1

    luck_bonus = st.session_state.level * 2
    boss_chance = 15 if selected_bait == "보스 미끼" else 2
    
    rand = random.randint(1, 100) + luck_bonus

    if rand > (100 - boss_chance):
        fish_name = random.choice(["심해의 크라켄", "천공의 고래", "차원의 레비아탄"])
    elif rand > 75 or selected_bait == "행운의 미끼":
        fish_name = "황금 잉어"
    elif rand > 45 or selected_bait == "초강력 미끼":
        fish_name = random.choice(["배스", "비단잉어"])
    else:
        fish_name = random.choice(["피라미", "붕어"])

    info = FISH_BOOK_TEMPLATE[fish_name]
    weight = round(random.uniform(info["min_w"], info["max_w"]), 2)
    trait = random.choice(TRAITS)

    if selected_bait == "황금 미끼":
        trait = {"name": "전설의", "mult": 3.0}

    caught_item = {
        "name": fish_name,
        "weight": weight,
        "trait": trait["name"],
        "mult": trait["mult"],
        "base_price": info["base_p"],
        "xp": info["xp"],
        "rarity": info["rarity"]
    }

    st.session_state.inventory.append(caught_item)
    st.session_state.records[fish_name] += 1
    
    add_xp(info["xp"])
    
    st.success(f"🎣 [{trait['name']} {fish_name}]을(를) 잡았습니다! ({weight}kg)")

def sell_all_fish():
    if not st.session_state.inventory:
        st.warning("판매할 물고기가 없습니다.")
        return

    total = 0
    for fish in st.session_state.inventory:
        price = int(fish["base_price"] * fish["weight"] * fish["mult"])
        total += price

    st.session_state.gold += total
    st.session_state.inventory.clear()
    st.success(f"💰 모든 물고기를 판매하여 {total:,} 골드를 획득했습니다!")

# -----------------------------------------------------------------------------
# 3. UI 화면 구성
# -----------------------------------------------------------------------------
st.title("🎣 판타지 낚시 게임")

# 사이드바: 플레이어 정보 및 저장/불러오기
with st.sidebar:
    st.header("👤 플레이어 정보")
    st.write(f"**레벨:** Lv.{st.session_state.level}")
    st.progress(min(st.session_state.xp / st.session_state.max_xp, 1.0))
    st.caption(f"XP: {st.session_state.xp} / {st.session_state.max_xp}")
    st.write(f"**골드:** {st.session_state.gold:,} G")
    
    st.divider()
    st.subheader("💾 게임 저장 / 불러오기")
    
    # Save Data JSON 다운로드
    save_data = {
        "level": st.session_state.level,
        "xp": st.session_state.xp,
        "max_xp": st.session_state.max_xp,
        "gold": st.session_state.gold,
        "inventory": st.session_state.inventory,
        "baits": st.session_state.baits,
        "records": st.session_state.records
    }
    json_str = json.dumps(save_data, ensure_ascii=False, indent=2)
    st.download_button("💾 데이터 저장 (다운로드)", data=json_str, file_name="fishing_save.json", mime="application/json")
    
    # Load Data JSON 업로드
    uploaded_file = st.file_uploader("📂 데이터 불러오기 (파일 업로드)", type=["json"])
    if uploaded_file is not None:
        if st.button("파일 적용하기"):
            data = json.load(uploaded_file)
            st.session_state.level = data["level"]
            st.session_state.xp = data["xp"]
            st.session_state.max_xp = data["max_xp"]
            st.session_state.gold = data["gold"]
            st.session_state.inventory = data["inventory"]
            st.session_state.baits = data["baits"]
            st.session_state.records = data["records"]
            st.rerun()

# 메인 탭
tab1, tab2, tab3, tab4 = st.tabs(["🎣 낚시터", "🎒 가방 & 판매", "🛒 상점", "📖 물고기 도감"])

# --- TAB 1: 낚시터 ---
with tab1:
    st.subheader("바다 낚시터")
    
    bait_options = []
    for b_name, count in st.session_state.baits.items():
        if count == float('inf'):
            bait_options.append(f"{b_name} (무제한)")
        else:
            bait_options.append(f"{b_name} ({count}개 보유)")
            
    selected_option = st.selectbox("사용할 미끼 선택", bait_options)
    selected_bait = selected_option.split(" (")[0]
    
    if st.button("🎣 찌 던지기!", use_container_width=True):
        catch_fish(selected_bait)

# --- TAB 2: 가방 & 판매 ---
with tab2:
    col1, col2 = st.columns([3, 1])
    with col1:
        st.subheader(f"보유 중인 물고기 ({len(st.session_state.inventory)}마리)")
    with col2:
        if st.button("💰 전체 판매하기", use_container_width=True):
            sell_all_fish()
            
    if st.session_state.inventory:
        for idx, item in enumerate(reversed(st.session_state.inventory)):
            price = int(item["base_price"] * item["weight"] * item["mult"])
            st.write(f"**[{item['rarity']}] {item['trait']} {item['name']}** | {item['weight']}kg | 예상가: {price:,} G")
    else:
        st.info("가방이 비어있습니다.")

# --- TAB 3: 상점 ---
with tab3:
    st.subheader("🛒 낚시 상점")
    for name, data in SHOP_ITEMS.items():
        c1, c2, c3 = st.columns([2, 3, 1])
        with c1:
            st.write(f"**{name}**")
            st.caption(f"가격: {data['price']:,} G")
        with c2:
            st.write(f"{data['desc']}")
        with c3:
            if st.button(f"구매", key=f"buy_{name}"):
                if st.session_state.gold >= data['price']:
                    st.session_state.gold -= data['price']
                    st.session_state.baits[name] += 1
                    st.success(f"{name} 구매 완료!")
                    st.rerun()
                else:
                    st.error("골드가 부족합니다.")

# --- TAB 4: 물고기 도감 ---
with tab4:
    st.subheader("📖 물고기 도감")
    cols = st.columns(2)
    for idx, (name, info) in enumerate(FISH_BOOK_TEMPLATE.items()):
        caught_count = st.session_state.records[name]
        with cols[idx % 2]:
            if caught_count > 0:
                is_boss = "👑 " if info["rarity"] == "Boss" else ""
                st.write(f"### {is_boss}{name}")
                st.caption(f"등급: {info['rarity']} | 잡은 횟수: {caught_count}회")
            else:
                st.write("### ??? (미발견)")
                st.caption("아직 낚지 못한 물고기입니다.")
        st.divider()
