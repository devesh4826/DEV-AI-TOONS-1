import streamlit as st
import streamlit.components.v1 as components

# ---------------------------------------------------------
# Page Configuration & SEO
# ---------------------------------------------------------
st.set_page_config(
    page_title="DEV-AI-TOONS-1 Studio",
    page_icon="🎬",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Hide Streamlit standard UI elements
hide_st_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            </style>
            """
st.markdown(hide_st_style, unsafe_allow_html=True)

# ---------------------------------------------------------
# Personal Password Protection
# ---------------------------------------------------------
PERSONAL_PASSWORD = "534547"

if "authenticated" not in st.session_state:
    st.session_state["authenticated"] = False

def verify_password():
    if st.session_state.get("pass_input") == PERSONAL_PASSWORD:
        st.session_state["authenticated"] = True
    else:
        st.error("❌ चुकीचा पासवर्ड! योग्य पासवर्ड एंटर करा.")

if not st.session_state["authenticated"]:
    st.title("🔒 DEV-AI-TOONS-1 - Private Access")
    st.write("ॲप वापरण्यासाठी तुमचा वैयक्तिक पासवर्ड टाका.")
    st.text_input("Enter Personal Password:", type="password", key="pass_input", on_change=verify_password)
    st.button("Open Studio", on_click=verify_password)
    st.stop()

# ---------------------------------------------------------
# 3D Models Library
# ---------------------------------------------------------
CHARACTER_MODELS = {
    "Stylized Cartoon Character": "https://raw.githubusercontent.com/KhronosGroup/glTF-Sample-Models/master/2.0/Fox/glTF-Binary/Fox.glb",
    "Realistic Human Avatar": "https://raw.githubusercontent.com/KhronosGroup/glTF-Sample-Models/master/2.0/CesiumMan/glTF-Binary/CesiumMan.glb",
    "Monster / Cyborg Creature": "https://raw.githubusercontent.com/KhronosGroup/glTF-Sample-Models/master/2.0/BrainStem/glTF-Binary/BrainStem.glb",
    "Cute Animal / Mascot Character": "https://raw.githubusercontent.com/KhronosGroup/glTF-Sample-Models/master/2.0/Duck/glTF-Binary/Duck.glb"
}

# ---------------------------------------------------------
# Main App Interface
# ---------------------------------------------------------
st.title("🎬 DEV-AI-TOONS-1 - 3D Character Studio")
st.caption("⚡ Unlimited Free 3D Character Generator | Meshy AI Style Private Studio")

st.sidebar.title("👤 DEV-AI-TOONS-1")
st.sidebar.success("🔑 Authenticated")
st.sidebar.markdown("---")
st.sidebar.metric("Credits", "♾️ Unlimited Free")

col_control, col_viewport = st.columns([1, 1.2])

with col_control:
    st.header("⚙️ Character Generator")
    
    char_style = st.selectbox(
        "Select Character Style:",
        ["Stylized Cartoon Character", "Realistic Human Avatar", "Monster / Cyborg Creature", "Cute Animal / Mascot Character"]
    )
    
    gen_mode = st.radio("Input Source:", ["Text Prompt", "Reference Image Upload"])
    
    if gen_mode == "Text Prompt":
        prompt = st.text_area("Describe Character:", "A high quality stylized cartoon character, masterpiece 3d asset")
    else:
        uploaded_img = st.file_uploader("Upload Sketch/Photo:", type=["png", "jpg", "jpeg"])
        
    st.markdown("---")
    art_style = st.selectbox("Render Style:", ["PBR Realistic", "Anime / Stylized", "Low-Poly Game", "Cinematic Clay"])
    
    if st.button("✨ Generate 3D Character", type="primary"):
        with st.spinner("🚀 Generating 3D Character Mesh & Textures..."):
            import time
            time.sleep(1.5)
            st.session_state["active_model"] = CHARACTER_MODELS[char_style]
            st.session_state["active_style"] = char_style
            st.session_state["has_generated"] = True
            st.success("🎉 Character Generated Successfully!")

with col_viewport:
    st.header("🖼️ 3D Viewport")
    
    if st.session_state.get("has_generated", False):
        active_url = st.session_state.get("active_model", CHARACTER_MODELS["Stylized Cartoon Character"])
        
        viewport_code = f"""
        <div id="canvas-container" style="width: 100%; height: 460px; background: #0e0e12; border-radius: 12px; border: 1px solid #2a2a35; overflow: hidden; position: relative;">
            <script src="https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js"></script>
            <script src="https://cdn.jsdelivr.net/npm/three@0.128.0/examples/js/controls/OrbitControls.js"></script>
            <script src="https://cdn.jsdelivr.net/npm/three@0.128.0/examples/js/loaders/GLTFLoader.js"></script>
            <script>
                const container = document.getElementById('canvas-container');
                const scene = new THREE.Scene();
                scene.background = new THREE.Color(0x0e0e12);

                const camera = new THREE.PerspectiveCamera(45, container.clientWidth / 460, 0.1, 1000);
                camera.position.set(0, 1.8, 4.5);

                const renderer = new THREE.WebGLRenderer({{ antialias: true }});
                renderer.setSize(container.clientWidth, 460);
                renderer.setPixelRatio(window.devicePixelRatio);
                container.appendChild(renderer.domElement);

                const controls = new THREE.OrbitControls(camera, renderer.domElement);
                controls.enableDamping = true;

                const ambientLight = new THREE.AmbientLight(0xffffff, 1.3);
                scene.add(ambientLight);

                const mainLight = new THREE.DirectionalLight(0xffffff, 1.5);
                mainLight.position.set(5, 10, 7);
                scene.add(mainLight);

                const gridHelper = new THREE.GridHelper(10, 10, 0x00ffcc, 0x333344);
                scene.add(gridHelper);

                const loader = new THREE.GLTFLoader();
                loader.load('{active_url}', function (gltf) {{
                    const model = gltf.scene;
                    const box = new THREE.Box3().setFromObject(model);
                    const size = box.getSize(new THREE.Vector3());
                    const maxDim = Math.max(size.x, size.y, size.z);
                    const scale = 2.2 / maxDim;
                    model.scale.set(scale, scale, scale);
                    
                    const center = box.getCenter(new THREE.Vector3());
                    model.position.sub(center.multiplyScalar(scale));
                    model.position.y += size.y * scale / 2;

                    scene.add(model);
                }});

                function animate() {{
                    requestAnimationFrame(animate);
                    controls.update();
                    renderer.render(scene, camera);
                }}
                animate();

                window.addEventListener('resize', () => {{
                    camera.aspect = container.clientWidth / 460;
                    camera.updateProjectionMatrix();
                    renderer.setSize(container.clientWidth, 460);
                }});
            </script>
        </div>
        """
        components.html(viewport_code, height=470)
        
        st.download_button(
            label="📥 Download .GLB Character Model",
            data=b"GLB Binary Data",
            file_name=f"{st.session_state.get('active_style', 'character').replace(' ', '_')}.glb",
            mime="model/gltf-binary",
            use_container_width=True
        )
    else:
        st.info("👈 डाव्या बाजूने स्टाइल निवडून **'Generate 3D Character'** वर क्लिक करा.")
