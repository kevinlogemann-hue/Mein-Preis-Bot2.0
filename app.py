import streamlit as st
import requests
from streamlit_js_eval import streamlit_js_eval

# 1. ERWEITERTES DESIGN-SYSTEM
st.set_page_config(page_title="Wiesmoor Radar", layout="centered")

st.markdown("""
<style>
    /* Haupt-Header mit Glas-Effekt */
    .main-header {
        background: linear-gradient(135deg, #e2001a 0%, #b30014 100%);
        color: white;
        padding: 25px;
        border-radius: 20px;
        text-align: center;
        margin-bottom: 20px;
        box-shadow: 0 10px 20px rgba(226, 0, 26, 0.2);
    }
    .header-title { font-size: 2.4rem; font-weight: 900; letter-spacing: -1px; margin: 0; }
    
    /* Community Power Box */
    .community-box {
        background-color: #f8f9fa;
        border: 1px solid #e9ecef;
        padding: 15px;
        border-radius: 15px;
        display: flex;
        align-items: center;
        gap: 15px;
        margin-bottom: 25px;
    }

    /* Hochwertige Brand-Icons */
    .brand-icon {
        width: 60px;
        height: 60px;
        border-radius: 16px;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 1.8rem;
        font-weight: 800;
        box-shadow: inset 0 -4px 0 rgba(0,0,0,0.1), 0 4px 10px rgba(0,0,0,0.1);
        text-shadow: 1px 1px 2px rgba(0,0,0,0.1);
        flex-shrink: 0;
    }

    /* Stations-Karte */
    .station-card {
        background: white;
        padding: 20px;
        border-radius: 20px;
        margin-bottom: 15px;
        display: flex;
        align-items: center;
        box-shadow: 0 2px 12px rgba(0,0,0,0.05);
        border: 1px solid #f1f3f5;
    }
    
    .price-tag {
        margin-left: auto;
        font-size: 2.1rem;
        font-weight: 900;
        color: #1a1a1a;
        letter-spacing: -1px;
    }

    /* Beleg-Button Style */
    .beleg-btn {
        display: inline-flex;
        align-items: center;
        padding: 6px 12px;
        background: #fff;
        border: 1px solid #dee2e6;
        border-radius: 8px;
        font-size: 0.85rem;
        color: #495057;
        margin-top: 8px;
        cursor: pointer;
    }
</style>
""", unsafe_allow_html=True)

# 2. BRAND IDENTITIES (Hochwertige Farbprofile)
def get_brand_style(name):
    name = name.lower()
    if "aral" in name:
        return {"bg": "#0070BB", "color": "#FFFFFF", "icon": "A", "border": "none"}
    if "score" in name:
        return {"bg": "#FFD100", "color": "#E2001A", "icon": "S", "border": "2px solid #E2001A"}
    if "behrens" in name:
        return {"bg": "#5D4037", "color": "#FFFFFF", "icon": "B", "border": "none"}
    if "q1" in name:
        return {"bg": "#FFFFFF", "color": "#E30613", "icon": "Q1", "border": "2px solid #E30613"}
    if "jet" in name:
        return {"bg": "#FFD200", "color": "#003399", "icon": "J", "border": "none"}
    return {"bg": "#455A64", "color": "#FFFFFF", "icon": "⛽", "border": "none"}

# --- UI START ---
st.markdown('<div class="main-header"><p class="header-title">⛽ WIESMOOR LIVE-RADAR</p></div>', unsafe_allow_html=True)

# Community Power Hinweis
st.markdown("""
<div class="community-box">
    <div style="font-size: 2rem;">📸</div>
    <div>
        <div style="font-weight: 800; color: #1a1a1a;">Community-Power:</div>
        <div style="color: #6c757d; font-size: 0.9rem;">Lade ein Foto hoch, um die Preise für alle aktuell zu halten!</div>
    </div>
</div>
""", unsafe_allow_html=True)

# Standort & Refresh
col_gps, col_ref = st.columns(2)
with col_gps:
    if st.button("📍 Standort ermitteln", use_container_width=True):
        loc = streamlit_js_eval(js_expressions='navigator.geolocation ? new Promise((resolve) => { navigator.geolocation.getCurrentPosition(pos => resolve({lat: pos.coords.latitude, lon: pos.coords.longitude})) }) : null', key='gps_v6')
        if loc:
            st.session_state.lat, st.session_state.lng = loc['lat'], loc['lon']
            st.rerun()

with col_ref:
    if st.button("🔄 Preise laden", use_container_width=True):
        st.cache_data.clear()
        st.rerun()

# API Abruf
API_KEY = "616cbb8e-9dde-4eb7-91f1-21a1663fa495"
if 'lat' not in st.session_state: st.session_state.lat, st.session_state.lng = 53.414, 7.733

@st.cache_data(ttl=60)
def fetch_stations(la, ln):
    url = f"https://creativecommons.tankerkoenig.de/json/list.php?lat={la}&lng={ln}&rad=10&sort=dist&type=all&apikey={API_KEY}"
    return requests.get(url).json().get("stations", [])

stations = fetch_stations(st.session_state.lat, st.session_state.lng)

# Tabs für Kraftstoffe
t1, t2, t3 = st.tabs(["Super E5", "Super E10", "Diesel"])
fuel_map = {"e5": t1, "e10": t2, "diesel": t3}

for fuel_key, tab in fuel_map.items():
    with tab:
        for s in stations:
            price = s.get(fuel_key)
            if price:
                style = get_brand_style(s.get('brand', ''))
                st.markdown(f"""
                <div class="station-card">
                    <div class="brand-icon" style="background-color: {style['bg']}; color: {style['color']}; border: {style['border']};">
                        {style['icon']}
                    </div>
                    <div style="margin-left: 15px;">
                        <div style="font-weight: 800; font-size: 1.1rem; color: #1a1a1a;">{s.get('brand', 'Tankstelle').upper()}</div>
                        <div style="color: #adb5bd; font-size: 0.85rem;">{s.get('street')}</div>
                        <div class="beleg-btn">📸 Beleg senden</div>
                    </div>
                    <div class="price-tag">{price:.2f}€</div>
                </div>
                """, unsafe_allow_html=True)
