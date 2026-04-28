import streamlit as st
import requests
from streamlit_js_eval import streamlit_js_eval
from datetime import datetime

# 1. DAS DESIGN-SYSTEM (Originalgetreue Markenfarben)
st.set_page_config(page_title="Wiesmoor Radar", layout="centered")

st.markdown("""
<style>
    /* Header & Info Box */
    .header-banner {
        width: 100%;
        height: 160px;
        background: linear-gradient(rgba(0,0,0,0.4), rgba(0,0,0,0.4)), url('https://images.unsplash.com/photo-1527018601619-a508a2be00cd?q=80&w=1000&auto=format&fit=crop');
        background-size: cover;
        background-position: center;
        border-radius: 15px;
        display: flex;
        align-items: center;
        justify-content: center;
        border-bottom: 5px solid #e2001a;
    }
    .header-text {
        color: white;
        font-size: 2.2rem;
        font-weight: 900;
        text-shadow: 2px 2px 8px rgba(0,0,0,0.8);
    }
    
    /* Station Card Style */
    .station-container {
        background: #ffffff;
        padding: 16px;
        border-radius: 18px;
        border: 1px solid #eef0f2;
        display: flex;
        align-items: center;
        margin-bottom: 12px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.03);
    }

    /* Icon-Boxen mit Markenfarben */
    .logo-box {
        width: 52px;
        height: 52px;
        border-radius: 10px;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 1.6rem;
        font-weight: 900;
        margin-right: 16px;
        flex-shrink: 0;
    }
    
    .price-text {
        margin-left: auto;
        font-size: 1.9rem;
        font-weight: 900;
        color: #1a1a1a;
    }
</style>
""", unsafe_allow_html=True)

# 2. BRAND DEFINITIONS (Abgleich mit offiziellen Webseiten)
def get_brand_identity(brand_name):
    bn = brand_name.lower()
    
    # ARAL: Hellblau (Sky Blue) & Weiß
    if "aral" in bn:
        return {"bg": "#0070BB", "color": "#FFFFFF", "icon": "A", "border": "none"}
    
    # SCORE: Gelber Hintergrund (#FFD100), Rote Schrift & Rand (#E2001A)
    elif "score" in bn:
        return {"bg": "#FFD100", "color": "#E2001A", "icon": "S", "border": "3px solid #E2001A"}
    
    # BEHRENS: Braun-Töne für das Bären-Logo
    elif "behrens" in bn:
        return {"bg": "#5D4037", "color": "#FFFFFF", "icon": "🐻", "border": "none"}
    
    # SHELL: Gelber Grund (#FBCE07), Roter Rand (#D50000)
    elif "shell" in bn:
        return {"bg": "#FBCE07", "color": "#D50000", "icon": "S", "border": "2px solid #D50000"}
    
    # JET: Rein-Gelb (#FFD200), Blaue Schrift (#003399)
    elif "jet" in bn:
        return {"bg": "#FFD200", "color": "#003399", "icon": "J", "border": "none"}
    
    # ESSO: Rot (#EF3340) & Weiß
    elif "esso" in bn:
        return {"bg": "#EF3340", "color": "#FFFFFF", "icon": "E", "border": "none"}

    # Q1: Weißer Grund, Rote Schrift & dicker Rand
    elif "q1" in bn:
        return {"bg": "#FFFFFF", "color": "#E30613", "icon": "Q1", "border": "3px solid #E30613"}
    
    # TOTAL: Orange/Rot Verlauf (hier Orange #FF5900)
    elif "total" in bn:
        return {"bg": "#FF5900", "color": "#FFFFFF", "icon": "T", "border": "none"}
    
    # Standard für Unbekannte
    return {"bg": "#455A64", "color": "#FFFFFF", "icon": "⛽", "border": "none"}

# --- LOGIK ---
st.markdown('<div class="header-banner"><div class="header-text">WIESMOOR RADAR</div></div>', unsafe_allow_html=True)

if 'lat' not in st.session_state: 
    st.session_state.lat, st.session_state.lng = 53.414, 7.733

col1, col2 = st.columns(2)
with col1:
    if st.button("📍 Mein Standort"):
        loc = streamlit_js_eval(js_expressions='navigator.geolocation ? new Promise((resolve) => { navigator.geolocation.getCurrentPosition(pos => resolve({lat: pos.coords.latitude, lon: pos.coords.longitude})) }) : null', key='gps_v5')
        if loc:
            st.session_state.lat, st.session_state.lng = loc['lat'], loc['lon']
            st.rerun()
with col2:
    if st.button("🔄 Preise laden"):
        st.cache_data.clear()
        st.rerun()

API_KEY = "616cbb8e-9dde-4eb7-91f1-21a1663fa495"
@st.cache_data(ttl=60)
def fetch_data(la, ln):
    try:
        url = f"https://creativecommons.tankerkoenig.de/json/list.php?lat={la}&lng={ln}&rad=10&sort=dist&type=all&apikey={API_KEY}"
        return requests.get(url).json().get("stations", [])
    except: return []

stations = fetch_data(st.session_state.lat, st.session_state.lng)

if stations:
    fuel_tabs = st.tabs(["Super E5", "Super E10", "Diesel"])
    keys = ["e5", "e10", "diesel"]

    for i, fuel in enumerate(keys):
        with fuel_tabs[i]:
            for s in stations:
                price = s.get(fuel)
                if price:
                    brand_style = get_brand_identity(s.get('brand', ''))
                    st.markdown(f"""
                    <div class="station-container">
                        <div class="logo-box" style="background-color: {brand_style['bg']}; color: {brand_style['color']}; border: {brand_style['border']};">
                            {brand_style['icon']}
                        </div>
                        <div>
                            <div style="font-weight:bold; font-size:1.1rem; color:#111;">{s.get('brand', 'Tankstelle').upper()}</div>
                            <div style="color:#777; font-size:0.8rem;">{s.get('street')}</div>
                        </div>
                        <div class="price-text">{price:.2f}€</div>
                    </div>
                    """, unsafe_allow_html=True)
else:
    st.warning("Keine Daten gefunden.")
