import streamlit as st
import time
from pathlib import Path
import base64
import random
from PIL import Image
import io
st.set_page_config(page_title="To My Best Friend Aayush", layout="centered", initial_sidebar_state="collapsed")

# Initialize Session State
if 'view' not in st.session_state:
    st.session_state.view = 'home'
if 'hidden_star_revealed' not in st.session_state:
    st.session_state.hidden_star_revealed = False

# --- Custom Cursor Base64 ---
# A small elegant glowing dot cursor
cursor_svg = """<svg width="24" height="24" xmlns="http://www.w3.org/2000/svg">
  <circle cx="12" cy="12" r="4" fill="#c7d2fe" filter="drop-shadow(0 0 4px #a5b4fc)"/>
</svg>"""
cursor_b64 = base64.b64encode(cursor_svg.encode()).decode()

# --- Global Scroll Settings ---
st.markdown("""
    <style>
    /* Hide the scrollbar but keep Streamlit's native scrolling active */
    * { 
        scrollbar-width: none !important; 
        -ms-overflow-style: none !important; 
    } 
    *::-webkit-scrollbar { 
        display: none !important; 
    }
    
    /* Ensure no container blocks pointer events incorrectly */
    [data-testid="stAppViewContainer"] {
        touch-action: auto !important;
    }
    </style>
""", unsafe_allow_html=True)

