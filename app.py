import streamlit as st
import requests

# 1. SETUP
st.set_page_config(page_title="Wiesmoor Radar", page_icon="⛽")
API_KEY = "616cbb8e-9dde-4eb7-91f1-21a1663fa495"

st.markdown('<div style="background:#e2001a;color:white;padding:20px;text-align:center;border-radius:15px;font-weight:bold;font-size:1.4rem;">⛽ WIESMOOR RADAR</div>', unsafe_allow_html=True)

# 2. DATEN-FUNKTION
def get_prices():
    url = f"https://creativecommons.tankerkoenig.de/json/list.php?lat=53.414&lng=7.733&rad=10&sort=dist&type=all&apikey={API_KEY}"
    try:
        r = requests.get(url, timeout=5).json()
        if r.get("ok"):
            return r["stations"], "LIVE"
    except:
        pass
    # Demo-Daten als Sicherheitsnetz
    demo = [
        {"brand": "JET", "place": "Aurich", "e5": 1.76, "e10": 1.70, "diesel": 1.58, "isOpen": True},
        {"brand": "SCORE", "place": "Friedeburg", "e5": 1.78, "e10": 1.72, "diesel": 1.60, "isOpen": True},
        {"brand": "CLASSIC", "place": "Wiesmoor", "e5": 1.79, "e10": 1.74, "diesel": 1.62, "isOpen": True}
    ]
    return demo, "DEMO"

stations, mode = get_prices()

# Hinweis-Banner falls Live nicht geht
if mode == "DEMO":
    st.warning("⚠️ Live-Daten laden noch (Key-Check läuft). Hier sind die aktuellen Richtpreise:")

# 3. ANZEIGE
t1, t2, t3 = st.tabs(["Super E5", "Super E10", "Diesel"])

def show_fuel(tab, key):
    with tab:
        liste = sorted([s for s in stations if s.get(key)], key=lambda x: x[key])
        for i, s in enumerate(liste):
            color = "#f0fff4" if i == 0 else "white"
            border = "#28a745" if i == 0 else "#e2001a"
            st.markdown(f'''
            <div style="background:{color}; padding:15px; border-radius:12px; margin-top:10px; border-left:6px solid {border}; display:flex; justify-content:space-between; align-items:center; box-shadow:2px 2px 5px rgba(0,0,0,0.1);">
                <div><b>{s["brand"]}</b><br><small>{s["place"]}</small></div>
                <div style="font-weight:bold; font-size:1.2rem;">{s[key]:.2f} €</div>
            </div>
            ''', unsafe_allow_html=True)

show_fuel(t1, "e5")
show_fuel(t2, "e10")
show_fuel(t3, "diesel")

# 4. SHOPPING (Wiesmoor Favoriten)
st.write("---")
st.subheader("🛒 Wiesmoor Shopping")
item = st.text_input("Suche bei Berends, Aldi & Co:", placeholder="z.B. Kaffee...")
if item:
    st.link_button(f"🏢 Kaufhaus Berends: {item}", f"https://www.google.com/search?q=Kaufhaus+Berends+Wiesmoor+{item}", use_container_width=True)
    st.link_button(f"🔵 Aldi Nord: {item}", f"https://www.aldi-nord.de/suche.html?q={item}", use_container_width=True)
    st.link_button(f"💊 Rossmann: {item}", f"https://www.rossmann.de/de/search?text={item}", use_container_width=True)
