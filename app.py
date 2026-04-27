import streamlit as st
import requests

# 1. SETUP
st.set_page_config(page_title="Wiesmoor Radar", page_icon="⛽")
API_KEY = "616cbb8e-9dde-4eb7-91f1-21a1663fa495"

st.markdown('<div style="background:#e2001a;color:white;padding:20px;text-align:center;border-radius:15px;font-weight:bold;font-size:1.4rem;">⛽ WIESMOOR LIVE-RADAR</div>', unsafe_allow_html=True)

# 2. DATEN-FUNKTION (Radius auf 20km erhöht für Decker)
def get_live_data():
    url = f"https://creativecommons.tankerkoenig.de/json/list.php?lat=53.414&lng=7.733&rad=20&sort=dist&type=all&apikey={API_KEY}"
    try:
        # Wir erzwingen eine frische Abfrage ohne Zwischenspeicher
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
            valid = [s for s in stations if s.get(fuel_type) and s.get(fuel_type) > 0]
            # Sortierung: Günstigste zuerst
            sorted_list = sorted(valid, key=lambda x: x[fuel_type])
            
            for i, s in enumerate(sorted_list):
                # Wir suchen Decker im Namen ODER in der Adresse (Wittmunder Str.)
                name_low = s["brand"].lower() + s["name"].lower()
                is_decker = "decker" in name_low or "wittmunder" in s["street"].lower()
                
                # Styling
                bg = "#f0fff4" if i == 0 else ("#eef6ff" if is_decker else "white")
                border = "#28a745" if i == 0 else ("#004a99" if is_decker else "#e2001a")
                
                # Decker bekommt einen Stern und wird hervorgehoben
                star = "⭐ " if is_decker else ""
                brand_name = s["brand"] if s["brand"] else s["name"]

                st.markdown(f'''
                <div style="background:{bg}; padding:15px; border-radius:12px; margin-top:10px; border-left:8px solid {border}; display:flex; justify-content:space-between; align-items:center; box-shadow:2px 2px 5px rgba(0,0,0,0.1);">
                    <div>
                        <b style="font-size:1.1rem;">{star}{brand_name}</b><br>
                        <small>{s["place"]}, {s["street"]}</small>
                    </div>
                    <div style="text-align:right;">
                        <div style="font-weight:bold; font-size:1.3rem;">{s[fuel_type]:.2f} €</div>
                        <small style="color:gray;">{"Offen" if s["isOpen"] else "Zu"}</small>
                    </div>
                </div>
                ''', unsafe_allow_html=True)

    render_fuel(t1, "e5")
    render_fuel(t2, "e10")
    render_fuel(t3, "diesel")
else:
    st.warning("Suche läuft... Falls nichts erscheint, bitte die Seite einmal kurz neu laden.")

# 3. SERVICE BEREICH
st.write("---")
st.subheader("🛠️ Wiesmoor Direkt-Hilfe")
col1, col2 = st.columns(2)
with col1:
    if st.button("📞 Decker anrufen"):
        st.success("04948 91990")
with col2:
    if st.button("🕒 Öffnungszeiten"):
        st.info("Meist 6:00 - 21:00 Uhr")
