import streamlit as st
import requests
from streamlit_js_eval import streamlit_js_eval

# 1. DAS EDLE LAYOUT (CSS)
st.set_page_config(page_title="Wiesmoor Radar", layout="centered")

st.markdown("""
<style>
    .hero-banner {
        width: 100%; height: 120px;
        background: linear-gradient(rgba(0,0,0,0.5), rgba(0,0,0,0.7)), 
                    url('https://images.unsplash.com/photo-1527018601619-a508a2be00cd?q=80&w=1000');
        background-size: cover; background-position: center; border-radius: 15px;
        display: flex; align-items: center; justify-content: center; margin-bottom: 20px;
    }
    .hero-title { color: white; font-size: 1.8rem; font-weight: 900; }

    .station-card {
        background: white; padding: 15px; border-radius: 18px;
        display: flex; align-items: center; border: 1px solid #eee;
        box-shadow: 0 4px 10px rgba(0,0,0,0.05); margin-bottom: 5px;
    }
    .brand-logo {
        width: 45px; height: 45px; border-radius: 10px;
        display: flex; align-items: center; justify-content: center;
        font-size: 1.2rem; font-weight: bold; flex-shrink: 0;
    }
    .price-tag { margin-left: auto; font-size: 1.8rem; font-weight: 900; color: #000; }

    /* Der Korrektur-Link-Button */
    div.stButton > button {
        background: none !important;
        border: none !important;
        color: #6c757d !important;
        font-size: 0.75rem !important;
        text-decoration: underline !important;
        padding: 0 !important;
        margin-top: -10px !important;
        margin-bottom: 20px !important;
        font-weight: 400 !important;
    }
    div.stButton > button:hover {
        color: #ff4b4b !important;
    }
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="hero-banner"><div class="hero-title">WIESMOOR RADAR</div></div>', unsafe_allow_html=True)

# 2. STANDORT & FILTER
if 'lat' not in st.session_state:
    st.session_state.lat, st.session_state.lng = 53.414, 7.733

c1, c2, c3 = st.columns([1, 1, 1.5])
with c1:
    if st.button("📍 GPS"):
        loc = streamlit_js_eval(js_expressions='navigator.geolocation ? new Promise((resolve) => { navigator.geolocation.getCurrentPosition(pos => resolve({lat: pos.coords.latitude, lon: pos.coords.longitude})) }) : null', key='gps_final')
        if loc:
            st.session_state.lat, st.session_state.lng = loc['lat'], loc['lon']
            st.rerun()
with c2:
    radius = st.selectbox("km", [5, 10, 25], index=1)
with c3:
    sort_by = st.selectbox("Sortierung", ["Günstigste", "Entfernung"])

# 3. DATEN-LOGIK
API_KEY = "616cbb8e-9dde-4eb7-91f1-21a1663fa495"

def get_style(brand):
    b = (brand or "").lower()
    if "aral" in b: return "#0070BB", "white", "A"
    if "score" in b: return "#FFD100", "#E2001A", "S"
    if "behrens" in b: return "#5D4037", "white", "B"
    if "jet" in b: return "#FFD200", "#003399", "J"
    return "#e9ecef", "#495057", "⛽"

@st.cache_data(ttl=60)
def fetch_stations(la, ln, rad):
    url = f"https://creativecommons.tankerkoenig.de/json/list.php?lat={la}&lng={ln}&rad={rad}&sort=dist&type=all&apikey={API_KEY}"
    try:
        return requests.get(url).json().get("stations", [])
    except: return []

stations = fetch_stations(st.session_state.lat, st.session_state.lng, radius)

# 4. ANZEIGE
if stations:
    tabs = st.tabs(["Super E5", "Super E10", "Diesel"])
    f_keys = {"Super E5": "e5", "Super E10": "e10", "Diesel": "diesel"}

    for i, (label, f_key) in enumerate(f_keys.items()):
        with tabs[i]:
            valid = [s for s in stations if s.get(f_key)]
            if sort_by == "Günstigste":
                sorted_list = sorted(valid, key=lambda x: x.get(f_key))
            else:
                sorted_list = sorted(valid, key=lambda x: x.get('dist'))

            for s in sorted_list:
                price = s.get(f_key)
                name = (s.get('brand') or s.get('name') or "Tankstelle").upper()
                bg, tx, icon = get_style(name)
                
                # Die schicke Karte
                st.markdown(f"""
                <div class="station-card">
                    <div class="brand-logo" style="background-color: {bg}; color: {tx};">{icon}</div>
                    <div style="margin-left: 15px;">
                        <div style="font-weight: 800; font-size: 1rem;">{name}</div>
                        <div style="color: #888; font-size: 0.75rem;">{s.get('street')} ({s.get('dist')} km)</div>
                    </div>
                    <div class="price-tag">{price:.2f}€</div>
                </div>
                """, unsafe_allow_html=True)
                
                # Dein Wunsch-Text als dezenter Button
                if st.button(f"ℹ️ Preis an der Tankanzeige stimmt nicht? Hier korrigieren", key=f"f_{s['id']}_{f_key}"):
                    st.session_state[f"cam_{s['id']}"] = True
                
                if st.session_state.get(f"cam_{s['id']}"):
                    st.info("Helfe der Community: Lade ein Foto der Preistafel hoch!")
                    st.file_uploader("Foto wählen", type=['jpg', 'png'], key=f"up_{s['id']}")
else:
    st.info("Suche läuft...")
