import streamlit as st
import requests
import folium
from streamlit_folium import st_folium
from streamlit_js_eval import streamlit_js_eval

# 1. SETUP
st.set_page_config(page_title="Wiesmoor Radar", page_icon="⛽", layout="centered")
API_KEY = "616cbb8e-9dde-4eb7-91f1-21a1663fa495"

st.markdown('<div style="background:#e2001a;color:white;padding:20px;text-align:center;border-radius:15px;font-weight:bold;font-size:1.6rem;">⛽ WIESMOOR LIVE-RADAR</div>', unsafe_allow_html=True)

# 2. STANDORT-LOGIK (Standard: Wiesmoor)
if 'user_lat' not in st.session_state:
    st.session_state.user_lat, st.session_state.user_lng = 53.414, 7.733

location = streamlit_js_eval(js_expressions='navigator.geolocation ? new Promise((resolve) => { navigator.geolocation.getCurrentPosition(pos => resolve({lat: pos.coords.latitude, lon: pos.coords.longitude}), () => resolve(null)) }) : null', key='get_loc')

if st.button("📍 Meinen Standort nutzen"):
    if location:
        st.session_state.user_lat, st.session_state.user_lng = location['lat'], location['lon']
        st.rerun()

# 3. DATEN LADEN
def get_data(lat, lng):
    url = f"https://creativecommons.tankerkoenig.de/json/list.php?lat={lat}&lng={lng}&rad=15&sort=dist&type=all&apikey={API_KEY}"
    try:
        r = requests.get(url, timeout=10)
        data = r.json()
        return data.get("stations", [])
    except:
        return []

stations = get_data(st.session_state.user_lat, st.session_state.user_lng)

# 4. ANZEIGE
if stations:
    tabs = st.tabs(["Super E5", "Super E10", "Diesel", "🗺️ Karte"])
    
    fuel_map = {"Super E5": "e5", "Super E10": "e10", "Diesel": "diesel"}
    for i, label in enumerate(["Super E5", "Super E10", "Diesel"]):
        fuel_key = fuel_map[label]
        with tabs[i]:
            valid = [s for s in stations if s.get(fuel_key) and s.get(fuel_key) > 0]
            if valid:
                sorted_s = sorted(valid, key=lambda x: (not x['isOpen'], x[fuel_key]))
                for s in sorted_s:
                    color = "#28a745" if s.get('isOpen') else
