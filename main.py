import streamlit as st
import streamlit.components.v1 as components
import random
import json
import time

# -----------------------------------------------------------------------------
# 1. 앱 설정 및 기본 데이터베이스 정의
# -----------------------------------------------------------------------------
st.set_page_config(page_title="판타지 3D 낚시 게임 v4.0", page_icon="🎣", layout="wide")

# 20종 낚시대 데이터
FISHING_RODS = {
    "대나무 낚시대": {"price": 0, "catch_rate": 60, "rare_bonus": 0, "exp_mult": 1.0, "gold_mult": 1.0, "desc": "가장 기본적이고 가벼운 대나무 낚시대."},
    "나무 낚시대": {"price": 250, "catch_rate": 63, "rare_bonus": 2, "exp_mult": 1.05, "gold_mult": 1.05, "desc": "조금 더 튼튼하게 깎아 만든 목재 낚시대."},
    "강화 글래스파이버": {"price": 700, "catch_rate": 66, "rare_bonus": 4, "exp_mult": 1.1, "gold_mult": 1.1, "desc": "탄력성 높은 유리섬유 재질의 낚시대."},
    "카본 흑연 로드": {"price": 1500, "catch_rate": 70, "rare_bonus": 7, "exp_mult": 1.15, "gold_mult": 1.2, "desc": "가볍고 단단하여 입질 감지가 뛰어납니다."},
    "티타늄 스틸 로드": {"price": 3500, "catch_rate": 73, "rare_bonus": 10, "exp_mult": 1.2, "gold_mult": 1.3, "desc": "어떤 중량급 물고기도 버티는 고강도 낚시대."},
    "네온 펄스 로드": {"price": 8000, "catch_rate": 76, "rare_bonus": 14, "exp_mult": 1.3, "gold_mult": 1.4, "desc": "야간 미끼 시야 확보에 특화된 네온 빛 로드."},
    "플래티넘 가디언": {"price": 18000, "catch_rate": 79, "rare_bonus": 18, "exp_mult": 1.4, "gold_mult": 1.5, "desc": "백금 장식으로 기품이 느껴지는 고급 로드."},
    "다이아몬드 캐스터": {"price": 35000, "catch_rate": 82, "rare_bonus": 23, "exp_mult": 1.5, "gold_mult": 1.7, "desc": "다이아몬드로 코팅되어 강도가 극대화된 로드."},
    "화염 드래곤 로드": {"price": 70000, "catch_rate": 85, "rare_bonus": 28, "exp_mult": 1.6, "gold_mult": 1.9, "desc": "드래곤의 숨결이 스며든 뜨거운 붉은 낚시대."},
    "빙결의 심해 로드": {"price": 120000, "catch_rate": 87, "rare_bonus": 34, "exp_mult": 1.7, "gold_mult": 2.1, "desc": "차가운 기운으로 물고기의 방심을 유도합니다."},
    "뇌전의 수호자": {"price": 200000, "catch_rate": 89, "rare_bonus": 40, "exp_mult": 1.8, "gold_mult": 2.4, "desc": "전기 파동으로 물고기를 빠르게 채어 올립니다."},
    "바람의 서곡": {"price": 350000, "catch_rate": 91, "rare_bonus": 47, "exp_mult": 2.0, "gold_mult": 2.7, "desc": "바람처럼 가벼워 입질 손실을 최소화합니다."},
    "그림자 포획자": {"price": 600000, "catch_rate": 92, "rare_bonus": 55, "exp_mult": 2.2, "gold_mult": 3.1, "desc": "물고기에게 모습을 숨기는 은밀한 그림자 로드."},
    "천사의 은총": {"price": 1000000, "catch_rate": 93, "rare_bonus": 64, "exp_mult": 2.5, "gold_mult": 3.6, "desc": "천상의 빛으로 희귀 등급 물고기를 홀립니다."},
    "악마의 삼지창": {"price": 1600000, "catch_rate": 94, "rare_bonus": 74, "exp_mult": 2.8, "gold_mult": 4.2, "desc": "압도적인 파괴력으로 거대 몬스터를 제압합니다."},
    "시공간 균열 로드": {"price": 2500000, "catch_rate": 95, "rare_bonus": 85, "exp_mult": 3.2, "gold_mult": 5.0, "desc": "시공간을 뒤틀어 신비한 고대종을 끌어당깁니다."},
    "은하수 캐스케이드": {"price": 4000000, "catch_rate": 96, "rare_bonus": 98, "exp_mult": 3.7, "gold_mult": 6.0, "desc": "별빛의 기운이 서려 있는 매혹적인 낚시대."},
    "코스믹 스타로드": {"price": 6500000, "catch_rate": 97, "rare_bonus": 115, "exp_mult": 4.3, "gold_mult": 7.5, "desc": "우주의 인력으로 물고기가 스스로 끌려옵니다."},
    "태양신 라의 분노": {"price": 10000000, "catch_rate": 98, "rare_bonus": 135, "exp_mult": 5.0, "gold_mult": 9.5, "desc": "태양의 축복을 받은 최고 등급 신화 낚시대."},
    "차원 창조주의 로드": {"price": 16000000, "catch_rate": 99, "rare_bonus": 160, "exp_mult": 6.0, "gold_mult": 12.0, "desc": "모든 바다 생태계를 지배하는 신의 도구."}
}

