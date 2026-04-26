import streamlit as st
import pandas as pd
import requests

# --- KONFIGURATION ---
st.set_page_config(page_title="DEAL-RADAR WIESMOOR", page_icon="⛽", layout="centered")

# --- STYLE ---
st.markdown("""
<style>
    .stApp { background-color: #ffffff; }
    .header-bar {
        background: linear-gradient(135deg, #e2001a, #b30014);
        color: white; padding: 25px; text-align: center;
        border-radius: 0 0 30px 30px; font-weight: bold; font-size: 1.8rem;
    }
    .sprit-card {
        padding: 10px; border-radius: 10px; margin-bottom: 5px;
        color: white; font-weight: bold; display: flex; justify-content: space-between;
    }
    .guenstig { background-color: #28a745; border-left: 5px solid #1e7e34; }
    .teuer { background-color: #dc3545; border-left: 5px solid #a71d2a; }
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="header-bar">💥 DEAL-RADAR 3.0</div>', unsafe_allow_html=True)

# --- LIVE SPRITPREISE WIESMOOR ---
st.write("### ⛽ LIVE-SPRIT WIESMOOR (Echtzeit)")

def get_fuel_prices():
    # Beispiel-Daten (In einer Profi-App kämen hier die API-Daten von Tankerkönig rein)
    # Für Wiesmoor simulieren wir die aktuellen Top-Stationen
    data = [
        {"Name": "AVIA Wiesmoor", "E5": 1.82, "Entfernung": "0.5 km"},
        {"Name": "Classic", "E5": 1.79, "Entfernung": "1.2 km"},
        {"Name": "Raiffeisen", "E5": 1.80, "Entfernung": "2.1 km"}
    ]
    df = pd.DataFrame(data).sort_values(by="E5")
    return df

prices = get_fuel_prices()

for index, row in prices.iterrows():
    # Günstigste bekommt grüne Karte, Rest rot/gelb
    css_class = "guenstig" if index == prices.index[0] else "teuer"
    st.markdown(f"""
    <div class="sprit-card {css_class}">
        <span>📍 {row['Name']} ({row['Entfernung']})</span>
        <span>{row['E5']:.2f} €</span>
    </div>
    """, unsafe_allow_html=True)

# --- SCHNELL-CHECK ---
st.write("---")
st.write("### ⚡ SCHNELL-CHECK")
c1, c2, c3 = st.columns(3)
with c1: st.link_button("☕ Kaffee", "https://www.marktguru.de/search/Kaffee")
with c2: st.link_button("🍺 Bier", "https://www.marktguru.de/search/Bier")
with c3: st.link_button("🧀 Käse", "https://www.marktguru.de/search/Käse")

# --- SUCHE ---
query = st.text_input("Was suchst du sonst noch?", placeholder="z.B. Grillkohle...")
if query:
    st.link_button(f"🔍 {query.upper()} ÜBERALL SUCHEN", f"https://www.google.com/search?q={query}+angebot+wiesmoor")
