import streamlit as st
import requests
import pandas as pd
import pydeck as pdk

# 1. SETUP
st.set_page_config(page_title="Wiesmoor Radar", page_icon="⛽", layout="centered")
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
    tabs = st.tabs(["Super E5", "Super E10", "Diesel", "🗺️ Live-Karte"])
    fuel_map = {"Super E5": "e5", "Super E10": "e10", "Diesel": "diesel"}
    
    for i, label in enumerate(["Super E5", "Super E10", "Diesel"]):
        fuel_key = fuel_map[label]
        with tabs[i]:
            valid = [s for s in stations if s.get(fuel_key) and s.get(fuel_key) > 0]
            sorted_s = sorted(valid, key=lambda x: x[fuel_key])
            if sorted_s:
                avg = sum(s[fuel_key] for s in sorted_s) / len(sorted_s)
                st.info(f"Durchschnittspreis: {avg:.2f} €")
                for s in sorted_s:
                    brand = s["brand"] if s.get("brand") else s["name"]
                    is_decker = "decker" in (brand + s.get("street", "")).lower()
                    bg = "#f0f7ff" if is_decker else "white"
                    bc = "#004a99" if is_decker else "#e2001a"
                    st.markdown(f'''
                    <div style="background:{bg}; padding:12px; border-radius:10px; margin-top:8px; border-left:6px solid {bc}; display:flex; justify-content:space-between; align-items:center; border-right: 1px solid #eee; border-top: 1px solid #eee; border-bottom: 1px solid #eee;">
                        <div><b>{brand}</b><br><small>{s.get("street", "")}</small></div>
                        <div style="text-align:right;"><b>{s[fuel_key]:.2f} €</b><br><small>{'● Offen' if s['isOpen'] else '● Zu'}</small></div>
                    </div>
                    ''', unsafe_allow_html=True)

    # 3. VERBESSERTE KARTE
    with tabs[3]:
        st.subheader("Tankstellen-Radar")
        m_data = []
        for s in stations:
            brand = s["brand"] if s.get("brand") else s["name"]
            is_fav = "decker" in (brand + s.get("street", "")).lower()
            m_data.append({
                "name": brand,
                "lat": s["lat"],
                "lon": s["lng"],
                "color": [0, 100, 255] if is_fav else [255, 0, 0]
            })
        df = pd.DataFrame(m_data)

        # Kartendesign: 'mapbox://styles/mapbox/streets-v11' für Farben oder 'satellite-streets-v11'
        st.pydeck_chart(pdk.Deck(
            map_style='mapbox://styles/mapbox/streets-v11', 
            initial_view_state=pdk.ViewState(
                latitude=53.414, 
                longitude=7.733, 
                zoom=12,
                pitch=45 # Leicht schräge Ansicht für 3D-Effekt
            ),
            layers=[
                # Farbige Kreise
                pdk.Layer(
                    "ScatterplotLayer",
                    df,
                    get_position='[lon, lat]',
                    get_color='color',
                    get_radius=180,
                    pickable=True
                ),
                # Schicke Text-Labels mit weißem Hintergrund
                pdk.Layer(
                    "TextLayer",
                    df,
                    get_position='[lon, lat]',
                    get_text='name',
                    get_size=20,
                    get_color=[0, 0, 0],
                    get_alignment_baseline="'bottom'",
                    background=True,
                    get_background_color=[255, 255, 255, 220],
                    padding=[4, 4],
                )
            ]
        ))
else:
    st.error("Daten konnten nicht geladen werden.")
