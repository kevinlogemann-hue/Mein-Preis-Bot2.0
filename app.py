import streamlit as st
from datetime import datetime

# --- SETUP ---
st.set_page_config(page_title="WIESMOOR RADAR 2.0", page_icon="⛽")

# --- DESIGN ---
st.markdown("""
<style>
    .header { background: #e2001a; color: white; padding: 20px; text-align: center; border-radius: 15px; font-weight: bold; }
    .card { background: #f0f2f6; padding: 12px; border-radius: 10px; margin-top: 10px; border-left: 5px solid #e2001a; display: flex; justify-content: space-between; align-items: center; }
    .open { color: #28a745; font-size: 0.8rem; font-weight: bold; }
    .price { font-weight: bold; color: #333; font-size: 1.1rem; }
    .best-card { border-left-color: #28a745; background-color: #e8f5e9; }
    .shop-btn { margin-bottom: 10px; }
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="header">⛽ SPRIT- & SHOP-RADAR WIESMOOR</div>', unsafe_allow_html=True)

# --- TANKSTELLEN-STATUS ---
# Wir nutzen die Logik aus deinem funktionierenden Stand
hour = datetime.now().hour
status = '<span class="open">● GEÖFFNET</span>' if 6 <= hour < 22 else '<span class="closed">○ GESCHLOSSEN</span>'

tabs = st.tabs(["Super E5", "Super E10", "Diesel", "LPG", "CNG"])

# Daten (Marke, Ort, Preis)
tanks_data = {
    "E5": [["JET", "Aurich", "1.76"], ["SCORE", "Friedeburg", "1.78"], ["CLASSIC", "Wiesmoor", "1.79"]],
    "E10": [["JET", "Aurich", "1.70"], ["SCORE", "Friedeburg", "1.72"], ["AVIA", "Wiesmoor", "1.76"]],
    "Diesel": [["JET", "Aurich", "1.58"], ["SCORE", "Friedeburg", "1.60"], ["RAIFFEISEN", "Wiesmoor", "1.64"]],
    "LPG": [["RAIFFEISEN", "Wiesmoor", "0.98"], ["CLASSIC", "Wiesmoor", "1.02"]],
    "CNG": [["STADTWERKE", "Aurich", "1.39", "kg"], ["SCORE", "Friedeburg", "1.42", "kg"]]
}

def render_fuel(key):
    for i, item in enumerate(tanks_data[key]):
        is_best = "best-card" if i == 0 else ""
        unit = item[3] if len(item) > 3 else "€"
        st.markdown(f'<div class="card {is_best}"><div><b>{item[0]}</b> ({item[1]})<br>{status}</div><div class="price">{item[2]} {unit}</div></div>', unsafe_allow_html=True)

with tabs[0]: render_fuel("E5")
with tabs[1]: render_fuel("E10")
with tabs[2]: render_fuel("Diesel")
with tabs[3]: render_fuel("LPG")
with tabs[4]: render_fuel("CNG")

# --- ERWEITERTE SHOP-SUCHE ---
st.write("---")
st.subheader("🛒 Wiesmoor Shopping-Check")
query = st.text_input("Was suchst du? (z.B. Hemden, Deko, Werkzeug)", placeholder="Suchbegriff eingeben...")

if query:
    st.write(f"Suche nach **'{query}'** in:")
    
    # Reihe 1: Die Klassiker
    c1, c2, c3 = st.columns(3)
    with c1: st.link_button("🏢 Berends", f"https://www.google.com/search?q=Kaufhaus+Berends+Wiesmoor+{query}")
    with c2: st.link_button("🔵 Aldi", f"https://www.aldi-nord.de/suche.html?q={query}")
    with c3: st.link_button("💊 Rossmann", f"https://www.rossmann.de/de/search?text={query}")
    
    # Reihe 2: Kleidung & Deals
    c4, c5, c6 = st.columns(3)
    with c4: st.link_button("🧣 KiK", f"https://www.kik.de/s?q={query}")
    with c5: st.link_button("🍎 Marktguru", f"https://www.marktguru.de/search/{query}")
    with c6: st.link_button("🛍️ Prospekte", f"https://www.kaufda.de/Wiesmoor#query={query}")

st.info("💡 Tipp: Bei Berends lohnt sich oft auch der Blick ins Schaufenster direkt am Marktplatz!")