# --- CSS Injection ---
st.markdown("""
<style>
/* Font Imports */
@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@700&family=Outfit:wght@700;800&family=Inter:wght@300;400;500;600&display=swap');
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,400;0,600;0,700;1,400&family=Dancing+Script:wght@600&display=swap');
@import url('https://fonts.googleapis.com/css2?family=Material+Symbols+Rounded:opsz,wght,FILL,GRAD@24,400,0,0');

/* Hide Defaults */
#MainMenu {visibility: hidden !important;}
header {visibility: hidden !important;}
footer {visibility: hidden !important;}
div[data-testid="stToolbar"] {visibility: hidden !important;}
div[data-testid="stDecoration"] {visibility: hidden !important;}
div[data-testid="stStatusWidget"] {visibility: hidden !important;}

/* Fix padding for all views */
.main .block-container {
    padding-top: 0rem !important;
    padding-bottom: 0rem !important;
    margin-top: -3rem !important;
    max-width: 1200px;
    z-index: 10;
}

/* Background Animation */
.stApp {
    background: linear-gradient(45deg, #090B1A, #13132B, #1C1838, #6C63FF, #B86BFF) !important;
    background-size: 400% 400% !important;
    animation: gradientBG 15s ease infinite !important;
    color: #ffffff;
    font-family: 'Inter', sans-serif;
}

.stApp::before {
    content: '';
    position: fixed;
    top: 50%; left: 50%; width: 100vw; height: 100vh;
    transform: translate(-50%, -50%);
    background: radial-gradient(circle at 50% 50%, rgba(168, 85, 247, 0.12) 0%, transparent 60%);
    pointer-events: none;
    z-index: 0;
}

.stApp::after {
    content: '';
    position: fixed;
    top: 0; left: 0; width: 100vw; height: 100vh;
    background: radial-gradient(circle at 50% 50%, transparent 60%, rgba(0,0,0,0.4) 150%);
    pointer-events: none;
    z-index: 9999;
}

@keyframes gradientBG {
    0% { background-position: 0% 50%; }
    50% { background-position: 100% 50%; }
    100% { background-position: 0% 50%; }
}

/* Typography for Home Hero */
.hero-wrapper {
    position: relative;
    z-index: 10;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    width: 100%;
    margin-top: -2rem; /* Force content upwards */
    gap: 1rem;
    
    /* Stronger Glassmorphism */
    background: rgba(255, 255, 255, 0.04);
    backdrop-filter: blur(20px);
    -webkit-backdrop-filter: blur(20px);
    border: 1px solid rgba(255, 255, 255, 0.15); /* Slightly brighter border */
    border-radius: 32px;
    padding: 2rem 1.5rem 0.8rem 1.5rem; /* Reduced height by ~50px */
    box-shadow: 0 0 60px rgba(155, 89, 255, 0.12), 0 30px 80px rgba(0, 0, 0, 0.35);
    animation: fadeIn 3s ease-out forwards;
}

.hero-wrapper::before {
    content: ''; position: absolute; top: 0; left: 0; width: 100%; height: 100%;
    background: linear-gradient(135deg, rgba(255,255,255,0.05) 0%, transparent 50%, rgba(187,134,252,0.05) 100%);
    border-radius: 32px; z-index: -1; pointer-events: none;
}

.badge-pill {
    padding: 0.6rem 1.8rem;
    background: rgba(255, 255, 255, 0.05);
    backdrop-filter: blur(12px);
    -webkit-backdrop-filter: blur(12px);
    border: 1px solid rgba(255, 255, 255, 0.15);
    border-radius: 50px;
    font-family: 'Inter', sans-serif;
    font-size: 0.9rem;
    letter-spacing: 0.15em;
    text-transform: uppercase;
    color: #cbd5e1;
    box-shadow: inset 0 1px 1px rgba(255, 255, 255, 0.2), 0 4px 15px rgba(0, 0, 0, 0.2);
    animation: slideUp 1s ease-out forwards, floatBadge 6s infinite ease-in-out;
    opacity: 0;
}

@keyframes floatBadge {
    0%, 100% { transform: translateY(0); }
    50% { transform: translateY(-8px); }
}

.hero-title {
    font-family: 'Outfit', sans-serif;
    font-size: 68px;
    font-weight: 800;
    letter-spacing: 10px;
    text-transform: uppercase;
    margin: 0;
    padding: 0;
    line-height: 1.1;
    background: linear-gradient(to right, #ffffff, #f8dfff, #bb86fc);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    text-shadow: 0 0 40px rgba(187, 134, 252, 0.5); /* 15% stronger glow */
    position: relative;
    z-index: 1;
    animation: fadeIn 4s ease forwards;
}

.hero-title::after {
    content: ''; position: absolute; top: 50%; left: 50%; transform: translate(-50%, -50%);
    width: 150%; height: 150%;
    background: radial-gradient(circle, rgba(187,134,252,0.25) 0%, transparent 60%);
    z-index: -1; pointer-events: none;
}

.hero-subtitle {
    font-family: 'Poppins', sans-serif;
    font-size: 56px;
    font-weight: 700;
    margin: 0;
    padding: 0;
    position: relative;
    z-index: 1;
    background: linear-gradient(135deg, #ffffff 0%, #b86bff 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    animation: slideUp 2s ease-out forwards, pulseGlow 6s infinite alternate;
}

.hero-subtitle::before {
    content: ''; position: absolute; top: 50%; left: 50%; transform: translate(-50%, -50%);
    width: 120%; height: 120%;
    background: radial-gradient(circle, rgba(187,134,252,0.18) 0%, transparent 60%);
    z-index: -1; pointer-events: none;
}

@keyframes pulseGlow {
    0% { filter: drop-shadow(0 0 5px rgba(168, 85, 247, 0.3)); }
    100% { filter: drop-shadow(0 0 20px rgba(168, 85, 247, 0.7)); }
}

.hero-quote {
    font-family: 'Inter', sans-serif;
    font-style: italic;
    font-size: 1.1rem;
    color: #cbd5e1;
    font-weight: 300;
    margin: 1rem 0 2rem 0;
    opacity: 0.82;
    animation: fadeIn 5s ease-out forwards;
}

/* Glass Buttons Container */
.glass-btn-container {
    display: flex;
    gap: 2rem;
    flex-wrap: wrap;
    justify-content: center;
    animation: slideUp 1s ease-out forwards;
    opacity: 0;
    animation-delay: 1.2s;
    width: 100%;
}

/* Glass Card Button */
.glass-card-btn {
    background: linear-gradient(135deg, rgba(168, 85, 247, 0.25), rgba(236, 72, 153, 0.25)) !important;
    backdrop-filter: blur(24px) !important;
    -webkit-backdrop-filter: blur(24px) !important;
    border: 1px solid rgba(210, 160, 255, 0.6) !important; 
    border-radius: 24px !important;
    padding: 0 !important;
    font-family: 'Inter', sans-serif !important;
    font-size: 1.2rem !important;
    font-weight: 500 !important;
    color: #ffffff !important;
    cursor: pointer !important;
    box-shadow: 0 10px 30px rgba(0, 0, 0, 0.25), 0 0 80px rgba(170, 120, 255, 0.12) !important; 
    transition: all 0.4s cubic-bezier(0.2, 0.8, 0.2, 1) !important;
    position: relative !important;
    overflow: hidden !important;
    display: flex !important;
    align-items: center !important;
    justify-content: center !important;
    width: 260px !important;
    height: 72px !important;
    max-width: 100% !important;
}

.glass-card-btn::before {
    content: '' !important;
    position: absolute !important;
    top: 0 !important; left: -100% !important; width: 50% !important; height: 100% !important;
    background: linear-gradient(to right, transparent, rgba(255, 255, 255, 0.1), transparent) !important;
    transform: skewX(-25deg) !important;
    transition: all 0.6s ease !important;
}

.glass-card-btn:hover {
    background: linear-gradient(135deg, rgba(168, 85, 247, 0.45), rgba(236, 72, 153, 0.45)) !important;
    border-color: rgba(210, 160, 255, 1) !important;
    transform: translateY(-6px) scale(1.02) !important;
    box-shadow: 0 15px 45px rgba(0,0,0,0.4), 0 0 50px rgba(187, 134, 252, 0.8) !important;
    color: #ffffff !important;
}

.glass-card-btn:hover::before {
    left: 200% !important;
}

.glass-card-btn p {
    color: #ffffff !important;
    margin: 0 !important;
    font-size: 1.1rem !important;
    font-weight: 500 !important;
}

/* Animations */
@keyframes slideUp {
    from { opacity: 0; transform: translateY(30px); }
    to { opacity: 1; transform: translateY(0); }
}
@keyframes scaleIn {
    from { opacity: 0; transform: scale(0.9); }
    to { opacity: 1; transform: scale(1); }
}
@keyframes fadeIn {
    from { opacity: 0; }
    to { opacity: 1; }
}

/* Floating particles CSS (for JS injection) */
.particle {
    position: fixed;
    background: white;
    border-radius: 50%;
    animation: floatParticle linear infinite;
    opacity: 0.5;
    box-shadow: 0 0 8px rgba(255, 255, 255, 0.8);
    pointer-events: none;
    z-index: 0;
}
@keyframes floatParticle {
    0% { transform: translateY(100vh) scale(0.5); opacity: 0; }
    10% { opacity: 0.8; }
    90% { opacity: 0.8; }
    100% { transform: translateY(-100vh) scale(1); opacity: 0; }
}
/* Decorative Elements & Confetti */
.decor-container { position: fixed; width: 100vw; height: 100vh; top: 0; left: 0; pointer-events: none; overflow: hidden; z-index: 5; }
.decor { position: absolute; opacity: 0; animation: twinkleFloat 3s infinite ease-in-out alternate; }

@keyframes twinkleFloat {
    0% { transform: translateY(0) scale(1); opacity: 0.1; }
    50% { opacity: 0.6; }
    100% { transform: translateY(-30px) scale(1.1); opacity: 0.3; }
}

/* Responsive */
@media (max-width: 768px) {
    .hero-title { font-size: 48px; }
    .hero-subtitle { font-size: 36px; }
    .glass-btn-container { flex-direction: column; gap: 1rem; width: 100%; padding: 0 2rem; }
    .glass-card-btn { width: 100%; }
}

/* Existing styles for other views */
.glass-card {
    background: rgba(20, 20, 28, 0.4);
    backdrop-filter: blur(16px);
    border: 1px solid rgba(255, 255, 255, 0.05);
    border-radius: 20px;
    padding: 1.5rem;
    box-shadow: 0 20px 40px -10px rgba(0, 0, 0, 0.5);
    margin: 0.5rem 0;
    position: relative;
    z-index: 10;
}
/* Memories Gallery */
.gallery-section-wrapper { position: relative; width: 100%; z-index: 10; }
.gallery-bg-glow { position: absolute; top: 50%; left: 50%; transform: translate(-50%, -50%); width: 100%; height: 100%; background: radial-gradient(circle, rgba(168,85,247,0.15) 0%, transparent 70%); filter: blur(60px); z-index: 0; pointer-events: none; }
.gallery-decor-container { position: absolute; width: 100%; height: 100%; top: 0; left: 0; pointer-events: none; z-index: 0; }
.gallery-decor { position: absolute; opacity: 0; animation: twinkleFloat 3s infinite ease-in-out alternate; }

.gallery-img-container {
    width: 100%; padding-top: 135%; position: relative; border-radius: 24px;
    overflow: hidden; 
    box-shadow: 0 10px 30px rgba(0,0,0,0.25), 0 0 25px rgba(170,120,255,0.08);
    border: 1px solid rgba(255, 255, 255, 0.08);
    backdrop-filter: blur(18px); -webkit-backdrop-filter: blur(18px);
    background: rgba(20, 20, 28, 0.4);
    transition: all 0.3s cubic-bezier(0.2, 0.8, 0.2, 1); margin-bottom: 0.5rem;
    animation: gentleFloat 6s ease-in-out infinite alternate;
}
@keyframes gentleFloat {
    0% { transform: translateY(2px); }
    100% { transform: translateY(-3px); }
}
.gallery-img-container:hover { 
    transform: scale(1.04) translateY(-8px); 
    box-shadow: 0 15px 40px rgba(0,0,0,0.4), 0 0 35px rgba(184, 107, 255, 0.25);
    border: 1px solid rgba(255, 255, 255, 0.2);
    animation-play-state: paused;
}
.img-blur-bg {
    position: absolute; top: -10%; left: -10%; width: 120%; height: 120%;
    background-size: cover; background-position: center;
    filter: blur(20px) brightness(0.4); z-index: 0;
}
.gallery-img-container img { position: absolute; top: 0; left: 0; width: 100%; height: 100%; object-fit: contain; z-index: 1; border-radius: 24px; }
.gallery-gradient-overlay { position: absolute; bottom: 0; left: 0; width: 100%; height: 40%; background: linear-gradient(to top, rgba(0,0,0,0.5) 0%, transparent 100%); z-index: 2; pointer-events: none; }

/* Quote & Divider */
.gradient-divider {
    height: 1px; width: 100%; max-width: 800px; margin: 0.5rem auto;
    background: linear-gradient(90deg, transparent, rgba(168, 85, 247, 0.8), transparent);
    box-shadow: 0 0 10px rgba(168, 85, 247, 0.5);
}
.quote-card {
    background: rgba(255, 255, 255, 0.03); backdrop-filter: blur(12px); -webkit-backdrop-filter: blur(12px);
    border: 1px solid rgba(255, 255, 255, 0.08); border-radius: 24px;
    padding: 1rem 1.5rem; margin: 0 auto 0.5rem auto; max-width: 700px;
    box-shadow: 0 10px 30px rgba(0,0,0,0.3); text-align: center;
}
.quote-text { font-family: 'Playfair Display', serif; font-size: 1.4rem; font-style: italic; color: rgba(248, 250, 252, 0.85); line-height: 1.5; margin: 0; text-shadow: 0 0 10px rgba(255, 255, 255, 0.1); }

/* Section Titles */
.memories-title {
    font-family: 'Poppins', sans-serif; font-size: 42px; font-weight: 800;
    background: linear-gradient(to right, #b86bff, #ec4899);
    -webkit-background-clip: text; -webkit-text-fill-color: transparent;
    text-shadow: 0 0 25px rgba(184, 107, 255, 0.4);
    margin: -3.5rem 0 1.5rem 0 !important; text-align: center;
}

.letter-text { font-family: 'Inter', sans-serif; font-size: 1.1rem; line-height: 1.8; color: #d1d5db; font-weight: 300; text-align: center; }
.letter-text p { margin-bottom: 0.8rem; }
.handwritten { font-family: 'Dancing Script', cursive; font-size: 2.5rem; color: #c7d2fe; }
.text-center { text-align: center; }
.delay-1 { animation-delay: 0.15s; } .delay-2 { animation-delay: 0.3s; } .delay-3 { animation-delay: 0.45s; } .delay-4 { animation-delay: 0.6s; }
.fade-in { animation: fadeIn 0.6s cubic-bezier(0.2, 0.8, 0.2, 1) forwards; opacity: 0; }
span.home-btn-anchor { display: none; }
div.element-container:has(.home-btn-anchor) {
    display: none !important;
    margin: 0 !important;
    padding: 0 !important;
    height: 0 !important;
}
div.element-container:has(.home-btn-anchor) + div.element-container {
    position: fixed !important;
    top: 20px !important;
    left: 20px !important;
    width: auto !important;
    z-index: 99999 !important;
    margin: 0 !important;
}
div.element-container:has(.home-btn-anchor) + div.element-container button {
    background: rgba(255, 255, 255, 0.05) !important;
    backdrop-filter: blur(12px) !important;
    -webkit-backdrop-filter: blur(12px) !important;
    border: 1px solid rgba(255, 255, 255, 0.15) !important;
    border-radius: 50px !important;
    color: #ffffff !important;
    font-size: 0.9rem !important;
    padding: 0.5rem 1.5rem !important;
    margin: 0 !important;
    transform: none !important;
    box-shadow: 0 4px 15px rgba(0, 0, 0, 0.2) !important;
    transition: all 0.3s ease !important;
    font-family: 'Inter', sans-serif !important;
    font-weight: 500 !important;
    letter-spacing: 0.05em !important;
    min-height: 0 !important;
}
div.element-container:has(.home-btn-anchor) + div.element-container button p {
    color: #ffffff !important;
    margin: 0 !important;
}
div.element-container:has(.home-btn-anchor) + div.element-container button:hover {
    background: rgba(255, 255, 255, 0.12) !important;
    border-color: rgba(184, 107, 255, 0.4) !important;
    box-shadow: 0 10px 30px rgba(0,0,0,0.25), 0 0 20px rgba(147,51,234,0.12) !important;
    transform: scale(1.04) translateY(-2px) !important;
}
</style>
""", unsafe_allow_html=True)

