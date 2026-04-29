import streamlit as st
import requests
from streamlit_js_eval import streamlit_js_eval

# 1. DAS DESIGN (Karten-Layout mit Fokus auf Korrektur)
st.set_page_config(page_title="Wiesmoor Radar", layout="centered")

st.markdown("""
<style>
    .hero-banner {
        width: 100%; height: 100px;
        background: linear-gradient(45deg, #1e3c72, #2a5298);
        border-radius: 15px; display: flex; align-items: center; 
        justify-content: center; margin-bottom: 20px; color: white;
        font-family: sans-serif; font-weight: 900; font-size: 1.5rem;
    }
    .station-card {
        background: white; padding: 15px; border-radius: 18px;
        display: flex; align-items: center; border: 1px solid #eee;
        box-shadow: 0 4px 12px rgba(0,0,0,0.08); margin-bottom: 8px;
    }
    .brand-tile {
        width: 50px; height: 50px; border-radius: 12px;
        display: flex; align-items: center; justify-content: center;
        font-weight: bold; font-size: 1.2rem; flex-shrink: 0;
    }
    .price-display { margin-left: auto; font-size: 1.8rem; font-weight: 900; }
    
    /* Button als dezenter Link unter der Karte */
    div.stButton > button {
        background: none !important; border: none !important;
        color: #ff4b4b !important; text-decoration: underline !important;
        font-size: 0.8rem !important; margin-top: -10px !important;
        padding-left: 65px !important;
    }
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="hero-banner">WIESMOOR RADAR 2.0</div>', unsafe_allow_html=True)

# 2. STANDORT & DATEN
if 'lat' not in st.session_state:
    st.session_state.lat, st.session_state.lng = 53.414, 7.733

# GPS Button
if st.button("📍 Meinen Standort für genaue Preise nutzen"):
    loc = streamlit_js_eval(js_expressions='navigator.geolocation ? new Promise((resolve) => { navigator.geolocation.getCurrentPosition(pos => resolve({lat: pos.coords.latitude, lon: pos.coords.longitude})) }) : null', key='gps_final')
    if loc:
        st.session_state.lat, st.session_state.lng = loc['lat'], loc['lon']
        st.rerun()

API_KEY = "616cbb8e-9dde-4eb7-91f1-21a1663fa495"

@st.cache_data(ttl=60)
def get_data(la, ln):
    url = f"https://creativecommons.tankerkoenig.de/json/list.php?lat={la}&lng={ln}&rad=10&sort=dist&type=all&apikey={API_KEY}"
    return requests.get(url).json().get("stations", [])

stations = get_data(st.session_state.lat, st.session_state.lng)

# 3. ANZEIGE MIT "LIVE-KORREKTUR" FUNKTION
if stations:
    tab1, tab2, tab3 = st.tabs(["Super E5", "Super E10", "Diesel"])
    fuels = {"Super E5": "e5", "Super E10": "e10", "Diesel": "diesel"}
    
    for i, (label, f_key) in enumerate(fuels.items()):
        with [tab1, tab2, tab3][i]:
            for s in sorted([x for x in stations if x.get(f_key)], key=lambda x: x.get(f_key)):
                name = str(s.get('brand', 'Freie Tankstelle')).upper()
                price = s.get(f_key)
                
                # Check ob Preis korrigiert wurde
                if st.session_state.get(f"new_price_{s['id']}"):
                    price = st.session_state[f"new_price_{s['id']}"]
                    st.success(f"✅ Preis durch dein Foto aktualisiert!")

                # Karte zeichnen
                st.markdown(f"""
                <div class="station-card">
                    <div class="brand-tile" style="background: #e9ecef; color: #495057;">{name[0]}</div>
                    <div style="margin-left: 15px;">
                        <div style="font-weight: 800;">{name}</div>
                        <div style="color: #888; font-size: 0.8rem;">{s.get('street')}</div>
                    </div>
                    <div class="price-display">{price:.2f}€</div>
                </div>
                """, unsafe_allow_html=True)
                
                # Der "Intelligente" Korrektur-Button
                if st.button(f"Preis an der Tankanzeige stimmt nicht? Hier korrigieren", key=f"btn_{s['id']}_{f_key}"):
                    st.session_state[f"show_cam_{s['id']}"] = True
                
                if st.session_state.get(f"show_cam_{s['id']}"):
                    with st.expander("Foto-Upload & Preis-Abgleich", expanded=True):
                        uploaded_file = st.file_uploader("Foto der Preistafel hochladen", type=['jpg', 'png'], key=f"file_{s['id']}")
                        if uploaded_file:
                            # SIMULATION: Hier würde normalerweise eine KI das Bild lesen.
                            # Wir simulieren das, indem wir den Preis leicht anpassen:
                            st.write("🔍 KI analysiert Bilddaten...")
                            new_p = price - 0.02 # Simulierter neuer Preis
                            if st.button("Gefundenen Preis übernehmen?", key=f"confirm_{s['id']}"):
                                st.session_state[f"new_price_{s['id']}"] = new_p
                                st.session_state[f"show_cam_{s['id']}"] = False
                                st.rerun()
