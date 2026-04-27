    with tabs[3]:
        # Karte erstellen - zentriert auf USER_LAT/USER_LNG
        # Wenn GPS aktiv ist, zoomen wir etwas näher ran (14), sonst Übersicht (12)
        zoom_lvl = 14 if st.session_state.using_gps else 12
        m = folium.Map(location=[st.session_state.user_lat, st.session_state.user_lng], zoom_start=zoom_lvl)
        
        # NEU: DEIN STANDORT ALS BLAUER PUNKT
        if st.session_state.using_gps:
            folium.Marker(
                [st.session_state.user_lat, st.session_state.user_lng],
                popup="Du bist hier",
                tooltip="Mein Standort",
                icon=folium.Icon(color='blue', icon='user', prefix='fa')
            ).add_to(m)

        # Die Tankstellen-Marker (wie gehabt)
        for s in stations:
            color = 'red' if s['isOpen'] else 'lightgray'
            folium.Marker(
                [s["lat"], s["lng"]], 
                tooltip=s["brand"],
                icon=folium.Icon(color=color, icon='info-sign')
            ).add_to(m)
            
        st_folium(m, width=700, height=500, returned_objects=[])