# Javascript Injection for Interactivity (Mouse glow, Particles, Button Clicks)
import streamlit.components.v1 as components
components.html("""
<script>
    const parentDoc = window.parent.document;

    // 1. Mouse Glow Effect
    let glow = parentDoc.getElementById('custom-mouse-glow');
    if (!glow) {
        glow = parentDoc.createElement('div');
        glow.id = 'custom-mouse-glow';
        glow.style.position = 'fixed';
        glow.style.width = '600px';
        glow.style.height = '600px';
        glow.style.background = 'radial-gradient(circle, rgba(184, 107, 255, 0.15) 0%, transparent 60%)';
        glow.style.borderRadius = '50%';
        glow.style.pointerEvents = 'none';
        glow.style.transform = 'translate(-50%, -50%)';
        glow.style.zIndex = '0';
        glow.style.mixBlendMode = 'screen';
        glow.style.transition = 'width 0.3s, height 0.3s';
        parentDoc.body.appendChild(glow);

        parentDoc.addEventListener('mousemove', (e) => {
            glow.style.left = e.clientX + 'px';
            glow.style.top = e.clientY + 'px';
        });
    }

    // 2. Particles
    let particlesContainer = parentDoc.getElementById('custom-particles');
    if (!particlesContainer) {
        particlesContainer = parentDoc.createElement('div');
        particlesContainer.id = 'custom-particles';
        parentDoc.body.appendChild(particlesContainer);
        
        for (let i = 0; i < 15; i++) {
            let p = parentDoc.createElement('div');
            p.classList.add('particle');
            p.style.width = Math.random() * 3 + 1 + 'px';
            p.style.height = p.style.width;
            p.style.left = Math.random() * 100 + 'vw';
            p.style.animationDuration = Math.random() * 20 + 10 + 's';
            p.style.animationDelay = Math.random() * 20 + 's';
            particlesContainer.appendChild(p);
        }
    }

    // 3. Native Button Styling and Icon Injection
    setInterval(() => {
        const stButtons = parentDoc.querySelectorAll('.stButton button');
        stButtons.forEach(btn => {
            if(btn.innerText.includes('Memories')) {
                if(!btn.classList.contains('glass-card-btn')) {
                    btn.classList.add('glass-card-btn');
                    const p = btn.querySelector('p') || btn.querySelector('div');
                    if (p) p.innerHTML = '<span class="material-symbols-rounded" style="font-size: 1.4rem; margin-right: 12px; vertical-align: middle;">photo_library</span> Memories';
                }
            }
            if(btn.innerText.includes('Letter')) {
                if(!btn.classList.contains('glass-card-btn')) {
                    btn.classList.add('glass-card-btn');
                    const p = btn.querySelector('p') || btn.querySelector('div');
                    if (p) p.innerHTML = '<span class="material-symbols-rounded" style="font-size: 1.4rem; margin-right: 12px; vertical-align: middle;">mail</span> Letter';
                }
            }
        });
    }, 500); // Poll slightly to catch DOM updates
</script>
""", height=0, width=0)


