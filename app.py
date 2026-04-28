import streamlit as st
import requests
from streamlit_js_eval import streamlit_js_eval
from datetime import datetime
from PIL import Image

# 1. SETUP & MODERNES DESIGN
st.set_page_config(page_title="Wiesmoor Radar", layout="centered")

st.markdown("""
<style>
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
    .info-text-box {
        background-color: #f8f9fa;
        border-radius: 10px;
        padding: 12px;
        margin-bottom: 20px;
        border: 1px solid #e0e0e0;
        text-align: center;
        color: #444;
        font-size: 0.9rem;
    }
    /* Logo Styling */
    .brand-icon {
        width: 40px;
        height: 40px;
        border-radius: 8px;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 1.5rem;
        margin-right: 12px;
        color: white;
        font-weight: bold;
    }
    .station-card {
        border: 1px solid #ddd; 
        padding: 12px; 
        margin: 10px 0; 
        background: white; 
        border-radius: 12px;
        display: flex;
        align-items: center;
    }
    .station-info {
        flex-grow: 1;
    }
    .price-display {
        font-size: 1.6rem;
        font-weight: 900;
        color: #111;
        min-width: 80px;
        text-align: right;
    }
</style>
""", unsafe_allow_html=True)

# 2. HEADER
st.markdown('<div class="header-container"><div class="header-overlay"><div class="header-title">WIESMOOR LIVE-RADAR</div></div></div>', unsafe_allow_html=True)
st.markdown('<div class="info-text-box">📸 <b>Mache Fotos für die Community.</b> Je mehr mitmachen, desto genauer werden die Preise!</div>', unsafe_allow_html=True)

# --- BRAND LOGIC FUNKTION ---
def get_brand_style(name):
    name = name.lower()
    if "aral" in name:
        return {"color": "#005596", "icon": "A", "label": "Aral"}
    elif "shell" in name:
        return {"color": "#FBCE07", "icon": "S", "label": "Shell"}
    elif "behrens" in name:
        return {"color": "#5D4037", "icon": "🐻", "label": "Behrens"} # Bär-Icon für Behrens
    elif "score" in name:
        return {"color": "#E30613", "icon": "SC", "label": "Score"}
    elif "jet" in name:
        return {"color": "#FFD200", "icon": "J", "label": "Jet"}
    elif "esso" in name:
        return {"color": "#ED1C24", "icon": "E", "label": "Esso"}
    elif "total" in name:
        return {"color": "#FF5900", "icon": "T", "label": "Total"}
    elif "avanti" in name:
        return {"color": "#008B45", "icon": "AV", "label": "Avanti"}
    else:
        return {"color": "#607D8B", "icon": "⛽", "label": "Freie"}

# --- API & LOGIK ---
API_KEY = "616cbb8e-9dde-4eb7-91f1-21a1663fa495"

if 'user_reports' not in st.session_state: st.session_state.user_reports = {}
if 'lat' not in st.session_state: st.session_state.lat = 53.414
if 'lng' not in st.session_state: st.session_state.lng = 7.733

col_a, col_b = st.columns(2)
with col_a:
    if st.button("📍 Standort"):
        loc = streamlit_js_eval(js_expressions='navigator.geolocation ? new Promise((resolve) => { navigator.geolocation.getCurrentPosition(pos => resolve({lat: pos.coords.latitude, lon: pos.coords.longitude})) }) : null', key='gps_radar_v2')
        if loc:
            st.session_state.lat, st.session_state.lng = loc['lat'], loc['lon']
            st.rerun()
with col_b:
    if st.button("🔄 Update"):
        st.cache_data.clear()
        st.rerun()

@st.cache_data(ttl=60)
def fetch_prices(lat, lng):
    url = f"https://creativecommons.tankerkoenig.de/json/list.php?lat={lat}&lng={lng}&rad=15&sort=dist&type=all&apikey={API_KEY}"
    try:
        return requests.get(url, timeout=5).json().get("stations", [])
    except: return []

stations = fetch_prices(st.session_state.lat, st.session_state.lng)

# 3. ANZEIGE
if stations:
    tabs = st.tabs(["Super E5", "Super E10", "Diesel"])
    fuels = {"Super E5": "e5", "Super E10": "e10", "Diesel": "diesel"}

    for i, (label, key) in enumerate(fuels.items()):
        with tabs[i]:
            valid_s = [s for s in stations if s.get(key) and s.get(key) > 0]
            for s in valid_s:
                sid = s['id']
                brand_info = get_brand_style(s.get('brand', 'Tankstelle'))
                status_color = "#28a745" if s.get('isOpen') else "#888"
                
                st.markdown(f"""
                <div class="station-card" style="border-left: 6px solid {status_color};">
                    <div class="brand-icon" style="background-color: {brand_info['color']};">
                        {brand_info['icon']}
                    </div>
                    <div class="station-info">
                        <div style="font-weight:bold; font-size:1rem; color:#222;">{s.get('brand', 'Tankstelle').upper()}</div>
                        <div style="color:#777; font-size:0.75rem;">{s.get('street')}</div>
                    </div>
                    <div class="price-display">{s.get(key):.2f}€</div>
                </div>
                """, unsafe_allow_html=True)

                # Melde-Funktion
                if st.button(f"📸 Beleg senden", key=f"up_{sid}_{key}"):
                    st.session_state[f"show_{sid}"] = True
                
                if st.session_state.get(f"show_{sid}"):
                    up = st.file_uploader("Foto wählen", type=['jpg','png'], key=f"file_{sid}")
                    if up:
                        st.session_state.user_reports[sid] = {"time": datetime.now().strftime("%H:%M"), "img": Image.open(up)}
                        del st.session_state[f"show_{sid}"]
                        st.rerun()

                if sid in st.session_state.user_reports:
                    st.success(f"✅ Foto-Update um {st.session_state.user_reports[sid]['time']} Uhr")
else:
    st.info("Suche Tankstellen...")
