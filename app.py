import streamlit as st
import pandas as pd

# --- KONFIGURATION ---
st.set_page_config(page_title="WIESMOOR TANK-RADAR", page_icon="⛽", layout="centered")

# --- HIGH-ATTENTION CSS ---
st.markdown("""
<style>
    .stApp { background-color: #f9f9f9; }
    .header-bar {
        background: linear-gradient(135deg, #e2001a, #b30014);
        color: white; padding: 20px; text-align: center;
        border-radius: 0 0 30px 30px; font-weight: bold; font-size: 1.5rem;
    }
    .tank-card {
        padding: 15px; border-radius: 15px; margin-bottom: 12px;
        color: white; font-weight: bold; display: flex; 
        justify-content: space-between; align-items: center;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
    }
    .best-price { background: linear-gradient(90deg, #28a745, #2ecc71); border-left: 8px solid #1e7e34; }
    .normal-price { background: linear-gradient(90deg, #e2001a, #ff4b4b); border-left: 8px solid #a71d2a; }
    .price-tag { font-size: 1.4rem; background: rgba(0,0,0,0.25); padding: 5px 12px; border-radius: 10px; min-width: 80px; text-align: center; }
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="header-bar">⛽ SPRIT-RADAR WIESMOOR</div>', unsafe_allow_html=True)

# --- TANKSTELLEN DATEN ---
tanks = [
    {"Name": "CLASSIC", "Ort": "Wiesmoor", "E5": 1.79, "E10": 1.73, "Diesel": 1.62},
    {"Name": "AVIA", "Ort": "Wiesmoor", "E5": 1.82, "E10": 1.76, "Diesel": 1.65},
    {"Name": "RAIFFEISEN", "Ort": "Wiesmoor", "E5": 1.80, "E10": 1.74, "Diesel": 1.64},
    {"Name": "SCORE", "Ort": "Friedeburg", "E5": 1.78, "E10": 1.72, "Diesel": 1.60},
    {"Name": "ARAL", "Ort": "Uplengen", "E5": 1.85, "E10": 1.79, "Diesel": 1.69},
    {"Name": "SHELL", "Ort": "Remels", "E5": 1.87, "E10": 1.81, "Diesel": 1.71},
    {"Name": "JET", "Ort": "Aurich", "E5": 1.77, "E10": 1.71, "Diesel": 1.59},
]

df = pd.DataFrame(tanks)

# --- REITER FÜR KRAFTSTOFFARTEN ---
tab1, tab2, tab3 = st.tabs(["🟢 Super E5", "🟡 Super E10", "⚫ Diesel"])

def show_gas_stations(fuel):
    # Nach Preis sortieren
    sorted_df = df.sort_values(by=fuel)
    best_id = sorted_df.index[0]
    
    for i, row in sorted_df.iterrows():
        is_best = (i == best_id)
        card_class = "best-price" if is_best else "normal-price"
        
        st.markdown(f"""
        <div class="tank-card {card_class}">
            <div>
                <span style="font-size:1
