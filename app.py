import streamlit as st
from datetime import datetime

# --- KONFIGURATION ---
st.set_page_config(page_title="WIESMOOR RADAR 2.0", page_icon="⛽")

# --- DESIGN ---
st.markdown("""
<style>
    .header { background: #e2001a; color: white; padding: 20px; text-align: center; border-radius: 15px; font-weight: bold; }
    .card { background: #f0f2f6; padding: 12px; border-radius: 10px; margin-top: 10px; border-left: 5px solid #e2001a; display: flex; justify-content: space-between; align-items: center; }
    .open { color: #28a745; font-size: 0.8rem; font-weight: bold; }
    .closed { color: #dc3545; font-size: 0.8rem; font-weight: bold; }
    .price { font-weight: bold; color: #333; font-size: 1.1rem; }
    .best-card { border-left-color: #28a745; background-color: #e8f5e9; }
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="header">⛽ SPRIT- & GAS-RADAR WIESMOOR</div>', unsafe_allow_html=True)

# --- HILFSFUNKTION FÜR ÖFFNUNGSZEITEN ---
def get_status_icon():
    hour = datetime.now().hour
    # Einfache Logik: Die meisten Stationen haben von 06:00 bis 22:00 Uhr offen
    if 6 <= hour < 22:
        return '<span class="open">● GEÖFFNET</span>'
    else:
        return '<span class="closed">○ GESCHLOSSEN</span>'

status = get_status_icon()

# --- REITER FÜR KRAFTSTOFFE ---
tabs = st.tabs(["Super E5", "Super E10", "Diesel", "LPG", "CNG"])

# Daten (Marke, Ort, Preis, Einheit)
data_e5 = [["JET", "Aurich", "1.76"], ["SCORE", "Friedeburg", "1.78"], ["CLASSIC", "Wiesmoor", "1.79"]]
data_e10 = [["JET", "Aurich", "1.70"], ["SCORE", "Friedeburg", "1.72"], ["AVIA", "Wiesmoor", "1.76"]]
data_diesel = [["JET", "Aurich", "1.58"], ["SCORE", "Friedeburg", "1.60"], ["RAIFFEISEN", "Wiesmoor", "1.64"]]
data_lpg = [["RAIFFEISEN", "Wiesmoor", "0.98"], ["CLASSIC", "Wiesmoor", "1.02"], ["ARAL", "Uplengen", "1.04"]]
data_cng = [["STADTWERKE", "Aurich", "1.39", "kg"], ["SCORE", "Friedeburg", "1.42", "kg"]]

def render_list(data_list, unit="€"):
    for i, item in enumerate(data_list):
        is_best = "best-card" if i == 0 else ""
        ext_unit = item[3] if len(item) > 3 else unit
        st.markdown(f"""
        <div class="card {is_best}">
            <div>
                <b>{item[0]}</b> ({item[1]})<br>
                {status}
            </div>
            <div class="price">{item[2]} {ext_unit}</div>
        </div>
        """, unsafe_allow_html=True)

with tabs[0]: render_list(data_e5)
with tabs[1]: render_list(data_e10)
with tabs[2]: render_list(data_diesel)
with tabs[3]: render_list(data_lpg)
with tabs[4]: render_list(data_cng)

# --- PRODUKTSUCHE ---
st.write("---")
st.subheader("🛒 Schnäppchen-Suche")
q = st.text_input("Was suchst du gerade?", placeholder="z.B. Kaffee, Bier, Grillkohle...")
if q:
    col1, col2 = st.columns(2)
    with col1:
        st.link_button(f"Lidl Angebote: {q}", f"https://www.lidl.de/q/search?q={q}")
    with col2:
        st.link_button(f"Marktguru: {q}", f"https://www.marktguru.de/search/{q}")
