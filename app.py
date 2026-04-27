import streamlit as st
import requests
import folium
from streamlit_folium import st_folium
from streamlit_js_eval import streamlit_js_eval

# 1. KONFIGURATION
st.set_page_config(page_title="Wiesmoor Radar", page_icon="⛽", layout="centered")
API_KEY = "616cbb8e-9dde-4eb7-91f1-21a1663fa495"

st.markdown('<div style="background:#e2001a;color:white;padding:20px;text-align:center;border-radius:15px;font-weight:bold;font-size:1.6rem;">⛽ WIESMOOR LIVE-RADAR</div>', unsafe_allow_html=True)

# 2. STANDORT-LOGIK
if 'user_lat' not in st.session_state:
    st.session_state.user_lat, st.session_state.user_lng = 53.414, 7.733

loc_data = streamlit_js_eval(js_expressions='navigator.geolocation ? new Promise((resolve) => { navigator.geolocation.getCurrentPosition(pos => resolve({lat: pos.coords.latitude, lon: pos.coords.longitude}), () => resolve(null), {enableHighAccuracy: true}) }) : null', key='get_gps_loc')

if st.button("📍 Meinen Standort finden"):
    if loc_data:
        st.session_state.user_lat, st.session_state.user_lng = loc_data['lat'], loc_data['lon']
        st.rerun()

# 3. DATEN LADEN
@st.cache_data(ttl=300)
def get_gas_data(lat, lng):
    url = f"https://creativecommons.tankerkoenig.de/json/list.php?lat={lat}&lng={lng}&rad=15&sort=dist&type=all&apikey={API_KEY}"
    try:
        return requests.get(url, timeout=10).json().get("stations", [])
    except: return []

stations = get_gas_data(st.session_state.user_lat, st.session_state.user_lng)
