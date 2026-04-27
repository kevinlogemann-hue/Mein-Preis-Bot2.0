import streamlit as st
import requests
import folium
from streamlit_folium import st_folium
from streamlit_js_eval import streamlit_js_eval

# 1. SETUP
st.set_page_config(page_title="Wiesmoor Radar", page_icon="⛽", layout="centered")
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
    # JavaScript für die Standortabfrage
    location = streamlit_js_eval(
        js_expressions='navigator.geolocation ? new Promise((resolve) => { navigator.geolocation.getCurrentPosition(pos => resolve({lat: pos.coords.latitude, lon: pos.coords.longitude}), () => resolve(null)) }) : null',
        key='get_loc'
    )
    if st.button("📍 GPS"):
        if location:
            st.session_state.user_lat, st.session_state.user_lng = location['lat'], location['lon']
            st.session_state.using_gps = True
            st.rerun()
        else:
            st.warning("Kein Signal")

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
                # Durchschnitt berechnen (für das Preis-Highlighting)
                avg_price = sum(s[fuel_key] for s in valid) / len(valid)
                
                # Sortieren: Offene nach oben
                sorted_s = sorted(valid, key=lambda x: (not x['isOpen'], x[fuel_key]))
                
                for s in sorted_s:
                    isOpen = s.get('isOpen', False)
                    price = s[fuel_key]
                    name = s.get("brand", s.get("name", "Tankstelle"))
                    
                    # DESIGN-LOGIK
                    if isOpen:
                        # JEDE offene Tankstelle bekommt den grünen Balken
                        card_style = "background:white; border-left:10px solid #28a745; opacity:1.0; box-shadow: 0 2px 5px rgba(0,0,0,0.1);"
                        text_color = "#000"
                        # Preis wird grün, wenn er unter dem Durchschnitt liegt
                        p_color = "#28a745" if price < avg_price else "#000"
                        status_label = '<b style="color:#28a745;">● OFFEN</b>'
                    else:
                        # Geschlossene sind grau und ohne Balken
                        card_style = "background:#f9f9f9; border-left:10px solid #ccc; opacity:0.4; filter: grayscale(100%);"
                        text_color = "#888"
                        p_color = "#888"
                        status_label = '<b style="color:#888;">○ ZU</b>'

                    st.markdown(f'''
                    <div style="{card_style} padding:15px; border-radius:10px; margin-bottom:10px; display:flex; justify-content:space-between; align-items:center; border: 1px solid #eee;">
                        <div>
                            <b style="font-size:1.1rem; color:{text_color};">{name}</b><br>
                            <span style="font-size:0.9rem; color:{text_color};">{s.get("street", "")}</span><br>
                            {status_label}
                        </div>
                        <div style="text-align:right;">
                            <b style="font-size:1.4rem; color:{p_color};">{price:.2f} €</b><br>
                            <small style="color:{text_color};">{s.get("dist")} km</small>
                        </div>
                    </div>
                    ''', unsafe_allow_html=True)

    with tabs[3]:
        m = folium.Map(location=[st.session_state.user_lat, st.session_state.user_lng], zoom_start=12)
        for s in stations:
            folium.Marker(
                [s["lat"], s["lng"]], 
                tooltip=s["brand"],
                icon=folium.Icon(color='red' if s['isOpen'] else 'gray')
            ).add_to(m)
        st_folium(m, width=700, height=500, returned_objects=[])
