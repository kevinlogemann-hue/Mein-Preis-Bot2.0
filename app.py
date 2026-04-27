import streamlit as st
import requests

# 1. SETUP
st.set_page_config(page_title="Wiesmoor Radar", page_icon="⛽")
API_KEY = "616cbb8e-9dde-4eb7-91f1-21a1663fa495"

st.markdown('<div style="background:#e2001a;color:white;padding:20px;text-align:center;border-radius:15px;font-weight:bold;font-size:1.4rem;">⛽ WIESMOOR LIVE-RADAR</div>', unsafe_allow_html=True)

# 2. DATEN LADEN
def get_data():
    # Wir suchen im Umkreis von 15km um Wiesmoor
    url = f"https://creativecommons.tankerkoenig.de/json/list.php?lat=53.414&lng=7.733&rad=15&sort=dist&type=all&apikey={API_KEY}"
    try:
        r = requests.get(url, timeout=10)
        return r.json().get("stations")
    except:
        return None

stations = get_data()

if stations:
    # Erstellt die Reiter für die Spritsorten
    tabs = st.tabs(["Super E5", "Super E10", "Diesel"])
    # Hier war der Fehler mit der Klammer - jetzt ist er korrigiert:
    fuel_map = {"Super E5": "e5", "Super E10": "e10", "Diesel": "diesel"}
    
    for tab, label in zip(tabs, fuel_map.keys()):
        fuel_key = fuel_map[label]
        with tab:
            # Sortieren: Günstigste zuerst
            valid_stations = [s for s in stations if s.get(fuel_key) and s.get(fuel_key) > 0]
            sorted_stations = sorted(valid_stations, key=lambda x: x[fuel_key])
            
            for s in sorted_stations:
                name = s["brand"] if s.get("brand") else s["name"]
                # Markierung für Decker
                is_decker = "decker" in (name + s.get("street", "")).lower()
                
                # Design der Kachel
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

else:
    st.error("Preise konnten nicht geladen werden. Bitte Seite neu laden.")

st.info("Tipp: Die Preise werden direkt von den Tankstellen gemeldet.")

