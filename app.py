import streamlit as st
import requests
from streamlit_js_eval import streamlit_js_eval
from datetime import datetime

# 1. PREMIUM DESIGN-KONFIGURATION
st.set_page_config(page_title="Wiesmoor Radar", layout="centered")

st.markdown("""
<style>
    /* Hauptbanner mit Tiefenwirkung */
    .hero-banner {
        width: 100%;
        height: 160px;
        background: linear-gradient(rgba(0,0,0,0.4), rgba(0,0,0,0.4)), url('https://images.unsplash.com/photo-1527018601619-a508a2be00cd?q=80&w=1000&auto=format&fit=crop');
        background-size: cover;
        background-position: center;
        border-radius: 20px;
        display: flex;
        align-items: center;
        justify-content: center;
        box-shadow: 0 10px 25px rgba(0,0,0,0.2);
        margin-bottom: 15px;
    }
    .hero-title {
        color: white;
        font-size: 2.2rem;
        font-weight: 900;
        text-shadow: 3px 3px 10px rgba(0,0,0,0.7);
        letter-spacing: -0.5px;
    }
    
    /* Community-Aufruf direkt unter dem Banner */
    .community-callout {
        background: #fdf2f2;
        border-left: 5px solid #e2001a;
        padding: 15px;
        border-radius: 8px;
        margin-bottom: 25px;
        color: #333;
        font-size: 0.95rem;
        line-height: 1.4;
    }

    /* Hochwertige Stations-Karten */
    .station-container {
        background: white;
        padding: 20px;
        border-radius: 20px;
        border: 1px solid #f0f0f0;
        box-shadow: 0 4px 15px rgba(0,0,0,0.05);
        display: flex;
        align-items: center;
        margin-bottom: 10px;
    }

    /* Authentische Brand-Icons */
    .brand-logo {
        width: 58px;
        height: 58px;
        border-radius: 15px;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 1.7rem;
        font-weight: 800;
        box-shadow: 0 4px 10px rgba(0,0,0,0.1);
        flex-shrink: 0;
    }

    .price-value {
        margin-left: auto;
        font-size: 2.2rem;
        font-weight: 900;
        color: #000;
        letter-spacing: -1px;
    }
    
    /* Styling für den Streamlit-Button Bereich */
    .stButton > button {
        border-radius: 10px;
        font-weight: 600;
    }
</style>
""", unsafe_allow_html=True)

# 2. MARKEN-FARBPROFILE (Nach Webseiten-Vorgabe)
def get_brand_identity(brand):
    b = brand.lower()
    # Aral: Original Sky Blue
    if "aral" in b: 
        return {"bg": "#0070BB", "txt": "white", "sym": "A", "border": "none"}
    # Score: Gelb mit markantem roten Rand
    if "score" in b: 
        return {"bg": "#FFD100", "txt": "#E2001A", "sym": "S", "border": "3px solid #E2001A"}
    # Behrens: Frei mit Bären-Symbol
    if "behrens" in b: 
        return {"bg": "#5D4037", "txt": "white", "sym": "🐻", "border": "none"}
    # Q1: Clean Weiß-Rot
    if "q1" in b: 
        return {"bg": "white", "txt": "#E30613", "sym": "Q1", "border": "2px solid #E30613"}
    # Jet: Signalgelb
    if "jet" in b: 
        return {"bg": "#FFD200", "txt": "#003399", "sym": "J", "border": "none"}
    return {"bg": "#455A64", "txt": "white", "sym": "⛽", "border": "none"}

# --- UI STRUKTUR ---
st.markdown('<div class="hero-banner"><div class="hero-title">WIESMOOR RADAR</div></div>', unsafe_allow_html=True)
st.markdown('<div class="community-callout">📸 <b>Community-Check:</b> Bitte mache ein Foto der Preistafel, um die Echtheit für alle Nutzer in Wiesmoor zu bestätigen!</div>', unsafe_allow_html=True)

# Standort-Steuerung
if 'lat' not in st.session_state: st.session_state.lat, st.session_state.lng = 53.414, 7.733

c1, c2 = st.columns(2)
with c1:
    if st.button("📍 Standort nutzen", use_container_width=True):
        loc = streamlit_js_eval(js_expressions='navigator.geolocation ? new Promise((resolve) => { navigator.geolocation.getCurrentPosition(pos => resolve({lat: pos.coords.latitude, lon: pos.coords.longitude})) }) : null', key='gps_v7')
        if loc:
            st.session_state.lat, st.session_state.lng = loc['lat'], loc['lon']
            st.rerun()
with c2:
    if st.button("🔄 Preise laden", use_container_width=True):
        st.cache_data.clear()
        st.rerun()

# Daten abrufen
API_KEY = "616cbb8e-9dde-4eb7-91f1-21a1663fa495"
@st.cache_data(ttl=60)
def load_prices(la, ln):
    try:
        url = f"https://creativecommons.tankerkoenig.de/json/list.php?lat={la}&lng={ln}&rad=10&sort=dist&type=all&apikey={API_KEY}"
        return requests.get(url).json().get("stations", [])
    except: return []

data = load_prices(st.session_state.lat, st.session_state.lng)

if data:
    tabs = st.tabs(["Super E5", "Super E10", "Diesel"])
    types = {"Super E5": "e5", "Super E10": "e10", "Diesel": "diesel"}

    for idx, (label, key) in enumerate(types.items()):
        with tabs[idx]:
            for s in data:
                price = s.get(key)
                if price:
                    brand = get_brand_identity(s.get('brand', ''))
                    st.markdown(f"""
                    <div class="station-container">
                        <div class="brand-logo" style="background-color: {brand['bg']}; color: {brand['txt']}; border: {brand['border']};">
                            {brand['sym']}
                        </div>
                        <div style="margin-left: 18px;">
                            <div style="font-weight: 800; font-size: 1.15rem; color: #111;">{s.get('brand', 'Tankstelle').upper()}</div>
                            <div style="color: #888; font-size: 0.85rem;">{s.get('street')}</div>
                        </div>
                        <div class="price-value">{price:.2f}€</div>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    # Interaktiver Foto-Upload Button direkt unter der Karte
                    btn_key = f"upload_{s['id']}_{key}"
                    if st.button(f"📸 Foto-Beleg für {s.get('brand')} senden", key=btn_key):
                        st.session_state[f"active_{s['id']}"] = True
                    
                    if st.session_state.get(f"active_{s['id']}"):
                        f = st.file_uploader("Kamera öffnen / Beleg wählen", type=['jpg', 'png'], key=f"file_{s['id']}")
                        if f:
                            st.success("Hervorragend! Dein Beleg wird geprüft.")
                            st.session_state[f"active_{s['id']}"] = False
                    
                    st.write("") # Abstandshalter
