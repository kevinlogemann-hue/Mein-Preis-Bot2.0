import streamlit as st
import requests
from streamlit_js_eval import streamlit_js_eval
from datetime import datetime
from PIL import Image

# 1. DESIGN-SYSTEM (Farben & Branding)
st.set_page_config(page_title="Wiesmoor Radar", layout="centered")

st.markdown("""
<style>
    /* Header mit dem atmosphärischen Tankstellen-Bild */
    .header-container {
        width: 100%;
        height: 160px;
        background-image: linear-gradient(rgba(0,0,0,0.3), rgba(0,0,0,0.3)), url('https://images.unsplash.com/photo-1527018601619-a508a2be00cd?q=80&w=1000&auto=format&fit=crop');
        background-size: cover;
        background-position: center;
        border-radius: 15px;
        display: flex;
        align-items: center;
        justify-content: center;
        border-bottom: 4px solid #e2001a;
        margin-bottom: 10px;
    }
    .header-title {
        color: white;
        font-size: 2rem;
        font-weight: 900;
        text-align: center;
        text-shadow: 3px 3px 6px rgba(0,0,0,0.8);
        letter-spacing: 1px;
    }
    .community-box {
        background-color: #f8f9fa;
        border-radius: 12px;
        padding: 15px;
        border: 1px solid #dee2e6;
        text-align: center;
        margin-bottom: 20px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
    }
    /* Brand Icon Styling */
    .brand-icon {
        width: 50px;
        height: 50px;
        border-radius: 8px;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 1.5rem;
        font-weight: bold;
        margin-right: 15px;
        box-shadow: 1px 1px 3px rgba(0,0,0,0.2);
    }
    .card {
        background: white;
        padding: 15px;
        border-radius: 15px;
        border: 1px solid #eee;
        display: flex;
        align-items: center;
        margin-bottom: 8px;
    }
    .price {
        margin-left: auto;
        font-size: 1.8rem;
        font-weight: 900;
        color: #111;
    }
</style>
""", unsafe_allow_html=True)

# --- LOGIK FÜR DIE MARKEN-IDENTITÄT ---
def get_brand_style(brand_name):
    name = brand_name.lower()
    
    # ARAL: Hellblau (#0070BB) & Weiß
    if "aral" in name:
        return {"bg": "#0070BB", "color": "white", "icon": "A", "border": "none"}
    
    # SCORE: Gelber Grund (#FFD100), Rotes Logo/Schrift
    elif "score" in name:
        return {"bg": "#FFD100", "color": "#E2001A", "icon": "SC", "border": "2px solid #E2001A"}
    
    # BEHRENS: Braun-Töne für den Bären 🐻
    elif "behrens" in name:
        return {"bg": "#5D4037", "color": "white", "icon": "🐻", "border": "none"}
    
    # SHELL: Muschel-Gelb (#FBCE07) & Rot
    elif "shell" in name:
        return {"bg": "#FBCE07", "color": "#D50000", "icon": "S", "border": "1px solid #D50000"}
    
    # JET: Rein-Gelb (#FFD200) & Dunkelblau
    elif "jet" in name:
        return {"bg": "#FFD200", "color": "#003399", "icon": "J", "border": "none"}
    
    # ESSO: Rot (#EF3340) & Weiß
    elif "esso" in name:
        return {"bg": "#EF3340", "color": "white", "icon": "E", "border": "none"}
        
    # Q1: Weißer Grund, Rote Schrift (oft schlichtes Design)
    elif "q1" in name:
        return {"bg": "#ffffff", "color": "#e30613", "icon": "Q1", "border": "2px solid #e30613"}

    # CLASSIC: Grün/Weiß/Rot
    elif "classic" in name:
        return {"bg": "#008B45", "color": "white", "icon": "C", "border": "none"}

    # DEFAULT für Unbekannte
    return {"bg": "#455A64", "color": "white", "icon": "⛽", "border": "none"}

# --- APP STRUKTUR ---
st.markdown('<div class="header-container"><div class="header-title">WIESMOOR LIVE-RADAR</div></div>', unsafe_allow_html=True)
st.markdown('<div class="community-box">📸 <b>Community-Power:</b> Lade ein Foto hoch, um die Preise aktuell zu halten!</div>', unsafe_allow_html=True)

# Standort-Steuerung
if 'lat' not in st.session_state: st.session_state.lat, st.session_state.lng = 53.414, 7.733

col1, col2 = st.columns(2)
with col1:
    if st.button("📍 Standort ermitteln"):
        loc = streamlit_js_eval(js_expressions='navigator.geolocation ? new Promise((resolve) => { navigator.geolocation.getCurrentPosition(pos => resolve({lat: pos.coords.latitude, lon: pos.coords.longitude})) }) : null', key='gps_v4')
        if loc:
            st.session_state.lat, st.session_state.lng = loc['lat'], loc['lon']
            st.rerun()
with col2:
    if st.button("🔄 Preise laden"):
        st.cache_data.clear()
        st.rerun()

# API Abfrage
API_KEY = "616cbb8e-9dde-4eb7-91f1-21a1663fa495"
@st.cache_data(ttl=60)
def load_data(la, ln):
    try:
        url = f"https://creativecommons.tankerkoenig.de/json/list.php?lat={la}&lng={ln}&rad=12&sort=dist&type=all&apikey={API_KEY}"
        return requests.get(url, timeout=5).json().get("stations", [])
    except: return []

data = load_data(st.session_state.lat, st.session_state.lng)

# Anzeige der Ergebnisse
if data:
    tabs = st.tabs(["Super E5", "Super E10", "Diesel"])
    mapping = {"Super E5": "e5", "Super E10": "e10", "Diesel": "diesel"}

    for i, (tab_name, fuel_key) in enumerate(mapping.items()):
        with tabs[i]:
            for s in data:
                price = s.get(fuel_key)
                if price:
                    style = get_brand_style(s.get('brand', ''))
                    st.markdown(f"""
                    <div class="card">
                        <div class="brand-icon" style="background-color: {style['bg']}; color: {style['color']}; border: {style['border']};">
                            {style['icon']}
                        </div>
                        <div>
                            <div style="font-weight:bold; font-size:1rem;">{s.get('brand', 'Tankstelle').upper()}</div>
                            <div style="color:#666; font-size:0.75rem;">{s.get('street')}</div>
                        </div>
                        <div class="price">{price:.2f}€</div>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    # Foto-Upload Button
                    if st.button(f"📸 Foto für {s.get('brand')}", key=f"photo_{s['id']}_{fuel_key}"):
                        st.session_state[f"up_{s['id']}"] = True
                    
                    if st.session_state.get(f"up_{s['id']}"):
                        file = st.file_uploader("Kamerabild auswählen", type=['jpg','png'], key=f"file_{s['id']}")
                        if file:
                            st.success("Danke! Foto wurde empfangen.")
                            del st.session_state[f"up_{s['id']}"]
                            st.rerun()
else:
    st.info("Suche läuft...")
