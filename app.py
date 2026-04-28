import streamlit as st
import requests
import folium
from streamlit_folium import st_folium
from streamlit_js_eval import streamlit_js_eval
from datetime import datetime

# 1. SETUP & DESIGN
st.set_page_config(page_title="Wiesmoor Radar", page_icon="⛽", layout="centered")

# Header
st.markdown('<div style="background:#e2001a;color:white;padding:20px;text-align:center;border-radius:15px;font-weight:bold;font-size:1.6rem;">⛽ WIESMOOR LIVE-RADAR</div>', unsafe_allow_html=True)

# --- NEU: HINWEIS ZUR PREISABWEICHUNG ---
st.info("ℹ️ **Hinweis:** Preise können systembedingt um einige Cent abweichen. Maßgeblich ist immer der Preis an der Zapfsäule vor Ort.")

API_KEY = "616cbb8e-9dde-4eb7-91f1-21a1663fa495"

if 'lat' not in st.session_state:
    st.session_state.lat, st.session_state.lng = 53.414, 7.733

# 2. BEDIENUNG
col_a, col_b = st.columns(2)
with col_a:
    loc = streamlit_js_eval(js_expressions='navigator.geolocation ? new Promise((resolve) => { navigator.geolocation.getCurrentPosition(pos => resolve({lat: pos.coords.latitude, lon: pos.coords.longitude}), () => resolve(null), {enableHighAccuracy: true}) }) : null', key='gps_final_v2')
    if st.button("📍 Standort finden"):
        if loc:
            st.session_state.lat, st.session_state.lng = loc['lat'], loc['lon']
            st.rerun()
with col_b:
    if st.button("🔄 JETZT AKTUALISIEREN"):
        st.cache_data.clear()
        st.rerun()

# 3. DATEN-ABFRAGE
@st.cache_data(ttl=10)
def fetch_now(lat, lng):
    url = f"https://creativecommons.tankerkoenig.de/json/list.php?lat={lat}&lng={lng}&rad=15&sort=dist&type=all&apikey={API_KEY}"
    try:
        r = requests.get(url, timeout=5)
        return r.json().get("stations", [])
    except:
        return []

stations = fetch_now(st.session_state.lat, st.session_state.lng)
st.caption(f"Letztes Daten-Update: {datetime.now().strftime('%H:%M:%S')} Uhr")

# 4. ANZEIGE
if stations:
    tabs = st.tabs(["Super E5", "Super E10", "Diesel", "🗺️ Karte"])
    fuels = {"Super E5": "e5", "Super E10": "e10", "Diesel": "diesel"}

    for i, (label, key) in enumerate(fuels.items()):
        with tabs[i]:
            valid_s = [s for s in stations if s.get(key) and s.get(key) > 0]
            valid_s.sort(key=lambda x: (not x.get('isOpen'), x.get(key)))

            for s in valid_s:
                name = str(s.get('brand') or s.get('name') or "Tankstelle").upper()
                isOpen = s.get('isOpen')
                status_color = "#28a745" if isOpen else "#d9534f"
                
                st.markdown(f"""
                <div style="border:1px solid #ddd; padding:15px; margin:10px 0; background:white; border-radius:12px; border-left: 8px solid {status_color};">
                    <div style="display: flex; justify-content: space-between; align-items: center;">
                        <div>
                            <div style="font-weight:bold; font-size:1.1rem; color:#222;">{name}</div>
                            <div style="color:{status_color}; font-size:0.8rem; font-weight:bold;">{"● GEÖFFNET" if isOpen else "○ GESCHLOSSEN"}</div>
                            <div style="color:#777; font-size:0.75rem;">{s.get('street')} • {s.get('dist')} km</div>
                        </div>
                        <div style="text-align: right;">
                            <div style="font-size:1.8rem; font-weight:900; color:#111;">{s.get(key):.2f}€</div>
                        </div>
                    </div>
                </div>
                """, unsafe_allow_html=True)

    with tabs[3]:
        m = folium.Map(location=[st.session_state.lat, st.session_state.lng], zoom_start=13)
        folium.Marker([st.session_state.lat, st.session_state.lng], tooltip="Deine Position", icon=folium.Icon(color='blue', icon='user', prefix='fa')).add_to(m)
        for s in stations:
            folium.Marker([s["lat"], s["lng"]], tooltip=str(s.get('brand')), icon=folium.Icon(color='red' if s.get('isOpen') else 'gray', icon='gas-pump', prefix='fa')).add_to(m)
        st_folium(m, width=700, height=500, key="map_final_v2")
else:
    st.error("Konnte keine Daten laden. Bitte versuche es in einem Moment erneut.")
