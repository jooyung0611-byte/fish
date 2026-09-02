import streamlit as st
import streamlit.components.v1 as components
import random
import json
import time

# -----------------------------------------------------------------------------
# 1. 앱 설정 및 기본 데이터베이스 정의
# -----------------------------------------------------------------------------
st.set_page_config(page_title="판타지 3D 낚시 게임 v6.0", page_icon="🎣", layout="wide")

# 20종 낚시대 데이터 (고유 외형 3D 스펙 및 테마 파티클 정의)
FISHING_RODS = {
    "대나무 낚시대": {"price": 0, "catch_rate": 60, "rare_bonus": 0, "exp_mult": 1.0, "gold_mult": 1.0, "color": 0x8b5a2b, "shape": "bamboo", "particle": "none", "desc": "가장 기본적이고 가벼운 대나무 낚시대."},
    "나무 낚시대": {"price": 250, "catch_rate": 63, "rare_bonus": 2, "exp_mult": 1.05, "gold_mult": 1.05, "color": 0xa0522d, "shape": "simple", "particle": "none", "desc": "조금 더 튼튼하게 깎아 만든 목재 낚시대."},
    "강화 글래스파이버": {"price": 700, "catch_rate": 66, "rare_bonus": 4, "exp_mult": 1.1, "gold_mult": 1.1, "color": 0x4682b4, "shape": "glass", "particle": "bubbles", "desc": "탄력성 높은 유리섬유 재질의 낚시대."},
    "카본 흑연 로드": {"price": 1500, "catch_rate": 70, "rare_bonus": 7, "exp_mult": 1.15, "gold_mult": 1.2, "color": 0x2f4f4f, "shape": "modern", "particle": "none", "desc": "가볍고 단단하여 입질 감지가 뛰어납니다."},
    "티타늄 스틸 로드": {"price": 3500, "catch_rate": 73, "rare_bonus": 10, "exp_mult": 1.2, "gold_mult": 1.3, "color": 0xc0c0c0, "shape": "heavy", "particle": "sparks", "desc": "어떤 중량급 물고기도 버티는 고강도 낚시대."},
    "네온 펄스 로드": {"price": 8000, "catch_rate": 76, "rare_bonus": 14, "exp_mult": 1.3, "gold_mult": 1.4, "color": 0x00ffcc, "shape": "neon_rings", "particle": "neon_glow", "desc": "야간 미끼 시야 확보에 특화된 네온 빛 로드."},
    "플래티넘 가디언": {"price": 18000, "catch_rate": 79, "rare_bonus": 18, "exp_mult": 1.4, "gold_mult": 1.5, "color": 0xe5e4e2, "shape": "guardian", "particle": "silver_dust", "desc": "백금 장식으로 기품이 느껴지는 고급 로드."},
    "다이아몬드 캐스터": {"price": 35000, "catch_rate": 82, "rare_bonus": 23, "exp_mult": 1.5, "gold_mult": 1.7, "color": 0xb9f2ff, "shape": "crystal", "particle": "glitter", "desc": "다이아몬드로 코팅되어 강도가 극대화된 로드."},
    "화염 드래곤 로드": {"price": 70000, "catch_rate": 85, "rare_bonus": 28, "exp_mult": 1.6, "gold_mult": 1.9, "color": 0xff3300, "shape": "dragon_horns", "particle": "fire", "desc": "드래곤의 숨결이 스며든 뜨거운 붉은 낚시대."},
    "빙결의 심해 로드": {"price": 120000, "catch_rate": 87, "rare_bonus": 34, "exp_mult": 1.7, "gold_mult": 2.1, "color": 0x00ffff, "shape": "ice_spikes", "particle": "snow", "desc": "차가운 기운으로 물고기의 방심을 유도합니다."},
    "뇌전의 수호자": {"price": 200000, "catch_rate": 89, "rare_bonus": 40, "exp_mult": 1.8, "gold_mult": 2.4, "color": 0xffff00, "shape": "lightning", "particle": "electric", "desc": "전기 파동으로 물고기를 빠르게 채어 올립니다."},
    "바람의 서곡": {"price": 350000, "catch_rate": 91, "rare_bonus": 47, "exp_mult": 2.0, "gold_mult": 2.7, "color": 0x7fffd4, "shape": "feather", "particle": "wind_swirl", "desc": "바람처럼 가벼워 입질 손실을 최소화합니다."},
    "그림자 포획자": {"price": 600000, "catch_rate": 92, "rare_bonus": 55, "exp_mult": 2.2, "gold_mult": 3.1, "color": 0x4b0082, "shape": "scythe", "particle": "shadow_smoke", "desc": "물고기에게 모습을 숨기는 은밀한 그림자 로드."},
    "천사의 은총": {"price": 1000000, "catch_rate": 93, "rare_bonus": 64, "exp_mult": 2.5, "gold_mult": 3.6, "color": 0xfff8dc, "shape": "wings", "particle": "holy_light", "desc": "천상의 빛으로 희귀 등급 물고기를 홀립니다."},
    "악마의 삼지창": {"price": 1600000, "catch_rate": 94, "rare_bonus": 74, "exp_mult": 2.8, "gold_mult": 4.2, "color": 0x800000, "shape": "trident", "particle": "hell_fire", "desc": "압도적인 파괴력으로 거대 몬스터를 제압합니다."},
    "시공간 균열 로드": {"price": 2500000, "catch_rate": 95, "rare_bonus": 85, "exp_mult": 3.2, "gold_mult": 5.0, "color": 0x9932cc, "shape": "portal_orb", "particle": "void_portal", "desc": "시공간을 뒤틀어 신비한 고대종을 끌어당깁니다."},
    "은하수 캐스케이드": {"price": 4000000, "catch_rate": 96, "rare_bonus": 98, "exp_mult": 3.7, "gold_mult": 6.0, "color": 0x4169e1, "shape": "galaxy_helix", "particle": "stardust", "desc": "별빛의 기운이 서려 있는 매혹적인 낚시대."},
    "코스믹 스타로드": {"price": 6500000, "catch_rate": 97, "rare_bonus": 115, "exp_mult": 4.3, "gold_mult": 7.5, "color": 0xff00ff, "shape": "star_staff", "particle": "cosmic_rays", "desc": "우주의 인력으로 물고기가 스스로 끌려옵니다."},
    "태양신 라의 분노": {"price": 10000000, "catch_rate": 98, "rare_bonus": 135, "exp_mult": 5.0, "gold_mult": 9.5, "color": 0xffd700, "shape": "sun_disc", "particle": "solar_flares", "desc": "태양의 축복을 받은 최고 등급 신화 낚시대."},
    "차원 창조주의 로드": {"price": 16000000, "catch_rate": 99, "rare_bonus": 160, "exp_mult": 6.0, "gold_mult": 12.0, "color": 0x00ffff, "shape": "creator_crown", "particle": "godly_aura", "desc": "모든 바다 생태계를 지배하는 신의 도구."}
}

