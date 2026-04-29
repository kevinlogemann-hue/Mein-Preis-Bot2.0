import streamlit as st
import requests
from streamlit_js_eval import streamlit_js_eval

# 1. SETUP & TITEL
st.set_page_config(page_title="Wiesmoor Radar", layout="centered")

st.title("⛽ Wiesmoor Radar")
st.subheader("Preis falsch oder Station fehlt? Hilf uns! 📸")

# 2. STANDORT & FILTER
if 'lat' not in st.session_state:
    st.session_state.lat, st.session_state.lng = 53.414, 7.733

# Buttons in Spalten
col1, col2, col3 = st.columns([1, 1, 1.5])

with col1:
    if st.button("📍 GPS finden"):
        loc = streamlit_js_eval(js_expressions='navigator.geolocation ? new Promise((resolve) => { navigator.geolocation.getCurrentPosition(pos => resolve({lat: pos.coords.latitude, lon: pos.coords.longitude})) }) : null', key='gps_safe')
        if loc:
            st.session_state.lat, st.session_state.lng = loc['lat'], loc['lon']
            st.rerun()

with col2:
    radius = st.selectbox("Radius km", [5, 10, 25, 50], index=1)

with col3:
    sort_by = st.selectbox("Sortierung", ["Günstigste", "Entfernung"])

# 3. DATEN LADEN
API_KEY = "616cbb8e-9dde-4eb7-91f1-21a1663fa495"

def fetch_data():
    url = "https://creativecommons.tankerkoenig.de/json/list.php?lat=" + str(st.session_state.lat) + "&lng=" + str(st.session_state.lng) + "&rad=" + str(radius) + "&sort=dist&type=all&apikey=" + API_KEY
    try:
        r = requests.get(url).json()
        return r.get("stations", [])
    except:
        return []

stations = fetch_data()

# 4. ANZEIGE OHNE HTML-GEFAHR
if stations:
    tab1, tab2, tab3 = st.tabs(["Super E5", "Super E10", "Diesel"])
    fuels = {"Super E5": "e5", "Super E10": "e10", "Diesel": "diesel"}

    fuel_list = [tab1, tab2, tab3]
    for i, label in enumerate(fuels.keys()):
        f_key = fuels[label]
        with fuel_list[i]:
            # Filterung
            valid = [s for s in stations if s.get(f_key)]
            
            # Sortierung
            if sort_by == "Günstigste":
                sorted_list = sorted(valid, key=lambda x: x.get(f_key))
            else:
                sorted_list = sorted(valid, key=lambda x: x.get('dist'))

            for s in sorted_list:
                price = s.get(f_key)
                name = str(s.get('brand', s.get('name', 'Tankstelle'))).upper()
                dist = s.get('dist', 0)
                
                # Einfache, stabile Anzeige mit Streamlit-Bordmitteln
                with st.container():
                    col_info, col_price = st.columns([3, 1])
                    col_info.write("**" + name + "**")
                    col_info.caption(s.get('street', '') + " (" + str(dist) + " km)")
                    col_price.metric("", str(price) + " €")
                    
                    # Korrektur-Bereich
                    if st.button("📸 Preis falsch?", key="btn_" + str(s['id']) + f_key):
                        st.session_state["cam_" + str(s['id'])] = True
                    
                    if st.session_state.get("cam_" +
