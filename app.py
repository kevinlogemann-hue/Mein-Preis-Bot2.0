import streamlit as st
import requests
from streamlit_js_eval import streamlit_js_eval

# 1. Grund-Konfiguration
st.set_page_config(page_title="Wiesmoor Radar")

st.title("Wiesmoor Radar")
st.write("Community-Preischeck fuer Tankstellen")

# 2. Standort-Logik
if 'lat' not in st.session_state:
    st.session_state.lat = 53.414
if 'lng' not in st.session_state:
    st.session_state.lng = 7.733

def get_location():
    loc = streamlit_js_eval(js_expressions='navigator.geolocation ? new Promise((resolve) => { navigator.geolocation.getCurrentPosition(pos => resolve({lat: pos.coords.latitude, lon: pos.coords.longitude})) }) : null', key='gps_final')
    if loc:
        st.session_state.lat = loc['lat']
        st.session_state.lng = loc['lng']

if st.button("Standort aktualisieren"):
    get_location()

# 3. Parameter
radius = st.slider("Umkreis in km", 1, 50, 10)
sort_choice = st.radio("Sortierung", ["Preis", "Entfernung"])

# 4. API Abfrage
API_KEY = "616cbb8e-9dde-4eb7-91f1-21a1663fa495"

def load_data():
    base_url = "https://creativecommons.tankerkoenig.de/json/list.php"
    params = {
        "lat": st.session_state.lat,
        "lng": st.session_state.lng,
        "rad": radius,
        "sort": "dist",
        "type": "all",
        "apikey": API_KEY
    }
    try:
        response = requests.get(base_url, params=params)
        return response.json().get("stations", [])
    except:
        return []

stations = load_data()

# 5. Anzeige der Ergebnisse
if stations:
    tab1, tab2, tab3 = st.tabs(["Super E5", "Super E10", "Diesel"])
    
    mapping = {"Super E5": "e5", "Super E10": "e10", "Diesel": "diesel"}
    tabs = [tab1, tab2, tab3]
    
    for i, label in enumerate(["Super E5", "Super E10", "Diesel"]):
        fuel_key = mapping[label]
        with tabs[i]:
            # Nur Stationen mit Preis fuer diesen Sprit
            valid_list = [s for s in stations if s.get(fuel_key)]
            
            # Sortieren
            if sort_choice == "Preis":
                sorted_list = sorted(valid_list, key=lambda x: x.get(fuel_key))
            else:
                sorted_list = sorted(valid_list, key=lambda x: x.get('dist'))
                
            for s in sorted_list:
                with st.expander(str(s.get(fuel_key)) + " EUR - " + str(s.get('brand', 'Tankstelle'))):
                    st.write("Adresse: " + str(s.get('street')) + " " + str(s.get('place')))
                    st.write("Entfernung: " + str(s.get('dist')) + " km")
                    
                    # Foto-Funktion
                    if st.button("Foto hochladen", key="cam_" + str(s['id']) + fuel_key):
                        st.session_state["upload_" + str(s['id'])] = True
                    
                    if st.session_state.get("upload_" + str(s['id'])):
                        st.file_uploader("Preisschild fotografieren", type=['jpg','png'], key="file_" + str(s['id']))
else:
    st.write("Suche läuft... Falls nichts erscheint, bitte Radius erhoehen.")

st.divider()
st.caption("Datenquelle: Tankerkoenig.de / Markttransparenzstelle")