# -----------------------------------------------------------------------------
# 60종 물고기 데이터베이스 (전설 이상 가격 및 크기 배수 대폭 하향 적용)
# -----------------------------------------------------------------------------
FISH_BOOK_TEMPLATE = {
    # 1. Common
    "피라미": {"rarity": "Common", "min_w": 0.1, "max_w": 0.5, "base_p": 1, "xp": 15},
    "붕어": {"rarity": "Common", "min_w": 0.5, "max_w": 2.0, "base_p": 2, "xp": 25},
    "송사리": {"rarity": "Common", "min_w": 0.05, "max_w": 0.3, "base_p": 1, "xp": 10},
    "망둥어": {"rarity": "Common", "min_w": 0.2, "max_w": 0.8, "base_p": 2, "xp": 20},
    "미꾸라지": {"rarity": "Common", "min_w": 0.1, "max_w": 0.6, "base_p": 1, "xp": 18},
    "블루길": {"rarity": "Common", "min_w": 0.4, "max_w": 1.5, "base_p": 3, "xp": 30},
    "꺽지": {"rarity": "Common", "min_w": 0.3, "max_w": 1.2, "base_p": 3, "xp": 35},
    "빙어": {"rarity": "Common", "min_w": 0.05, "max_w": 0.2, "base_p": 1, "xp": 12},
    "피라니아": {"rarity": "Common", "min_w": 0.5, "max_w": 2.5, "base_p": 4, "xp": 40},
    "정어리": {"rarity": "Common", "min_w": 0.1, "max_w": 0.4, "base_p": 1, "xp": 16},

    # 2. Uncommon
    "배스": {"rarity": "Uncommon", "min_w": 1.0, "max_w": 4.0, "base_p": 5, "xp": 50},
    "메기": {"rarity": "Uncommon", "min_w": 2.0, "max_w": 6.0, "base_p": 8, "xp": 75},
    "가물치": {"rarity": "Uncommon", "min_w": 2.5, "max_w": 7.5, "base_p": 10, "xp": 95},
    "광어": {"rarity": "Uncommon", "min_w": 1.5, "max_w": 5.0, "base_p": 9, "xp": 80},
    "우럭": {"rarity": "Uncommon", "min_w": 1.2, "max_w": 4.5, "base_p": 7, "xp": 70},
    "연어": {"rarity": "Uncommon", "min_w": 3.0, "max_w": 9.0, "base_p": 12, "xp": 110},
    "방어": {"rarity": "Uncommon", "min_w": 4.0, "max_w": 12.0, "base_p": 15, "xp": 130},
    "삼치": {"rarity": "Uncommon", "min_w": 2.0, "max_w": 7.0, "base_p": 10, "xp": 90},

    # 3. Rare
    "비단잉어": {"rarity": "Rare", "min_w": 3.0, "max_w": 8.0, "base_p": 20, "xp": 180},
    "참돔": {"rarity": "Rare", "min_w": 3.5, "max_w": 10.0, "base_p": 25, "xp": 220},
    "감성돔": {"rarity": "Rare", "min_w": 2.5, "max_w": 7.0, "base_p": 22, "xp": 200},
    "다금바리": {"rarity": "Rare", "min_w": 5.0, "max_w": 15.0, "base_p": 35, "xp": 350},
    "청새치": {"rarity": "Rare", "min_w": 15.0, "max_w": 45.0, "base_p": 50, "xp": 480},
    "민어": {"rarity": "Rare", "min_w": 4.0, "max_w": 12.0, "base_p": 30, "xp": 280},
    "황새치": {"rarity": "Rare", "min_w": 20.0, "max_w": 50.0, "base_p": 60, "xp": 500},

    # 4. Epic
    "황금 잉어": {"rarity": "Epic", "min_w": 5.0, "max_w": 12.0, "base_p": 80, "xp": 700},
    "심해 아귀": {"rarity": "Epic", "min_w": 8.0, "max_w": 25.0, "base_p": 120, "xp": 950},
    "대왕 샐러맨더": {"rarity": "Epic", "min_w": 10.0, "max_w": 30.0, "base_p": 150, "xp": 1200},
    "일렉트릭 뱀장어": {"rarity": "Epic", "min_w": 6.0, "max_w": 18.0, "base_p": 110, "xp": 850},
    "크리스탈 가오리": {"rarity": "Epic", "min_w": 12.0, "max_w": 35.0, "base_p": 180, "xp": 1400},
    "볼케이노 해마": {"rarity": "Epic", "min_w": 2.0, "max_w": 8.0, "base_p": 200, "xp": 1600},

    # 5. Legendary (대폭 하락)
    "심해 펠리칸장어": {"rarity": "Legendary", "min_w": 15.0, "max_w": 40.0, "base_p": 45, "xp": 2500},
    "아비스 블레이드": {"rarity": "Legendary", "min_w": 25.0, "max_w": 70.0, "base_p": 55, "xp": 3200},
    "플라즈마 복어": {"rarity": "Legendary", "min_w": 10.0, "max_w": 30.0, "base_p": 60, "xp": 3800},
    "프로스트 샤크": {"rarity": "Legendary", "min_w": 50.0, "max_w": 150.0, "base_p": 75, "xp": 4500},
    "루비 메갈로돈": {"rarity": "Legendary", "min_w": 80.0, "max_w": 200.0, "base_p": 90, "xp": 5500},
    "에메랄드 청새치": {"rarity": "Legendary", "min_w": 40.0, "max_w": 100.0, "base_p": 80, "xp": 5000},

    # 6. Mythic (대폭 하락)
    "바다의 환영 발키리": {"rarity": "Mythic", "min_w": 100.0, "max_w": 300.0, "base_p": 120, "xp": 8000},
    "신화의 히드라 해뱀": {"rarity": "Mythic", "min_w": 150.0, "max_w": 450.0, "base_p": 150, "xp": 10000},
    "포세이돈의 삼지창어": {"rarity": "Mythic", "min_w": 80.0, "max_w": 250.0, "base_p": 180, "xp": 12500},
    "성스러운 빛의 해마": {"rarity": "Mythic", "min_w": 30.0, "max_w": 90.0, "base_p": 210, "xp": 15000},
    "타이탄 심해 대구": {"rarity": "Mythic", "min_w": 200.0, "max_w": 600.0, "base_p": 250, "xp": 18000},

    # 7. Ancient (대폭 하락)
    "고대 씨라캔스": {"rarity": "Ancient", "min_w": 100.0, "max_w": 350.0, "base_p": 320, "xp": 22000},
    "시공의 암모나이트": {"rarity": "Ancient", "min_w": 80.0, "max_w": 280.0, "base_p": 380, "xp": 28000},
    "원시 던클레오스테우스": {"rarity": "Ancient", "min_w": 300.0, "max_w": 900.0, "base_p": 450, "xp": 35000},
    "고대 리오플레우로돈": {"rarity": "Ancient", "min_w": 450.0, "max_w": 1200.0, "base_p": 520, "xp": 42000},
    "빙하기 아노말로카리스": {"rarity": "Ancient", "min_w": 50.0, "max_w": 200.0, "base_p": 600, "xp": 50000},

    # 8. Celestial (대폭 하락)
    "천상의 은하 가오리": {"rarity": "Celestial", "min_w": 300.0, "max_w": 800.0, "base_p": 750, "xp": 65000},
    "세라핌 피쉬": {"rarity": "Celestial", "min_w": 150.0, "max_w": 500.0, "base_p": 900, "xp": 80000},
    "스타더스트 고래": {"rarity": "Celestial", "min_w": 1000.0, "max_w": 3000.0, "base_p": 1100, "xp": 100000},
    "빛의 주권자 오라클": {"rarity": "Celestial", "min_w": 500.0, "max_w": 1500.0, "base_p": 1350, "xp": 130000},

    # 9. Cosmic (대폭 하락)
    "코스믹 퀘이사 피쉬": {"rarity": "Cosmic", "min_w": 800.0, "max_w": 2500.0, "base_p": 1600, "xp": 170000},
    "블랙홀 스쿼드": {"rarity": "Cosmic", "min_w": 1200.0, "max_w": 4000.0, "base_p": 2000, "xp": 220000},
    "초신성 라이어": {"rarity": "Cosmic", "min_w": 2000.0, "max_w": 6000.0, "base_p": 2500, "xp": 300000},
    "차원 파쇄자 다크매터": {"rarity": "Cosmic", "min_w": 3500.0, "max_w": 9999.0, "base_p": 3200, "xp": 400000},

    # 10. Boss (대폭 하락)
    "심해의 크라켄": {"rarity": "Boss", "min_w": 2000.0, "max_w": 6000.0, "base_p": 4500, "xp": 550000},
    "천공의 고래": {"rarity": "Boss", "min_w": 4000.0, "max_w": 12000.0, "base_p": 6000, "xp": 800000},
    "차원의 레비아탄": {"rarity": "Boss", "min_w": 8000.0, "max_w": 25000.0, "base_p": 8000, "xp": 1200000},
    "종말의 요르문간드": {"rarity": "Boss", "min_w": 15000.0, "max_w": 45000.0, "base_p": 10000, "xp": 1800000},
    "창세의 아우라드래곤": {"rarity": "Boss", "min_w": 30000.0, "max_w": 99999.0, "base_p": 15000, "xp": 3000000}
}

