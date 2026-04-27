import streamlit as st
import requests
import folium
from streamlit_folium import st_folium
from streamlit_js_eval import streamlit_js_eval

# 1. SETUP
st.set_page_config(page_title="Wiesmoor Radar", page_icon="⛽", layout="centered")
API_KEY = "616cbb8e-9dde-4eb7-91f1-21a1663fa495"

st.markdown('<div style="background:linear-gradient(90deg, #e2001a, #b10014);color:white;padding:20px;text-align:center;border-radius:15px;font-weight:bold;font-size:1.6rem;box-shadow: 0 4px 10px rgba(0,0,0,0.2);">⛽ WIESMOOR LIVE-RADAR</div>', unsafe_allow_html=True)

# 2. STANDORT-LOGIK
if 'user_lat' not in st.session_state:
    st.session_state.user_lat, st.session_state.user_lng = 53.414, 7.733
    st.session_state.using_gps = False

st.write("")
c1, c2 = st.columns([3, 1])

with c1:
    msg = "📍 Fokus: Wiesmoor Zentrum" if not st.session_state.using_gps else "🎯 GPS-Standort aktiv"
    st.info(msg)

with c2:
    location = streamlit_js_eval(
        js_expressions='navigator.geolocation ? new Promise((resolve) => { navigator.geolocation.getCurrentPosition(pos => resolve({lat: pos.coords.latitude, lon: pos.coords.longitude}), () => resolve(null)) }) : null',
        key='get_loc'
    )
    if st.button("📍 GPS"):
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
                avg_price = sum(s[fuel_key] for s in valid) / len(valid)
                sorted_s = sorted(valid, key=lambda x: (not x['isOpen'], x[fuel_key]))
                
                for s in sorted_s:
                    isOpen = s.get('isOpen', False)
                    price = s[fuel_key]
                    brand_name = s.get("brand", "Tankstelle").upper()
                    
                    # LOGO LOGIK: Offizielles Logo oder schicker Platzhalter
                    logo_url = f"https://creativecommons.tankerkoenig.de/img/stations/{s.get('id')}.png"
                    fallback_icon = "https://cdn-icons-png.flaticon.com/512/483/483497.png"
                    
                    if isOpen:
                        card_style = "background:white; border-left:12px solid #28a745; box-shadow: 0 4px 12px rgba(0,0,0,0.1);"
                        p_color = "#28a745" if price < avg_price else "#000"
                        status = '<b style="color:#28a745;">● OFFEN</b>'
                        img_style = "filter: none;"
                    else:
                        card_style = "background:#f9f9f9; border-left:12px solid #ccc; opacity:0.5; filter: grayscale(100%);"
                        p_color = "#888"
                        status = '<b style="color:#888;">○ ZU</b>'
                        img_style = "filter: grayscale(100%);"

                    st.markdown(f'''
                    <div style="{card_style} padding:15px; border-radius:12px; margin-bottom:12px; display:flex; justify-content:space-between; align-items:center; border: 1px solid #eee;">
                        <div style="display:flex; align-items:center; gap:15px;">
