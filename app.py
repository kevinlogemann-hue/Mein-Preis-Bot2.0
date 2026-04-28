import streamlit as st
import requests
from streamlit_js_eval import streamlit_js_eval
from datetime import datetime
from PIL import Image

# 1. Seiteneinstellungen & Modernes CSS (Hübsches Design)
st.set_page_config(page_title="Wiesmoor Radar", layout="centered")

st.markdown("""
<style>
    /* Das neue, bild-basierte Banner */
    .header-container {
        position: relative;
        width: 100%;
        height: 150px;
        background-color: #e2001a;
        background-image: url('https://images.unsplash.com/photo-1527018601619-a508a2be00cd?q=80&w=1000&auto=format&fit=crop');
        background-size: cover;
        background-position: center;
        border-radius: 15px;
        display: flex;
        align-items: center;
        justify-content: center;
        border: 2px solid #c10016;
        margin-bottom: 5px;
    }
    .header-overlay {
        background: rgba(180, 0, 0, 0.4); 
        width: 100%;
        height: 100%;
        border-radius: 13px;
        display: flex;
        align-items: center;
        justify-content: center;
    }
    .header-title {
        color: white;
        font-size: 1.8rem;
        font-weight: 900;
        text-align: center;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.7);
    }
    /* Die Community-Infobox */
    .info-text-box {
        background-color: #f8f9fa;
        border-radius: 10px;
        padding: 12px;
        margin-top: 5px;
        margin-bottom: 20px;
        border: 1px solid #e0e0e0;
        text-align: center;
        color: #444;
        font-size: 0.9rem;
        line-height: 1.4;
    }
    /* Tankstellen-Karte */
    .station-card {
        border: 1px solid #ddd; 
        padding: 15px; 
        margin: 10px 0; 
        background: white; 
        border-radius: 12px;
        display: flex;
        justify-content: space-between;
        align-items: center;
    }
    .station-name {
        font-weight: bold;
        font-size: 1.1rem;
        color: #222;
        text-transform: uppercase;
    }
    .station-address {
        color: #777;
        font-size: 0.8rem;
    }
    .price-display {
        font-size: 1.7rem;
        font-weight: 900;
        color: #111;
        text-align: right;
    }
</style>
""", unsafe_allow_html=True)

# 2. Header & Community-Aufruf anzeigen
# Wir laden das Foto als Hintergrund des Banners
st.markdown("""
<div class="header-container">
    <div class="header-overlay">
        <div class="header-title">WIESMOOR LIVE-RADAR</div>
    </div>
</div>
""", unsafe_allow_html=True)

# Der Community-Aufruf mit Icon, dezent und modern verpackt
st.markdown("""
<div class="info-text-box">
    📸 <b>Mache Fotos für die Community für die Echtzeit-Preisangaben.</b><br>
    Umso mehr mitmachen, desto genauer werden die Preise werden!
</div>
""", unsafe_allow_html=True)

# --- API & LOGIK ---
API_KEY = "616cbb8e-9dde-4eb7-91f1-21a1663fa495"

if 'user_reports' not in st.session_state:
    st.session_state.user_reports = {}
if 'lat' not in st.session_state:
    st.session_state.lat = 53.414
if 'lng' not in st.session_state:
    st.session_state.lng = 7.733

# Standort & Update Buttons
col_a, col_b = st.columns(2)
with col_a:
    # Standort-Button mit Icon
    if st.button("📍 Standort"):
        loc = streamlit_js_eval(js_expressions='navigator.geolocation ? new Promise((resolve) => { navigator.geolocation.getCurrentPosition(pos => resolve({lat: pos.coords.latitude, lon: pos.coords.longitude})) }) : null', key='gps_radar_v1')
        if loc:
            st.session_state.lat = loc['lat']
            st.session_state.lng = loc['lon']
            st.rerun()
with col_b:
    # Aktualisieren-Button
    if st.button("🔄 Aktualisieren"):
        st.cache_data.clear()
        st.rerun()

# Daten laden
@st.cache_data(ttl=60)
def fetch_prices(lat, lng):
    url = f"https://creativecommons.tankerkoenig.de/json/list.php?lat={lat}&lng={lng}&rad=15&sort=dist&type=all&apikey={API_KEY}"
    try:
        r = requests.get(url, timeout=5)
        return r.json().get("stations", [])
    except: return []

stations = fetch_prices(st.session_state.lat, st.session_state.lng)

# Liste anzeigen
if stations:
    tabs = st.tabs(["Super E5", "Super E10", "Diesel"])
    fuels = {"Super E5": "e5", "Super E10": "e10", "Diesel": "diesel"}

    for i, (label, key) in enumerate(fuels.items()):
        with tabs[i]:
            valid_s = [s for s in stations if s.get(key) and s.get(key) > 0]
            for s in valid_s:
                sid = s['id']
                
                # Wir bauen die Tankstellen-Karte mit HTML für das saubere Design
                st.markdown(f"""
                <div class="station-card">
                    <div>
                        <div class="station-name">{s.get('brand', 'Tankstelle').upper()}</div>
                        <div class="station-address">{s.get('street')}</div>
                    </div>
                    <div class="price-display">{s.get(key):.2f}€</div>
                </div>
                """, unsafe_allow_html=True)

                # Melde-Funktion (Community-Update) dezent darunter
                if st.button(f"📸 Beleg senden", key=f"up_btn_{sid}_{key}"):
                    st.session_state[f"show_up_{sid}"] = True
                
                if st.session_state.get(f"show_up_{sid}"):
                    up = st.file_uploader("Kamera öffnen / Foto wählen", type=['jpg','png'], key=f"file_{sid}")
                    if up:
                        st.session_state.user_reports[sid] = {"time": datetime.now().strftime("%H:%M"), "img": Image.open(up)}
                        del st.session_state[f"show_up_{sid}"]
                        st.rerun()

                if sid in st.session_state.user_reports:
                    rep = st.session_state.user_reports[sid]
                    st.success(f"✅ Foto-Update um {rep['time']} Uhr")
                    # Optional: Button zum Foto-Ansehen (kann man später aktivieren)
                    # if st.button("Foto zeigen", key=f"view_{sid}_{key}"):
                    #     st.image(rep['img'])
else:
    st.info("Suche nach Tankstellen in Wiesmoor...")
