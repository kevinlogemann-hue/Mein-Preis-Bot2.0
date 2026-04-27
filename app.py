import streamlit as st
import requests
import folium
from streamlit_folium import st_folium
from streamlit_js_eval import streamlit_js_eval

# 1. KONFIGURATION
st.set_page_config(page_title="Wiesmoor Radar", page_icon="⛽", layout="centered")
API_KEY = "616cbb8e-9dde-4eb7-91f1-21a1663fa495"

st.markdown('<div style="background:#e2001a;color:white;padding:20px;text-align:center;border-radius:15px;font-weight:bold;font-size:1.6rem;">⛽ WIESMOOR LIVE-RADAR</div>', unsafe_allow_html=True)

# 2. STANDORT
if 'user_lat' not in st.session_state:
    st.session_state.user_lat, st.session_state.user_lng = 53.414, 7.733

loc_data = streamlit_js_eval(js_expressions='navigator.geolocation ? new Promise((resolve) => { navigator.geolocation.getCurrentPosition(pos => resolve({lat: pos.coords.latitude, lon: pos.coords.longitude}), () => resolve(null), {enableHighAccuracy: true}) }) : null', key='get_gps_loc')

if st.button("📍 Standort aktualisieren"):
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

# 4. SORTIERUNG & UI
if stations:
    sort_option = st.selectbox("Sortieren nach:", ["Günstigste Preise", "Kürzeste Entfernung", "Name (A-Z)"])
    
    tabs = st.tabs(["Super E5", "Super E10", "Diesel", "🗺️ Karte"])
    fuel_map = {"Super E5": "e5", "Super E10": "e10", "Diesel": "diesel"}
    
    for i, label in enumerate(["Super E5", "Super E10", "Diesel"]):
        fuel_key = fuel_map[label]
        with tabs[i]:
            valid = [s for s in stations if s.get(fuel_key) and s.get(fuel_key) > 0]
            
            if valid:
                # SORTIER-LOGIK (Fix)
                if sort_option == "Günstigste Preise":
                    valid.sort(key=lambda x: (not x.get('isOpen', False), x.get(fuel_key, 9.99)))
                elif sort_option == "Kürzeste Entfernung":
                    valid.sort(key=lambda x: x.get('dist', 999))
                else:
                    valid.sort(key=lambda x: str(x.get("brand") or x.get("name") or "ZZZ").upper())

                for s in valid:
                    color = "#28a745" if s.get('isOpen') else "#888"
                    brand = str(s.get("brand") or s.get("name") or "Tankstelle").upper()
                    st.markdown(f"""
                    <div style="border:1px solid #eee; padding:15px; margin:10px 0; background:white; border-radius:12px; box-shadow: 0 2px 4px rgba(0,0,0,0.05);">
                        <div style="display: flex; justify-content: space-between; align-items: center;">
                            <div style="flex: 1;">
                                <div style="font-weight:bold; font-size:1.1rem; color:#222;">⛽ {brand}</div>
                                <div style="color:{color}; font-size:0.85rem; font-weight:bold; margin: 4px 0;">{"● OFFEN" if s.get('isOpen') else "○ ZU"}</div>
                                <div style="color:#666; font-size:0.8rem;">📍 {s.get('street', '')} • {s.get('dist')} km</div>
                            </div>
                            <div style="text-align: right;">
                                <div style="font-size:1.5rem; font-weight:bold; color:#28a745;">{s.get(fuel_key):.2f}€</div>
                            </div>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)

    with tabs[3]:
        m = folium.Map(location=[st.session_state.user_lat, st.session_state.user_lng], zoom_start=13)
        folium.Marker([st.session_state.user_lat, st.session_state.user_lng], tooltip="Du", icon=folium.Icon(color='blue', icon='user', prefix='fa')).add_to(m)
        for s in stations:
            n = str(s.get("brand") or s.get("name") or "Tankstelle").upper()
            folium.Marker([s["lat"], s["lng"]], tooltip=n, icon=folium.Icon(color='red' if s.get('isOpen') else 'gray', icon='gas-pump', prefix='fa')).add_to(m)
        st_folium(m, width=700, height=500, key="map_v3")
else:
    st.info("Lade Daten...")