# -----------------------------------------------------------------------------
# 60종 확장 물고기 데이터베이스 (총 10개 등급)
# -----------------------------------------------------------------------------
FISH_BOOK_TEMPLATE = {
    # 1. Common (10종)
    "피라미": {"rarity": "Common", "min_w": 0.1, "max_w": 0.5, "base_p": 10, "xp": 15},
    "붕어": {"rarity": "Common", "min_w": 0.5, "max_w": 2.0, "base_p": 25, "xp": 25},
    "송사리": {"rarity": "Common", "min_w": 0.05, "max_w": 0.3, "base_p": 8, "xp": 10},
    "망둥어": {"rarity": "Common", "min_w": 0.2, "max_w": 0.8, "base_p": 18, "xp": 20},
    "미꾸라지": {"rarity": "Common", "min_w": 0.1, "max_w": 0.6, "base_p": 15, "xp": 18},
    "블루길": {"rarity": "Common", "min_w": 0.4, "max_w": 1.5, "base_p": 30, "xp": 30},
    "꺽지": {"rarity": "Common", "min_w": 0.3, "max_w": 1.2, "base_p": 35, "xp": 35},
    "빙어": {"rarity": "Common", "min_w": 0.05, "max_w": 0.2, "base_p": 12, "xp": 12},
    "피라니아": {"rarity": "Common", "min_w": 0.5, "max_w": 2.5, "base_p": 40, "xp": 40},
    "정어리": {"rarity": "Common", "min_w": 0.1, "max_w": 0.4, "base_p": 14, "xp": 16},

    # 2. Uncommon (8종)
    "배스": {"rarity": "Uncommon", "min_w": 1.0, "max_w": 4.0, "base_p": 60, "xp": 50},
    "메기": {"rarity": "Uncommon", "min_w": 2.0, "max_w": 6.0, "base_p": 90, "xp": 75},
    "가물치": {"rarity": "Uncommon", "min_w": 2.5, "max_w": 7.5, "base_p": 120, "xp": 95},
    "광어": {"rarity": "Uncommon", "min_w": 1.5, "max_w": 5.0, "base_p": 100, "xp": 80},
    "우럭": {"rarity": "Uncommon", "min_w": 1.2, "max_w": 4.5, "base_p": 85, "xp": 70},
    "연어": {"rarity": "Uncommon", "min_w": 3.0, "max_w": 9.0, "base_p": 140, "xp": 110},
    "방어": {"rarity": "Uncommon", "min_w": 4.0, "max_w": 12.0, "base_p": 180, "xp": 130},
    "삼치": {"rarity": "Uncommon", "min_w": 2.0, "max_w": 7.0, "base_p": 110, "xp": 90},

    # 3. Rare (7종)
    "비단잉어": {"rarity": "Rare", "min_w": 3.0, "max_w": 8.0, "base_p": 250, "xp": 180},
    "참돔": {"rarity": "Rare", "min_w": 3.5, "max_w": 10.0, "base_p": 320, "xp": 220},
    "감성돔": {"rarity": "Rare", "min_w": 2.5, "max_w": 7.0, "base_p": 290, "xp": 200},
    "다금바리": {"rarity": "Rare", "min_w": 5.0, "max_w": 15.0, "base_p": 500, "xp": 350},
    "청새치": {"rarity": "Rare", "min_w": 15.0, "max_w": 45.0, "base_p": 750, "xp": 480},
    "민어": {"rarity": "Rare", "min_w": 4.0, "max_w": 12.0, "base_p": 400, "xp": 280},
    "황새치": {"rarity": "Rare", "min_w": 20.0, "max_w": 50.0, "base_p": 800, "xp": 500},

    # 4. Epic (6종)
    "황금 잉어": {"rarity": "Epic", "min_w": 5.0, "max_w": 12.0, "base_p": 1200, "xp": 700},
    "심해 아귀": {"rarity": "Epic", "min_w": 8.0, "max_w": 25.0, "base_p": 1800, "xp": 950},
    "대왕 샐러맨더": {"rarity": "Epic", "min_w": 10.0, "max_w": 30.0, "base_p": 2300, "xp": 1200},
    "일렉트릭 뱀장어": {"rarity": "Epic", "min_w": 6.0, "max_w": 18.0, "base_p": 1600, "xp": 850},
    "크리스탈 가오리": {"rarity": "Epic", "min_w": 12.0, "max_w": 35.0, "base_p": 2800, "xp": 1400},
    "볼케이노 해마": {"rarity": "Epic", "min_w": 2.0, "max_w": 8.0, "base_p": 3200, "xp": 1600},

    # 5. Legendary (6종)
    "심해 펠리칸장어": {"rarity": "Legendary", "min_w": 15.0, "max_w": 40.0, "base_p": 5000, "xp": 2500},
    "아비스 블레이드": {"rarity": "Legendary", "min_w": 25.0, "max_w": 70.0, "base_p": 7500, "xp": 3200},
    "플라즈마 복어": {"rarity": "Legendary", "min_w": 10.0, "max_w": 30.0, "base_p": 9000, "xp": 3800},
    "프로스트 샤크": {"rarity": "Legendary", "min_w": 50.0, "max_w": 150.0, "base_p": 12000, "xp": 4500},
    "루비 메갈로돈": {"rarity": "Legendary", "min_w": 80.0, "max_w": 200.0, "base_p": 16000, "xp": 5500},
    "에메랄드 청새치": {"rarity": "Legendary", "min_w": 40.0, "max_w": 100.0, "base_p": 14000, "xp": 5000},

    # 6. Mythic (5종)
    "바다의 환영 발키리": {"rarity": "Mythic", "min_w": 100.0, "max_w": 300.0, "base_p": 25000, "xp": 8000},
    "신화의 히드라 해뱀": {"rarity": "Mythic", "min_w": 150.0, "max_w": 450.0, "base_p": 35000, "xp": 10000},
    "포세이돈의 삼지창어": {"rarity": "Mythic", "min_w": 80.0, "max_w": 250.0, "base_p": 45000, "xp": 12500},
    "성스러운 빛의 해마": {"rarity": "Mythic", "min_w": 30.0, "max_w": 90.0, "base_p": 55000, "xp": 15000},
    "타이탄 심해 대구": {"rarity": "Mythic", "min_w": 200.0, "max_w": 600.0, "base_p": 68000, "xp": 18000},

    # 7. Ancient (5종)
    "고대 씨라캔스": {"rarity": "Ancient", "min_w": 100.0, "max_w": 350.0, "base_p": 90000, "xp": 22000},
    "시공의 암모나이트": {"rarity": "Ancient", "min_w": 80.0, "max_w": 280.0, "base_p": 120000, "xp": 28000},
    "원시 던클레오스테우스": {"rarity": "Ancient", "min_w": 300.0, "max_w": 900.0, "base_p": 160000, "xp": 35000},
    "고대 리오플레우로돈": {"rarity": "Ancient", "min_w": 450.0, "max_w": 1200.0, "base_p": 210000, "xp": 42000},
    "빙하기 아노말로카리스": {"rarity": "Ancient", "min_w": 50.0, "max_w": 200.0, "base_p": 270000, "xp": 50000},

    # 8. Celestial (4종)
    "천상의 은하 가오리": {"rarity": "Celestial", "min_w": 300.0, "max_w": 800.0, "base_p": 380000, "xp": 65000},
    "세라핌 피쉬": {"rarity": "Celestial", "min_w": 150.0, "max_w": 500.0, "base_p": 500000, "xp": 80000},
    "스타더스트 고래": {"rarity": "Celestial", "min_w": 1000.0, "max_w": 3000.0, "base_p": 680000, "xp": 100000},
    "빛의 주권자 오라클": {"rarity": "Celestial", "min_w": 500.0, "max_w": 1500.0, "base_p": 900000, "xp": 130000},

    # 9. Cosmic (4종)
    "코스믹 퀘이사 피쉬": {"rarity": "Cosmic", "min_w": 800.0, "max_w": 2500.0, "base_p": 1300000, "xp": 170000},
    "블랙홀 스쿼드": {"rarity": "Cosmic", "min_w": 1200.0, "max_w": 4000.0, "base_p": 1800000, "xp": 220000},
    "초신성 라이어": {"rarity": "Cosmic", "min_w": 2000.0, "max_w": 6000.0, "base_p": 2500000, "xp": 300000},
    "차원 파쇄자 다크매터": {"rarity": "Cosmic", "min_w": 3500.0, "max_w": 9999.0, "base_p": 3500000, "xp": 400000},

    # 10. Boss (5종)
    "심해의 크라켄": {"rarity": "Boss", "min_w": 2000.0, "max_w": 6000.0, "base_p": 5000000, "xp": 550000},
    "천공의 고래": {"rarity": "Boss", "min_w": 4000.0, "max_w": 12000.0, "base_p": 8000000, "xp": 800000},
    "차원의 레비아탄": {"rarity": "Boss", "min_w": 8000.0, "max_w": 25000.0, "base_p": 12000000, "xp": 1200000},
    "종말의 요르문간드": {"rarity": "Boss", "min_w": 15000.0, "max_w": 45000.0, "base_p": 20000000, "xp": 1800000},
    "창세의 아우라드래곤": {"rarity": "Boss", "min_w": 30000.0, "max_w": 99999.0, "base_p": 35000000, "xp": 3000000}
}

