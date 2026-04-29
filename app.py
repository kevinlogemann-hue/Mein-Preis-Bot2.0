import streamlit as st
import requests
from streamlit_js_eval import streamlit_js_eval

# 1. DESIGN SETUP (Absolut sicher ohne f-strings im CSS)
st.set_page_config(page_title="Wiesmoor Radar", layout="centered")

st.markdown("""
<style>
    .hero {
        background: #1e3c72; color: white; padding: 20px;
        border-radius: 15px; text-align: center; margin-bottom: 20px;
    }
    .card {
        background: white; padding: 15px; border-radius: 15px;
        display: flex; align-items: center; border: 1px solid #eee;
        box-shadow: 0 2px 8px rgba(0,0,0,0.05); margin-bottom: 10px;
    }
    .logo {
        width: 45px; height: 45px; border-radius: 10px; background: #f0f2f6;
        display: flex; align-items: center; justify-content: center;
        font-weight: bold; margin-right: 15px;
    }
    .price { margin-left: auto; font-size: 1.6rem; font-weight: 800; }
    
    /* Button Styling */
    div.stButton > button {
        background: none !important; border: none !important;
        color: #ff4b4b !important; text-decoration: underline !important;
        font-size: 0.85rem !important; padding: 0 !important;
        margin-bottom: 20px !important; margin-left: 60px !important;
    }
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="hero"><h1>WIESMOOR RADAR</h1><p>Preise prüfen & korrigieren</p></div>', unsafe_allow_html=True)

# 2. STANDORT
if 'lat' not in st.session_state:
    st.session_state.lat, st.session_state.lng = 53.414, 7.733

if st.button("📍 Meinen Standort aktualisieren"):
    loc = streamlit_js_eval(js_expressions='navigator.geolocation ? new Promise((resolve) => { navigator.geolocation.getCurrentPosition(pos => resolve({lat: pos.coords.latitude, lon: pos.coords.longitude})) }) : null', key='gps_v3')
    if loc:
        st.session_state.lat, st.session_state.lng = loc['lat'], loc['lon']
        st.rerun()

# 3. DATEN LADEN
API_KEY = "616cbb8e-9dde-4eb7-91f1-21a1663fa495"

@st.cache_data(ttl=60)
def fetch_stations(lat, lng):
    url = "https://creativecommons.tankerkoenig.de/json/list.php?lat=" + str(lat) + "&lng=" + str(lng) + "&rad=10&sort=dist&type=all&apikey=" + API_KEY
    try:
        return requests.get(url).json().get("stations", [])
    except: return []

stations = fetch_stations(st.session_state.lat, st.session_state.lng)

# 4. ANZEIGE & LOGIK
if stations:
    tabs = st.tabs(["Super E5", "Super E10", "Diesel"])
    fuel_keys = {"Super E5": "e5", "Super E10": "e10", "Diesel": "diesel"}

    for i, (label, f_key) in enumerate(fuel_keys.items()):
        with tabs[i]:
            # Sortieren nach Preis
            valid = [s for s in stations if s.get(f_key)]
            sorted_s = sorted(valid, key=lambda x: x.get(f_key))

            for s in sorted_s:
                s_id = str(s['id'])
                current_price = s.get(f_key)
                
                # Falls User korrigiert hat, diesen Preis nehmen
                if f"fix_{s_id}_{f_key}" in st.session_state:
                    current_price = st.session_state[f"fix_{s_id}_{f_key}"]
                    st.success("✅ Preis wurde durch dein Foto-Beleg aktualisiert!")

                # Karte anzeigen (Strings einzeln zusammengefügt gegen Syntax-Fehler)
                st.markdown('<div class="card">' +
                    '<div class="logo">⛽</div>' +
                    '<div>' +
                        '<div style="font-weight:bold; text-transform:uppercase;">' + str(s.get('brand', 'Freie Tanke')) + '</div>' +
                        '<div style="color:gray; font-size:0.8rem;">' + str(s.get('street')) + '</div>' +
                    '</div>' +
                    '<div class="price">' + str(current_price) + ' €</div>' +
                '</div>', unsafe_allow_html=True)
                
                # Korrektur-Sektion
                if st.button("⚠️ Preis an der Tankanzeige stimmt nicht? Hier korrigieren", key="btn_" + s_id + f_key):
                    st.session_state["cam_" + s_id] = True
                
                if st.session_state.get("cam_" + s_id):
                    with st.container():
                        img = st.camera_input("Foto der Preistafel machen", key="input_" + s_id)
                        if img:
                            st.info("Foto erkannt. Der Preis wird in Kürze abgeglichen.")
                            # Simulation der Korrektur:
                            if st.button("Korrektur bestätigen", key="conf_" + s_id):
                                st.session_state[f"fix_{s_id}_{f_key}"] = current_price - 0.05 # Beispiel-Anpassung
                                st.session_state["cam_" + s_id] = False
                                st.rerun()
else:
    st.warning("Suche läuft oder keine Daten verfügbar.")
