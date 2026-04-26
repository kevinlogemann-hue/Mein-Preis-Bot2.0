import streamlit as st
from datetime import datetime

# --- 1. ICON & TITEL FÜR DEN HOME-SCREEN ---
st.set_page_config(
    page_title="Wiesmoor Radar", 
    page_icon="⛽", 
    layout="centered"
)

# --- 2. DESIGN (Optimiert für Handy) ---
st.markdown("""
<style>
    .main-header { 
        background: linear-gradient(135deg, #e2001a, #b30014); 
        color: white; padding: 20px; 
        text-align: center; border-radius: 15px; 
        font-weight: bold; margin-bottom: 20px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    .card { 
        background: white; padding: 15px; 
        border-radius: 12px; margin-top: 10px; 
        border-left: 6px solid #e2001a; 
        display: flex; justify-content: space-between; align-items: center;
        box-shadow: 2px 2px 10px rgba(0,0,0,0.05);
    }
    .best-card { border-left-color: #28a745; background-color: #f0fff4; }
    .open-tag { color: #28a745; font-size: 0.8rem; font-weight: bold; }
    .price-text { font-weight: 900; color: #333; font-size: 1.2rem; }
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="main-header">⛽ WIESMOOR RADAR 2.0</div>', unsafe_allow_html=True)

# --- 3. LIVE STATUS CHECK ---
hour = datetime.now().hour
status = '<span class="open-tag">● JETZT GEÖFFNET</span>' if 6 <= hour < 21 else '<span style="color:red">○ GESCHLOSSEN</span>'

# --- 4. TANKSTELLEN ABSCHNITT ---
fuel_tab = st.tabs(["Super E5", "Super E10", "Diesel", "LPG/CNG"])

# Aktuelle Preis-Daten (Demo bis Key da ist)
prices = {
    "E5": [["JET", "Aurich", "1.76"], ["SCORE", "Friedeburg", "1.78"], ["CLASSIC", "Wiesmoor", "1.79"]],
    "E10": [["JET", "Aurich", "1.70"], ["SCORE", "Friedeburg", "1.72"], ["AVIA", "Wiesmoor", "1.76"]],
    "Diesel": [["JET", "Aurich", "1.58"], ["SCORE", "Friedeburg", "1.60"], ["RAIFFEISEN", "Wiesmoor", "1.64"]],
    "Gas": [["STADTWERKE", "Aurich (CNG)", "1.39"], ["RAIFFEISEN", "Wiesmoor (LPG)", "0.98"]]
}

def show_fuel(type_key):
    for i, s in enumerate(prices[type_key]):
        is_best = "best-card" if i == 0 else ""
        st.markdown(f'<div class="card {is_best}"><div><b>{s[0]}</b><br><small>{s[1]}</small><br>{status}</div><div class="price-text">{s[2]} €</div></div>', unsafe_allow_html=True)

with fuel_tab[0]: show_fuel("E5")
with fuel_tab[1]: show_fuel("E10")
with fuel_tab[2]: show_fuel("Diesel")
with fuel_tab[3]: show_fuel("Gas")

# --- 5. SHOPPING ABSCHNITT (Wiesmoor Favoriten) ---
st.write("---")
st.subheader("🛒 Wiesmoor Shopping-Check")
item = st.text_input("Was suchst du?", placeholder="z.B. Kaffee, Hemden, Werkzeug...")

if item:
    # Untereinander gestapelte Buttons für bessere Handy-Bedienung
    st.link_button(f"🏢 Kaufhaus Berends: {item}", f"https://www.google.com/search?q=Kaufhaus+Berends+Wiesmoor+{item}", use_container_width=True)
    st.link_button(f"🔵 Aldi Nord: {item}", f"https://www.aldi-nord.de/suche.html?q={item}", use_container_width=True)
    st.link_button(f"💊 Rossmann: {item}", f"https://www.rossmann.de/de/search?text={item}", use_container_width=True)
    st.link_button(f"🧣 KiK Textilien: {item}", f"https://www.kik.de/s?q={item}", use_container_width=True)
    st.link_button(f"🍎 Marktguru Deals", f"https://www.marktguru.de/search/{item}", use_container_width=True)

st.info("💡 Speichere diese Seite über 'Zum Home-Bildschirm hinzufügen' für das echte App-Gefühl!")
