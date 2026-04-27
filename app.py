import streamlit as st
import requests

# SETUP
st.set_page_config(page_title="Wiesmoor Radar", page_icon="⛽")
API_KEY = "616cbb8e-9dde-4eb7-91f1-21a1663fa495"

st.markdown('<div style="background:#e2001a;color:white;padding:20px;text-align:center;border-radius:15px;font-weight:bold;font-size:1.4rem;">⛽ WIESMOOR LIVE-RADAR</div>', unsafe_allow_html=True)

# DATEN LADEN (Cache deaktiviert für maximale Aktualität)
def get_live_data():
    # Wir nehmen einen Radius von 15km, damit wir alles um Wiesmoor/Großefehn/Mullberg abdecken
    url = f"https://creativecommons.tankerkoenig.de/json/list.php?lat=53.414&lng=7.733&rad=15&sort=dist&type=all&apikey={API_KEY}"
    try:
        r = requests.get(url, timeout=10).json()
        if r.get("ok"):
            return r["stations"]
    except:
        return None
    return None

stations = get_live_data()

if stations:
    t1, t2, t3 = st.tabs(["Super E5", "Super E10", "Diesel"])
    
    def render_fuel(tab, fuel_type):
        with tab:
            # Nur Stationen mit Preisen anzeigen und sortieren
            valid = [s for s in stations if s.get(fuel_type) and s.get(fuel_type) > 0]
            sorted_list = sorted(valid, key=lambda x: x[fuel_type])
            
            for i, s in enumerate(sorted_list):
                # Decker Check
                name = s["brand"].upper()
                is_decker = "DECKER" in name or "DECKER" in s["name"].upper()
                
                # Design-Logik
                bg = "#f0fff4" if i == 0 else ("#eef6ff" if is_decker else "white")
                border = "#28a745" if i == 0 else ("#004a99" if is_decker else "#e2001a")
                star = "⭐ " if is_decker else ""
                
                st.markdown(f'''
                <div style="background:{bg}; padding:15px; border-radius:12px; margin-top:10px; border-left:8px solid {border}; display:flex; justify-content:space-between; align-items:center; box-shadow:2px 2px 5px rgba(0,0,0,0.1);">
                    <div><b>{star}{s["brand"]}</b><br><small>{s["place"]}, {s["street"]}</small></div>
                    <div style="font-weight:bold; font-size:1.2rem;">{s[fuel_type]:.2f} €</div>
                </div>
                ''', unsafe_allow_html=True)

    render_fuel(t1, "e5")
    render_fuel(t2, "e10")
    render_fuel(t3, "diesel")
else:
    st.error("Warte kurz... Die Preise werden gerade aktualisiert. Bitte Seite in 10 Sekunden neu laden.")

st.write("---")
st.info("Hinweis: Die Preise werden direkt von der Markttransparenzstelle gemeldet. Bei extremen Abweichungen (z.B. über 2€) liegt oft ein Übermittlungsfehler der Tankstelle vor.")