TRAITS = [
    {"name": "일반", "mult": 1.0},
    {"name": "반짝이는", "mult": 1.2},
    {"name": "거대한", "mult": 1.3},
    {"name": "전설의", "mult": 1.5}
]

SHOP_BAITS = {
    "초강력 미끼": {"price": 2500, "desc": "Uncommon / Rare 등급 등장 확률 증가"},
    "행운의 미끼": {"price": 12000, "desc": "Epic / Legendary / Mythic 등급 등장 확정"},
    "황금 미끼": {"price": 55000, "desc": "전설 특성 고정 및 골드 배수 적용"},
    "보스 미끼": {"price": 200000, "desc": "보스 물고기 출현 확률 100% 확정"}
}

# -----------------------------------------------------------------------------
# 2. 게임 세션 초기화
# -----------------------------------------------------------------------------
def init_game():
    if "level" not in st.session_state:
        st.session_state.level = 1
        st.session_state.xp = 0
        st.session_state.max_xp = 100
        st.session_state.gold = 10000  # 업그레이드 테스트용 초기 자금
        st.session_state.inventory = []
        st.session_state.max_inventory = 5  # 기본 5칸 제한
        st.session_state.inventory_upgrades = 0
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
        st.session_state.fishing_state = "idle"  # idle -> biting (3초 대기) -> caught
        st.session_state.pending_fish = None