# Helper function to render base64 image (Optimized for faster loading)
@st.cache_data
def get_base64_image(image_path_str, max_size=(500, 500)):
    try:
        with Image.open(image_path_str) as img:
            # Convert to RGB to avoid issues with saving alpha channels as JPEG if needed,
            # but we can try to preserve the original format if it's PNG/WebP.
            if img.mode != 'RGB' and img.format != 'PNG':
                img = img.convert('RGB')
            img.thumbnail(max_size, Image.Resampling.LANCZOS)
            buffered = io.BytesIO()
            # Default to JPEG if format is somehow missing
            fmt = img.format if img.format else "JPEG"
            # For JPEGs, we can add some compression
            if fmt == "JPEG" or fmt == "MPO":
                img.save(buffered, format="JPEG", quality=85)
            else:
                img.save(buffered, format=fmt)
            return base64.b64encode(buffered.getvalue()).decode()
    except Exception as e:
        print(f"Error loading {image_path_str}: {e}")
        return ""

def nav_to(view_name):
    st.session_state.view = view_name

# --- Global Background Decor ---
import random
random.seed(42) # Consistent random placement
decor_html = '<div class="decor-container">'

# 20 perfectly balanced particles
particle_coords = [
    (10, 15), (25, 30), (35, 10), 
    (48, 75), (55, 8), 
    (65, 35), (75, 12), 
    (82, 60), (95, 20), (15, 50)
]
for t, l in particle_coords:
    d, s = random.uniform(0, 3), random.uniform(0.6, 1.2)
    decor_html += f'<div class="decor" style="top:{t}%; left:{l}%; animation-delay:{d}s; font-size:{s}rem;">✨</div>'
    
