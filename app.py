import streamlit as st
import requests
from streamlit_js_eval import streamlit_js_eval

# 1. PREMIUM UI-SETUP & FIXES
st.set_page_config(page_title="Wiesmoor Radar", layout="centered")

st.markdown("""
<style>
    /* Das markante Hauptbanner */
    .hero-banner {
        width: 100%;
        height: 150px;
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
        text-align: center;
    }
    .hero-title {
        color: white;
        font-size: 2.2rem;
        font-weight: 900;
        margin: 0;
    }
    .hero-subtitle {
        color: #d1ffcd;
        font-size: 0.9rem;
    }

    /* Tankstellen Karten */
    .station-card {
        background: white;
        padding: 16px;
        border-radius: 20px;
        display: flex;
        align-items: center;
        border: 1px solid #f0f0f0;
        box-shadow: 0 4px 12px rgba(0,0,0,0.04);
        margin-bottom: 6px;
    }

    .brand-logo {
        width: 52px;
        height: 52px;
        border-radius: 14px;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 1.5rem;
        font-weight: bold;
        flex-shrink: 0;
    }

    .price-tag {
        margin-left: auto;
        font-size: 2rem;
        font-weight: 900;
        color: #000;
        letter-spacing: -1px;
    }

    /* Der freundliche grüne Button */
    div.stButton > button {
        background-color: #f1fff1 !important;
        color: #28a745 !important;
        border: 2px solid #28a745 !important;
        border-radius: 14px !important;
        padding: 4px 16px !important;
        font-size: 0.8rem !important;
        font-weight: 700 !important;
        margin-top: -12px !important;
        margin-bottom: 24px !important;
        width: auto !important;
    }
    
    div.stButton > button:hover {
        background-color: #28a745 !important;
        color: white !important;
    }
</style>
""", unsafe_allow_html=True)

# --- HEADER ---
st.markdown("""
<div class="hero-banner">
    <div class="hero-title">WIESMOOR RADAR</div>
    <div class="hero-subtitle">Gemeinsam für echte Preise vor Ort</div>
</div>
""", unsafe_allow_html=True)

# 2. STANDORT & FILTER
if 'lat' not in st.session_state:
    st.session_state.lat, st.session_state.lng = 53.414, 7.733

col1, col2 = st.columns([2, 1])
with col1:
    if st.button("📍 Standort aktualisieren", use_container_width=True):
        loc = streamlit_js_eval(js_expressions='navigator.geolocation ? new Promise((resolve) => { navigator.geolocation.getCurrentPosition(pos => resolve({lat: pos.coords.latitude, lon: pos.coords.longitude})) }) : null', key='gps_radar_v10')
        if loc:
            st.session_state.lat, st.session_state.lng = loc['lat'], loc['lon']
            st.rerun()

with col2:
    radius = st.selectbox("Umkreis", [5, 10, 20], index=0)

# 3. DATEN & LOGIK (Namens-Fix inkludiert)
API_KEY = "616cbb8e-9dde-4eb7-91f1-21a1663fa495"

@st.cache_data(ttl=60)
def get_stations(la, ln, rad):
    url = f"https://creativecommons.tankerkoenig.de/json/list.php?lat={la}&lng={ln}&rad={rad}&sort=dist&type=all&apikey={API_KEY}"
    try:
        return requests.get(url).json().get("stations", [])
    except:
        return []

def get_brand_style(brand_name):
    bn = brand_name.lower()
    if "aral" in bn: return {"bg": "#0070BB", "c": "white", "s": "A"}
    if "score" in bn: return {"bg": "#FFD100", "c": "#E2001A", "s": "S"}
    if "behrens" in bn: return {"bg": "#5D4037", "c": "white", "s": "B"}
    if "jet" in bn: return {"bg": "#FFD200", "c": "#003399", "s": "J"}
    if "q1" in bn: return {"bg": "white", "c": "#E30613", "s": "Q1"}
    return {"bg": "#455A64", "c": "white", "s": "⛽"}

stations = get_stations(st.session_state.lat, st.session_state.lng, radius)

# 4. ANZEIGE
if stations:
    tabs = st.tabs(["Super E5", "Super E10", "Diesel"])
    fuel_types = {"Super E5": "e5", "Super E10": "e10", "Diesel": "diesel"}

    for i, (label, key) in enumerate(fuel_types.items()):
        with tabs[i]:
            for s in stations:
                price = s.get(key)
                if price:
                    # NAMENS-FIX: Falls 'brand' leer ist, nutze 'name' oder 'Freie Tankstelle'
                    raw_name = s.get('brand') or s.get('name') or "Freie Tankstelle"
                    display_name = raw_name.upper()
                    
                    ui = get_brand_style(raw_name)
                    
                    st.markdown(f"""
                    <div class="station-card">
                        <div class="brand-logo" style="background-color: {ui['bg']}; color: {ui['c']}; border: { '2px solid ' + ui['c'] if ui['bg'] == 'white' else 'none' };">
                            {ui['s']}
                        </div>
                        <div style="margin-left: 15px;">
                            <div style="font-weight: 900; font-size: 1.1rem; color: #111;">{display_name}</div>
                            <div style="color: #888; font-size: 0.8rem;">{s.get('street')} ({s.get('dist')} km)</div>
                        </div>
                        <div class="price-tag">{price:.2f}€</div>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    # Der freundliche Foto-Button
                    if st.button(f"📸 Preis korrigieren (Foto)", key=f"btn_{s['id']}_{key}"):
                        st.session_state[f"cam_{s['id']}"] = True
                    
                    if st.session_state.get(f"cam_{s['id']}"):
                        st.info(f"H
