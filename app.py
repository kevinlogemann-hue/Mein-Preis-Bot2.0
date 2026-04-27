import streamlit as st
import requests
import folium
from streamlit_folium import st_folium
from streamlit_js_eval import streamlit_js_eval

# 1. SETUP
st.set_page_config(page_title="Wiesmoor Radar", page_icon="⛽", layout="centered")
API_KEY = "616cbb8e-9dde-4eb7-91f1-21a1663fa495"

st.markdown('<div style="background:#e2001a;color:white;padding:20px;text-align:center;border-radius:15px;font-weight:bold;font-size:1.6rem;">⛽ WIESMOOR LIVE-RADAR</div>', unsafe_allow_html=True)

# 2. STANDORT
if 'user_lat' not in st.session_state:
    st.session_state.user_lat, st.session_state.user_lng = 53.414, 7.733
    st.session_state.using_gps = False

location = streamlit_js_eval(js_expressions='navigator.geolocation ? new Promise((resolve) => { navigator.geolocation.getCurrentPosition(pos => resolve({lat: pos.coords.latitude, lon: pos.coords.longitude}), () => resolve(null)) }) : null', key='get_loc')

if st.button("📍 Meinen Standort nutzen"):
    if location:
        st.session_state.user_lat, st.session_state.user_lng = location['lat'], location['lon']
        st.session_state.using_gps = True
        st.rerun()

# 3. DATEN
def get_data(lat, lng):
    url = f"https://creativecommons.tankerkoenig.de/json/list.php?lat={lat}&lng={lng}&rad=15&sort=dist&type=all&apikey={API_KEY}"
    try:
        r = requests.get(url, timeout=10)
        return r.json().get("stations")
    except: return None

stations = get_data(st.session_state.user_lat, st.session_state.user_lng)

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
                    isOpen = s.get('isOpen', False)
                    status_text = "● OFFEN" if isOpen else "○ ZU"
                    color = "#28a745" if isOpen else "#888"
                    # Wir nutzen Emojis als Logo-Ersatz für 100% Stabilität
                    st.markdown(f"""
                    <div style="border-left:8px solid {color}; padding:15px; margin:10px 0; background:white; border-radius:10px; box-shadow: 0 2px 5px rgba(0,0,0,0.1); display:flex; justify-content:space-between; align-items:center;">
                        <div>
                            <span style="font-size:1.5rem;">⛽</span> <b>{s.get('brand','').upper()}</b><br>
                            <small>{s.get('street','')}</small><br>
                            <span style="color:{color}; font-weight:bold;">{status_text}</span>
                        </div>
                        <div style="text-align:right;">
                            <span style="font-size:1.4rem; font-weight:bold;">{s[fuel_key]:.2f} €</span><br>
                            <small>{s.get('dist')} km</small>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)

    with tabs[3]:
        m = folium.Map(location=[st.session_state.user_lat, st.session_state.user_lng], zoom_start=13)
        if st.session_state.using_gps:
            folium.Marker([st.session_state.user_lat, st.session_state.user_lng], icon=folium.Icon(color='blue', icon='user', prefix='fa')).add_to(m)
        for s in stations:
            folium.Marker([s["lat"], s["lng"]], tooltip=s["brand"], icon=folium.Icon(color='red' if s['isOpen'] else 'gray')).add_to(m)
        st_folium(m, width=700, height=500, returned_objects=[])
