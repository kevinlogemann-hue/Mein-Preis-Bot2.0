import streamlit as st
import requests
import folium
from streamlit_folium import st_folium
from streamlit_js_eval import streamlit_js_eval

# 1. SETUP & STYLING
st.set_page_config(page_title="Wiesmoor Radar", page_icon="⛽", layout="centered")

# Custom CSS für die Karten-Optik
st.markdown("""
    <style>
    .stTabs [data-baseweb="tab-list"] { gap: 10px; }
    .stTabs [data-baseweb="tab"] {
        background-color: #f0f2f6; border-radius: 10px 10px 0 0; padding: 10px 20px;
    }
    </style>
""", unsafe_allow_html=True)

API_KEY = "616cbb8e-9dde-4eb7-91f1-21a1663fa495"

st.markdown('<div style="background:linear-gradient(90deg, #e2001a, #b10014);color:white;padding:20px;text-align:center;border-radius:15px;font-weight:bold;font-size:1.6rem;box-shadow: 0 4px 10px rgba(0,0,0,0.2);">⛽ WIESMOOR LIVE-RADAR</div>', unsafe_allow_html=True)

# 2. STANDORT-LOGIK
if 'user_lat' not in st.session_state:
    st.session_state.user_lat, st.session_state.user_lng = 53.414, 7.733
    st.session_state.using_gps = False

st.write("")
c1, c2 = st.columns([3, 1])

with c1:
    msg = "📍 Fokus: Wiesmoor Zentrum" if not st.session_state.using_gps else "🎯 GPS-Standort aktiv"
    st.info(msg)

with c2:
    location = streamlit_js_eval(
        js_expressions='navigator.geolocation ? new Promise((resolve) => { navigator.geolocation.getCurrentPosition(pos => resolve({lat: pos.coords.latitude, lon: pos.coords.longitude}), () => resolve(null)) }) : null',
        key='get_loc'
    )
    if st.button("📍 GPS"):
        if location:
            st.session_state.user_lat, st.session_state.user_lng = location['lat'], location['lon']
            st.session_state.using_gps = True
            st.rerun()

# 3. DATEN LADEN
def get_data(lat, lng):
    url = f"https://creativecommons.tankerkoenig.de/json/list.php?lat={lat}&lng={lng}&rad=15&sort=dist&type=all&apikey={API_KEY}"
    try:
        r = requests.get(url, timeout=10)
        return r.json().get("stations")
    except: return None

stations = get_data(st.session_state.user_lat, st.session_state.user_lng)

if stations:
    tabs = st.tabs(["Super E5", "Super E10", "Diesel", "🗺️ Karte"])
    fuel_map = {"Super E5": "e5", "Super E10": "e10", "Diesel": "diesel"}
    
    for i, label in enumerate(["Super E5", "Super E10", "Diesel"]):
        fuel_key = fuel_map[label]
        with tabs[i]:
            valid = [s for s in stations if s.get(fuel_key) and s.get(fuel_key) > 0]
            if valid:
                avg_price = sum(s[fuel_key] for s in valid) / len(valid)
                sorted_s = sorted(valid, key=lambda x: (not x['isOpen'], x[fuel_key]))
                
                for s in sorted_s:
                    isOpen = s.get('isOpen', False)
                    price = s[fuel_key]
                    brand = s.get("brand", "Tankstelle").upper()
                    
                    # LOGO LOGIK
                    # Fallback-Icon (Zapfsäule), falls das Tankerkönig-Logo nicht lädt
                    fallback_logo = "https://cdn-icons-png.flaticon.com/512/864/864831.png"
                    logo_url = f"https://creativecommons.tankerkoenig.de/img/stations/{s.get('id')}.png"
                    
                    if isOpen:
                        card_style = "background:white; border-left:12px solid #28a745; box-shadow: 0 4px 12px rgba(0,0,0,0.1);"
                        p_color = "#28a745" if price < avg_price else "#000"
                        status = '<b style="color:#28a745;">● OFFEN</b>'
                        img_css = "filter: none;"
                    else:
                        card_style = "background:#f9f9f9; border-left:12px solid #ccc; opacity:0.6;"
                        p_color = "#888"
                        status = '<b style="color:#888;">○ ZU</b>'
                        img_css = "filter: grayscale(100%); opacity: 0.5;"

                    st.markdown(f'''
                    <div style="{card_style} padding:15px; border-radius:12px; margin-bottom:12px; display:flex; justify-content:space-between; align-items:center; border: 1px solid #eee;">
                        <div style="display:flex; align-items:center; gap:15px;">
                            <div style="width:50px; height:50px; background:#f0f2f6; border-radius:8px; display:flex; align-items:center; justify-content:center; overflow:hidden;">
                                <img src="{logo_url}" onerror="this.src='{fallback_logo}'" style="width:40px; height:40px; object-fit:contain; {img_css}">
                            </div>
                            <div>
                                <b style="font-size:1.1rem;">{brand}</b><br>
                                <small style="color:#666;">{s.get("street", "")}</small><br>
                                {status}
                            </div>
                        </div>
                        <div style="text-align:right;">
                            <b style="font-size:1.5rem; color:{p_color};">{price:.2f} €</b><br>
                            <small style="color:#999;">{s.get("dist")} km</small>
                        </div>
                    </div>
                    ''', unsafe_allow_html=True)

    with tabs[3]:
        zoom = 14 if st.session_state.using_gps else 12
        m = folium.Map(location=[st.session_state.user_lat, st.session_state.user_lng], zoom_start=zoom)
        if st.session_state.using_gps:
            folium.Marker([st.session_state.user_lat, st.session_state.user_lng], tooltip="

