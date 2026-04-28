import streamlit as st
import requests
import folium
from streamlit_folium import st_folium
from streamlit_js_eval import streamlit_js_eval
from datetime import datetime
from PIL import Image

# 1. SETUP & MODERNES DESIGN (CSS)
st.set_page_config(page_title="Wiesmoor Radar", page_icon="⛽", layout="centered")

st.markdown("""
    <style>
    /* Die Community-Box */
    .community-box {
        background-color: #f8f9fa;
        border: 1px solid #e0e0e0;
        border-radius: 10px;
        padding: 12px;
        margin-top: 8px;
        color: #444;
        font-size: 0.85rem;
        display: flex;
        align-items: center;
        gap: 10px;
    }
    .report-icon {
        font-size: 1.2rem;
    }
    /* Button Styling */
    .stButton>button {
        border-radius: 20px;
        text-transform: uppercase;
        font-size: 0.7rem;
        letter-spacing: 0.5px;
    }
    </style>
    """, unsafe_allow_html=True)

# Header
st.markdown('<div style="background:#e2001a;color:white;padding:20px;text-align:center;border-radius:15px;font-weight:bold;font-size:1.6rem;">⛽ WIESMOOR LIVE-RADAR</div>', unsafe_allow_html=True)

# Kurzer, freundlicher Hinweis
st.caption("Echtzeit-Preise für Wiesmoor & Umgebung. Melde Abweichungen für die Community!")

API_KEY = "616cbb8e-9dde-4eb7-91f1-21a1663fa495"

# Speicher für Meldungen
if 'user_reports' not in st.session_state:
    st.session_state.user_reports = {}
if 'lat' not in st.session_state:
    st.session_state.lat, st.session_state.lng = 53.414, 7.733

# 2. BEDIENUNG
col_a, col_b = st.columns(2)
with col_a:
    loc = streamlit_js_eval(js_expressions='navigator.geolocation ? new Promise((resolve) => { navigator.geolocation.getCurrentPosition(pos => resolve({lat: pos.coords.latitude, lon: pos.coords.longitude}), () => resolve(null), {enableHighAccuracy: true}) }) : null', key='gps_final')
    if st.button("📍 Standort"):
        if loc:
            st.session_state.lat, st.session_state.lng = loc['lat'], loc['lon']
            st.rerun()
with col_b:
    if st.button("🔄 Aktualisieren"):
        st.cache_data.clear()
        st.rerun()

# 3. DATEN-ABFRAGE
@st.cache_data(ttl=60)
def fetch_now(lat, lng):
    url = f"https://creativecommons.tankerkoenig.de/json/list.php?lat={lat}&lng={lng}&rad=15&sort=dist&type=all&apikey={API_KEY}"
    try:
        r = requests.get(url, timeout=5)
        return r.json().get("stations", [])
    except: return []

stations = fetch_now(st.session_state.lat, st.session_state.lng)

# 4. TABS & LISTEN
if stations:
    tabs = st.tabs(["Super E5", "Super E10", "Diesel", "🗺️ Karte"])
    fuels = {"Super E5": "e5", "Super E10": "e10", "Diesel": "diesel"}

    for i, (label, key) in enumerate(fuels.items()):
        with tabs[i]:
            valid_s = [s for s in stations if s.get(key) and s.get(key) > 0]
            valid_s.sort(key=lambda x: (not x.get('isOpen'), x.get(key)))

            for s in valid_s:
                sid = s['id']
                name = str(s.get('brand') or s.get('name') or "Tankstelle").upper()
                col = "#28a745" if s.get('isOpen') else "#888"
                
                # Tankstellen-Karte
                st.markdown(f"""
                <div style="border:1px solid #ddd; padding:15px; margin:10px 0 5px 0; background:white; border-radius:12px; border-left: 6px solid {col};">
                    <div style="display: flex; justify-content: space-between; align-items: center;">
                        <div>
                            <div style="font-weight:bold; font-size:1rem; color:#222;">{name}</div>
                            <div style="color:#777; font-size:0.75rem;">{s.get('street')} • {s.get('dist')} km</div>
                        </div>
                        <div style="font-size:1.6rem; font-weight:900; color:#111;">{s.get(key):.2f}€</div>
                    </div>
                </div>
                """, unsafe_allow_html=True)

                # Melde-Bereich (Dezent unter der Karte)
                c1, c2 = st.columns([1, 1])
                
                # Falls eine Meldung vorliegt, zeige sie hübsch an
                if sid in st.session_state.user_reports:
                    rep = st.session_state.user_reports[sid]
                    st.markdown(f"""
                        <div class="community-box">
                            <span class="report-icon">📸</span>
                            <div><b>Live-Update ({rep['time']}):</b> Preis wurde per Foto bestätigt/korrigiert.</div>
                        </div>
                    """, unsafe_allow_html=True)
                    if st.button("Foto zeigen", key=f"v_{sid}_{key}"):
                        st.image(rep['img'], use_container_width=True)

                # Melde-Button
                if c1.button("📸 Preis-Foto senden", key=f"m_{sid}_{key}"):
                    st.session_state[f"up_{sid}"] = True

                if st.session_state.get(f"up_{sid}"):
                    up = st.file_uploader("Foto der Preistafel wählen", type=['jpg','jpeg','png'], key=f"f_{sid}_{key}")
                    if up:
                        st.session_state.user_reports[sid] = {"time": datetime.now().strftime("%H:%M"), "img": Image.open(up)}
                        del st.session_state[f"up_{sid}"]
                        st.rerun()
else:
    st.info("Suche Tankstellen...")
