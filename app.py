import streamlit as st
import requests
import pandas as pd
import folium
from streamlit_folium import st_folium
from streamlit_js_eval import streamlit_js_eval

# 1. SETUP
st.set_page_config(page_title="Wiesmoor Radar", page_icon="⛽", layout="centered")
API_KEY = "616cbb8e-9dde-4eb7-91f1-21a1663fa495"

st.markdown('<div style="background:linear-gradient(90deg, #e2001a, #b10014);color:white;padding:20px;text-align:center;border-radius:15px;font-weight:bold;font-size:1.6rem;">⛽ WIESMOOR LIVE-RADAR</div>', unsafe_allow_html=True)

# 2. STANDORT-ABFRAGE (Hier lag der kleine Fehler)
st.write("")
# Wir fragen den Browser nach den Koordinaten
loc = streamlit_js_eval(js_expressions='done(list(navigator.geolocation.getCurrentPosition(pos => { const {latitude, longitude} = pos.coords; done({latitude, longitude}) })))', key='get_location')

if loc and isinstance(loc, dict) and 'latitude' in loc:
    USER_LAT, USER_LNG = loc['latitude'], loc['longitude']
    st.success(f"📍 Position erkannt! Preise werden für deinen Standort berechnet.")
else:
    USER_LAT, USER_LNG = 53.414, 7.733 # Standard Wiesmoor
    st.info("ℹ️ Nutze Standard-Position (Wiesmoor). Für GPS bitte den Zugriff im Browser erlauben.")

# 3. DATEN LADEN
def get_data(lat, lng):
    url = f"https://creativecommons.tankerkoenig.de/json/list.php?lat={lat}&lng={lng}&rad=15&sort=dist&type=all&apikey={API_KEY}"
    try:
        r = requests.get(url, timeout=10)
        return r.json().get("stations")
    except: return None

stations = get_data(USER_LAT, USER_LNG)

if stations:
    tabs = st.tabs(["Super E5", "Super E10", "Diesel", "🗺️ Live-Karte"])
    fuel_map = {"Super E5": "e5", "Super E10": "e10", "Diesel": "diesel"}
    
    for i, label in enumerate(["Super E5", "Super E10", "Diesel"]):
        fuel_key = fuel_map[label]
        with tabs[i]:
            valid = [s for s in stations if s.get(fuel_key) and s.get(fuel_key) > 0]
            if valid:
                sorted_s = sorted(valid, key=lambda x: (not x['isOpen'], x[fuel_key]))
                avg_price = sum(s[fuel_key] for s in sorted_s) / len(sorted_s)
                
                st.markdown(f"💡 **Durchschnittspreis: {avg_price:.2f} €**")
                
                for s in sorted_s:
                    name_display = s["brand"] if s.get("brand") else s["name"]
                    price = s[fuel_key]
                    trend = "📉" if price < avg_price else "📈"
                    price_color = "#28a745" if price < avg_price else "#000000"
                    opacity = "1.0" if s['isOpen'] else "0.6"
                    
                    st.markdown(f'''
                    <div style="background:white; padding:12px; border-radius:12px; margin-top:8px; border: 1px solid #eee; display:flex; justify-content:space-between; align-items:center; opacity:{opacity}; shadow: 0 2px 4px rgba(0,0,0,0.1);">
                        <div>
                            <b style="font-size:1.1rem;">{name_display}</b><br>
                            <small>{s.get("street", "")}</small><br>
                            <small style="color:{'#28a745' if s['isOpen'] else '#e2001a'};">{'● OFFEN' if s['isOpen'] else '○ GESCHLOSSEN'}</small>
                        </div>
                        <div style="text-align:right;">
                            <span style="font-size:1.2rem; font-weight:bold; color:{price_color};">{price:.2f} €</span> {trend}<br>
                            <small style="color:#888;">{s.get("dist")} km</small>
                        </div>
                    </div>
                    ''', unsafe_allow_html=True)

    # 4. KARTE
    with tabs[3]:
        m = folium.Map(location=[USER_LAT, USER_LNG], zoom_start=12)
        
        # Markierung für dich selbst
        if loc:
            folium.Marker([USER_LAT, USER_LNG], tooltip="Deine Position", icon=folium.Icon(color='blue', icon='user', prefix='fa')).add_to(m)

        for s in stations:
            brand = s["brand"] if s.get("brand") else s["name"]
            gmaps_url = f"https://www.google.com/maps/dir/?api=1&destination={s['lat']},{s['lng']}"
            
            folium.Marker(
                [s["lat"], s["lng"]],
                popup=folium.Popup(f'<b>{brand}</b><br><br><a href="{gmaps_url}" target="_blank" style="background:#e2001a; color:white; padding:8px; border-radius:5px; text-decoration:none; display:block; text-align:center;">🚀 Route starten</a>', max_width=200),
                tooltip=folium.Tooltip(brand, permanent=True, direction="top"),
                icon=folium.Icon(color='red' if s['isOpen'] else 'gray')
            ).add_to(m)
        
        st_folium(m, width=700, height=500, returned_objects=[])

else:
    st.error("Daten konnten nicht geladen werden.")
