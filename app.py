import streamlit as st

# --- KONFIGURATION ---
st.set_page_config(page_title="WIESMOOR RADAR", page_icon="⛽")

# --- DESIGN (Extrem stabil & auffällig) ---
st.markdown("""
<style>
    .header { background: linear-gradient(135deg, #e2001a, #b30014); color: white; padding: 25px; text-align: center; border-radius: 0 0 20px 20px; font-weight: bold; font-size: 1.6rem; margin-bottom: 15px; }
    .station-card { background: #f8f9fa; padding: 12px; border-radius: 10px; margin-bottom: 8px; border-left: 6px solid #e2001a; display: flex; justify-content: space-between; align-items: center; box-shadow: 2px 2px 5px rgba(0,0,0,0.05); }
    .best { border-left-color: #28a745; background-color: #f0fff4; }
    .price-box { background: #333; color: white; padding: 5px 10px; border-radius: 8px; font-family: monospace; font-size: 1.1rem; }
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="header">⛽ SPRIT-RADAR WIESMOOR</div>', unsafe_allow_html=True)

# --- REITER FÜR ALLE KRAFTSTOFFE ---
tab1, tab2, tab3, tab4, tab5 = st.tabs(["🟢 E5", "🟡 E10", "⚫ Diesel", "💨 LPG", "💎 CNG"])

# --- DATEN-LISTE (Marke, Ort, E5, E10, Diesel, LPG, CNG) ---
# Hier sind die wichtigsten Stationen deiner Region hinterlegt
tanks = [
    ["JET", "Aurich", 1.76, 1.70, 1.58, 0.94, None],
    ["SCORE", "Friedeburg", 1.78, 1.72, 1.60, 0.95, 1.42],
    ["CLASSIC", "Wiesmoor", 1.79, 1.73, 1.62, 1.02, None],
    ["RAIFFEISEN", "Wiesmoor", 1.80, 1.74, 1.64, 0.98, 1.45],
    ["AVIA", "Wiesmoor", 1.82, 1.76, 1.65, 1.02, None],
    ["STADTWERKE", "Aurich", None, None, None, None, 1.39],
