import streamlit as st
import pd as pd

# --- KONFIGURATION ---
st.set_page_config(page_title="WIESMOOR GAS-RADAR", page_icon="💨", layout="centered")

# --- DESIGN ---
st.markdown("""
<style>
    .stApp { background-color: #ffffff; }
    .header-bar {
        background: #0050aa; /* Blau für Gas-Thema */
        color: white; padding: 20px; text-align: center;
        border-radius: 0 0 20px 20px; font-weight: bold; font-size: 1.5rem;
        margin-bottom: 20px;
    }
    .gas-card {
        background-color: #f8f9fa; color: #333;
        padding: 15px; border-radius: 12px;
        display: flex; justify-content: space-between; align-items: center;
        margin-bottom: 10px; border-left: 8px solid #0050aa;
        box-shadow: 0 2px 5px rgba(0,0,0,0.1);
    }
    .best-price { border-left-color: #28a745; background-color: #e8f5e9; }
    .price-val { font-size: 1.3rem; font-weight: bold; color: #0050aa; }
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="header-bar">💨 CNG & LPG RADAR WIESMOOR</div>', unsafe_allow_html=True)

# --- GAS-TANKSTELLEN DATEN (Beispiele Region Wiesmoor/Aurich) ---
# Preise pro kg (CNG) oder pro Liter (LPG)
gas_data = [
    {"Name": "Raiffeisen", "Ort": "Wiesmoor", "LPG": 0.98, "CNG": 1.45},
    {"Name": "AVIA", "Ort": "Wiesmoor", "LPG": 1.02, "CNG": None},
    {"Name": "Stadtwerke", "Ort": "Aurich", "LPG": None, "CNG": 1.39},
    {"Name": "Score", "Ort": "Emden", "LPG": 0.95, "CNG": 1.42},
    {"Name": "Shell", "Ort": "Oldenburg", "LPG": 1.05, "CNG": 1.55}
]

import pandas as pd
df = pd.DataFrame(gas_data)

# --- TABS FÜR GAS-ARTEN ---
tab1, tab2 = st.tabs(["💎 CNG (Erdgas)", "⛽ LPG (Autogas)"])

def show_gas(typ):
    # Nur Tankstellen anzeigen, die diesen Kraftstoff führen
    filtered = df[df[typ].notnull()].sort_values(by=typ)
    
    if filtered.empty:
        st.warning(f"Keine aktuellen Daten für {typ} in der direkten Umgebung.")
        return

    for i, row in filtered.iterrows():
        is_first = (i == filtered.index[0])
        extra_style = "best-price" if is_first else ""
        einheit = "kg" if typ == "CNG" else "l"
        
        st.markdown(f"""
        <div class="gas-card {extra_style}">
            <div>
                <b style="font-size:1.1rem;">{row['Name']}</b><br>
                <small>{row['Ort']}</small>
            </div>
            <div class="price-val">{row[typ]:.2f} €/{einheit}</div>
        </div>
        """, unsafe_allow_html=True)

with tab1:
    st.write("### Aktuelle CNG-Preise (pro kg)")
    show_gas("CNG")

with tab2:
    st.write("### Aktuelle LPG-Preise (pro Liter)")
    show_gas("LPG")

# --- SUCHE ---
st.write("---")
query = st.text_input("Günstiges Zubehör suchen?", placeholder="z.B. Adapter, Öl...")
if query:
    st.link_button(f"🔍 {query} Preisvergleich", f"https://www.idealo.de/preisvergleich/MainSearchProductCategory.html?q={query}")
