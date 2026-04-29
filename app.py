import streamlit as st
import requests
from streamlit_js_eval import streamlit_js_eval

# 1. Seite konfigurieren
st.set_page_config(page_title="Wiesmoor Radar", layout="centered")

# Schickes Design (CSS) - sicher verpackt
st.markdown("""
<style>
    .stApp { background-color: #f8f9fa; }
    .fuel-card {
        background: white;
        padding: 20px;
        border-radius: 15px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        margin-bottom: 15px;
        border-left: 5px solid #ff4b4b;
    }
    .price-tag {
        font-size: 24px;
        font-weight: bold;
        color: #1f1f1f;
        float: right;
    }
    .station-name {
        font-size: 18px;
        font-weight: bold;
        margin-bottom: 2px;
        text-transform: uppercase;
    }
    .station-addr {
        color: #6c757d;
        font-size: 14px;
    }
    .fix-button-text {
        font-size: 13px;
        color: #ff4b4b;
        font-weight: bold;
    }
</style>
""", unsafe_allow_html=True)

st.title("⛽ Wiesmoor Radar")

# 2. Standort-Logik
if 'lat' not in st.session_state:
    st.session_state.lat, st.session_state.lng = 53.414, 7.733

col_gps, col_rad = st.columns([1, 1])
with col_gps:
    if st.button("📍 Standort finden"):
        loc = streamlit_js_eval(js_expressions='navigator.geolocation ? new Promise((resolve) => { navigator.geolocation.getCurrentPosition(pos => resolve({lat: pos.coords.latitude, lon: pos.coords.longitude})) }) : null', key='gps_final')
        if loc:
            st.session_state.lat, st.session_state.lng = loc['lat'], loc['lon']
            st.rerun()
with col_rad:
    radius = st.selectbox("Umkreis km", [5, 10, 20, 50], index=1)

# 3. Daten von Tankerkoenig
API_KEY = "616cbb8e-9dde-4eb7-91f1-21a1663fa495"

def get_stations():
    url = f"https://creativecommons.tankerkoenig.de/json/list.php?lat={st.session_state.lat}&lng={st.session_state.lng}&rad={radius}&sort=dist&type=all&apikey={API_KEY}"
    try:
        return requests.get(url).json().get("stations", [])
    except:
        return []

stations = get_stations()

# 4. Anzeige im Karten-Design
if stations:
    tab1, tab2, tab3 = st.tabs(["Super E5", "Super E10", "Diesel"])
    fuel_map = {"Super E5": "e5", "Super E10": "e10", "Diesel": "diesel"}
    tabs = [tab1, tab2, tab3]

    for i, label in enumerate(fuel_map.keys()):
        with tabs[i]:
            f_key = fuel_map[label]
            # Nur Stationen mit Preisen anzeigen und nach Preis sortieren
            valid = [s for s in stations if s.get(f_key)]
            sorted_stations = sorted(valid, key=lambda x: x.get(f_key))

            for s in sorted_stations:
                price = s.get(f_key)
                brand = str(s.get('brand', 'Tankstelle')).upper()
                addr = f"{s.get('street')} ({s.get('dist')} km)"
                
                # Die schicke Karte
                st.markdown(f"""
                <div class="fuel-card">
                    <span class="price-tag">{price} €</span>
                    <div class="station-name">{brand}</div>
                    <div class="station-addr">{addr}</div>
                </div>
                """, unsafe_allow_html=True)
                
                # Der Korrektur-Button direkt unter der Karte
                btn_label = "⚠️ Preis an der Tankanzeige stimmt nicht? Hier korrigieren"
                if st.button(btn_label, key=f"corr_{s['id']}_{f_key}"):
                    st.session_state[f"cam_{s['id']}"] = True
                
                if st.session_state.get(f"cam_{s['id']}"):
                    st.info("Bitte mache ein Foto der Preistafel zur Verifizierung:")
                    st.camera_input("Kamera öffnen", key=f"cam_input_{s['id']}")
                    if st.button("Abbrechen", key=f"cancel_{s['id']}"):
                        st.session_state[f"cam_{s['id']}"] = False
                        st.rerun()
                
                st.write("") # Abstandhalter
else:
    st.warning("Keine Tankstellen gefunden. Erhöhe eventuell den Radius.")