# 8 perfectly balanced stars
star_coords = [
    (8, 25), (32, 8),
    (68, 15), (92, 65)
]
for t, l in star_coords:
    d, s = random.uniform(0, 3), random.uniform(0.8, 1.6)
    decor_html += f'<div class="decor" style="top:{t}%; left:{l}%; animation-delay:{d}s; font-size:{s}rem;">⭐</div>'
    
# Fixed elegant elements
decor_html += '<div class="decor" style="top:25%; left:12%; animation-delay:1s; font-size:2rem;">🦋</div>'
decor_html += '<div class="decor" style="bottom:30%; right:15%; animation-delay:2s; font-size:1.5rem;">🦋</div>'
decor_html += '<div class="decor" style="top:12%; right:18%; animation-delay:0s; font-size:2.5rem;">🌙</div>'
decor_html += '</div>'

st.markdown(decor_html, unsafe_allow_html=True)

# ----------------- HOME VIEW -----------------
if st.session_state.view == 'home':
    st.markdown("""
        <div class="hero-wrapper">
            <div class="badge-pill">✦ A Token Of Gratitude ✦</div>
            <div style="text-align: center;">
                <h1 class="hero-title">AAYUSH</h1>
                <h2 class="hero-subtitle">✦ Best Friend ✦</h2>
                <p class="hero-quote" style="margin-bottom: 1rem;">✦ "Talking to you is always nice." ✦</p>
            </div>
        </div>
    """, unsafe_allow_html=True)
    
    # Use native Streamlit columns to display the buttons side-by-side.
    # The javascript snippet injects `.glass-card-btn` into these buttons to style them.
    col_spacer1, col1, col2, col_spacer2 = st.columns([1, 2, 2, 1], gap="medium")
    with col1:
        if st.button("Memories", key="btn_mem"):
            nav_to('memories')
            st.rerun()
    with col2:
        if st.button("Letter", key="btn_let"):
            nav_to('letter')
            st.rerun()
            
    # Tiny Footer Section
    st.markdown("""
        <div style="text-align: center; margin-top: 0.5rem; color: rgba(255,255,255,0.55); font-size: 0.8rem; font-family: 'Inter', sans-serif; letter-spacing: 0.1em; opacity: 0; animation: fadeIn 5s ease forwards;">
            ✦ Every memory with you is special ✦
        </div>
    """, unsafe_allow_html=True)

