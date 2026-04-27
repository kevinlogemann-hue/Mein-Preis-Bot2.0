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
    if st.button("📍 GPS"):
        loc = streamlit_js_eval(js_expressions='done(list(navigator.geolocation.getCurrentPosition(pos => { const {latitude, longitude} = pos.coords; done({latitude, longitude}) })))', key='get_loc')
        if loc:
            st.session_state.user_lat, st.session_state.user_lng = loc['latitude'], loc['longitude']
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
                # Sortieren: Offen nach oben, dann Preis
                sorted_s = sorted(valid, key=lambda x: (not x['isOpen'], x[fuel_key]))
                avg = sum(s[fuel_key] for s in sorted_s) / len(sorted_s)
                
                for s in sorted_s:
                    name = s["brand"] if s.get("brand") else s["name"]
                    price = s[fuel_key]
                    isOpen = s['isOpen']
                    
                    # STYLING-LOGIK FÜR MAXIMALEN KONTRAST
                    if isOpen:
                        card_style = "background:white; border-left:8px solid #28a745; opacity:1.0; box-shadow: 0 4px 8px rgba(0,0,0,0.1);"
                        text_color = "#000"
                        status_label = '<b style="color:#28a745;">● JETZT GEÖFFNET</b>'
                    else:
                        card_style = "background:#f2f2f2; border-left:8px solid #999; opacity:0.4; filter: grayscale(100%);"
                        text_color = "#777"
                        status_label = '<b style="color:#666;">○ GESCHLOSSEN</b>'

                    st.markdown(f'''
                    <div style="{card_style} padding:15px; border-radius:12px; margin-top:10px; display:flex; justify-content:space-between; align-items:center; border-top:1px solid #ddd; border-right:1px solid #ddd; border-bottom:1px solid #ddd;">
                        <div style="color:{text_color};">
                            <b style="font-size:1.2rem;">{name}</b><br>
                            <small>{s.get("street", "")}</small><br>
                            {status_label}
                        </div>
                        <div style="text-align:right;">
                            <span style="font-size:1.4rem; font-weight:bold; color:{'#28a745' if price < avg and isOpen else text_color};">{price:.2f} €</span><br>
                            <small style="color:{text_color};">{s.get("dist")} km</small>
                        </div>
                    </div>
                    ''', unsafe_allow_html=True)

    with tabs[3]:
        m = folium.Map(location=[st.session_state.user_lat, st.session_state.user_lng], zoom_start=12)
        for s in stations:
            # Karte: Rot für offen, Grau für zu
            color = 'red' if s['isOpen'] else 'lightgray'
            folium.Marker(
                [s["lat"], s["lng"]], 
                tooltip=s["brand"],
                icon=folium.Icon(color=color, icon='info-sign')
            ).add_to(m)
        st_folium(m, width=700, height=500, returned_objects=[])

else:
    st.error("Keine Daten gefunden.")
