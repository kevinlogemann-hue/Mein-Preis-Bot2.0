import streamlit as st
import requests
import folium
from streamlit_folium import st_folium
from streamlit_js_eval import streamlit_js_eval

# 1. SETUP
st.set_page_config(page_title="Wiesmoor Radar", page_icon="⛽", layout="centered")

# Header
st.markdown('<div style="background:#e2001a;color:white;padding:20px;text-align:center;border-radius:15px;font-weight:bold;font-size:1.6rem;">⛽ WIESMOOR LIVE-RADAR</div>', unsafe_allow_html=True)

API_KEY = "616cbb8e-9dde-4eb7-91f1-21a1663fa495"

if 'lat' not in st.session_state:
    st.session_state.lat, st.session_state.lng = 53.414, 7.733

# 2. STANDORT & REFRESH
col_a, col_b = st.columns(2)
with col_a:
    loc = streamlit_js_eval(js_expressions='navigator.geolocation ? new Promise((resolve) => { navigator.geolocation.getCurrentPosition(pos => resolve({lat: pos.coords.latitude, lon: pos.coords.longitude}), () => resolve(null), {enableHighAccuracy: true}) }) : null', key='gps')
    if st.button("📍 Standort finden"):
        if loc:
            st.session_state.lat, st.session_state.lng = loc['lat'], loc['lon']
            st.rerun()
with col_b:
    if st.button("🔄 Preise aktualisieren"):
        st.cache_data.clear() # Löscht den alten Cache sofort
        st.rerun()

# 3. DATEN LADEN (Cache auf 60 Sekunden reduziert)
@st.cache_data(ttl=60)
def fetch_data(lat, lng):
    url = f"https://creativecommons.tankerkoenig.de/json/list.php?lat={lat}&lng={lng}&rad=10&sort=dist&type=all&apikey={API_KEY}"
    try:
        res = requests.get(url, timeout=10).json()
        return res.get("stations", [])
    except:
        return []

stations = fetch_data(st.session_state.lat, st.session_state.lng)

# 4. ANZEIGE
if stations:
    tabs = st.tabs(["Super E5", "Super E10", "Diesel", "🗺️ Karte"])
    fuels = {"Super E5": "e5", "Super E10": "e10", "Diesel": "diesel"}

    for i, (label, key) in enumerate(fuels.items()):
        with tabs[i]:
            # Nur Stationen mit Preis, sortiert nach günstigstem Preis zuerst
            list_s = [s for s in stations if s.get(key) and s.get(key) > 0]
            list_s.sort(key=lambda x: (not x.get('isOpen'), x.get(key)))

            for s in list_s:
                name = str(s.get('brand') or s.get('name') or "Tankstelle").upper()
                isOpen = s.get('isOpen')
                col = "#28a745" if isOpen else "#888"
                price = s.get(key)
                
                st.markdown(f"""
                <div style="border:1px solid #eee; padding:15px; margin:10px 0; background:white; border-radius:12px; box-shadow: 0 2px 4px rgba(0,0,0,0.05);">
                    <div style="display: flex; justify-content: space-between; align-items: center;">
                        <div>
                            <div style="font-weight:bold; font-size:1.1rem;">⛽ {name}</div>
                            <div style="color:{col}; font-size:0.85rem; font-weight:bold;">{"● OFFEN" if isOpen else "○ ZU"}</div>
                            <div style="color:#666; font-size:0.8rem;">📍 {s.get('street')} • {s.get('dist')} km</div>
                        </div>
                        <div style="font-size:1.7rem; font-weight:bold; color:#28a745;">{price:.2f}€</div>
                    </div>
                </div>
                """, unsafe_allow_html=True)

    with tabs[3]:
        m = folium.Map(location=[st.session_state.lat, st.session_state.lng], zoom_start=13)
        folium.Marker([st.session_state.lat, st.session_state.lng], icon=folium.Icon(color='blue')).add_to(m)
        for s in stations:
            folium.Marker([s["lat"], s["lng"]], tooltip=s.get('brand'), icon=folium.Icon(color='red' if s.get('isOpen') else 'gray', icon='gas-pump', prefix='fa')).add_to(m)
        st_folium(m, width=700, height=500, key="map")
else:
    st.warning("Keine aktuellen Daten empfangen. Bitte 'Preise aktualisieren' klicken.")
