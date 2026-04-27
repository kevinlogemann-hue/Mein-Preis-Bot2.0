import streamlit as st
import requests
import folium
from streamlit_folium import st_folium
from streamlit_js_eval import streamlit_js_eval

# 1. SETUP
st.set_page_config(page_title="Wiesmoor Radar", page_icon="⛽", layout="centered")
API_KEY = "616cbb8e-9dde-4eb7-91f1-21a1663fa495"

st.markdown('<div style="background:#e2001a;color:white;padding:20px;text-align:center;border-radius:15px;font-weight:bold;font-size:1.6rem;">⛽ WIESMOOR LIVE-RADAR</div>', unsafe_allow_html=True)

# 2. STANDORT-LOGIK
if 'user_lat' not in st.session_state:
    st.session_state.user_lat, st.session_state.user_lng = 53.414, 7.733
    st.session_state.using_gps = False

location = streamlit_js_eval(js_expressions='navigator.geolocation ? new Promise((resolve) => { navigator.geolocation.getCurrentPosition(pos => resolve({lat: pos.coords.latitude, lon: pos.coords.longitude}), () => resolve(null)) }) : null', key='get_loc')

if st.button("📍 Meinen Standort nutzen"):
    if location:
        st.session_state.user_lat, st.session_state.user_lng = location['lat'], location['lon']
        st.session_state.using_gps = True
        st.rerun()

# 3. DATEN LADEN
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
                    color = "#28a745" if s.get('isOpen') else "#888"
                    st.markdown(f'<div style="border-left:8px solid {color}; padding:10px; margin:5px 0; background:white; border-radius:10px; border:1px solid #ddd;"><b>{s.get("brand").upper()}</b><br>{s.get(fuel_key):.2f} € - {s.get("dist")} km</div>', unsafe_allow_html=True)

    # 4. KARTEN-TAB (Permanente Namen & Person)
    with tabs[3]:
        m = folium.Map(location=[st.session_state.user_lat, st.session_state.user_lng], zoom_start=13)
        
        # DEIN STANDORT (Personen-Icon)
        folium.Marker(
            [st.session_state.user_lat, st.session_state.user_lng],
            tooltip="Das bist du",
            icon=folium.Icon(color='blue', icon='user', prefix='fa')
        ).add_to(m)
        
        # TANKSTELLEN mit permanentem Label
        for s in stations:
            brand_name = str(s.get("brand")).upper()
            price_e5 = s.get('e5')
            
            # Wir erstellen ein permanentes Text-Label über dem Marker
            folium.map.Marker(
                [s["lat"], s["lng"]],
                icon=folium.DivIcon(
                    icon_size=(150,36),
                    icon_anchor=(75,60),
                    html=f'<div style="font-size: 10pt; color: black; font-weight: bold; text-align: center; background-color: rgba(255, 255, 255, 0.7); border-radius: 5px; padding: 2px;">{brand_name}</div>',
                )
            ).add_to(m)

            # Der eigentliche Pin
            folium.Marker(
                location=[s["lat"], s["lng"]],
                popup=f"{brand_name}: {price_e5}€",
                icon=folium.Icon(color='red' if s.get('isOpen') else 'gray', icon='gas-pump', prefix='fa')
            ).add_to(m)
            
        st_folium(m, width=700, height=500, returned_objects=[])
else:
    st.info("Lade Daten...")
