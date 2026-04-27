import streamlit as st
import requests
import pandas as pd
import folium
from streamlit_folium import st_folium

# 1. SETUP
st.set_page_config(page_title="Wiesmoor Radar", page_icon="⛽", layout="centered")
API_KEY = "616cbb8e-9dde-4eb7-91f1-21a1663fa495"

# Kopfzeile (Die bleibt immer oben sichtbar)
st.markdown('<div style="background:#e2001a;color:white;padding:20px;text-align:center;border-radius:15px;font-weight:bold;font-size:1.4rem;">⛽ WIESMOOR LIVE-RADAR</div>', unsafe_allow_html=True)

# 2. DATEN LADEN
def get_data():
    url = f"https://creativecommons.tankerkoenig.de/json/list.php?lat=53.414&lng=7.733&rad=15&sort=dist&type=all&apikey={API_KEY}"
    try:
        r = requests.get(url, timeout=10)
        return r.json().get("stations")
    except: return None

stations = get_data()

if stations:
    # Wir speichern den aktuellen Tab in einem "Sitzungsspeicher"
    if 'active_tab' not in st.session_state:
        st.session_state.active_tab = 0

    tabs = st.tabs(["Super E5", "Super E10", "Diesel", "🗺️ Karte"])
    
    fuel_map = {"Super E5": "e5", "Super E10": "e10", "Diesel": "diesel"}
    
    # Preislisten (Tabs 0-2)
    for i, label in enumerate(["Super E5", "Super E10", "Diesel"]):
        fuel_key = fuel_map[label]
        with tabs[i]:
            valid = [s for s in stations if s.get(fuel_key) and s.get(fuel_key) > 0]
            sorted_s = sorted(valid, key=lambda x: x[fuel_key])
            if sorted_s:
                for s in sorted_s:
                    brand = s["brand"] if s.get("brand") else s["name"]
                    is_decker = "decker" in (brand + s.get("street", "")).lower()
                    bg = "#f0f7ff" if is_decker else "white"
                    bc = "#004a99" if is_decker else "#e2001a"
                    st.markdown(f'''
                    <div style="background:{bg}; padding:10px; border-radius:10px; margin-top:5px; border-left:5px solid {bc}; border: 1px solid #eee; display:flex; justify-content:space-between; align-items:center;">
                        <div><b>{brand}</b><br><small>{s.get("street", "")}</small></div>
                        <div style="text-align:right;"><b>{s[fuel_key]:.2f} €</b><br><small>{'●' if s['isOpen'] else '○'}</small></div>
                    </div>
                    ''', unsafe_allow_html=True)

    # 3. KARTE MIT "ZURÜCK"-FUNKTION
    with tabs[3]:
        st.subheader("Übersicht & Navigation")
        
        # Karte erstellen
        m = folium.Map(location=[53.414, 7.733], zoom_start=12)
        
        for s in stations:
            brand = s["brand"] if s.get("brand") else s["name"]
            dist = s.get("dist", 0)
            gmaps_url = f"https://www.google.com/maps/search/?api=1&query={s['lat']},{s['lng']}"
            
            popup_html = f'''
                <div style="font-family: Arial; width: 160px;">
                    <b>{brand}</b><br>Entfernung: {dist} km<br><br>
                    <a href="{gmaps_url}" target="_blank" style="background:#e2001a; color:white; padding:8px; border-radius:5px; text-decoration:none; display:inline-block; text-align:center; width:100%;">📍 Navigieren</a>
                </div>
            '''
            
            folium.Marker(
                [s["lat"], s["lng"]],
                popup=folium.Popup(popup_html, max_width=200),
                tooltip=folium.Tooltip(brand, permanent=True, direction="top"),
                icon=folium.Icon(color='red', icon='info-sign')
            ).add_to(m)
        
        # Anzeige der Karte
        st_folium(m, width=700, height=500, returned_objects=[])
        
        # Der neue "Zurück zur Liste" Button
        st.write("") # Kleiner Abstand
        if st.button("⬅️ Zurück zur Preisliste"):
             st.markdown('<script>window.parent.document.querySelector(".stTabs [aria-selected=\'false\']").click();</script>', unsafe_allow_html=True)
             st.rerun()

else:
    st.error("Daten konnten nicht geladen werden.")
