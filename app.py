import streamlit as st
import requests
from streamlit_js_eval import streamlit_js_eval

# 1. REFINED PREMIUM CSS
st.set_page_config(page_title="Wiesmoor Radar", layout="centered")

st.markdown("""
<style>
    /* Hero Banner */
    .hero-banner {
        background: linear-gradient(135deg, #e2001a 0%, #9b0012 100%);
        padding: 30px;
        border-radius: 24px;
        text-align: center;
        color: white;
        margin-bottom: 10px;
        box-shadow: 0 8px 20px rgba(226, 0, 26, 0.2);
    }
    
    /* Community Info Text */
    .info-subtext {
        text-align: center;
        color: #555;
        font-size: 0.9rem;
        font-weight: 500;
        margin-bottom: 25px;
        padding: 0 15px;
    }

    /* Station Card */
    .station-card {
        background: white;
        padding: 20px;
        border-radius: 22px;
        display: flex;
        align-items: center;
        border: 1px solid #f0f2f6;
        box-shadow: 0 4px 12px rgba(0,0,0,0.03);
        margin-bottom: 8px;
    }

    /* Brand Icons */
    .brand-logo {
        width: 62px;
        height: 62px;
        border-radius: 18px;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 1.8rem;
        font-weight: 900;
        box-shadow: inset 0 -3px 0 rgba(0,0,0,0.1);
        flex-shrink: 0;
    }

    .price-big {
        margin-left: auto;
        font-size: 2.2rem;
        font-weight: 900;
        color: #111;
        letter-spacing: -1px;
    }

    /* Custom Photo-Action Button */
    div.stButton > button:first-child {
        background-color: #f8f9fb;
        color: #555;
        border: 1px solid #e0e4e9;
        border-radius: 12px;
        padding: 8px 16px;
        font-size: 0.85rem;
        transition: all 0.2s;
        width: 100%;
        margin-top: -5px;
        margin-bottom: 20px;
    }
    
    div.stButton > button:first-child:hover {
        background-color: #e2001a;
        color: white;
        border-color: #e2001a;
    }
</style>
""", unsafe_allow_html=True)

# 2. BRAND PROFILES
def get_brand_style(brand_name):
    bn = brand_name.lower()
    if "aral" in bn: return {"bg": "#0070BB", "c": "white", "s": "A", "b": "none"}
    if "score" in bn: return {"bg": "#FFD100", "c": "#E2001A", "s": "S", "b": "3px solid #E2001A"}
    if "behrens" in bn: return {"bg": "#5D4037", "c": "white", "s": "🐻", "b": "none"}
    if "q1" in bn: return {"bg": "white", "c": "#E30613", "s": "Q1", "b": "3px solid #E30613"}
    if "jet" in bn: return {"bg": "#FFD200", "c": "#003399", "s": "J", "b": "none"}
    return {"bg": "#455A64", "c": "white", "s": "⛽", "b": "none"}

# --- UI CONTENT ---
st.markdown('<div class="hero-banner"><h1 style="margin:0; font-size:2rem;">WIESMOOR RADAR</h1></div>', unsafe_allow_html=True)
st.markdown('<div class="info-subtext">📸 Mache ein Foto der Preistafel für die Community, um die Echtheit der Preise zu bestätigen!</div>', unsafe_allow_html=True)

# App Logik
if 'lat' not in st.session_state: st.session_state.lat, st.session_state.lng = 53.414, 7.733

col_gps, col_ref = st.columns(2)
with col_gps:
    if st.button("📍 Standort"):
        loc = streamlit_js_eval(js_expressions='navigator.geolocation ? new Promise((resolve) => { navigator.geolocation.getCurrentPosition(pos => resolve({lat: pos.coords.latitude, lon: pos.coords.longitude})) }) : null', key='gps_final_v1')
        if loc:
            st.session_state.lat, st.session_state.lng = loc['lat'], loc['lon']
            st.rerun()
with col_ref:
    if st.button("🔄 Aktualisieren"):
        st.cache_data.clear()
        st.rerun()

# API
API_KEY = "616cbb8e-9dde-4eb7-91f1-21a1663fa495"
@st.cache_data(ttl=60)
def fetch_prices(la, ln):
    url = f"https://creativecommons.tankerkoenig.de/json/list.php?lat={la}&lng={ln}&rad=10&sort=dist&type=all&apikey={API_KEY}"
    return requests.get(url).json().get("stations", [])

stations = fetch_prices(st.session_state.lat, st.session_state.lng)

if stations:
    t1, t2, t3 = st.tabs(["Super E5", "Super E10", "Diesel"])
    map_fuel = {"Super E5": "e5", "Super E10": "e10", "Diesel": "diesel"}
    
    for i, (label, key) in enumerate(map_fuel.items()):
        with [t1, t2, t3][i]:
            for s in stations:
                price = s.get(key)
                if price:
                    style = get_brand_style(s.get('brand', ''))
                    
                    # Die Hauptkarte
                    st.markdown(f"""
                    <div class="station-card">
                        <div class="brand-logo" style="background-color: {style['bg']}; color: {style['c']}; border: {style['b']};">
                            {style['s']}
                        </div>
                        <div style="margin-left: 18px;">
                            <div style="font-weight: 800; font-size: 1.1rem;">{s.get('brand', 'Tankstelle').upper()}</div>
                            <div style="color: #888; font-size: 0.8rem;">{s.get('street')}</div>
                        </div>
                        <div class="price-big">{price:.2f}€</div>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    # Der Beleg-Button (jetzt im modernen Look via CSS)
                    if st.button(f"📸 Beleg für {s.get('brand')} senden", key=f"photo_{s['id']}_{key}"):
                        st.session_state[f"cam_{s['id']}"] = True
                    
                    if st.session_state.get(f"cam_{s['id']}"):
                        st.file_uploader("Kamera öffnen", type=['jpg', 'png'], key=f"up_{s['id']}")
else:
    st.info("Suche läuft...")
