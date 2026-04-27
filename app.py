import streamlit as st
import requests

# 1. SETUP & KEY
st.set_page_config(page_title="Wiesmoor Radar", page_icon="⛽")
API_KEY = "616cbb8e-9dde-4eb7-91f1-21a1663fa495"

st.markdown('<div style="background:#e2001a;color:white;padding:20px;text-align:center;border-radius:15px;font-weight:bold;font-size:1.4rem;">⛽ WIESMOOR RADAR</div>', unsafe_allow_html=True)

# 2. DATEN-FUNKTION (Inklusive Decker-Suche)
def get_prices():
    # Wir vergrößern den Suchradius auf 12km, um sicherzugehen, dass Decker (Wittmunder Str.) dabei ist
    url = f"https://creativecommons.tankerkoenig.de/json/list.php?lat=53.414&lng=7.733&rad=12&sort=dist&type=all&apikey={API_KEY}"
    try:
        r = requests.get(url, timeout=5).json()
        if r.get("ok"):
            return r["stations"], "LIVE"
    except:
        pass
    return [], "ERROR"

stations, mode = get_prices()

# 3. ANZEIGE DER PREISE
if mode == "LIVE":
    t1, t2, t3 = st.tabs(["Super E5", "Super E10", "Diesel"])

    def show_fuel(tab, key):
        with tab:
            # Sortieren nach Preis
            liste = sorted([s for s in stations if s.get(key) and s.get(key) > 0], key=lambda x: x[key])
            
            for i, s in enumerate(liste):
                # Markierung für Decker oder den günstigsten Preis
                is_decker = "Decker" in s["brand"] or "Decker" in s["name"]
                color = "#f0fff4" if i == 0 else "white"
                # Falls Decker, bekommt die Karte einen blauen Rand, sonst grün/rot
                border = "#004a99" if is_decker else ("#28a745" if i == 0 else "#e2001a")
                
                label = "⭐ FAVORIT: " if is_decker else ""
                
                st.markdown(f'''
                <div style="background:{color}; padding:15px; border-radius:12px; margin-top:10px; border-left:8px solid {border}; display:flex; justify-content:space-between; align-items:center; box-shadow:2px 2px 5px rgba(0,0,0,0.1);">
                    <div><b>{label}{s["brand"]}</b><br><small>{s["place"]}, {s["street"]}</small></div>
                    <div style="font-weight:bold; font-size:1.2rem;">{s[key]:.2f} €</div>
                </div>
                ''', unsafe_allow_html=True)

    show_fuel(t1, "e5")
    show_fuel(t2, "e10")
    show_fuel(t3, "diesel")
else:
    st.error("Preise konnten nicht geladen werden. Bitte Internetverbindung oder API-Key prüfen.")

# 4. SHOPPING & SERVICE
st.write("---")
st.subheader("🛠️ Wiesmoor Service & Shopping")
if st.button("📞 Gebr. Decker anrufen"):
    st.info("Rufnummer: 04948 91990")

item = st.text_input("Suche bei Berends, Aldi & Co:", placeholder="z.B. Kaffee...")
if item:
    st.link_button(f"🏢 Kaufhaus Berends: {item}", f"https://www.google.com/search?q=Kaufhaus+Berends+Wiesmoor+{item}", use_container_width=True)
    st.link_button(f"🔵 Aldi Nord: {item}", f"https://www.aldi-nord.de/suche.html?q={item}", use_container_width=True)
