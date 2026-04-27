import streamlit as st
import requests
import pandas as pd

# 1. SETUP
st.set_page_config(page_title="Wiesmoor Radar", page_icon="⛽")
API_KEY = "616cbb8e-9dde-4eb7-91f1-21a1663fa495"

st.markdown('<div style="background:#e2001a;color:white;padding:20px;text-align:center;border-radius:15px;font-weight:bold;font-size:1.4rem;">⛽ WIESMOOR LIVE-RADAR</div>', unsafe_allow_html=True)

# 2. DATEN LADEN
def get_data():
    url = f"https://creativecommons.tankerkoenig.de/json/list.php?lat=53.414&lng=7.733&rad=15&sort=dist&type=all&apikey={API_KEY}"
    try:
        r = requests.get(url, timeout=10)
        return r.json().get("stations")
    except:
        return None

stations = get_data()

if stations:
    # Reiter erstellen: Jetzt mit Karte!
    tabs = st.tabs(["Super E5", "Super E10", "Diesel", "🗺️ Karte"])
    fuel_map = {"Super E5": "e5", "Super E10": "e10", "Diesel": "diesel"}
    
    # Die ersten drei Tabs für die Preislisten
    for i, label in enumerate(["Super E5", "Super E10", "Diesel"]):
        fuel_key = fuel_map[label]
        with tabs[i]:
            valid_stations = [s for s in stations if s.get(fuel_key) and s.get(fuel_key) > 0]
            sorted_stations = sorted(valid_stations, key=lambda x: x[fuel_key])
            
            if sorted_stations:
                # KLEINE STATISTIK
                avg_price = sum(s[fuel_key] for s in sorted_stations) / len(sorted_stations)
                st.write(f"📊 Durchschnittspreis in der Region: **{avg_price:.2f} €**")
                
                for s in sorted_stations:
                    name = s["brand"] if s.get("brand") else s["name"]
                    is_decker = "decker" in (name + s.get("street", "")).lower()
                    bg_color = "#eef6ff" if is_decker else "white"
                    border_color = "#004a99" if is_decker else "#e2001a"
                    
                    st.markdown(f'''
                    <div style="background:{bg_color}; padding:15px; border-radius:12px; margin-top:10px; border-left:8px solid {border_color}; display:flex; justify-content:space-between; align-items:center; box-shadow:2px 2px 5px rgba(0,0,0,0.1);">
                        <div>
                            <b style="font-size:1.1rem;">{"⭐ " if is_decker else ""}{name}</b><br>
                            <small>{s.get("street", "")}, {s.get("place", "")}</small>
                        </div>
                        <div style="text-align:right;">
                            <div style="font-weight:bold; font-size:1.3rem;">{s[fuel_key]:.2f} €</div>
                            <small style="color:{'green' if s['isOpen'] else 'red'};">{'● Offen' if s['isOpen'] else '● Zu'}</small>
                        </div>
                    </div>
                    ''', unsafe_allow_html=True)

    # DER KARTEN-TAB
    with tabs[3]:
        st.subheader("Tankstellen in deiner Nähe")
        map_data = []
        for s in stations:
            map_data.append({
                "name": s["brand"] if s.get("brand") else s["name"],
                "lat": s["lat"],
                "lon": s["lng"]
            })
        df = pd.DataFrame(map_data)
        st.map(df) # Erstellt automatisch eine Google-Maps ähnliche Karte

else:
    st.error("Daten konnten nicht geladen werden.")