# ----------------- MEMORIES VIEW -----------------
elif st.session_state.view == 'memories':
    st.markdown("<span class='home-btn-anchor'></span>", unsafe_allow_html=True)
    if st.button("🏠 HOME", key="btn_home_mem"):
        nav_to('home')
        st.rerun()
    
    st.markdown("""
        <div style="text-align: center; margin-top: 1rem;">
            <h2 class="memories-title fade-in"><span style="-webkit-text-fill-color: initial;">✨</span> Some Moments Worth Keeping <span style="-webkit-text-fill-color: initial;">✨</span></h2>
        </div>
    """, unsafe_allow_html=True)
    
    # Image discovery
    images_dir = Path("images")
    valid_exts = {".jpg", ".jpeg", ".png", ".webp"}
    image_paths = []
    
    if images_dir.exists():
        image_paths = [p for p in images_dir.iterdir() if p.suffix.lower() in valid_exts]
    
    if not image_paths:
        # Empty state
        st.markdown("""
            <div class='glass-card fade-in delay-1 text-center'>
                <h3 style='color: #cbd5e1; font-weight:300;'>A space waiting for memories.</h3>
                <p style='color: #64748b; font-size: 0.9rem;'>Please add images to the `images/` directory.</p>
            </div>
        """, unsafe_allow_html=True)
    else:
        # Gallery Layout using columns
        st.markdown("<div class='gallery-section-wrapper fade-in delay-1'><div class='gallery-bg-glow'></div>", unsafe_allow_html=True)
        
        # Twinkling stars specifically for gallery
        decor_html = '<div class="gallery-decor-container">'
        star_coords = [(5, 10), (15, 90), (85, 12), (75, 88)]
        for t, l in star_coords:
            d, s = random.uniform(0, 3), random.uniform(0.8, 1.2)
            decor_html += f'<div class="gallery-decor" style="top:{t}%; left:{l}%; animation-delay:{d}s; font-size:{s}rem;">⭐</div>'
        decor_html += '</div>'
        st.markdown(decor_html, unsafe_allow_html=True)

        cols = st.columns(3)
        for i, img_path in enumerate(image_paths):
            b64_img = get_base64_image(str(img_path))
            col_idx = i % 3
            with cols[col_idx]:
                st.markdown(f"""
                    <div class='gallery-img-container fade-in delay-{min(i%4 + 1, 4)}'>
                        <div class='img-blur-bg' style='background-image: url(data:image/jpeg;base64,{b64_img})'></div>
                        <img src="data:image/jpeg;base64,{b64_img}" alt="Memory {i}">
                        <div class='gallery-gradient-overlay'></div>
                    </div>
                """, unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)
                
    # Quote Card
    st.markdown("""
        <div class="gradient-divider fade-in delay-2"></div>
        <div class="quote-card fade-in delay-3">
            <div class="quote-text">"Thanks for being there. Time is the best thing you can give to someone."</div>
        </div>
    """, unsafe_allow_html=True)
    



