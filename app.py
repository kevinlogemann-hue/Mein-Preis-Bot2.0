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
    tabs = st.tabs(["Super E5", "Super E10", "Diesel", "🗺️ Karte"])
    fuel_map = {"Super E5": "e5", "Super E10": "e10", "Diesel": "diesel"}
    
    # Preislisten-Tabs
    for i, label in enumerate(["Super E5", "Super E10", "Diesel"]):
        fuel_key = fuel_map[label]
        with tabs[i]:
            valid = [s for s in stations if s.get(fuel_key) and s.get(fuel_key) > 0]
            sorted_s = sorted(valid, key=lambda x: x[fuel_key])
            if sorted_s:
                avg = sum(s[fuel_key] for s in sorted_s) / len(sorted_s)
                st.info(f"Durchschnitt: {avg:.2f} €")
                for s in sorted_s:
                    brand = s["brand"] if s.get("brand") else s["name"]
                    is_decker = "decker" in (brand + s.get("street", "")).lower()
                    bg = "#f0f7ff" if is_decker else "white"
                    bc = "#004a99" if is_decker else "#e2001a"
                    st.markdown(f'''
                    <div style="background:{bg}; padding:10px; border-radius:10px; margin-top:5px; border-left:5px solid {bc}; border: 1px solid #eee; display:flex; justify-content:space-between; align-items:center;">
                        <div><b>{brand}</b><br><small>{s.get("street", "")}</small></div>
                        <div style="text-align:right;"><b>{s[fuel_key]:.2f} €</b><br><small>{'● Offen' if s['isOpen'] else '○ Zu'}</small></div>
                    </div>
                    ''', unsafe_allow_html=True)

    # 3. INTERAKTIVE KARTE
    with tabs[3]:
        st.subheader("Interaktive Übersicht")
        map_data = []
        for s in stations:
            brand = s["brand"] if s.get("brand") else s["name"]
            dist = s.get("dist", 0)
            # Link für Google Maps
            gmaps_link = f"https://www.google.com/maps/search/?api=1&query={s['lat']},{s['lng']}"
            
            map_data.append({
                "name": brand,
                "lat": s["lat"],
                "lon": s["lng"],
                "distance": f"{dist} km",
                "link": gmaps_link
            })
        df = pd.DataFrame(map_data)

        st.pydeck_chart(pdk.Deck(
            map_style='mapbox://styles/mapbox/streets-v11',
            initial_view_state=pdk.ViewState(latitude=53.414, longitude=7.733, zoom=11),
            tooltip={
                "html": "<b>{name}</b><br>Entfernung: {distance}<br><a href='{link}' target='_blank' style='color:white;'>📍 In Google Maps öffnen</a>",
                "style": {"backgroundColor": "#e2001a", "color": "white"}
            },
            layers=[
                pdk.Layer(
                    "ScatterplotLayer", df, get_position='[lon, lat]',
                    get_color='[226, 0, 26, 200]', get_radius=250, pickable=True
                ),
                pdk.Layer(
                    "TextLayer", df, get_position='[lon, lat]', get_text='name',
                    get_size=18, get_color=[0, 0, 0], get_alignment_baseline="'bottom'",
                    background=True, get_background_color=[255, 255, 255, 180], pickable=True
                )
            ]
        ))
        st.caption("Tipp: Klicke auf einen Namen für Details und Google Maps Link.")

else:
    st.error("Daten konnten nicht geladen werden.")
