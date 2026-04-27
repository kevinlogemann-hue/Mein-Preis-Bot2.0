import streamlit as st
import requests

# 1. SETUP & KEY
st.set_page_config(page_title="Wiesmoor Radar", page_icon="⛽")
API_KEY = "616cbb8e-9dde-4eb7-91f1-21a1663fa495"

# 2. DESIGN
st.markdown('<style>.main-header { background: #e2001a; color: white; padding: 20px; text-align: center; border-radius: 15px; font-weight: bold; margin-bottom: 20px; } .card { background: white; padding: 15px; border-radius: 12px; margin-top: 10px; border-left: 6px solid #e2001a; display: flex; justify-content: space-between; align-items: center; box-shadow: 2px 2px 10px rgba(0,0,0,0.05); } .best { border-left-color: #28a745; background-color: #f0fff4; }</style>', unsafe_allow_html=True)

st.markdown('<div class="main-header">⛽ WIESMOOR LIVE-RADAR</div>', unsafe_allow_html=True)

# 3. DATEN LADEN
url = f"https://creativecommons.tankerkoenig.de/json/list.php?lat=53.414&lng=7.733&rad=10&sort=dist&type=all&apikey={API_KEY}"

try:
    r = requests.get(url).json()
    if r["ok"]:
        stanz = r["stations"]
        
        t1, t2, t3 = st.tabs(["Super E5", "Super E10", "Diesel"])
        
        # SUPER E5
        with t1:
            liste = sorted([s for s in stanz if s["e5"] > 0], key=lambda x: x["e5"])
            for i, s in enumerate(liste):
                top = "best" if i == 0 else ""
                st.markdown(f'<div class="card {top}"><div><b>{s["brand"]}</b><br><small>{s["place"]}</small></div><div style="font-weight:bold">{s["e5"]:.2f} €</div></div>', unsafe_allow_html=True)

        # SUPER E10
        with t2:
            liste = sorted([s for s in stanz if s["e10"] > 0], key=lambda x: x["e10"])
            for i, s in enumerate(liste):
                top = "best" if i == 0 else ""
                st.markdown(f'<div class="card {top}"><div><b>{s["brand"]}</b><br><small>{s["place"]}</small></div><div style="font-weight:bold">{s["e10"]:.2f} €</div></div>', unsafe_allow_html=True)

        # DIESEL
        with t3:
            liste = sorted([s for s in stanz if s["diesel"] > 0], key=lambda x: x["diesel"])
            for i, s in enumerate(liste):
                top = "best" if i == 0 else ""
                st.markdown(f'<div class="card {top}"><div><b>{s["brand"]}</b><br><small>{s["place"]}</small></div><div style="font-weight:bold">{s["diesel"]:.2f} €</div></div>', unsafe_allow_html=True)
except:
    st.error("Fehler beim Laden der Preise.")

# 4. SHOPPING
st.write("---")
item = st.text_input("Suche (Berends, Aldi, Rossmann):")
if item:
    st.link_button(f"🏢 Kaufhaus Berends: {item}", f"https://www.google.com/search?q=Kaufhaus+Berends+Wiesmoor+{item}")
    st.link_button(f"🔵 Aldi Nord: {item}", f"https://www.aldi-nord.de/suche.html?q={item}")
    st.link_button(f"💊 Rossmann: {item}", f"https://www.rossmann.de/de/search?text={item}")
