import streamlit as st
import requests
import folium
from streamlit_folium import st_folium
from streamlit_js_eval import streamlit_js_eval

# 1. KONFIGURATION
st.set_page_config(page_title="Wiesmoor Radar", page_icon="⛽", layout="centered")
API_KEY = "616cbb8e-9dde-4eb7-91f1-21a1663fa495"

st.markdown('<div style="background:#e2001a;color:white;padding:20px;text-align:center;border-radius:15px;font-weight:bold;font-size:1.6rem;">⛽ WIESMOOR LIVE-RADAR</div>', unsafe_allow_html=True)

# 2. STANDORT INITIALISIEREN
if 'user_lat' not in st.session_state:
    st.session_state.user_lat, st.session_state.user_lng = 53.414, 7.733

# GPS Button Logik
location = streamlit_js_eval(js_expressions='navigator.geolocation ? new Promise((resolve) => { navigator.geolocation.getCurrentPosition(pos => resolve({lat: pos.coords.latitude, lon: pos.coords.longitude}), () => resolve(null)) }) : null', key='get_loc')

if st.button("📍 Meinen Standort nutzen"):
    if location:
        st.session_state.user_lat, st.session_state.user_lng = location['lat'], location['lon']
        st.rerun()

# 3. DATEN ABFRAGEN
@st.cache_data(ttl=300)
def get_gas_data(lat, lng):
    url = f"https://creativecommons.tankerkoenig.de/json/list.php?lat={lat}&lng={lng}&rad=15&sort=dist&type=all&apikey={API_KEY}"
    try:
        return requests.get(url, timeout=10).json().get("stations", [])
    except:
        return []

stations = get_gas_data(st.session_state.user_lat, st.session_state.user_lng)

# 4. UI RENDERN
if stations:
    tab_labels = ["Super E5", "Super E10", "Diesel", "🗺️ Karte"]
    tabs = st.tabs(tab_labels)
    
    # Listenansicht
    fuel_map = {"Super E5": "e5", "Super E10": "e10", "Diesel": "diesel"}
    for i, label in enumerate(["Super E5", "Super E10", "Diesel"]):
        fuel_key = fuel_map[label]
        with tabs[i]:
            valid = [s for s in stations if s.get(fuel_key) and s.get(fuel_key) > 0]
            if valid:
                sorted_s = sorted(valid, key=lambda x: (not x['isOpen'], x[fuel_key]))
                for s in sorted_s:
                    color = "#28a745" if s.get('isOpen') else "#888"
                    st.markdown(f'<div style="border-left:8px solid {color}; padding:10px; margin:5px 0; background:white; border-radius:10px; border:1px solid #ddd;"><b>{str(s.get("brand","")).upper()}</b><br>{s.get(fuel_key):.2f} €</div>', unsafe_allow_html=True)

    # Kartenansicht
    with tabs[3]:
        m = folium.Map(location=[st.session_state.user_lat, st.session_state.user_lng], zoom_start=13)
        
        # Blaue Person für den User
        folium.Marker(
            [st.session_state.user_lat, st.session_state.user_lng],
            tooltip="Du bist hier",
            icon=folium.Icon(color='blue', icon='user', prefix='fa')
        ).add_to(m)
        
        # Tankstellen Markierungen
        for s in stations:
            s_name = str(s.get("brand") or s.get("name") or "Tankstelle").upper()
            s_color = 'red' if s.get('isOpen') else 'gray'
            
            # Marker mit permanentem Label darunter
            folium.Marker(
                location=[s["lat"], s["lng"]],
                popup=f"<b>{s_name}</b>",
                tooltip=s_name,
                icon=folium.Icon(color=s_color, icon='gas-pump', prefix='fa')
            ).add_to(m)
            
        st_folium(m, width=700, height=500, key="fixed_map_wiesmoor")
else:
    st.info("Daten werden geladen...")
