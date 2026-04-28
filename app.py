import streamlit as st
import requests
from streamlit_js_eval import streamlit_js_eval

# 1. CLEAN UI-SETUP (Stabil & Freundlich)
st.set_page_config(page_title="Wiesmoor Radar", layout="centered")

st.markdown("""
<style>
    .hero-banner {
        width: 100%;
        height: 140px;
        background: linear-gradient(rgba(0,0,0,0.5), rgba(0,0,0,0.7)), 
                    url('https://images.unsplash.com/photo-1527018601619-a508a2be00cd?q=80&w=1000');
        background-size: cover;
        background-position: center;
        border-radius: 20px;
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        margin-bottom: 20px;
    }
    .hero-title { color: white; font-size: 2rem; font-weight: 900; margin: 0; }
    .hero-subtitle { color: #e0e0e0; font-size: 0.85rem; }

    .station-card {
        background: white;
        padding: 16px;
        border-radius: 20px;
        display: flex;
        align-items: center;
        border: 1px solid #eee;
        box-shadow: 0 4px 10px rgba(0,0,0,0.03);
        margin-bottom: 8px;
    }

    .brand-logo {
        width: 50px; height: 50px; border-radius: 12px;
        display: flex; align-items: center; justify-content: center;
        font-size: 1.4rem; font-weight: bold; flex-shrink: 0;
    }

    .price-tag {
        margin-left: auto; font-size: 1.9rem; font-weight: 900; color: #000;
    }

    /* Freundlicher Blau-Ton für Community-Aktionen */
    div.stButton > button {
        background-color: #f0f7ff !important;
        color: #007bff !important;
        border: 2px solid #007bff !important;
        border-radius: 12px !important;
        padding: 5px 15px !important;
        font-size: 0.8rem !important;
        font-weight: 700 !important;
        margin-top: -12px !important;
        margin-bottom: 25px !important;
    }
    div.stButton > button:hover {
        background-color: #007bff !important;
        color: white !important;
    }
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="hero-banner"><div class="hero-title">WIESMOOR RADAR</div><div class="hero-subtitle">Echte Preise durch Community-Power</div></div>', unsafe_allow_html=True)

# 2. STANDORT & DATEN
if 'lat' not in st.session_state:
    st.session_state.lat, st.session_state.lng = 53.414, 7.733

col1, col2 = st.columns([2, 1])
with col1:
    if st.button("📍 Standort finden", use_container_width=True):
        loc = streamlit_js_eval(js_expressions='navigator.geolocation ? new Promise((resolve) => { navigator.geolocation.getCurrentPosition(pos => resolve({lat: pos.coords.latitude, lon: pos.coords.longitude})) }) : null', key='gps_final')
        if loc:
            st.session_state.lat, st.session_state.lng = loc['lat'], loc['lon']
            st.rerun()

with col2:
    radius = st.selectbox("Umkreis", [5, 10, 20], index=0)

API_KEY = "616cbb8e-9dde-4eb7-91f1-21a1663fa495"

@st.cache_data(ttl=60)
def get_stations(la, ln, rad):
    url = f"https://creativecommons.tankerkoenig.de/json/list.php?lat={la}&lng={ln}&rad={rad}&sort=dist&type=all&apikey={API_KEY}"
    return requests.get(url).json().get("stations", [])

def get_style(brand):
    b = (brand or "").lower()
    if "aral" in b: return {"bg": "#0070BB", "c": "white", "s": "A"}
    if "score" in b: return {"bg": "#FFD100", "c": "#E2001A", "s": "S"}
    if "behrens" in b: return {"bg": "#5D4037", "c": "white", "s": "B"}
    return {"bg": "#e9ecef", "c": "#495057", "s": "⛽"}

stations = get_stations(st.session_state.lat, st.session_state.lng, radius)

# 3. ANZEIGE MIT NAMENS-SICHERHEIT
if stations:
    tab1, tab2, tab3 = st.tabs(["Super E5", "Super E10", "Diesel"])
    fuels = {"Super E5": "e5", "Super E10": "e10", "Diesel": "diesel"}

    for i, (label, key) in enumerate(fuels.items()):
        with [tab1, tab2, tab3][i]:
            for s in stations:
                price = s.get(key)
                if price:
                    # SICHERER NAME (Brand -> Name -> Fallback)
                    name = s.get('brand') or s.get('name') or "Tankstelle"
                    dist = s.get('dist', 0)
                    ui = get_style(name)
                    
                    st.markdown(f"""
                    <div class="station-card">
                        <div class="brand-logo" style="background-color: {ui['bg']}; color: {ui['c']};">
                            {ui['s']}
                        </div>
                        <div style="margin-left: 15px;">
                            <div style="font-weight: 800; font-size: 1rem;">{name.upper()}</div>
                            <div style="color: #888; font-size: 0.75rem;">{s.get('street')} ({dist} km)</div>
                        </div>
                        <div class="price-tag">{price:.2f}€</div>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    if st.button(f"📸 Preis-Foto senden", key=f"fix_{s['id']}_{key}"):
                        st.session_state[f"cam_{s['id']}"] = True
                    
                    if st.session_state.get(f"cam_{s['id']}"):
                        st.success(f"Danke! Bitte lade ein Foto vom Preis bei {name} hoch:")
                        st.file_uploader("Bild auswählen", type=['jpg', 'png'], key=f"up_{s['id']}")
else:
    st.info("Suche Tankstellen...")
