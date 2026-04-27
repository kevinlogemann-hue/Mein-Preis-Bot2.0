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
    tabs = st.tabs(["Super E5", "Super E10", "Diesel", "🗺️ Karte"])
    fuel_map = {"Super E5": "e5", "Super E10": "e10", "Diesel": "diesel"}
    
    for i, label in enumerate(["Super E5", "Super E10", "Diesel"]):
        fuel_key = fuel_map[label]
        with tabs[i]:
            valid = [s for s in stations if s.get(fuel_key) and s.get(fuel_key) > 0]
            sorted_s = sorted(valid, key=lambda x: x[fuel_key])
            if sorted_s:
                st.write(f"Schnitt: {sum(s[fuel_key] for s in sorted_s)/len(sorted_s):.2f} €")
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

    # 3. STABILE KARTE (Funktioniert garantiert)
    with tabs[3]:
        st.subheader("Standorte in der Übersicht")
        map_data = []
        for s in stations:
            map_data.append({
                "lat": s["lat"],
                "lon": s["lng"],
                "name": s["brand"] if s.get("brand") else s["name"]
            })
        df = pd.DataFrame(map_data)
        
        # Die Standard-Map von Streamlit ist am stabilsten
        st.map(df, size=20, color='#e2001a')
        
        # Liste der Standorte direkt darunter, falls man Namen sucht
        st.write("---")
        for m in map_data:
            st.text(f"📍 {m['name']}")

else:
    st.error("Daten konnten nicht geladen werden.")