TRAITS = [
    {"name": "일반", "mult": 1.0},
    {"name": "반짝이는", "mult": 1.5},
    {"name": "거대한", "mult": 1.8},
    {"name": "전설의", "mult": 3.0}
]

SHOP_BAITS = {
    "초강력 미끼": {"price": 100, "desc": "Uncommon / Rare 등급 등장 확률 증가"},
    "행운의 미끼": {"price": 150, "desc": "Epic / Legendary / Mythic 등급 등장 확정"},
    "황금 미끼": {"price": 300, "desc": "전설 특성 고정 및 골드 배수 적용"},
    "보스 미끼": {"price": 1000, "desc": "보스 물고기 출현 확률 100% 확정"}
}

# -----------------------------------------------------------------------------
# 2. 게임 세션 초기화
# -----------------------------------------------------------------------------
def init_game():
    if "level" not in st.session_state:
        st.session_state.level = 1
        st.session_state.xp = 0
        st.session_state.max_xp = 100
        st.session_state.gold = 100
        st.session_state.inventory = []
        st.session_state.baits = {
            "일반 미끼": float('inf'),
            "초강력 미끼": 0,
            "행운의 미끼": 0,
            "황금 미끼": 0,
            "보스 미끼": 0
        }
        st.session_state.equipped_rod = "대나무 낚시대"
        st.session_state.owned_rods = ["대나무 낚시대"]
        st.session_state.records = {name: 0 for name in FISH_BOOK_TEMPLATE.keys()}
        st.session_state.auto_fishing = False
        st.session_state.last_catch_msg = ""
        st.session_state.last_catch_status = "idle"