init_game()

def get_inventory_upgrade_cost():
    # 시작 비용 1만원, 1.5배의 레벨제곱 (10000 * 1.5^level)
    return int(10000 * (1.5 ** st.session_state.inventory_upgrades))

# -----------------------------------------------------------------------------
# 3. Three.js 3D 고급 시뮬레이터 렌더러 (20종 외형 & 파티클 & 찌 변경)
# -----------------------------------------------------------------------------
def render_3d_ocean_view(status="idle", rod_name="대나무 낚시대", bait_name="일반 미끼", pending_fish=None):
    rod_data = FISHING_RODS.get(rod_name, FISHING_RODS["대나무 낚시대"])
    rod_color_hex = hex(rod_data["color"])
    rod_shape = rod_data["shape"]
    rod_particle = rod_data["particle"]

    # 물고기 등급/크기 스펙 전달
    fish_rarity = pending_fish["rarity"] if pending_fish else "Common"
    fish_weight = pending_fish["weight"] if pending_fish else 1.0

    html_code = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <style>
            body {{ margin: 0; overflow: hidden; background: #0f172a; font-family: sans-serif; }}
            #canvas-container {{ width: 100%; height: 420px; border-radius: 12px; overflow: hidden; position: relative; }}
            #ui-overlay {{ position: absolute; top: 10px; left: 10px; color: #00f0ff; font-size: 14px; font-weight: bold; background: rgba(0,0,0,0.6); padding: 6px 12px; border-radius: 6px; border: 1px solid rgba(0,240,255,0.3); }}
            #rod-info {{ position: absolute; bottom: 10px; right: 10px; color: #ffffff; font-size: 13px; background: rgba(0,0,0,0.7); padding: 6px 12px; border-radius: 6px; }}
            #status-banner {{ position: absolute; top: 50%; left: 50%; transform: translate(-50%, -50%); color: #ffeb3b; font-size: 24px; font-weight: bold; text-shadow: 0 0 10px #000; display: none; pointer-events: none; }}
        </style>
        <script src="https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js"></script>
    </head>
    <body>
        <div id="canvas-container">
            <div id="ui-overlay">🎮 3D ADVANCED REAL-TIME FISHING ENGINE</div>
            <div id="status-banner" id="banner">🚨 물고기가 찌를 건드리고 있습니다! (3초 대기) 🚨</div>
            <div id="rod-info">🎣 {rod_name} | 🪱 {bait_name}</div>
        </div>
        <script>
            const container = document.getElementById('canvas-container');
            const scene = new THREE.Scene();
            scene.background = new THREE.Color(0x0a1128);
            scene.fog = new THREE.FogExp2(0x0a1128, 0.02);

            const camera = new THREE.PerspectiveCamera(60, container.clientWidth / 420, 0.1, 1000);
            camera.position.set(0, 4, 10);
            camera.lookAt(0, 1, 0);

            const renderer = new THREE.WebGLRenderer({{ antialias: true }});
            renderer.setSize(container.clientWidth, 420);
            renderer.shadowMap.enabled = true;
            container.appendChild(renderer.domElement);

            const ambientLight = new THREE.AmbientLight(0xdff0ff, 0.8);
            scene.add(ambientLight);

            const dirLight = new THREE.DirectionalLight(0xffa500, 1.2);
            dirLight.position.set(10, 20, 10);
            scene.add(dirLight);

            // 바다
            const oceanGeo = new THREE.PlaneGeometry(60, 60, 45, 45);
            const oceanMat = new THREE.MeshPhongMaterial({{
                color: 0x003366,
                wireframe: true,
                transparent: true,
                opacity: 0.85,
                shininess: 90
            }});
            const ocean = new THREE.Mesh(oceanGeo, oceanMat);
            ocean.rotation.x = -Math.PI / 2;
            scene.add(ocean);

            // --- 20종 낚시대 고유 모델 빌드 ---
            const rodGroup = new THREE.Group();
            const rodColor = {rod_color_hex};
            const shapeType = "{rod_shape}";

            // 손잡이
            const handleGeo = new THREE.CylinderGeometry(0.12, 0.15, 1.3, 16);
            const handleMat = new THREE.MeshStandardMaterial({{ color: 0x1f1f1f, roughness: 0.7 }});
            const handleMesh = new THREE.Mesh(handleGeo, handleMat);
            handleMesh.position.set(0, -0.65, 0);
            rodGroup.add(handleMesh);

            // 메인 로드
            const mainRodGeo = new THREE.CylinderGeometry(0.03, 0.09, 4.8, 16);
            const mainRodMat = new THREE.MeshStandardMaterial({{ color: rodColor, metalness: 0.7, roughness: 0.2, emissive: rodColor, emissiveIntensity: 0.25 }});
            const mainRodMesh = new THREE.Mesh(mainRodGeo, mainRodMat);
            mainRodMesh.position.set(0, 2.2, 0);
            rodGroup.add(mainRodMesh);

            // 외형 커스텀 쉐이프
            if (shapeType === "bamboo") {{
                for(let b=0; b<5; b++) {{
                    const nodeGeo = new THREE.TorusGeometry(0.07 - b*0.008, 0.02, 8, 16);
                    const nodeMat = new THREE.MeshBasicMaterial({{ color: 0x5c3a21 }});
                    const node = new THREE.Mesh(nodeGeo, nodeMat);
                    node.position.set(0, b * 0.9, 0);
                    node.rotation.x = Math.PI / 2;
                    rodGroup.add(node);
                }}
            }} else if (shapeType === "trident" || shapeType === "dragon_horns") {{
                const hornGeo = new THREE.ConeGeometry(0.1, 1.0, 8);
                const hornMat = new THREE.MeshStandardMaterial({{ color: rodColor, metalness: 0.9 }});
                const h1 = new THREE.Mesh(hornGeo, hornMat); h1.position.set(-0.25, 4.4, 0); h1.rotation.z = -0.3;
                const h2 = new THREE.Mesh(hornGeo, hornMat); h2.position.set(0.25, 4.4, 0); h2.rotation.z = 0.3;
                rodGroup.add(h1); rodGroup.add(h2);
            }} else if (shapeType === "wings" || shapeType === "feather") {{
                const wingGeo = new THREE.BoxGeometry(0.02, 1.2, 0.4);
                const wingMat = new THREE.MeshStandardMaterial({{ color: 0xffffff, transparent: true, opacity: 0.8 }});
                const w1 = new THREE.Mesh(wingGeo, wingMat); w1.position.set(-0.2, 2.5, 0); w1.rotation.z = 0.4;
                const w2 = new THREE.Mesh(wingGeo, wingMat); w2.position.set(0.2, 2.5, 0); w2.rotation.z = -0.4;
                rodGroup.add(w1); rodGroup.add(w2);
            }} else if (shapeType === "neon_rings" || shapeType === "portal_orb") {{
                const ringGeo = new THREE.TorusGeometry(0.3, 0.03, 16, 32);
                const ringMat = new THREE.MeshBasicMaterial({{ color: rodColor }});
                const ring = new THREE.Mesh(ringGeo, ringMat);
                ring.position.set(0, 3.5, 0);
                rodGroup.add(ring);
            }}

            rodGroup.position.set(2.2, -0.5, 6.0);
            rodGroup.rotation.x = -Math.PI / 6;
            rodGroup.rotation.z = -Math.PI / 8;
            scene.add(rodGroup);

            // --- 테마별 파티클 시스템 ---
            const pCount = 60;
            const pGeo = new THREE.BufferGeometry();
            const pPos = new Float32Array(pCount * 3);
            for(let i=0; i<pCount*3; i++) {{
                pPos[i] = (Math.random() - 0.5) * 2;
            }}
            pGeo.setAttribute('position', new THREE.BufferAttribute(pPos, 3));
            const pMat = new THREE.PointsMaterial({{ size: 0.08, color: rodColor, transparent: true, opacity: 0.8 }});
            const particles = new THREE.Points(pGeo, pMat);
            particles.position.set(2.2, 2.0, 6.0);
            scene.add(particles);

            // --- 선택된 미끼에 따른 찌 모양 변경 ---
            const baitType = "{bait_name}";
            const floatGroup = new THREE.Group();
            let floatMesh;

            if (baitType === "초강력 미끼") {{
                const geo = new THREE.OctahedronGeometry(0.25);
                const mat = new THREE.MeshStandardMaterial({{ color: 0x00ff00, metalness: 0.5 }});
                floatMesh = new THREE.Mesh(geo, mat);
            }} else if (baitType === "행운의 미끼") {{
                const geo = new THREE.IcosahedronGeometry(0.25);
                const mat = new THREE.MeshStandardMaterial({{ color: 0xff00ff, roughness: 0.1 }});
                floatMesh = new THREE.Mesh(geo, mat);
            }} else if (baitType === "황금 미끼") {{
                const geo = new THREE.BoxGeometry(0.3, 0.3, 0.3);
                const mat = new THREE.MeshStandardMaterial({{ color: 0xffd700, metalness: 0.9, roughness: 0.1 }});
                floatMesh = new THREE.Mesh(geo, mat);
            }} else if (baitType === "보스 미끼") {{
                const geo = new THREE.DodecahedronGeometry(0.35);
                const mat = new THREE.MeshStandardMaterial({{ color: 0xff1100, emissive: 0x550000 }});
                floatMesh = new THREE.Mesh(geo, mat);
            }} else {{ // 일반 미끼
                const geo = new THREE.SphereGeometry(0.22, 16, 16);
                const mat = new THREE.MeshStandardMaterial({{ color: 0xff3300 }});
                floatMesh = new THREE.Mesh(geo, mat);
            }}
            floatGroup.add(floatMesh);
            floatGroup.position.set(0, 0.1, 1.5);
            scene.add(floatGroup);

            // 낚싯줄
            const lineMat = new THREE.LineBasicMaterial({{ color: 0xffffff, transparent: true, opacity: 0.6 }});
            const lineGeo = new THREE.BufferGeometry();
            lineGeo.setAttribute('position', new THREE.BufferAttribute(new Float32Array(6), 3));
            const fishingLine = new THREE.Line(lineGeo, lineMat);
            scene.add(fishingLine);

            // --- 등급 및 크기(무게)에 따른 물고기 모델 생성 ---
            const rarity = "{fish_rarity}";
            const weight = {fish_weight};
            
            // 크기에 따른 스케일 계산
            let scaleBase = 0.3 + Math.log10(Math.max(1, weight)) * 0.25;
            if (rarity === "Boss") scaleBase *= 1.8;
            else if (rarity === "Cosmic" || rarity === "Celestial") scaleBase *= 1.4;

            const fishGroup = new THREE.Group();
            const fBodyGeo = new THREE.ConeGeometry(0.3 * scaleBase, 1.2 * scaleBase, 8);
            fBodyGeo.rotateX(Math.PI / 2);
            
            let fColor = 0x00f0ff;
            if (rarity === "Epic") fColor = 0xa020f0;
            else if (rarity === "Legendary") fColor = 0xffa500;
            else if (rarity === "Mythic" || rarity === "Ancient") fColor = 0xff0055;
            else if (rarity === "Boss") fColor = 0xff0000;

            const fMat = new THREE.MeshStandardMaterial({{ color: fColor, wireframe: true, emissive: fColor, emissiveIntensity: 0.3 }});
            const fMesh = new THREE.Mesh(fBodyGeo, fMat);
            fishGroup.add(fMesh);
            fishGroup.position.set(2, -0.8, 1.5);
            scene.add(fishGroup);

            let clock = new THREE.Clock();
            let status = "{status}";

            function animate() {{
                requestAnimationFrame(animate);
                let time = clock.getElapsedTime();

                // 파도 애니메이션
                const pos = oceanGeo.attributes.position;
                for (let i = 0; i < pos.count; i++) {{
                    let u = pos.getX(i);
                    let v = pos.getY(i);
                    pos.setZ(i, Math.sin(u * 0.6 + time * 2) * 0.15 + Math.cos(v * 0.6 + time * 1.5) * 0.15);
                }}
                pos.needsUpdate = true;

                // 파티클 회전
                particles.rotation.y = time * 0.5;

                // --- 낚시 상태별 애니메이션 (입질 및 찌 건드리는 모션) ---
                if (status === "biting") {{
                    document.getElementById("status-banner").style.display = "block";
                    
                    // 물고기가 찌 주위를 빙글빙글 돌며 건드림
                    let touchFreq = (rarity === "Boss" || rarity === "Cosmic") ? 12 : 6;
                    let approachDist = Math.sin(time * touchFreq) * (0.4 * scaleBase);
                    
                    fishGroup.position.x = floatGroup.position.x + Math.cos(time * 5) * (0.6 + approachDist);
                    fishGroup.position.z = floatGroup.position.z + Math.sin(time * 5) * (0.6 + approachDist);
                    fishGroup.position.y = -0.4 + Math.sin(time * touchFreq) * 0.2;

                    // 찌가 물고기 건드림에 반응하여 출렁거림
                    floatGroup.position.y = Math.sin(time * touchFreq) * (0.15 * scaleBase) - 0.1;
                    rodGroup.rotation.x = -Math.PI / 6 + Math.sin(time * touchFreq) * 0.03;

                }} else if (status === "success") {{
                    document.getElementById("status-banner").style.display = "none";
                    floatGroup.position.y = Math.sin(time * 18) * 0.3 - 0.2;
                    rodGroup.rotation.x = -Math.PI / 6 + Math.sin(time * 15) * 0.05;
                    fishGroup.position.set(floatGroup.position.x, floatGroup.position.y - 0.5, floatGroup.position.z);
                }} else if (status === "fail") {{
                    document.getElementById("status-banner").style.display = "none";
                    floatGroup.position.y = -1.5;
                    rodGroup.rotation.x = -Math.PI / 4;
                    fishGroup.position.y = -3.0;
                }} else {{
                    document.getElementById("status-banner").style.display = "none";
                    floatGroup.position.y = Math.sin(time * 3) * 0.08 + 0.05;
                    rodGroup.rotation.x = -Math.PI / 6 + Math.sin(time * 1.5) * 0.02;
                    
                    // 평상시 서성임
                    fishGroup.position.x = Math.sin(time * 1.2) * 3;
                    fishGroup.position.z = Math.cos(time * 1.2) * 2 + 1;
                }}

                // 낚싯줄 연결 위치 업데이터
                const rodTipWorldPos = new THREE.Vector3(0, 4.4, 0);
                rodGroup.localToWorld(rodTipWorldPos);
                const linePositions = fishingLine.geometry.attributes.position.array;
                linePositions[0] = rodTipWorldPos.x; linePositions[1] = rodTipWorldPos.y; linePositions[2] = rodTipWorldPos.z;
                linePositions[3] = floatGroup.position.x; linePositions[4] = floatGroup.position.y + 0.2; linePositions[5] = floatGroup.position.z;
                fishingLine.geometry.attributes.position.needsUpdate = true;

                renderer.render(scene, camera);
            }}
            animate();

            window.addEventListener('resize', () => {{
                camera.aspect = container.clientWidth / 420;
                camera.updateProjectionMatrix();
                renderer.setSize(container.clientWidth, 420);
            }});
        </script>
    </body>
    </html>
    """
    components.html(html_code, height=430)

# -----------------------------------------------------------------------------
# 4. 핵심 낚시 로직 및 가격 산출식
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

def prepare_fish(selected_bait):
    # 인벤토리 가득 참 검사
    if len(st.session_state.inventory) >= st.session_state.max_inventory:
        st.session_state.last_catch_msg = "⚠️ 가방이 가득 찼습니다! 물고기를 판매하거나 인벤토리를 업그레이드하세요."
        st.session_state.auto_fishing = False
        st.session_state.last_catch_status = "idle"
        st.session_state.fishing_state = "idle"
        return False

    if st.session_state.baits[selected_bait] <= 0:
        st.session_state.last_catch_msg = "⚠️ 선택한 미끼가 부족하여 낚시를 진행할 수 없습니다."
        st.session_state.auto_fishing = False
        st.session_state.last_catch_status = "idle"
        st.session_state.fishing_state = "idle"
        return False

    if selected_bait != "일반 미끼":
        st.session_state.baits[selected_bait] -= 1

    rod_data = FISHING_RODS[st.session_state.equipped_rod]
    luck_score = (st.session_state.level * 1.5) + rod_data["rare_bonus"]
    rand_tier = random.uniform(0, 100) + (luck_score * 0.1)

    if selected_bait == "보스 미끼": target_rarity = "Boss"
    elif selected_bait == "행운의 미끼": target_rarity = random.choice(["Epic", "Legendary", "Mythic"])
    elif rand_tier >= 99.9: target_rarity = "Boss"
    elif rand_tier >= 99.5: target_rarity = "Cosmic"
    elif rand_tier >= 98.6: target_rarity = "Celestial"
    elif rand_tier >= 96.6: target_rarity = "Ancient"
    elif rand_tier >= 93.1: target_rarity = "Mythic"
    elif rand_tier >= 87.1: target_rarity = "Legendary"
    elif rand_tier >= 75.1: target_rarity = "Epic"
    elif rand_tier >= 55.1: target_rarity = "Rare"
    elif rand_tier >= 30.1: target_rarity = "Uncommon"
    else: target_rarity = "Common"

    candidates = [k for k, v in FISH_BOOK_TEMPLATE.items() if v["rarity"] == target_rarity]
    if not candidates: candidates = [k for k, v in FISH_BOOK_TEMPLATE.items() if v["rarity"] == "Common"]

    fish_name = random.choice(candidates)
    info = FISH_BOOK_TEMPLATE[fish_name]
    weight = round(random.uniform(info["min_w"], info["max_w"]), 2)
    trait = random.choice(TRAITS)

    if selected_bait == "황금 미끼":
        trait = {"name": "전설의", "mult": 1.5}

    st.session_state.pending_fish = {
        "name": fish_name,
        "weight": weight,
        "trait": trait["name"],
        "mult": trait["mult"],
        "base_price": info["base_p"],
        "rod_gold_mult": rod_data["gold_mult"],
        "xp": info["xp"],
        "rarity": info["rarity"]
    }
    
    st.session_state.fishing_state = "biting"
    st.session_state.last_catch_status = "biting"
    st.session_state.last_catch_msg = "🚨 찌가 강하게 흔들립니다! 물고기가 입질 중입니다..."
    return True

def finalize_catch():
    success_rate = get_current_success_rate()
    roll = random.uniform(0, 100)

    if roll > success_rate:
        st.session_state.last_catch_msg = f"💥 낚싯줄이 터졌거나 물고기가 도망쳤습니다! (성공률: {success_rate:.1f}%)"
        st.session_state.last_catch_status = "fail"
    else:
        item = st.session_state.pending_fish
        st.session_state.inventory.append(item)
        st.session_state.records[item["name"]] += 1
        add_xp(item["xp"])
        st.session_state.last_catch_msg = f"🎉 [{item['rarity']}] {item['trait']} {item['name']} (을)를 낚았습니다! ({item['weight']}kg)"
        st.session_state.last_catch_status = "success"

    st.session_state.pending_fish = None
    st.session_state.fishing_state = "idle"

def calculate_fish_price(fish):
    # 무게/크기 배수 대폭 낮춤 (제곱근 보정 적용)
    weight_factor = (fish["weight"] ** 0.5)
    price = int(fish["base_price"] * weight_factor * fish["mult"] * fish.get("rod_gold_mult", 1.0))
    return max(1, price)

def sell_all_fish():
    if not st.session_state.inventory:
        st.warning("판매할 물고기가 없습니다.")
        return

    total = sum(calculate_fish_price(f) for f in st.session_state.inventory)
    st.session_state.gold += total
    st.session_state.inventory.clear()
    st.success(f"💰 모든 물고기를 판매하여 {total:,} 골드를 획득했습니다!")

# -----------------------------------------------------------------------------
# 5. UI 화면 구성 및 입질 3초 타이머 처리
# -----------------------------------------------------------------------------
st.title("🎣 판타지 3D 낚시 게임 v6.0")

# 사이드바
with st.sidebar:
    st.header("👤 플레이어 정보")
    st.write(f"**레벨:** Lv.{st.session_state.level}")
    st.progress(min(st.session_state.xp / st.session_state.max_xp, 1.0))
    st.caption(f"XP: {st.session_state.xp} / {st.session_state.max_xp}")
    st.write(f"**소지금:** {st.session_state.gold:,} G")
    st.write(f"**장착 중인 낚시대:** `{st.session_state.equipped_rod}`")
    
    st.divider()
    st.subheader("🎒 인벤토리 관리")
    st.write(f"**용량:** {len(st.session_state.inventory)} / {st.session_state.max_inventory} 칸")
    
    cost = get_inventory_upgrade_cost()
    if st.button(f"➕ 인벤토리 +5칸 확장 ({cost:,} G)"):
        if st.session_state.gold >= cost:
            st.session_state.gold -= cost
            st.session_state.max_inventory += 5
            st.session_state.inventory_upgrades += 1
            st.success("인벤토리 용량이 +5칸 확장되었습니다!")
            st.rerun()
        else:
            st.error("골드가 부족합니다.")

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
        "max_inventory": st.session_state.max_inventory,
        "inventory_upgrades": st.session_state.inventory_upgrades,
        "baits": st.session_state.baits,
        "records": st.session_state.records
    }
    json_str = json.dumps(save_data, ensure_ascii=False, indent=2)
    st.download_button("💾 데이터 다운로드", data=json_str, file_name="fishing_save_v6.json", mime="application/json")

# 메인 탭
tab1, tab2, tab3, tab4, tab5 = st.tabs(["🌊 3D 낚시터", "🎣 낚시대 상점", "🎒 가방 & 판매", "🛒 미끼 상점", "📖 물고기 도감"])

# --- TAB 1: 3D 낚시터 ---
with tab1:
    st.subheader("🌊 실시간 3D 바다 낚시터")

    bait_options = [f"{b_name} ({count if count != float('inf') else '무제한'}개)" for b_name, count in st.session_state.baits.items()]
    selected_option = st.selectbox("사용할 미끼 선택", bait_options)
    selected_bait = selected_option.split(" (")[0]

    # 3D 뷰포트 렌더링
    render_3d_ocean_view(
        status=st.session_state.last_catch_status,
        rod_name=st.session_state.equipped_rod,
        bait_name=selected_bait,
        pending_fish=st.session_state.pending_fish
    )

    equipped_info = FISHING_RODS[st.session_state.equipped_rod]
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("낚시 성공률", f"{get_current_success_rate():.1f}%")
    c2.metric("행운 수치", f"+{equipped_info['rare_bonus']}")
    c3.metric("가방 공간", f"{len(st.session_state.inventory)}/{st.session_state.max_inventory}")
    c4.metric("XP 배수", f"{equipped_info['exp_mult']}x")

    st.divider()

    # 낚시 진행 컨트롤러 (입질 후 3초 대기 시스템)
    if st.session_state.fishing_state == "biting":
        st.warning("⏳ 물고기가 입질 중입니다... 3초 후 건져올립니다!")
        time.sleep(3)  # 3초 입질 대기 모션
        finalize_catch()
        st.rerun()

    col_manual, col_auto = st.columns(2)
    with col_manual:
        if st.button("🎣 낚시 시작 (찌 던지기)", use_container_width=True, disabled=(st.session_state.fishing_state != "idle")):
            if prepare_fish(selected_bait):
                st.rerun()

    with col_auto:
        if not st.session_state.auto_fishing:
            if st.button("▶️ 자동 낚시 시작", use_container_width=True, type="primary"):
                st.session_state.auto_fishing = True
                st.rerun()
        else:
            if st.button("⏹️ 자동 낚시 정지", use_container_width=True):
                st.session_state.auto_fishing = False
                st.session_state.fishing_state = "idle"
                st.session_state.last_catch_status = "idle"
                st.rerun()

    if st.session_state.last_catch_msg:
        if "💥" in st.session_state.last_catch_msg or "⚠️" in st.session_state.last_catch_msg:
            st.error(st.session_state.last_catch_msg)
        else:
            st.success(st.session_state.last_catch_msg)

    # 자동 낚시 주기 처리
    if st.session_state.auto_fishing and st.session_state.fishing_state == "idle":
        time.sleep(1.0)
        if prepare_fish(selected_bait):
            st.rerun()

# --- TAB 2: 낚시대 상점 ---
with tab2:
    st.subheader("🎣 낚시대 상점 & 장비 관리")
    for r_name, r_data in FISHING_RODS.items():
        is_owned = r_name in st.session_state.owned_rods
        is_equipped = st.session_state.equipped_rod == r_name
        
        ca, cb, cc = st.columns([2.5, 4, 1.5])
        with ca:
            st.write(f"### {r_name}")
            if is_equipped: st.caption("🟢 **장착 중**")
            elif is_owned: st.caption("🔵 **보유 중**")
            else: st.caption(f"가격: **{r_data['price']:,} G**")
        with cb:
            st.write(f"{r_data['desc']}")
            st.caption(f"성공률: {r_data['catch_rate']}% | 외형: {r_data['shape']} | 이펙트: {r_data['particle']}")
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
        st.subheader(f"🎒 가방 ({len(st.session_state.inventory)} / {st.session_state.max_inventory} 칸)")
    with col_inv2:
        if st.button("💰 전체 판매하기", use_container_width=True):
            sell_all_fish()
            st.rerun()
            
    if st.session_state.inventory:
        for idx, item in enumerate(reversed(st.session_state.inventory)):
            price = calculate_fish_price(item)
            st.write(f"**[{item['rarity']}] {item['trait']} {item['name']}** | {item['weight']}kg | 판매가: **{price:,} G**")
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
