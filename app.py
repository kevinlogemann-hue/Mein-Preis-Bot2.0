import streamlit as st
import requests
import folium
from streamlit_folium import st_folium
from streamlit_js_eval import streamlit_js_eval

# 1. SETUP
st.set_page_config(page_title="Wiesmoor Radar", page_icon="⛽", layout="centered")
API_KEY = "616cbb8e-9dde-4eb7-91f1-21a1663fa495"

st.markdown('<div style="background:linear-gradient(90deg, #e2001a, #b10014);color:white;padding:20px;text-align:center;border-radius:15px;font-weight:bold;font-size:1.6rem;">⛽ WIESMOOR LIVE-RADAR</div>', unsafe_allow_html=True)

# 2. STANDORT-LOGIK
# Wir prüfen, ob wir schon Koordinaten haben
if 'user_lat' not in st.session_state:
    st.session_state.user_lat = 53.414
    st.session_state.user_lng = 7.733
    st.session_state.using_gps = False

st.write("")
col1, col2 = st.columns([2, 1])

with col1:
    if not st.session_state.using_gps:
        st.info("📍 Zeige Preise für Wiesmoor Zentrum")
    else:
        st.success("🎯 GPS-Standort aktiv!")

with col2:
    # Der Button löst die JavaScript-Abfrage aus
    if st.button("📍 Mein Standort"):
        loc = streamlit_js_eval(js_expressions='done(list(navigator.geolocation.getCurrentPosition(pos => { const {latitude, longitude} = pos.coords; done({latitude, longitude}) })))', key='get_location')
        if loc and isinstance(loc, dict):
            st.session_state.user_lat = loc['latitude']
            st.session_state.user_lng = loc['longitude']
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
    tabs = st.tabs(["Super E5", "Super E10", "Diesel", "🗺️ Live-Karte"])
    fuel_map = {"Super E5": "e5", "Super E10": "e10", "Diesel": "diesel"}
    
    for i, label in enumerate(["Super E5", "Super E10", "Diesel"]):
        fuel_key = fuel_map[label]
        with tabs[i]:
            valid = [s for s in stations if s.get(fuel_key) and s.get(fuel_key) > 0]
            if valid:
                sorted_s = sorted(valid, key=lambda x: (not x['isOpen'], x[fuel_key]))
                avg_price = sum(s[fuel_key] for s in sorted_s) / len(sorted_s)
                
                st.markdown(f"💡 **Durchschnitt: {avg_price:.2f} €**")
                
                for s in sorted_s:
                    name = s["brand"] if s.get("brand") else s["name"]
                    price = s[fuel_key]
                    trend = "📉" if price < avg_price else "📈"
                    st.markdown(f'''
                    <div style="background:white; padding:12px; border-radius:12px; margin-top:8px; border: 1px solid #eee; display:flex; justify-content:space-between; align-items:center; opacity:{'1.0' if s['isOpen'] else '0.6'};">
                        <div><b>{name}</b><br><small>{s.get("street", "")}</small></div>
                        <div style="text-align:right;"><span style="font-size:1.2rem; font-weight:bold; color:{'#28a745' if price < avg_price else '#000'};">{price:.2f} €</span> {trend}<br><small>{s.get("dist")} km</small></div>
                    </div>
                    ''', unsafe_allow_html=True)

    with tabs[3]:
        m = folium.Map(location=[st.session_state.user_lat, st.session_state.user_lng], zoom_start=12)
        if st.session_state.using_gps:
            folium.Marker([st.session_state.user_lat, st.session_state.user_lng], tooltip="Du", icon=folium.Icon(color='blue')).add_to(m)
        for s in stations:
            folium.Marker([s["lat"], s["lng"]], tooltip=s["brand"], icon=folium.Icon(color='red' if s['isOpen'] else 'gray')).add_to(m)
        st_folium(m, width=700, height=500, returned_objects=[])
