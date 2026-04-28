import streamlit as st
import requests
import folium
from streamlit_folium import st_folium
from streamlit_js_eval import streamlit_js_eval
from datetime import datetime
from PIL import Image

# 1. SETUP & VERBESSERTES DESIGN
st.set_page_config(page_title="Wiesmoor Radar", page_icon="⛽", layout="centered")

st.markdown("""
    <style>
    /* Der stabilere Retro-Header */
    .header-container {
        position: relative;
        width: 100%;
        height: 150px;
        background: #e2001a; /* Fallback Farbe Rot */
        background-image: url('https://images.unsplash.com/photo-1527018601619-a508a2be00cd?q=80&w=1000&auto=format&fit=crop');
        background-size: cover;
        background-position: center;
        border-radius: 15px;
        display: flex;
        align-items: center;
        justify-content: center;
        margin-bottom: 20px;
        border: 2px solid #c10016;
    }
    
    .header-overlay {
        background: rgba(226, 0, 26, 0.4); /* Roter Schimmer über dem Bild */
        width: 100%;
        height: 100%;
        border-radius: 13px;
        display: flex;
        align-items: center;
        justify-content: center;
    }

    .header-title {
        color: white;
        font-size: 1.8rem;
        font-weight: 900;
        text-align: center;
        text-shadow: 3px 3px 6px rgba(0,0,0,0.7);
        letter-spacing: 1px;
    }

    /* Community-Box Styling */
    .community-box {
        background-color: #f0f2f6;
        border-radius: 10px;
        padding: 10px;
        margin-top: 5px;
        border-left: 5px solid #e2001a;
    }
    </style>
    """, unsafe_allow_html=True)

# --- HEADER ANZEIGEN ---
st.markdown("""
    <div class="header-container">
        <div class="header-overlay">
            <div class="header-title">WIESMOOR LIVE-RADAR</div>
        </div>
    </div>
""", unsafe_allow_html=True)

st.caption("📍 Echtzeit-Preise für Wiesmoor & Umgebung")

# --- API & LOGIK ---
API_KEY = "616cbb8e-9dde-4eb7-91f1-21a1663fa495"

if 'user_reports' not in st.session_state:
    st.session_state.user_reports = {}
if 'lat' not in st.session_state:
    st.session_state.lat, st.session_state.lng = 53.414, 7.733

# Buttons
col_a, col_b = st.columns(2)
with col_a:
    loc = streamlit_js_eval(js_expressions='navigator.geolocation ? new Promise((resolve) => { navigator.geolocation.getCurrentPosition(pos => resolve({lat: pos.coords.latitude, lon: pos.coords.longitude})) }) : null', key='gps_final_v4')
    if st.button("📍 Standort"):
        if loc:
            st.session_state.lat, st.session_state.lng = loc['lat'], loc['lon']
            st.rerun()
with col_b:
    if st.button("🔄 Update"):
        st.cache_data.clear()
        st.rerun()

# Daten laden
@st.cache_data(ttl=60)
def fetch_now(lat, lng):
    url = f"https://creativecommons.tankerkoenig.de/json/list.php?lat={lat}&lng={lng}&rad=15&sort=dist&type=all&apikey={API_KEY}"
    try:
        r = requests.get(url, timeout=5)
        return r.json().get("stations", [])
    except: return []

stations = fetch_now(st.session_state.lat, st.session_state.lng)

# Liste anzeigen
if stations:
    tab_labels = ["Super E5", "Super E10", "Diesel"]
    tabs = st.tabs(tab_labels)
    fuels = {"Super E5": "e5", "Super E10": "e10", "Diesel": "diesel"}

    for i, (label, key) in enumerate(fuels.items()):
        with tabs[i]:
            valid_s = [s for s in stations if s.get(key) and s.get(key) > 0]
            for s in valid_s:
                sid = s['id']
                name = str(s.get('brand') or s.get('name')).upper()
                
                st.markdown(f"""
                <div style="border:1px solid #ddd; padding:15px; margin:10px 0; background:white; border-radius:12px; border-left: 6px solid {'#28a745' if s.get('isOpen') else '#888'};">
                    <div style="display: flex; justify-content: space-between; align-items: center;">
                        <div>
                            <div style="font-weight:bold; font-size:1.1rem;">{name}</div>
                            <div style="color:#777; font-size:0.8rem;">{s.get('street')}</div>
                        </div>
                        <div style="font-size:1.7rem; font-weight:900;">{s.get(key):.2f}€</div>
                    </div>
                </div>
                """, unsafe_allow_html=True)

                # Melde-Button dezent darunter
                if st.button(f"📸 Foto-Beleg senden", key=f"btn_{sid}_{key}"):
                    st.session_state[f"up_{sid}"] = True
                
                if st.session_state.get(f"up_{sid}"):
                    up = st.file_uploader("Preistafel fotografieren", type=['jpg','png'], key=f"f_{sid}")
                    if up:
                        st.session_state.user_reports[sid] = {"time": datetime.now().strftime("%H:%M"), "img": Image.open(up)}
                        del st.session_state[f"up_{sid}"]
                        st.rerun()

                if sid in st.session_state.user_reports:
                    rep = st.session_state.user_reports[sid]
                    st.info(f"✅ Bestätigt um {rep['time']} Uhr (Klick für Foto)")
                    if st.button("Beleg öffnen", key=f"show_{sid}_{key}"):
                        st.image(rep['img'])
else:
    st.warning("Suche Tankstellen...")
