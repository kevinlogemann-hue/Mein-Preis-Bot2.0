import streamlit as st
import requests
from streamlit_js_eval import streamlit_js_eval

# 1. CLEAN DESIGN (Stabile CSS-Struktur)
st.set_page_config(page_title="Wiesmoor Radar", layout="centered")

st.markdown("""
<style>
    .main-header {
        background: #1e3c72; color: white; padding: 25px;
        border-radius: 20px; text-align: center; margin-bottom: 25px;
    }
    .station-container {
        background: white; padding: 18px; border-radius: 20px;
        border: 1px solid #eaeaea; box-shadow: 0 4px 12px rgba(0,0,0,0.05);
        margin-bottom: 10px; display: flex; align-items: center;
    }
    .brand-icon {
        width: 50px; height: 50px; border-radius: 12px;
        background: #f1f3f6; display: flex; align-items: center;
        justify-content: center; font-size: 1.4rem; margin-right: 15px;
    }
    .price-box {
        margin-left: auto; text-align: right; font-size: 1.8rem;
        font-weight: 900; color: #1a1a1a; min-width: 100px;
    }
    /* Roter Korrektur-Link */
    .fix-link {
        color: #ff4b4b !important; font-size: 0.85rem;
        text-decoration: underline; cursor: pointer;
        margin-left: 65px; margin-bottom: 25px; display: block;
    }
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="main-header"><h1>WIESMOOR RADAR</h1><p>Community Preis-Check</p></div>', unsafe_allow_html=True)

# 2. STANDORT & API
if 'lat' not in st.session_state:
    st.session_state.lat, st.session_state.lng = 53.414, 7.733

if st.button("📍 Standort für Echtzeit-Preise ermitteln"):
    loc = streamlit_js_eval(js_expressions='navigator.geolocation ? new Promise((resolve) => { navigator.geolocation.getCurrentPosition(pos => resolve({lat: pos.coords.latitude, lon: pos.coords.longitude})) }) : null', key='gps_final_v4')
    if loc:
        st.session_state.lat, st.session_state.lng = loc['lat'], loc['lon']
        st.rerun()

@st.cache_data(ttl=60)
def get_stations(lat, lng):
    api_url = "https://creativecommons.tankerkoenig.de/json/list.php?lat=" + str(lat) + "&lng=" + str(lng) + "&rad=10&sort=dist&type=all&apikey=616cbb8e-9dde-4eb7-91f1-21a1663fa495"
    return requests.get(api_url).json().get("stations", [])

stations = get_stations(st.session_state.lat, st.session_state.lng)

# 3. ANZEIGE MIT ÜBERNAHME-LOGIK
if stations:
    tabs = st.tabs(["Super E5", "Super E10", "Diesel"])
    fuels = {"Super E5": "e5", "Super E10": "e10", "Diesel": "diesel"}

    for i, (label, f_key) in enumerate(fuels.items()):
        with tabs[i]:
            for s in sorted([x for x in stations if x.get(f_key)], key=lambda x: x.get(f_key)):
                s_id = str(s['id'])
                display_price = s.get(f_key)
                
                # Check ob User einen Preis "belegt" hat
                if f"user_price_{s_id}_{f_key}" in st.session_state:
                    display_price = st.session_state[f"user_price_{s_id}_{f_key}"]
                    st.success("✅ Preis durch Foto-Beleg aktualisiert!")

                # Tankstellen-Karte
                st.markdown('<div class="station-container">' +
                    '<div class="brand-icon">⛽</div>' +
                    '<div>' +
                        '<div style="font-weight:800; font-size:1.1rem;">' + str(s.get('brand', 'Tankstelle')).upper() + '</div>' +
                        '<div style="color:#777; font-size:0.8rem;">' + str(s.get('street')) + '</div>' +
                    '</div>' +
                    '<div class="price-box">' + "{:.2f}".format(display_price) + ' €</div>' +
                '</div>', unsafe_allow_html=True)
                
                # Korrektur-Button
                if st.button("⚠️ Preis an der Tankanzeige stimmt nicht? Hier korrigieren", key="btn_"+s_id+f_key):
                    st.session_state["cam_"+s_id] = True
                
                # Foto-Logik
                if st.session_state.get("cam_"+s_id):
                    with st.expander("Beweis-Foto hochladen", expanded=True):
                        pic = st.camera_input("Foto machen", key="pic_"+s_id)
                        if pic:
                            st.info("Foto empfangen! Welchen Preis siehst du auf dem Schild?")
                            new_val = st.number_input("Preis korrigieren:", value=display_price, step=0.01, key="num_"+s_id)
                            if st.button("Diesen Preis für alle bestätigen", key="save_"+s_id):
                                st.session_state[f"user_price_{s_id}_{f_key}"] = new_val
                                st.session_state["cam_"+s_id] = False
                                st.rerun()
else:
    st.info("Suche Tankstellen...")
