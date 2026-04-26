import streamlit as st
import pandas as pd

# --- KONFIGURATION ---
st.set_page_config(page_title="WIESMOOR SPRIT-CHECK", page_icon="⛽")

# --- STYLE ---
st.markdown("""
<style>
    .stApp { background-color: #ffffff; }
    .header-bar {
        background: linear-gradient(135deg, #e2001a, #b30014);
        color: white; padding: 20px; text-align: center;
        border-radius: 0 0 30px 30px; font-weight: bold; font-size: 1.8rem;
    }
    .tank-card {
        padding: 15px; border-radius: 12px; margin-bottom: 10px;
        color: white; font-weight: bold; display: flex; 
        justify-content: space-between; align-items: center;
        box-shadow: 2px 2px 10px rgba(0,0,0,0.1);
    }
    .brand-label { font-size: 1.1rem; }
    .price-label { font-size: 1.3rem; background: rgba(0,0,0,0.2); padding: 5px 10px; border-radius: 8px; }
    .best { background-color: #28a745; border: 2px solid #1e7e34; }
    .normal { background-color: #e2001a; }
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="header-bar">⛽ SPRIT-RADAR WIESMOOR</div>', unsafe_allow_html=True)

# --- DATEN-SIMULATION (Wiesmoor & Umzu) ---
# Hier sind alle gängigen Marken der Region drin
tanks_data = [
    {"Marke": "CLASSIC", "Ort": "Wiesmoor", "E5": 1.79, "E10": 1.73, "Diesel": 1.62},
    {"Marke": "AVIA", "Ort": "Wiesmoor", "E5": 1.82, "E10": 1.76, "Diesel": 1.65},
    {"Marke": "RAIFFEISEN", "Ort": "Wiesmoor", "E5": 1.80, "E10": 1.74, "Diesel": 1.64},
    {"Marke": "SCORE", "Ort": "Friedeburg", "E5": 1.78, "E10": 1.72, "Diesel": 1.60},
    {"Marke": "ARAL", "Ort": "Uplengen", "E5": 1.85, "E10": 1.79, "Diesel": 1.69},
    {"Marke": "SHELL", "Ort": "Remels", "E5": 1.87, "E10": 1.81, "Diesel": 1.71},
]

df = pd.DataFrame(tanks_data)

# --- TABS FÜR KRAFTSTOFFE ---
tab1, tab2, tab3 = st.tabs(["🟢 E5", "🟡 E10", "⚫ Diesel"])

def draw_cards(fuel_type):
    sorted_df = df.sort_values(by=fuel_type)
    for i, row in sorted_df.iterrows():
        is_best = i == sorted_df.index[0]
        style_class = "best" if is_best else "normal"
        st.markdown(f"""
        <div class="tank-card {style_class}">
            <div class="brand-label">
                {row['Marke']} <br>
                <small style="font-weight:normal; opacity:0.8;">{row['Ort']}</small>
            </div>
            <div class="price-label">{row[fuel_type]:.2f} €</div>
        </div>
        """, unsafe_allow_html=True)

with tab1:
    st.write("### Aktuelle Preise für Super E5")
    draw_cards("E5")

with tab2:
    st.write("### Aktuelle Preise für Super E10")
    draw_cards("E10")

with tab3:
    st.write("### Aktuelle Preise für Diesel")
    draw_cards("Diesel")

# --- FOOTER ---
st.markdown("---")
st.caption("📍 Preise werden automatisch sortiert. Die günstigste Tankstelle ist grün markiert.")
