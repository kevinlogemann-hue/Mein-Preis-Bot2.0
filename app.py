import streamlit as st
import requests
from streamlit_js_eval import streamlit_js_eval
from datetime import datetime
from PIL import Image

# 1. SETUP & PREMIUM DESIGN
st.set_page_config(page_title="Wiesmoor Radar", layout="centered")

st.markdown("""
<style>
    .header-container {
        width: 100%;
        height: 150px;
        background-image: linear-gradient(rgba(0,0,0,0.3), rgba(0,0,0,0.3)), url('https://images.unsplash.com/photo-1527018601619-a508a2be00cd?q=80&w=1000&auto=format&fit=crop');
        background-size: cover;
        background-position: center;
        border-radius: 20px;
        display: flex;
        align-items: center;
        justify-content: center;
        border: 2px solid #e2001a;
        margin-bottom: 10px;
    }
    .header-title {
        color: white;
        font-size: 2rem;
        font-weight: 900;
        text-shadow: 2px 2px 8px rgba(0,0,0,0.8);
    }
    .community-text {
        text-align: center;
        color: #444;
        font-size: 0.95rem;
        font-weight: 600;
        margin-bottom: 25px;
        line-height: 1.4;
        padding: 0 10px;
    }
    .brand-icon {
        width: 55px;
        height: 55px;
        border-radius: 14px;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 1.6rem;
        font-weight: 800;
        box-shadow: 0 4px 8px rgba(0,0,0,0.15);
        flex-shrink: 0;
    }
    .station-card {
        background: white;
        padding: 15px;
        border-radius: 18px;
        display: flex;
        align-items: center;
        border: 1px solid #f0f0f0;
        box-shadow: 0 2px 8px rgba(0,0,0,0.05);
    }
    .price-display {
        margin-left: auto;
        font-size: 1.9rem;
        font-weight: 900;
        color: #111;
    }
</style>
""", unsafe_allow_html=True)

# 2. BRAND LOGIC (Originalfarben & Icons)
def get_brand_style(name):
    n = name.lower()
    if "aral" in n: return {"bg": "#0070BB", "color": "white", "icon": "A", "border": "none"}
    if "score" in n: return {"bg": "#FFD100", "color": "#E2001A", "icon": "S", "border": "2px solid #E2001A"}
    if "behrens" in n: return {"bg": "#5D4037", "color": "white", "icon": "🐻", "border": "none"}
    if "shell" in n: return {"bg": "#FBCE07", "color": "#D50000", "icon": "S", "border": "1px solid #D50000"}
    if "jet" in n: return {"bg": "#FFD200", "color": "#003399", "icon": "J", "border": "none"}
    return {"bg": "#455A64", "color": "white", "icon": "⛽", "border": "none"}

# --- HEADER & TEXT ---
st.markdown('<div class="header-container"><div class="header-title">WIESMOOR RADAR</div></div>', unsafe_allow_html=True)
st.markdown('<div class="community-text">📸 Bitte macht Fotos für die Community, um die Echtheit der Preise zu bestätigen! Je mehr Belege, desto sicherer für alle.</div>', unsafe_allow_html=True)

# --- APP LOGIK ---
API_KEY = "616cbb8e-9dde-4eb7-91f1-21a1663fa495"
if 'user_reports' not in st.session_state: st.session_state.user_reports = {}
if 'lat' not in st.session_state: st.session_state.lat, st.session_state.lng = 53.414, 7.733

# Buttons
col_a, col_b = st.columns(2)
with col_a:
    if st.button("📍 Standort", use_container_width=True):
        loc = streamlit_js_eval(js_expressions='navigator.geolocation ? new Promise((resolve) => { navigator.geolocation.getCurrentPosition(pos => resolve({lat: pos.coords.latitude, lon: pos.coords.longitude})) }) : null', key='gps_final')
        if loc:
            st.session_state.lat, st.session_state.lng = loc['lat'], loc['lon']
            st.rerun()
with col_b:
    if st.button("🔄 Aktualisieren", use_container_width=True):
        st.cache_data.clear()
        st.rerun()

@st.cache_data(ttl=60)
def fetch_data(la, ln):
    try:
        url = f"https://creativecommons.tankerkoenig.de/json/list.php?lat={la}&lng={ln}&rad=10&sort=dist&type=all&apikey={API_KEY}"
        return requests.get(url).json().get("stations", [])
    except: return []

stations = fetch_data(st.session_state.lat, st.session_state.lng)

# 3. ANZEIGE DER TANKSTELLEN
if stations:
    tabs = st.tabs(["Super E5", "Super E10", "Diesel"])
    fuels = {"Super E5": "e5", "Super E10": "e10", "Diesel": "diesel"}

    for i, (label, key) in enumerate(fuels.items()):
        with tabs[i]:
            for s in stations:
                price = s.get(key)
                if price:
                    sid = s['id']
                    style = get_brand_style(s.get('brand', ''))
                    
                    # Die Karte
                    st.markdown(f"""
                    <div class="station-card">
                        <div class="brand-icon" style="background-color: {style['bg']}; color: {style['color']}; border: {style['border']};">
                            {style['icon']}
                        </div>
                        <div style="margin-left:15px;">
                            <div style="font-weight:bold; font-size:1.1rem;">{s.get('brand', 'Tankstelle').upper()}</div>
                            <div style="color:#777; font-size:0.8rem;">{s.get('street')}</div>
                        </div>
                        <div class="price-display">{price:.2f}€</div>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    # --- DER FUNKTIONIERENDE BUTTON ---
                    # Wir platzieren den Button direkt unter der Karte
                    if st.button(f"📸 Foto-Beleg für {s.get('brand')} senden", key=f"btn_{sid}_{key}"):
                        st.session_state[f"show_{sid}"] = True
                    
                    # Das Upload-Feld öffnet sich nur, wenn man auf den Button klickt
                    if st.session_state.get(f"show_{sid}"):
                        up = st.file_uploader("Kamera öffnen / Bild wählen", type=['jpg','png'], key=f"file_{sid}")
                        if up:
                            st.session_state.user_reports[sid] = {"time": datetime.now().strftime("%H:%M")}
                            st.success("Danke! Foto wurde hochgeladen.")
                            del st.session_state[f"show_{sid}"]
                            st.rerun()

                    # Anzeige, wenn bereits ein Foto für diese Station gemeldet wurde
                    if sid in st.session_state.user_reports:
                        st.info(f"✅ Community-Bestätigung erhalten ({st.session_state.user_reports[sid]['time']} Uhr)")
                    
                    st.markdown("<br>", unsafe_allow_html=True)
else:
    st.info("Suche Tankstellen in Wiesmoor...")
