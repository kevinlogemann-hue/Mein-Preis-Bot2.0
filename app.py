import streamlit as st
import requests
from streamlit_js_eval import streamlit_js_eval
from datetime import datetime
from PIL import Image

# 1. Seiteneinstellungen
st.set_page_config(page_title="Wiesmoor Radar")

# 2. Einfacher Header (Verhindert Kopierfehler)
st.title("⛽ WIESMOOR LIVE-RADAR")
st.write("📸 **Mache Fotos für die Community für die Echtzeit-Preisangaben.**")
st.write("Umso mehr mitmachen, desto genauer werden die Preise!")

# 3. Logik & API
API_KEY = "616cbb8e-9dde-4eb7-91f1-21a1663fa495"

if 'user_reports' not in st.session_state:
    st.session_state.user_reports = {}
if 'lat' not in st.session_state:
    st.session_state.lat = 53.414
if 'lng' not in st.session_state:
    st.session_state.lng = 7.733

# Standort Buttons
c1, c2 = st.columns(2)
with c1:
    if st.button("📍 Standort"):
        loc = streamlit_js_eval(js_expressions='navigator.geolocation ? new Promise((resolve) => { navigator.geolocation.getCurrentPosition(pos => resolve({lat: pos.coords.latitude, lon: pos.coords.longitude})) }) : null', key='gps_final')
        if loc:
            st.session_state.lat = loc['lat']
            st.session_state.lng = loc['lon']
            st.rerun()
with c2:
    if st.button("🔄 Update"):
        st.cache_data.clear()
        st.rerun()

# Daten laden
@st.cache_data(ttl=60)
def load_prices(la, ln):
    url = f"https://creativecommons.tankerkoenig.de/json/list.php?lat={la}&lng={ln}&rad=15&sort=dist&type=all&apikey={API_KEY}"
    try:
        return requests.get(url).json().get("stations", [])
    except:
        return []

data = load_prices(st.session_state.lat, st.session_state.lng)

# 4. Anzeige
if data:
    tabs = st.tabs(["E5", "E10", "Diesel"])
    keys = ["e5", "e10", "diesel"]
    
    for i, k in enumerate(keys):
        with tabs[i]:
            for s in data:
                if s.get(k):
                    sid = s['id']
                    # Einfache Box
                    with st.container():
                        st.markdown(f"### {s.get('brand', 'Tankstelle')} - {s.get(k):.2f}€")
                        st.write(f"🏠 {s.get('street')}")
                        
                        # Foto-Update Button
                        if st.button(f"📸 Foto senden", key=f"btn_{sid}_{k}"):
                            st.session_state[f"up_{sid}"] = True
                        
                        if st.session_state.get(f"up_{sid}"):
                            img_file = st.file_uploader("Preistafel fotografieren", type=['jpg','png'], key=f"file_{sid}")
                            if img_file:
                                st.session_state.user_reports[sid] = {"t": datetime.now().strftime("%H:%M"), "i": Image.open(img_file)}
                                del st.session_state[f"up_{sid}"]
                                st.rerun()
                        
                        if sid in st.session_state.user_reports:
                            st.success(f"✅ Foto-Update von {st.session_state.user_reports[sid]['t']} Uhr")
                        st.divider()
else:
    st.info("Suche Tankstellen in Wiesmoor...")
