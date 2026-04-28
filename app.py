import streamlit as st
import requests
from streamlit_js_eval import streamlit_js_eval
from datetime import datetime
from PIL import Image

# 1. Seiteneinstellungen
st.set_page_config(page_title="Wiesmoor Radar", layout="centered")

# 2. Einfaches Styling ohne komplizierte Python-Variablen
st.markdown("""
<style>
    .header-box {
        background-color: #e2001a;
        background-image: url('https://images.unsplash.com/photo-1527018601619-a508a2be00cd?q=80&w=1000&auto=format&fit=crop');
        background-size: cover;
        background-position: center;
        height: 150px;
        border-radius: 15px;
        display: flex;
        align-items: center;
        justify-content: center;
        border: 2px solid #c10016;
    }
    .header-text {
        color: white;
        font-size: 1.8rem;
        font-weight: 900;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.7);
        text-align: center;
    }
    .info-text {
        text-align: center;
        color: #555;
        margin: 15px 0;
    }
</style>
""", unsafe_allow_html=True)

# 3. Header & Text anzeigen
st.markdown('<div class="header-box"><div class="header-text">WIESMOOR LIVE-RADAR</div></div>', unsafe_allow_html=True)

st.markdown("""
<div class="info-text">
    📸 <b>Mache Fotos für die Community für die Echtzeit-Preisangaben.</b><br>
    Umso mehr mitmachen, desto genauer werden die Preise werden!
</div>
""", unsafe_allow_html=True)

# 4. App Logik
API_KEY = "616cbb8e-9dde-4eb7-91f1-21a1663fa495"

if 'user_reports' not in st.session_state:
    st.session_state.user_reports = {}
if 'lat' not in st.session_state:
    st.session_state.lat = 53.414
if 'lng' not in st.session_state:
    st.session_state.lng = 7.733

# Buttons
c1, c2 = st.columns(2)
with c1:
    if st.button("📍 Standort"):
        loc = streamlit_js_eval(js_expressions='navigator.geolocation ? new Promise((resolve) => { navigator.geolocation.getCurrentPosition(pos => resolve({lat: pos.coords.latitude, lon: pos.coords.longitude})) }) : null', key='gps_btn')
        if loc:
            st.session_state.lat = loc['lat']
            st.session_state.lng = loc['lon']
            st.rerun()
with c2:
    if st.button("🔄 Update"):
        st.cache_data.clear()
        st.rerun()

# Daten laden
@st.cache_data(ttl=60)
def load_data(la, ln):
    u = f"https://creativecommons.tankerkoenig.de/json/list.php?lat={la}&lng={ln}&rad=15&sort=dist&type=all&apikey={API_KEY}"
    try:
        return requests.get(u).json().get("stations", [])
    except:
        return []

data = load_data(st.session_state.lat, st.session_state.lng)

# 5. Anzeige
if data:
    tabs = st.tabs(["Super E5", "Super E10", "Diesel"])
    keys = ["e5", "e10", "diesel"]
    
    for i, k in enumerate(keys):
        with tabs[i]:
            for s in data:
                if s.get(k):
                    sid = s['id']
                    # Tankstellen-Karte
                    st.markdown(f"""
                    <div style="border:1px solid #ddd; padding:10px; margin:10px 0; border-radius:10px; border-left: 5px solid {'#28a745' if s.get('isOpen') else '#888'};">
                        <b style="font-size:1.1rem;">{(s.get('brand') or 'Tankstelle').upper()}</b><br>
                        <span style="color:#666;">{s.get('street')}</span><br>
                        <span style="font-size:1.5rem; font-weight:bold; float:right; margin-top:-25px;">{s.get(k):.2f}€</span>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    # Melde-Logik
                    if st.button(f"📸 Foto senden", key=f"btn_{sid}_{k}"):
                        st.session_state[f"up_{sid}"] = True
                    
                    if st.session_state.get(f"up_{sid}"):
                        f = st.file_uploader("Bild wählen", type=['jpg','
