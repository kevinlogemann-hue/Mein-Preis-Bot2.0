import streamlit as st
import requests

# 1. SETUP
st.set_page_config(page_title="Wiesmoor Radar", page_icon="⛽")
API_KEY = "616cbb8e-9dde-4eb7-91f1-21a1663fa495"

st.markdown('<div style="background:#e2001a;color:white;padding:20px;text-align:center;border-radius:15px;font-weight:bold;font-size:1.4rem;">⛽ WIESMOOR LIVE-RADAR</div>', unsafe_allow_html=True)

# 2. DATEN-FUNKTIONEN
def get_live_data():
    url = f"https://creativecommons.tankerkoenig.de/json/list.php?lat=53.414&lng=7.733&rad=20&sort=dist&type=all&apikey={API_KEY}"
    try:
        r = requests.get(url, timeout=10).json()
        return r.get("stations") if r.get("ok") else None
    except: return None

def get_opening_times(station_id):
    url = f"https://creativecommons.tankerkoenig.de/json/detail.php?id={station_id}&apikey={API_KEY}"
    try:
        r = requests.get(url, timeout=5).json()
        if r.get("ok") and "openingTimes" in r["station"]:
            return r["station"]["openingTimes"]
        return None
    except: return None

stations = get_live_data()

if stations:
    tabs = st.tabs(["Super E5", "Super E10", "Diesel"])
    fuel_types = ["e5", "e10", "diesel"]
    
    for i, tab in enumerate(tabs):
        fuel = fuel_types[i]
        with tab:
            # Filtern und Sortieren
            valid = [s for s in stations if s.get(fuel) and s.get(fuel) > 0]
            sorted_list = sorted(valid, key=lambda x: x[fuel])
            
            for s in sorted_list:
                name_low = (s["brand"] + s["name"]).lower()
                is_decker = "decker" in name_low or "wittmunder" in s["street"].lower()
                
                # Farben & Styling
                bg = "#eef6ff" if is_decker else "white"
                border = "#004a99" if is_decker else "#e2001a"
                brand_display = s["brand"] if s["brand"] else s["name"]

                st.markdown(f'''
                <div style="background:{bg}; padding:15px; border-radius:12px; margin-top:10px; border-left:8px solid {border}; display:flex; justify-content:space-between; align-items:center; box-shadow:2px 2px 5px rgba(0,0,0,0.1);">
                    <div><b>{"⭐ " if is_decker else ""}{brand_display}</b><br><small>{s["place"]}, {s["street"]}</small></div>
                    <div style="text-align:right;"><div style="font-weight:bold; font-size:1.3rem; color:#333;">{s[fuel]:.2f} €</div></div>
                </div>
                ''', unsafe_allow_html=True)
                
                # INFO-BEREICH
                with st.expander(f"🕒 Details & Öffnungszeiten"):
                    status = "🟢 JETZT GEÖFFNET" if s["isOpen"] else "🔴 GESCHLOSSEN"
                    st.write(f"Aktueller Status: **{status}**")
                    
                    if st.button("Wochenplan abrufen", key=f"plan_{s['id']}_{fuel}"):
                        times = get_opening_times(s['id'])
                        if times:
                            for t in times:
                                st.write(f"📅 **{t['text']}**: {t['start']} - {t['end']} Uhr")
                        else:
                            st.info("Diese Station ist ein 24h-Automat oder meldet keine festen Wochenzeiten.")

else:
    st.warning("Preise werden geladen... bitte Seite ggf. neu laden.")
