# ... (Vorheriger Code für Daten laden bleibt gleich)

for s in sorted_s:
    name = s["brand"] if s.get("brand") else s["name"]
    price = s[fuel_key]
    isOpen = s['isOpen']
    
    # KORRIGIERTE LOGIK:
    if isOpen:
        # JEDE offene Tankstelle bekommt jetzt den grünen Balken (border-left)
        card_style = "background:white; border-left:8px solid #28a745; opacity:1.0; box-shadow: 0 4px 8px rgba(0,0,0,0.1);"
        text_color = "#000"
        status_label = '<b style="color:#28a745;">● OFFEN</b>'
        # Preis wird grün, wenn unter Durchschnitt
        price_style = f"color:{'#28a745' if price < avg else '#000'};"
    else:
        # Geschlossene bleiben grau und ohne Balken
        card_style = "background:#f2f2f2; border-left:8px solid #999; opacity:0.35; filter: grayscale(100%);"
        text_color = "#777"
        status_label = '<b style="color:#666;">○ ZU</b>'
        price_style = "color:#777;"

    st.markdown(f'''
    <div style="{card_style} padding:15px; border-radius:12px; margin-top:10px; display:flex; justify-content:space-between; align-items:center; border-top:1px solid #ddd; border-right:1px solid #ddd; border-bottom:1px solid #ddd;">
        <div style="color:{text_color};">
            <b style="font-size:1.2rem;">{name}</b><br>
            <small>{s.get("street", "Keine Adresse")}</small><br>
            {status_label}
        </div>
        <div style="text-align:right;">
            <span style="font-size:1.4rem; font-weight:bold; {price_style}">{price:.2f} €</span><br>
            <small style="color:{text_color};">{s.get("dist")} km</small>
        </div>
    </div>
    ''', unsafe_allow_html=True)
