import streamlit as st
import requests
from streamlit_js_eval import streamlit_js_eval

# 1. PREMIUM UI-SETUP
st.set_page_config(page_title="Wiesmoor Radar", layout="centered")

st.markdown("""
<style>
    /* Das markante Hauptbanner */
    .hero-banner {
        width: 100%;
        height: 150px;
        background: linear-gradient(rgba(0,0,0,0.4), rgba(0,0,0,0.6)), 
                    url('https://images.unsplash.com/photo-1527018601619-a508a2be00cd?q=80&w=1000');
        background-size: cover;
        background-position: center;
        border-radius: 20px;
        display: flex;
        align-items: center;
        justify-content: center;
        margin-bottom: 15px;
    }
    .hero-title {
        color: white;
        font-size: 2rem;
        font-weight: 900;
        letter-spacing: 1px;
    }

    /* Filter & Standort Bereich */
    .filter-container {
        background: #f8f9fa;
        padding: 15px;
        border-radius: 15px;
        margin-bottom: 20px;
    }

    /* Tankstellen Karten */
    .station-card {
        background: white;
        padding: 15px;
        border-radius: 18px;
        display: flex;
        align-items: center;
        border: 1px solid #eee;
        box-shadow: 0 4px 10px rgba(0,0,0,0.03);
        margin-bottom: 5px;
    }

    .brand-logo {
        width: 50px;
        height: 50px;
        border-radius: 12px;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 1.4rem;
        font-weight: bold;
        flex-shrink: 0;
    }

    .price-tag {
        margin-left: auto;
        font-size: 1.8rem;
        font-weight: 900;
        color: #000;
    }

    /* Die neuen Foto-Buttons (Modern & Dezent) */
    div.stButton > button {
        background-color: #f1f3f5 !important;
        color: #444 !important;
        border: none !important;
        border-radius: 10px !important;
        padding: 5px 15px !important;
        font-size: 0.75rem !important;
        font-weight: 600 !important;
        margin-top: -10px !important;
        margin-bottom: 20px !important;
        width: auto !important;
    }
    
    div.stButton > button:hover {
        background-color: #e2001a !important;
        color: white !important;
    }
</style>
""", unsafe_allow_html=True)

# --- APP HEADER ---
st.markdown('<div class="hero-banner"><div class="hero-title">WIESMOOR RADAR</div></div>', unsafe_allow_html=True)

# 2. FILTER & STANDORT LOGIK
if 'lat' not in st.session_state:
    st.session_state.lat, st.session_state.lng = 53.414, 7.733

with st.container():
    st.markdown("### Filter & Standort")
    col1, col2 = st.columns([2, 1])
    
    with col1:
        if st.button("📍 Standort aktualisieren", use_container_width=True):
            loc = streamlit_js_eval(js_expressions='navigator.geolocation ? new Promise((resolve) => { navigator.geolocation.getCurrentPosition(pos => resolve({lat: pos.coords.latitude, lon: pos.coords.longitude})) }) : null', key='gps_final')
            if loc:
                st.session_state.lat, st.session_state.lng = loc['lat'], loc['lon']
                st.rerun()
    
    with col2:
        radius = st.selectbox("Umkreis", [5, 10, 20, 50], index=1)

# 3. DATEN ABRUFEN
API_KEY = "616cbb8e-9dde-4eb7-91f1-21a1663fa495"

@st.cache_data(ttl=60)
def get_data(la, ln, rad):
    url = f"https://creativecommons.tankerkoenig.de/json/list.php?lat={la}&lng={ln}&rad={rad}&sort=dist&type=all&apikey={API_KEY}"
    return requests.get(url).json().get("stations", [])

def get_brand_style(brand):
    b = brand.lower()
    if "aral" in b: return {"bg": "#0070BB", "c": "white", "s": "A"}
    if "score" in b: return {"bg": "#FFD100", "c": "#E2001A", "s": "S"}
    if "behrens" in b: return {"bg": "#5D4037", "c": "white", "s": "B"}
    return {"bg": "#eee", "c": "#333", "s": "⛽"}

stations = get_data(st.session_state.lat, st.session_state.lng, radius)

# 4. PREIS-ANZEIGE
if stations:
    tab1, tab2, tab3 = st.tabs(["Super E5", "Super E10", "Diesel"])
    fuel_map = {"Super E5": "e5", "Super E10": "e10", "Diesel": "diesel"}

    for i, (label, key) in enumerate(fuel_map.items()):
        with [tab1, tab2, tab3][i]:
            for s in stations:
                price = s.get(key)
                if price:
                    style = get_brand_style(s.get('brand', ''))
                    
                    # Karte
                    st.markdown(f"""
                    <div class="station-card">
                        <div class="brand-logo" style="background-color: {style['bg']}; color: {style['c']};">
                            {style['s']}
                        </div>
                        <div style="margin-left: 15px;">
                            <div style="font-weight: 800; font-size: 1rem;">{s.get('brand').upper()}</div>
                            <div style="color: #888; font-size: 0.75rem;">{s.get('street')} ({s.get('dist')} km)</div>
                        </div>
                        <div class="price-tag">{price:.2f}€</div>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    # Foto-Button
                    if st.button(f"📷 Beleg senden", key=f"photo_{s['id']}_{key}"):
                        st.session_state[f"cam_{s['id']}"] = True
                    
                    if st.session_state.get(f"cam_{s['id']}"):
                        st.file_uploader("Foto wählen", type=['jpg', 'png'], key=f"up_{s['id']}")
else:
    st.info("Keine Stationen gefunden. Bitte Standort oder Umkreis prüfen.")