init_game()

# -----------------------------------------------------------------------------
# 3. Three.js 3D 실시간 바다 시뮬레이터 렌더러
# -----------------------------------------------------------------------------
def render_3d_ocean_view(status="idle"):
    html_code = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <style>
            body {{ margin: 0; overflow: hidden; background: #0f172a; font-family: sans-serif; }}
            #canvas-container {{ width: 100%; height: 350px; border-radius: 12px; overflow: hidden; position: relative; }}
            #ui-overlay {{ position: absolute; top: 10px; left: 10px; color: #00f0ff; font-size: 14px; font-weight: bold; background: rgba(0,0,0,0.5); padding: 6px 12px; border-radius: 6px; }}
        </style>
        <script src="https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js"></script>
    </head>
    <body>
        <div id="canvas-container">
            <div id="ui-overlay">🎮 3D REAL-TIME OCEAN ENGINE</div>
        </div>
        <script>
            const container = document.getElementById('canvas-container');
            const scene = new THREE.Scene();
            scene.background = new THREE.Color(0x0a1128);
            scene.fog = new THREE.FogExp2(0x0a1128, 0.03);

            const camera = new THREE.PerspectiveCamera(60, container.clientWidth / 350, 0.1, 1000);
            camera.position.set(0, 6, 12);
            camera.lookAt(0, 1, 0);

            const renderer = new THREE.WebGLRenderer({{ antialias: true }});
            renderer.setSize(container.clientWidth, 350);
            renderer.shadowMap.enabled = true;
            container.appendChild(renderer.domElement);

            const ambientLight = new THREE.AmbientLight(0xdff0ff, 0.7);
            scene.add(ambientLight);

            const dirLight = new THREE.DirectionalLight(0xffa500, 1.2);
            dirLight.position.set(10, 20, 10);
            dirLight.castShadow = true;
            scene.add(dirLight);

            const oceanGeo = new THREE.PlaneGeometry(40, 40, 40, 40);
            const oceanMat = new THREE.MeshPhongMaterial({{
                color: 0x006699,
                wireframe: true,
                transparent: true,
                opacity: 0.85,
                shininess: 80
            }});
            const ocean = new THREE.Mesh(oceanGeo, oceanMat);
            ocean.rotation.x = -Math.PI / 2;
            scene.add(ocean);

            const floatGroup = new THREE.Group();
            const floatGeo = new THREE.SphereGeometry(0.35, 16, 16);
            const floatMat = new THREE.MeshStandardMaterial({{ color: 0xff3300, roughness: 0.2 }});
            const floatMesh = new THREE.Mesh(floatGeo, floatMat);
            floatGroup.add(floatMesh);

            const topGeo = new THREE.CylinderGeometry(0.05, 0.05, 0.5, 8);
            const topMat = new THREE.MeshBasicMaterial({{ color: 0xffffff }});
            const topMesh = new THREE.Mesh(topGeo, topMat);
            topMesh.position.y = 0.3;
            floatGroup.add(topMesh);

            floatGroup.position.set(0, 0.2, 2);
            scene.add(floatGroup);

            const fishGeo = new THREE.ConeGeometry(0.3, 1, 8);
            fishGeo.rotateX(Math.PI / 2);
            const fishMat = new THREE.MeshBasicMaterial({{ color: 0x00f0ff, wireframe: true }});
            const fishMesh = new THREE.Mesh(fishGeo, fishMat);
            fishMesh.position.set(2, -0.5, 1);
            scene.add(fishMesh);

            let clock = new THREE.Clock();
            let status = "{status}";

            function animate() {{
                requestAnimationFrame(animate);
                let time = clock.getElapsedTime();

                const pos = oceanGeo.attributes.position;
                for (let i = 0; i < pos.count; i++) {{
                    let u = pos.getX(i);
                    let v = pos.getY(i);
                    let z = Math.sin(u * 0.8 + time * 2) * 0.25 + Math.cos(v * 0.8 + time * 1.5) * 0.25;
                    pos.setZ(i, z);
                }}
                pos.needsUpdate = true;

                if (status === "success") {{
                    floatGroup.position.y = Math.sin(time * 15) * 0.4 - 0.2;
                }} else if (status === "fail") {{
                    floatGroup.position.y = -1.5;
                }} else {{
                    floatGroup.position.y = Math.sin(time * 3) * 0.15 + 0.1;
                }}

                fishMesh.position.x = Math.sin(time * 1.2) * 3;
                fishMesh.position.z = Math.cos(time * 1.2) * 2 + 1;
                fishMesh.rotation.y = time * 1.2 + Math.PI / 2;

                renderer.render(scene, camera);
            }}
            animate();

            window.addEventListener('resize', () => {{
                camera.aspect = container.clientWidth / 350;
                camera.updateProjectionMatrix();
                renderer.setSize(container.clientWidth, 350);
            }});
        </script>
    </body>
    </html>
    """
    components.html(html_code, height=360)

# -----------------------------------------------------------------------------
# 4. 핵심 산출 및 확률 로직
# -----------------------------------------------------------------------------
def get_current_success_rate():
    rod_rate = FISHING_RODS[st.session_state.equipped_rod]["catch_rate"]
    lvl_bonus = (st.session_state.level - 1) * 0.5
    return min(99.0, rod_rate + lvl_bonus)

def add_xp(amount):
    rod_xp_mult = FISHING_RODS[st.session_state.equipped_rod]["exp_mult"]
    actual_xp = int(amount * rod_xp_mult)
    st.session_state.xp += actual_xp
    
    while st.session_state.xp >= st.session_state.max_xp:
        st.session_state.xp -= st.session_state.max_xp
        st.session_state.level += 1
        st.session_state.max_xp = int(st.session_state.max_xp * 1.5)
        st.toast(f"🎉 레벨업! 현재 레벨: Lv.{st.session_state.level}", icon="⭐")

def catch_fish(selected_bait):
    if st.session_state.baits[selected_bait] <= 0:
        st.session_state.last_catch_msg = "⚠️ 선택한 미끼가 부족하여 낚시를 중단합니다."
        st.session_state.auto_fishing = False
        st.session_state.last_catch_status = "idle"
        return False

    if selected_bait != "일반 미끼":
        st.session_state.baits[selected_bait] -= 1

    success_rate = get_current_success_rate()
    roll = random.uniform(0, 100)

    if roll > success_rate:
        st.session_state.last_catch_msg = f"💥 낚싯줄이 터졌거나 물고기가 도망쳤습니다! (성공률: {success_rate:.1f}%)"
        st.session_state.last_catch_status = "fail"
        return False

    rod_data = FISHING_RODS[st.session_state.equipped_rod]
    luck_score = (st.session_state.level * 1.5) + rod_data["rare_bonus"]
    rand_tier = random.uniform(0, 100) + (luck_score * 0.1)

    if selected_bait == "보스 미끼":
        target_rarity = "Boss"
    elif selected_bait == "행운의 미끼":
        target_rarity = random.choice(["Epic", "Legendary", "Mythic"])
    elif rand_tier >= 99.9:
        target_rarity = "Boss"
    elif rand_tier >= 99.5:
        target_rarity = "Cosmic"
    elif rand_tier >= 98.6:
        target_rarity = "Celestial"
    elif rand_tier >= 96.6:
        target_rarity = "Ancient"
    elif rand_tier >= 93.1:
        target_rarity = "Mythic"
    elif rand_tier >= 87.1:
        target_rarity = "Legendary"
    elif rand_tier >= 75.1:
        target_rarity = "Epic"
    elif rand_tier >= 55.1:
        target_rarity = "Rare"
    elif rand_tier >= 30.1:
        target_rarity = "Uncommon"
    else:
        target_rarity = "Common"

    candidates = [k for k, v in FISH_BOOK_TEMPLATE.items() if v["rarity"] == target_rarity]
    if not candidates:
        candidates = [k for k, v in FISH_BOOK_TEMPLATE.items() if v["rarity"] == "Common"]

    fish_name = random.choice(candidates)
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
        "rod_gold_mult": rod_data["gold_mult"],
        "xp": info["xp"],
        "rarity": info["rarity"]
    }

    st.session_state.inventory.append(caught_item)
    st.session_state.records[fish_name] += 1
    add_xp(info["xp"])
    
    st.session_state.last_catch_msg = f"🎣 [{info['rarity']}] {trait['name']} {fish_name} (을)를 잡았습니다! ({weight}kg)"
    st.session_state.last_catch_status = "success"
    return True

def sell_all_fish():
    if not st.session_state.inventory:
        st.warning("판매할 물고기가 없습니다.")
        return

    total = 0
    for fish in st.session_state.inventory:
        price = int(fish["base_price"] * fish["weight"] * fish["mult"] * fish.get("rod_gold_mult", 1.0))
        total += price

    st.session_state.gold += total
    st.session_state.inventory.clear()
    st.success(f"💰 모든 물고기를 판매하여 {total:,} 골드를 획득했습니다!")

# -----------------------------------------------------------------------------
# 5. 자동 낚시 전용 루프 (Fragment)
# -----------------------------------------------------------------------------
@st.fragment(run_every=2.5)
def auto_fishing_loop(selected_bait):
    if st.session_state.auto_fishing:
        catch_fish(selected_bait)
        st.rerun()

# -----------------------------------------------------------------------------
# 6. UI 화면 구성
# -----------------------------------------------------------------------------
st.title("🎣 판타지 낚시 게임 v4.0 (3D Engine Integrated)")

# 사이드바: 프로필 및 저장/불러오기
with st.sidebar:
    st.header("👤 플레이어 정보")
    st.write(f"**레벨:** Lv.{st.session_state.level}")
    st.progress(min(st.session_state.xp / st.session_state.max_xp, 1.0))
    st.caption(f"XP: {st.session_state.xp} / {st.session_state.max_xp}")
    st.write(f"**소지금:** {st.session_state.gold:,} G")
    st.write(f"**장착 중인 낚시대:** `{st.session_state.equipped_rod}`")
    
    st.divider()
    st.subheader("💾 게임 저장 / 불러오기")
    
    save_data = {
        "level": st.session_state.level,
        "xp": st.session_state.xp,
        "max_xp": st.session_state.max_xp,
        "gold": st.session_state.gold,
        "equipped_rod": st.session_state.equipped_rod,
        "owned_rods": st.session_state.owned_rods,
        "inventory": st.session_state.inventory,
        "baits": st.session_state.baits,
        "records": st.session_state.records
    }
    json_str = json.dumps(save_data, ensure_ascii=False, indent=2)
    st.download_button("💾 데이터 다운로드", data=json_str, file_name="fishing_save.json", mime="application/json")
    
    uploaded_file = st.file_uploader("📂 데이터 불러오기", type=["json"])
    if uploaded_file is not None:
        if st.button("파일 적용하기"):
            data = json.load(uploaded_file)
            st.session_state.level = data["level"]
            st.session_state.xp = data["xp"]
            st.session_state.max_xp = data["max_xp"]
            st.session_state.gold = data["gold"]
            st.session_state.equipped_rod = data.get("equipped_rod", "대나무 낚시대")
            st.session_state.owned_rods = data.get("owned_rods", ["대나무 낚시대"])
            st.session_state.inventory = data["inventory"]
            st.session_state.baits = data["baits"]
            st.session_state.records = data["records"]
            st.rerun()

# 메인 탭
tab1, tab2, tab3, tab4, tab5 = st.tabs(["🌊 3D 낚시터 (수동/자동)", "🎣 낚시대 상점", "🎒 가방 & 판매", "🛒 미끼 상점", "📖 물고기 도감"])

# --- TAB 1: 3D 낚시터 ---
with tab1:
    st.subheader("🌊 실시간 3D 바다 낚시터")
    
    render_3d_ocean_view(status=st.session_state.last_catch_status)

    equipped_info = FISHING_RODS[st.session_state.equipped_rod]
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("낚시 성공률", f"{get_current_success_rate():.1f}%")
    c2.metric("행운 수치", f"+{equipped_info['rare_bonus']}")
    c3.metric("골드 배수", f"{equipped_info['gold_mult']}x")
    c4.metric("XP 배수", f"{equipped_info['exp_mult']}x")

    st.divider()

    bait_options = []
    for b_name, count in st.session_state.baits.items():
        if count == float('inf'):
            bait_options.append(f"{b_name} (무제한)")
        else:
            bait_options.append(f"{b_name} ({count}개 보유)")
            
    selected_option = st.selectbox("사용할 미끼 선택", bait_options)
    selected_bait = selected_option.split(" (")[0]
    
    col_manual, col_auto = st.columns(2)
    
    with col_manual:
        if st.button("🎣 수동 찌 던지기", use_container_width=True):
            catch_fish(selected_bait)
            st.rerun()

    with col_auto:
        if not st.session_state.auto_fishing:
            if st.button("▶️ 자동 낚시 시작", use_container_width=True, type="primary"):
                st.session_state.auto_fishing = True
                st.rerun()
        else:
            if st.button("⏹️ 자동 낚시 정지", use_container_width=True):
                st.session_state.auto_fishing = False
                st.session_state.last_catch_status = "idle"
                st.rerun()

    if st.session_state.last_catch_msg:
        if "💥" in st.session_state.last_catch_msg or "⚠️" in st.session_state.last_catch_msg:
            st.error(st.session_state.last_catch_msg)
        else:
            st.success(st.session_state.last_catch_msg)

    if st.session_state.auto_fishing:
        st.info("🔄 자동 낚시 작동 중... (2.5초 간격)")
        auto_fishing_loop(selected_bait)

# --- TAB 2: 낚시대 상점 ---
with tab2:
    st.subheader("🎣 낚시대 상점 & 장비 관리 (총 20종)")
    for r_name, r_data in FISHING_RODS.items():
        is_owned = r_name in st.session_state.owned_rods
        is_equipped = st.session_state.equipped_rod == r_name
        
        ca, cb, cc = st.columns([2.5, 4, 1.5])
        with ca:
            st.write(f"### {r_name}")
            if is_equipped:
                st.caption("🟢 **장착 중**")
            elif is_owned:
                st.caption("🔵 **보유 중**")
            else:
                st.caption(f"가격: **{r_data['price']:,} G**")
        with cb:
            st.write(f"{r_data['desc']}")
            st.caption(f"성공률: {r_data['catch_rate']}% | 행운: +{r_data['rare_bonus']} | 골드: {r_data['gold_mult']}x | XP: {r_data['exp_mult']}x")
        with cc:
            if is_equipped:
                st.button("장착됨", key=f"eq_{r_name}", disabled=True)
            elif is_owned:
                if st.button("장착하기", key=f"use_{r_name}"):
                    st.session_state.equipped_rod = r_name
                    st.success(f"{r_name}(으)로 변경 완료!")
                    st.rerun()
            else:
                if st.button("구매", key=f"buy_rod_{r_name}"):
                    if st.session_state.gold >= r_data['price']:
                        st.session_state.gold -= r_data['price']
                        st.session_state.owned_rods.append(r_name)
                        st.session_state.equipped_rod = r_name
                        st.success(f"{r_name} 구매 및 장착 완료!")
                        st.rerun()
                    else:
                        st.error("골드가 부족합니다.")
        st.divider()

# --- TAB 3: 가방 & 판매 ---
with tab3:
    col_inv1, col_inv2 = st.columns([3, 1])
    with col_inv1:
        st.subheader(f"보유 중인 물고기 ({len(st.session_state.inventory)}마리)")
    with col_inv2:
        if st.button("💰 전체 판매하기", use_container_width=True):
            sell_all_fish()
            st.rerun()
            
    if st.session_state.inventory:
        for item in reversed(st.session_state.inventory):
            price = int(item["base_price"] * item["weight"] * item["mult"] * item.get("rod_gold_mult", 1.0))
            st.write(f"**[{item['rarity']}] {item['trait']} {item['name']}** | {item['weight']}kg | 판매가: {price:,} G")
    else:
        st.info("가방이 비어있습니다.")

# --- TAB 4: 미끼 상점 ---
with tab4:
    st.subheader("🛒 미끼 상점")
    for name, data in SHOP_BAITS.items():
        c_b1, c_b2, c_b3 = st.columns([2, 3, 1])
        with c_b1:
            st.write(f"**{name}**")
            st.caption(f"가격: {data['price']:,} G")
        with c_b2:
            st.write(f"{data['desc']}")
        with c_b3:
            if st.button("구매", key=f"buy_bait_{name}"):
                if st.session_state.gold >= data['price']:
                    st.session_state.gold -= data['price']
                    st.session_state.baits[name] += 1
                    st.success(f"{name} 구매 완료!")
                    st.rerun()
                else:
                    st.error("골드가 부족합니다.")

# --- TAB 5: 물고기 도감 ---
with tab5:
    st.subheader("📖 물고기 도감 (총 60종)")
    cols = st.columns(2)
    for idx, (name, info) in enumerate(FISH_BOOK_TEMPLATE.items()):
        caught_count = st.session_state.records.get(name, 0)
        with cols[idx % 2]:
            if caught_count > 0:
                is_boss = "👑 " if info["rarity"] == "Boss" else ""
                st.write(f"### {is_boss}{name}")
                st.caption(f"등급: **{info['rarity']}** | 잡은 횟수: **{caught_count}회** | 기준가: {info['base_p']:,} G")
            else:
                st.write("### ??? (미발견)")
                st.caption(f"등급: **{info['rarity']}** | 아직 발견하지 못한 물고기입니다.")
        st.divider()
