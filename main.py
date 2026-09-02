import streamlit as st
import streamlit.components.v1 as components
import random
import json

# -----------------------------------------------------------------------------
# 1. 3D 시각화 엔진 (Three.js WebGL 컴포넌트)
# -----------------------------------------------------------------------------
def render_3d_ocean_view(is_fishing=False, catch_status="idle"):
    html_code = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <style>
            body {{ margin: 0; overflow: hidden; background-color: #1a202c; }}
            #canvas-container {{ width: 100%; height: 350px; }}
        </style>
        <script src="https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js"></script>
    </head>
    <body>
        <div id="canvas-container"></div>
        <script>
            // 3D Scene 기본 설정
            const container = document.getElementById('canvas-container');
            const scene = new THREE.Scene();
            scene.background = new THREE.Color(0x0e1726);

            const camera = new THREE.PerspectiveCamera(60, container.clientWidth / 350, 0.1, 1000);
            camera.position.set(0, 5, 12);
            camera.lookAt(0, 0, 0);

            const renderer = new THREE.WebGLRenderer({{ antialias: true }});
            renderer.setSize(container.clientWidth, 350);
            container.appendChild(renderer.domElement);

            // 조명 설정
            const ambientLight = new THREE.AmbientLight(0xffffff, 0.6);
            scene.add(ambientLight);
            const dirLight = new THREE.DirectionalLight(0xffd700, 0.8);
            dirLight.position.set(10, 20, 10);
            scene.add(dirLight);

            // 3D 바다 수면 구현 (Grid Plane)
            const oceanGeo = new THREE.PlaneGeometry(30, 30, 32, 32);
            const oceanMat = new THREE.MeshPhongMaterial({{
                color: 0x006699,
                wireframe: true,
                transparent: true,
                opacity: 0.8
            }});
            const ocean = new THREE.Mesh(oceanGeo, oceanMat);
            ocean.rotation.x = -Math.PI / 2;
            scene.add(ocean);

            // 3D 낚시찌 구현 (Sphere)
            const floatGeo = new THREE.SphereGeometry(0.3, 16, 16);
            const floatMat = new THREE.MeshBasicMaterial({{ color: 0xff3300 }});
            const floatMesh = new THREE.Mesh(floatGeo, floatMat);
            floatMesh.position.set(0, 0.2, 2);
            scene.add(floatMesh);

            // 파도 및 찌 애니메이션 변수
            let clock = new THREE.Clock();

            function animate() {{
                requestAnimationFrame(animate);
                let time = clock.getElapsedTime();

                // 수면 웨이브 애니메이션
                const pos = oceanGeo.attributes.position;
                for (let i = 0; i < pos.count; i++) {{
                    let u = pos.getX(i);
                    let v = pos.getY(i);
                    let z = Math.sin(u + time * 2) * 0.2 + Math.cos(v + time * 1.5) * 0.2;
                    pos.setZ(i, z);
                }}
                pos.needsUpdate = true;

                // 낚시찌 수면 연동 유동 효과
                floatMesh.position.y = Math.sin(time * 3) * 0.15 + 0.1;

                renderer.render(scene, camera);
            }}
            animate();

            // 리사이즈 대응
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
# 2. 메인 UI 통합 (탭 레이아웃 및 3D 뷰어 배치)
# -----------------------------------------------------------------------------
st.set_page_config(page_title="3D 판타지 낚시 게임", page_icon="🎣", layout="wide")

st.title("🎣 3D 판타지 낚시 게임 (3D Graphic Engine Integrated)")

tab1, tab2, tab3 = st.tabs(["🌊 3D 낚시터", "🐠 3D 개인 수족관", "📖 도감"])

with tab1:
    st.subheader("🌊 실시간 3D 바다 수면")
    # 3D 그래픽 렌더링 영역 출력
    render_3d_ocean_view()
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("🎣 3D 찌 던지기", use_container_width=True):
            st.toast("3D 찌를 성공적으로 던졌습니다!", icon="🌊")
    with col2:
        st.button("⚙️ 낚시 설정", use_container_width=True)

with tab2:
    st.subheader("🐠 3D 내 개인 수족관 (New)")
    st.info("잡은 3D 물고기들이 헤엄치는 모습을 감상할 수 있는 공간입니다.")
    # 3D 수족관 시각화 영역 추가 위치

with tab3:
    st.caption("기존 도감 정보 연동 영역")
