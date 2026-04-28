import streamlit as st
import requests
from streamlit_js_eval import streamlit_js_eval
from datetime import datetime
from PIL import Image

# 1. SETUP & DESIGN
st.set_page_config(page_title="Wiesmoor Radar", layout="centered")

st.markdown("""
<style>
    .header-container {
        width: 100%;
        height: 150px;
        background-image: url('https://images.unsplash.com/photo-1527018601619-a508a2be00cd?q=80&w=1000&auto=format&fit=crop');
        background-size: cover;
        background-position: center;
        border-radius: 15px;
        display: flex;
        align-items: center;
        justify-content: center;
        border: 2px solid #c10016;
    }
    .header-title {
        color: white;
        font-size: 1.8rem;
        font-weight: 900;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.7);
        background: rgba(180, 0, 0, 0.3);
        padding: 10px 20px;
        border-radius: 10px;
    }
    .info-box {
        background-color: #f0f2f6;
        border-radius: 10px;
        padding: 15px;
        margin: 15px 0;
        text-align: center;
        border: 1px solid #dcdfe3;
    }
    /* Das neue Icon-System */
    .brand-logo {
        width: 45px;
        height: 45px;
        border-radius: 10px;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 1.4rem;
        font-weight: 900;
        margin-right: 15px;
        box-shadow: 2px 2px 5px rgba(0,0,0,0.1);
    }
    .station-card {
        background: white;
        padding: 15px;
        margin: 10px 0;
        border-radius: 15px;
        border: 1px solid #eee;
        display: flex;
        align-items: center;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
    }
    .price-tag {
        font-size: 1.8rem;
        font-weight: 900;
        margin-left: auto;
    }
</style>
""", unsafe_allow_html=True)

# 2. BRAND STYLE LOGIC (Original Farben)
def get_brand_design(name):
    n = name.lower()
    # Aral: Hellblau / Weiß
    if "aral" in n:
        return {"bg": "#0070BB", "text": "white", "icon": "A", "border": "none"}
    # Score: Gelber Hintergrund, rote Schrift/Akzent
    elif "score" in n:
        return {"bg": "#FFD100", "text": "#E2001A", "icon": "SC", "border": "2px solid #E2001A"}
    # Behrens: Bär-Icon
    elif "behrens" in n:
        return {"bg": "#5D4037", "text": "white", "icon": "🐻", "border": "none"}
    # Shell: Gelb / Rot
    elif "shell" in n:
        return {"bg": "#FBCE07", "text": "#D50000", "icon": "S", "border": "1px solid #D50000"}
    # Jet: Gelb / Blau
    elif "jet" in n:
        return {"bg": "#FFD200", "text": "#003399", "icon": "J", "border": "none"}
    # Esso: Rot / Weiß
    elif "esso" in n:
        return {"bg": "#EF3340", "text": "white", "icon": "E", "border": "none"}
    else:
        return {"bg": "#455A64", "text": "white", "icon": "⛽", "border": "none"}

# --- APP START ---
st.markdown('<div class="header-container"><div class="header-title">WIESMOOR LIVE-RADAR</div></div>', unsafe_allow_html=True)
st.markdown('<div class="info-box">📸 <b>Community-Power:</b> Lade ein Foto hoch, um die Preise für alle aktuell zu halten!</div>', unsafe_allow_html=True)

# API Setup
API_KEY = "616cbb8e-9dde-4eb7-91f1-21a1663fa495"
if 'user_reports' not in st.session_state: st.session_state.user_reports = {}
if 'lat' not in st.session_state: st.session_state.lat, st.session_state.lng = 53.414, 7.733

c1, c2 = st.columns(2)
with c1:
    if st.button("📍 Standort"):
        loc = streamlit_js_eval(js_expressions='navigator.geolocation ? new Promise((resolve) => { navigator.geolocation.getCurrentPosition(pos => resolve({lat: pos.coords.latitude, lon: pos.coords.longitude})) }) : null', key='gps_v3')
        if loc:
            st.session_state.lat, st.session_state.lng = loc['lat'], loc['lon']
            st.rerun()
with c2:
    if st.button("🔄 Update"):
        st.cache_data.clear()
        st.rerun()

@st.cache_data(ttl=60)
def get_data(la, ln):
    try:
        url = f"https://creativecommons.tankerkoenig.de/json/list.php?lat={la}&lng={ln}&rad=10&sort=dist&type=all&apikey={API_KEY}"
        return requests.get(url).json().get("stations", [])
    except: return []

stations = get_data(st.session_state.lat, st.session_state.lng)

if stations:
    tabs = st.tabs(["Super E5", "Super E10", "Diesel"])
    keys = {"Super E5": "e5", "Super E10": "e10", "Diesel": "diesel"}

    for i, (label, k) in enumerate(keys.items()):
        with tabs[i]:
            for s in stations:
                if s.get(k):
                    sid = s['id']
                    design = get_brand_design(s.get('brand', ''))
                    
                    st.markdown(f"""
                    <div class="station-card">
                        <div class="brand-logo" style="background-color: {design['bg']}; color: {design['text']}; border: {design['border']};">
                            {design['icon']}
                        </div>
                        <div>
                            <div style="font-weight:bold; font-size:1.1rem;">{s.get('brand', 'Tankstelle').upper()}</div>
                            <div style="color:#666; font-size:0.8rem;">{s.get('street')}</div>
                        </div>
                        <div class="price-tag">{s.get(k):.2f}€</div>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    if st.button(f"📸 Beleg senden", key=f"btn_{sid}_{k}"):
                        st.session_state[f"up_{sid}"] = True
                    
                    if st.session_state.get(f"up_{sid}"):
                        f = st.file_uploader("Foto machen", type=['jpg','png'], key=f"f_{sid}")
                        if f:
                            st.session_state.user_reports[sid] = {"t": datetime.now().strftime("%H:%M")}
                            st.success("Danke für deine Hilfe!")
                            del st.session_state[f"up_{sid}"]
                            st.rerun()
                            
                    if sid in st.session_state.user_reports:
                        st.info(f"✅ Community-Bestätigung ({st.session_state.user_reports[sid]['t']} Uhr)")
else:
    st.warning("Keine Daten gefunden. Bitte Standort prüfen.")
