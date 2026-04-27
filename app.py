import streamlit as st
import requests
import folium
from streamlit_folium import st_folium
from streamlit_js_eval import streamlit_js_eval

# 1. KONFIGURATION
st.set_page_config(page_title="Wiesmoor Radar", page_icon="⛽", layout="centered")
API_KEY = "616cbb8e-9dde-4eb7-91f1-21a1663fa495"

# Header mit Icon
st.markdown('<div style="background:#e2001a;color:white;padding:20px;text-align:center;border-radius:15px;font-weight:bold;font-size:1.6rem;">⛽ WIESMOOR LIVE-RADAR</div>', unsafe_allow_html=True)

# 2. STANDORT INITIALISIEREN
if 'user_lat' not in st.session_state:
    st.session_state.user_lat, st.session_state.user_lng = 53.414, 7.733

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
    tabs = st.tabs(["Super E5", "Super E10", "Diesel", "🗺️ Karte"])
    fuel_map = {"Super E5": "e5", "Super E10": "e10", "Diesel": "diesel"}
    
    # Listen mit Icons
    for i, label in enumerate(["Super E5", "Super E10", "Diesel"]):
        fuel_key = fuel_map[label]
        with tabs[i]:
            valid = [s for s in stations if s.get(fuel_key) and s.get(fuel_key) > 0]
            if valid:
                sorted_s = sorted(valid, key=lambda x: (not x['isOpen'], x[fuel_key]))
                for s in sorted_s:
                    color = "#28a745" if s.get('isOpen') else "#888"
                    status_text = "● OFFEN" if s.get('isOpen') else "○ GESCHLOSSEN"
                    brand = str(s.get("brand", "Tankstelle")).upper()
                    
                    # Hier sind die Icons in der Liste wieder drin:
                    st.markdown(f"""
                    <div style="border:1px solid #ddd; padding:15px; margin:10px 0; background:white; border-radius:15px; box-shadow: 2px 2px 5px rgba(0,0,0,0.05);">
                        <div style="display: flex; justify-content: space-between; align-items: center;">
                            <div>
                                <div style="font-weight:bold; font-size:1.1rem; color:#333;">⛽ {brand}</div>
                                <div style="color:{color}; font-size:0.9rem; font-weight:bold; margin-top:4px;">{status_text}</div>
                                <div style="color:#666; font-size:0.8rem;">📍 {s.get('street', '')} • {s.get('dist')} km</div>
                            </div>
                            <div style="font-size:1.6rem; font-weight:bold; color:#28a745;">{s.get(fuel_key):.2f} €</div>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)

    # Kartenansicht
    with tabs[3]:
        m = folium.Map(location=[st.session_state.user_lat, st.session_state.user_lng], zoom_start=13)
        folium.Marker(
            [st.session_state.user_lat, st.session_state.user_lng],
            tooltip="Du bist hier",
            icon=folium.Icon(color='blue', icon='user', prefix='fa')
        ).add_to(m)
        
        for s in stations:
            s_name = str(s.get("brand") or s.get("name") or "Tankstelle").upper()
            folium.Marker(
                location=[s["lat"], s["lng"]],
                tooltip=s_name,
                popup=f"<b>{s_name}</b>",
                icon=folium.Icon(color='red' if s.get('isOpen') else 'gray', icon='gas-pump', prefix='fa')
            ).add_to(m)
        st_folium(m, width=700, height=500, key="final_wiesmoor_map")
else:
    st.info("Suche Tankstellen...")