# ----------------- LETTER VIEW -----------------
elif st.session_state.view == 'letter':
    st.markdown("""
        <style>
        .main .block-container { padding-bottom: 6rem !important; }
        </style>
    """, unsafe_allow_html=True)
    st.markdown("<span class='home-btn-anchor'></span>", unsafe_allow_html=True)
    if st.button("🏠 HOME", key="btn_home_let"):
        nav_to('home')
        st.rerun()

    st.markdown("""
        <div style="text-align: center; margin-top: 1rem;">
            <h2 class="memories-title fade-in"><span style="-webkit-text-fill-color: initial;">🌙</span> A Letter For You <span style="-webkit-text-fill-color: initial;">✨</span></h2>
        </div>
    """, unsafe_allow_html=True)

    st.markdown("""
        <div class='glass-card fade-in'>
            <div class='handwritten fade-in' style='margin-bottom: 2rem;'>Dear Aayush,</div>
            <div class='letter-text'>
                <p>I don’t really know how to start this, but I just wanted to say something that’s been on my mind.</p>
                <p>You’re genuinely one of the easiest people to talk to. It felt natural talking to you. Whether it was something important or complete nonsense, talking to you was always nice.</p>
                <p>I still remember you saying, <em>“If something ever bothers you, you can always talk to me.”</em> Maybe you don't even remember saying it, but I do. It wasn't some life-changing moment or anything dramatic, it just felt nice knowing someone genuinely meant it.</p>
                <p>I just wanted to take the chance to say all of this and show my gratitude. I hope life brings you a lot of good memories, people who make you happy, and plenty of moments that make you smile.</p>
            </div>
            <div class='handwritten fade-in' style='text-align: right; margin-top: 3rem;'>Your Best Friend,</div>
            <div class='handwritten fade-in' style='text-align: right; font-size: 1.8rem; margin-top: -10px;'>— Rajveer</div>
        </div>
    """, unsafe_allow_html=True)
    st.write("<div style='height: 1rem;'></div>", unsafe_allow_html=True)
            

