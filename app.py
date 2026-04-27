import streamlit as st
import requests
import pandas as pd
import pydeck as pdk

# ... (Dein bisheriger Code für Setup und Daten laden bleibt gleich) ...

if stations:
    tabs = st.tabs(["Super E5", "Super E10", "Diesel", "🗺️ Karte"])
    # ... (Dein Code für die Preislisten bleibt gleich) ...

    with tabs[3]:
        st.subheader("Interaktive Karte")
        map_list = []
        for s in stations:
            name = s["brand"] if s.get("brand") else s["name"]
            dist = s.get("dist", 0)
            addr = f"{s.get('street', '')}, {s.get('place', '')}"
            
            # Google Maps Link erstellen
            gmaps_url = f"https://www.google.com/maps/search/?api=1&query={s['lat']},{s['lng']}"
            
            map_list.append({
                "name": name,
                "lat": s["lat"],
                "lon": s["lng"],
                "distance": f"{dist} km",
                "address": addr,
                "gmaps_url": gmaps_url
            })
        df = pd.DataFrame(map_list)

        # Karte mit Klick-Funktion (Tooltip)
        st.pydeck_chart(pdk.Deck(
            map_style='mapbox://styles/mapbox/streets-v11',
            initial_view_state=pdk.ViewState(
                latitude=53.414, 
                longitude=7.733, 
                zoom=11,
                pitch=0
            ),
            # Das ist das Infofenster beim Klicken/Draufzeigen
            tooltip={
                "html": "<b>{name}</b><br>Entfernung: {distance}<br><br>👉 <a href='{gmaps_url}' style='color:white;'>In Google Maps öffnen</a>",
                "style": {"backgroundColor": "#e2001a", "color": "white", "borderRadius": "10px"}
            },
            layers=[
                pdk.Layer(
                    "ScatterplotLayer",
                    df,
                    get_position='[lon, lat]',
                    get_color='[226, 0, 26, 200]',
                    get_radius=250,
                    pickable=True, # Macht die Punkte anklickbar
                ),
                pdk.Layer(
                    "TextLayer",
                    df,
                    get_position='[lon, lat]',
                    get_text='name',
                    get_size=20,
                    get_color=[0, 0, 0, 255],
                    get_alignment_baseline="'bottom'",
                    background=True,
                    get_background_color=[255, 255, 255, 200],
                    pickable=True, # Macht auch die Namen anklickbar
                )
            ]
        ))
        st.caption("Tipp: Klicke auf eine Tankstelle, um die Entfernung zu sehen und die Navigation zu starten.")
