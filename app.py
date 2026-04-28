import streamlit as st
import requests
from streamlit_js_eval import streamlit_js_eval

# 1. PREMIUM DESIGN KONFIGURATION
st.set_page_config(page_title="Wiesmoor Radar", layout="centered")

st.markdown("""
<style>
    /* Das hochwertige Hero-Banner mit Bild */
    .hero-banner {
        width: 100%;
        height: 150px;
        background: linear-gradient(rgba(0,0,0,0.5), rgba(0,0,0,0.5)), 
                    url('https://images.unsplash.com/photo-1527018601619-a508a2be00cd?q=80&w=1000');
        background-size: cover;
        background-position: center;
        border-radius: 25px;
        display: flex;
        align-items: center;
        justify-content: center;
        box-shadow: 0 10px 30px rgba(0,0,0,0.2);
        margin-bottom: 10px;
        border: 1px solid rgba(255,255,255,0.2);
    }
    .hero-title {
        color: white;
        font-size: 2.2rem;
        font-weight: 900;
        text-shadow: 2px 2px 10px rgba(0,0,0,0.8);
        letter-spacing: 1px;
    }
    
    /* Community-Text direkt unter dem Banner */
    .promo-box {
        text-align: center;
        background: #fdf2f2;
        padding: 12px;
        border-radius: 15px;
        font-size: 0.85rem;
        color: #d32f2f;
        margin-bottom: 20px;
        border: 1px solid #ffcdd2;
        font-weight: 500;
    }

    /* Tankstellen-Karten */
    .station-card {
        background: white;
        padding: 18px;
        border-radius: 22px;
        display: flex;
        align-items: center;
        border: 1px solid #f0f0f0;
        box-shadow: 0 5px 15px rgba(0,0,0,0.04);
        margin-bottom: 12px;
    }

    .brand-logo {
        width: 55px;
        height: 55px;
        border-radius: 15px;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 1.6rem;
        font-weight: 900;
        flex-shrink: 0;
    }

    .price-text {
        margin-left: auto;
        font-size: 2.1rem;
        font-weight: 900;
        color: #111;
        letter-spacing: -1px;
    }

    /* Dezenter Foto-Button Style */
    div.stButton > button {
        background-color: #ffffff !important;
        color: #666 !important;
        border: 1px solid #eee !important;
        border-radius: 10px !important;
        padding: 2px 10px !important;
        font-size: 0.75rem !important;
        height: auto !important;
        width: auto !important;
        margin-top: -8px !important;
        margin-bottom: 15px !important;
        box-shadow: 0 2px 5px rgba(0,0,0,0.05) !important;
    }
    
    div.stButton > button:hover {
        border-color: #e2001a !important;
        color: #e2001a !important;
    }
</style>
""", unsafe_allow_html=True)

# 2. UI LOGIK
st.markdown('<div class="hero-banner"><div class="hero-title">WIESMOOR RADAR</div></div>', unsafe_allow_html=True)
st.markdown('<div class="promo-box">📸 Community-Check: Foto hochladen & Preise bestätigen!</div>', unsafe_allow_html=True)

if 'lat' not in st.session_state: st.session_state.lat, st.session_state.lng = 53.414, 7.733

col1, col2 = st.columns(2)
with col1:
    if st.button("📍 Standort ermitteln", use_container_width=True):
        loc = streamlit_js_eval(js_expressions='navigator.geolocation ? new Promise((resolve) => { navigator.geolocation.getCurrentPosition(pos => resolve({lat: pos.coords.latitude, lon: pos.coords.longitude})) }) : null', key='gps_v9')
        if loc:
            st.session_state.lat, st.session_state.lng = loc['lat'], loc['lon']
            st.rerun()
with col2:
    if st.button("🔄 Preise laden", use_container_width=True):
        st.cache_data.clear()
        st.rerun()

# 3. DATEN & MARKEN-STYLES
def get_brand_ui(name):
    n = name.lower()
    if "aral" in n: return {"bg": "#0070BB", "c": "white", "s": "A", "b": "none"}
    if "score" in n: return {"bg": "#FFD100", "c": "#E2001A", "s": "S", "b": "2px solid #E2001A"}
    if "behrens" in n: return {"bg": "#5D4037", "c": "white", "s": "B", "b": "none"}
    if "q1" in n: return {"bg": "white", "c": "#E30613", "s": "Q1", "b": "2px solid #E30613"}
    return {"bg": "#455A64", "c": "white", "s": "⛽", "b": "none"}

API_KEY = "616cbb8e-9dde-4eb7-91f1-21a1663fa495"
@st.cache_data(ttl=60)
def get_prices(la, ln):
    url = f"https://creativecommons.tankerkoenig.de/json/list.php?lat={la}&lng={ln}&rad=10&sort=dist&type=all&apikey={API_KEY}"
    return requests.get(url).json().get("stations", [])

data = get_prices(st.session_state.lat, st.session_state.lng)

if data:
    fuel_tabs = st.tabs(["Super E5", "Super E10", "Diesel"])
    fuel_keys = {"Super E5": "e5", "Super E10": "e10", "Diesel": "diesel"}

    for idx, (label, key) in enumerate(fuel_keys.items()):
        with fuel_tabs[idx]:
            for s in data:
                val = s.get(key)
                if val:
                    ui = get_brand_ui(s.get('brand', ''))
                    st.markdown(f"""
                    <div class="station-card">
                        <div class="brand-logo" style="background-color: {ui['bg']}; color: {ui['c']}; border: {ui['b']};">
                            {ui['s']}
                        </div>
                        <div style="margin-left: 15px;">
                            <div style="font-weight: 800; font-size: 1.05rem; color: #111;">{s.get('brand', 'Tankstelle').upper()}</div>
                            <div style="color: #999; font-size: 0.8rem;">{s.get('street')}</div>
                        </div>
                        <div class="price-text">{val:.2f}€</div>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    # Der optimierte Foto-Button
                    if st.button(f"📷 Beleg senden: {s.get('brand')}", key=f"photo_{s['id']}_{key}"):
                        st.session_state[f"active_{s['id']}"] = True
                    
                    if st.session_state.get(f"active_{s['id']}"):
                        st.file_uploader("Kamera/Galerie", type=['jpg', 'png'], key=f"up_{s['id']}")
