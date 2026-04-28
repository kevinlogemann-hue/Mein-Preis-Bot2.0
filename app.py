import streamlit as st
import requests
import folium
from streamlit_folium import st_folium
from streamlit_js_eval import streamlit_js_eval
from datetime import datetime
from PIL import Image

# 1. SETUP & DESIGN
st.set_page_config(page_title="Wiesmoor Radar", page_icon="⛽", layout="centered")

# Custom CSS für bessere Lesbarkeit der Meldungen
st.markdown("""
    <style>
    .report-box {
        background-color: #fff3cd;
        border-left: 5px solid #ffc107;
        padding: 10px;
        margin-top: 10px;
        border-radius: 5px;
        font-size: 0.9rem;
    }
    </style>
    """, unsafe_allow_html=True)

# Header
st.markdown('<div style="background:#e2001a;color:white;padding:20px;text-align:center;border-radius:15px;font-weight:bold;font-size:1.6rem;">⛽ WIESMOOR LIVE-RADAR</div>', unsafe_allow_html=True)

st.info("ℹ️ **Hinweis:** Preise können systembedingt leicht abweichen. Maßgeblich ist die Anzeige an der Zapfsäule.")

API_KEY = "616cbb8e-9dde-4eb7-91f1-21a1663fa495"

# Speicher für Nutzer-Meldungen (simuliert)
if 'user_reports' not in st.session_state:
    st.session_state.user_reports = {}

if 'lat' not in st.session_state:
    st.session_state.lat, st.session_state.lng = 53.414, 7.733

# 2. BEDIENUNG
col_a, col_b = st.columns(2)
with col_a:
    loc = streamlit_js_eval(js_expressions='navigator.geolocation ? new Promise((resolve) => { navigator.geolocation.getCurrentPosition(pos => resolve({lat: pos.coords.latitude, lon: pos.coords.longitude}), () => resolve(null), {enableHighAccuracy: true}) }) : null', key='gps_v3')
    if st.button("📍 Standort finden"):
        if loc:
            st.session_state.lat, st.session_state.lng = loc['lat'], loc['lon']
            st.rerun()
with col_b:
    if st.button("🔄 AKTUALISIEREN"):
        st.cache_data.clear()
        st.rerun()

# 3. DATEN-ABFRAGE
@st.cache_data(ttl=60)
def fetch_now(lat, lng):
    url = f"https://creativecommons.tankerkoenig.de/json/list.php?lat={lat}&lng={lng}&rad=15&sort=dist&type=all&apikey={API_KEY}"
    try:
        r = requests.get(url, timeout=5)
        return r.json().get("stations", [])
    except:
        return []

stations = fetch_now(st.session_state.lat, st.session_state.lng)

# 4. ANZEIGE & LOGIK
if stations:
    tabs = st.tabs(["Super E5", "Super E10", "Diesel", "🗺️ Karte"])
    fuels = {"Super E5": "e5", "Super E10": "e10", "Diesel": "diesel"}

    for i, (label, key) in enumerate(fuels.items()):
        with tabs[i]:
            valid_s = [s for s in stations if s.get(key) and s.get(key) > 0]
            for s in valid_s:
                s_id = s['id']
                name = str(s.get('brand') or s.get('name') or "Tankstelle").upper()
                isOpen = s.get('isOpen')
                status_color = "#28a745" if isOpen else "#d9534f"
                
                # Container für die Tankstelle
                with st.container():
                    st.markdown(f"""
                    <div style="border:1px solid #ddd; padding:15px; margin:10px 0; background:white; border-radius:12px; border-left: 8px solid {status_color};">
                        <div style="display: flex; justify-content: space-between; align-items: center;">
                            <div>
                                <div style="font-weight:bold; font-size:1.1rem; color:#222;">{name}</div>
                                <div style="color:{status_color}; font-size:0.8rem; font-weight:bold;">{"● GEÖFFNET" if isOpen else "○ GESCHLOSSEN"}</div>
                                <div style="color:#777; font-size:0.75rem;">{s.get('street')}</div>
                            </div>
                            <div style="text-align: right;">
                                <div style="font-size:1.8rem; font-weight:900; color:#111;">{s.get(key):.2f}€</div>
                            </div>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)

                    # --- USER REPORT SEKTION ---
                    col1, col2 = st.columns([1, 1])
                    
                    # Button zum Melden
                    if col1.button(f"⚠️ Abweichung melden", key=f"btn_{s_id}_{key}"):
                        st.session_state[f"reporting_{s_id}"] = True

                    # Wenn Melde-Modus aktiv ist
                    if st.session_state.get(f"reporting_{s_id}"):
                        with st.expander("Foto-Beweis hochladen", expanded=True):
                            uploaded_file = st.file_uploader("Kamera öffnen / Foto wählen", type=['png', 'jpg', 'jpeg'], key=f"file_{s_id}_{key}")
                            if uploaded_file:
                                img = Image.open(uploaded_file)
                                # Speichere Meldung im Session State
                                st.session_state.user_reports[s_id] = {
                                    "time": datetime.now().strftime("%H:%M"),
                                    "img": img
                                }
                                st.success("Danke! Dein Beleg wurde hinzugefügt.")
                                del st.session_state[f"reporting_{s_id}"]
                                st.rerun()

                    # Anzeige vorhandener Meldungen
                    if s_id in st.session_state.user_reports:
                        report = st.session_state.user_reports[s_id]
                        st.markdown(f"""<div class="report-box">⚠️ <b>Nutzer-Meldung ({report['time']} Uhr):</b><br>Preis weicht laut Foto-Beleg ab!</div>""", unsafe_allow_html=True)
                        if st.button("Beweis-Foto ansehen", key=f"view_{s_id}_{key}"):
                            st.image(report['img'], caption=f"Beleg von {report['time']} Uhr", use_container_width=True)

    with tabs[3]:
        m = folium.Map(location=[st.session_state.lat, st.session_state.lng], zoom_start=13)
        for s in stations:
            folium.Marker([s["lat"], s["lng"]], tooltip=str(s.get('brand'))).add_to(m)
        st_folium(m, width=700, height=500, key="map_v3")
else:
    st.error("Keine Daten gefunden.")
