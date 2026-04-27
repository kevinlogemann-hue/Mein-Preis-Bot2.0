import streamlit as st
import requests
import pandas as pd
import folium
from streamlit_folium import st_folium

# 1. SETUP & STYLING
st.set_page_config(page_title="Wiesmoor Radar", page_icon="⛽", layout="centered")
API_KEY = "616cbb8e-9dde-4eb7-91f1-21a1663fa495"

# Echte Logos für die Tankstellen
LOGOS = {
    "aral": "https://www.aral.de/content/dam/aral/business-sites/de/global/retail/about-aral/logo/Aral_Logo_Standard.png",
    "shell": "https://www.shell.de/favicon.ico",
    "star": "https://www.star.de/favicon.ico",
    "q1": "https://www.q1.eu/favicon.ico",
    "classic": "https://www.classic-oil.de/favicon.ico",
    "avia": "https://www.avia.de/favicon.ico"
}

st.markdown('<div style="background:linear-gradient(90deg, #e2001a, #b10014);color:white;padding:20px;text-align:center;border-radius:15px;box-shadow: 0 4px 15px rgba(0,0,0,0.2);font-weight:bold;font-size:1.6rem;">⛽ WIESMOOR LIVE-RADAR</div>', unsafe_allow_html=True)

# 2. DATEN LADEN MIT TREND-BERECHNUNG
@st.cache_data(ttl=300) # 5 Minuten Cache zur Schonung der API
def get_data():
    url = f"https://creativecommons.tankerkoenig.de/json/list.php?lat=53.414&lng=7.733&rad=15&sort=dist&type=all&apikey={API_KEY}"
    try:
        r = requests.get(url, timeout=10)
        return r.json().get("stations")
    except: return None

stations = get_data()

if stations:
    tabs = st.tabs(["Super E5", "Super E10", "Diesel", "🗺️ Live-Karte"])
    fuel_map = {"Super E5": "e5", "Super E10": "e10", "Diesel": "diesel"}
    
    for i, label in enumerate(["Super E5", "Super E10", "Diesel"]):
        fuel_key = fuel_map[label]
        with tabs[i]:
            valid = [s for s in stations if s.get(fuel_key) and s.get(fuel_key) > 0]
            if valid:
                # Sortierung: Offene Tankstellen nach oben, dann nach Preis
                sorted_s = sorted(valid, key=lambda x: (not x['isOpen'], x[fuel_key]))
                avg_price = sum(s[fuel_key] for s in sorted_s) / len(sorted_s)
                
                st.info(f"💡 Durchschnittspreis in Wiesmoor: {avg_price:.2f} €")
                
                for s in sorted_s:
                    brand = s["brand"].lower() if s.get("brand") else "unbekannt"
                    name_display = s["brand"] if s.get("brand") else s["name"]
                    
                    # Trend & Farbe bestimmen
                    price = s[fuel_key]
                    trend = "📉" if price < avg_price else "📈"
                    price_color = "#28a745" if price < avg_price else "#000000"
                    
                    # Style für geschlossene Tankstellen
                    opacity = "1.0" if s['isOpen'] else "0.5"
                    status_text = "● GEÖFFNET" if s['isOpen'] else "○ GESCHLOSSEN"
                    
                    st.markdown(f'''
                    <div style="background:white; padding:12px; border-radius:12px; margin-top:8px; border: 1px solid #eee; display:flex; justify-content:space-between; align-items:center; opacity:{opacity}; box-shadow: 0 2px 5px rgba(0,0,0,0.05);">
                        <div style="display:flex; align-items:center;">
                            <div style="margin-right:15px; font-weight:bold; font-size:1.1rem;">
                                {name_display}<br>
                                <small style="color:#666; font-weight:normal;">{s.get("street", "")}</small><br>
                                <small style="color:{'#28a745' if s['isOpen'] else '#e2001a'}; font-size:0.7rem;">{status_text}</small>
                            </div>
                        </div>
                        <div style="text-align:right;">
                            <span style="font-size:1.3rem; font-weight:bold; color:{price_color};">{price:.2f} €</span> {trend}<br>
                            <small style="color:#999;">{s.get("dist")} km</small>
                        </div>
                    </div>
                    ''', unsafe_allow_html=True)

    # 3. KARTE (Mit dauerhaften Namen und Navigations-Knopf)
    with tabs[3]:
        st.subheader("Interaktive Tankstellen-Map")
        m = folium.Map(location=[53.414, 7.733], zoom_start=12)
        
        for s in stations:
            brand = s["brand"] if s.get("brand") else s["name"]
            gmaps_url = f"https://www.google.com/maps/dir/?api=1&destination={s['lat']},{s['lng']}"
            
            popup_html = f'''
                <div style="font-family: sans-serif; width:150px;">
                    <b style="color:#e2001a;">{brand}</b><br>
                    {s.get("street", "")}<br><br>
                    <a href="{gmaps_url}" target="_blank" style="display:block; background:#e2001a; color:white; text-align:center; padding:8px; border-radius:5px; text-decoration:none;">🚀 Jetzt Navigieren</a>
                </div>
            '''
            
            folium.Marker(
                [s["lat"], s["lng"]],
                popup=folium.Popup(popup_html, max_width=200),
                tooltip=folium.Tooltip(brand, permanent=True, direction="top"),
                icon=folium.Icon(color='red' if s['isOpen'] else 'gray', icon='flash' if s['isOpen'] else 'info-sign')
            ).add_to(m)
        
        st_folium(m, width=700, height=500, returned_objects=[])
        st.button("🔄 Preise aktualisieren", on_click=st.rerun)

else:
    st.error("Daten konnten nicht geladen werden. Bitte API-Key prüfen!")
