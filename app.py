import streamlit as st

# --- SETUP ---
st.set_page_config(page_title="WIESMOOR RADAR", page_icon="⛽")

# --- HIER KOMMT DEIN KEY REIN, WENN ER DA IST ---
# Sobald du die Mail hast, lösche die Nullen und füge deinen Key ein!
MY_API_KEY = "00000000-0000-0000-0000-000000000000" 

# --- DESIGN ---
st.markdown("""
<style>
    .header { background: #e2001a; color: white; padding: 20px; text-align: center; border-radius: 15px; font-weight: bold; }
    .card { background: #f0f2f6; padding: 12px; border-radius: 10px; margin-top: 10px; border-left: 5px solid #e2001a; display: flex; justify-content: space-between; }
    .best { border-left-color: #28a745; background-color: #e8f5e9; }
    .price { font-weight: bold; color: #1e7e34; }
    .status-box { background: #fff3cd; color: #856404; padding: 10px; border-radius: 10px; text-align: center; margin-bottom: 15px; font-size: 0.9rem; border: 1px solid #ffeeba; }
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="header">⛽ LIVE-RADAR WIESMOOR</div>', unsafe_allow_html=True)

# Status-Meldung für die Wartezeit
if MY_API_KEY == "00000000-0000-0000-0000-000000000000":
    st.markdown('<div class="status-box">⏳ Warte auf API-Key... Aktuell werden Demo-Daten angezeigt.</div>', unsafe_allow_html=True)

# Kraftstoff-Auswahl
tab1, tab2, tab3 = st.tabs(["Super E5", "Super E10", "Diesel"])

def show_data(fuel_name, demo_price_best, demo_price_other):
    # Hier wird später die echte Abfrage stehen. 
    # Jetzt zeigen wir schicke Platzhalter:
    st.markdown(f'<div class="card best">JET (Aurich) <span class="price">{demo_price_best} €</span></div>', unsafe_allow_html=True)
    st.markdown(f'<div class="card">SCORE (Friedeburg) <span class="price">{demo_price_other} €</span></div>', unsafe_allow_html=True)
    st.markdown(f'<div class="card">CLASSIC (Wiesmoor) <span class="price">{demo_price_other + 0.01:.2f} €</span></div>', unsafe_allow_html=True)

with tab1: show_data("E5", 1.76, 1.78)
with tab2: show_data("E10", 1.70, 1.72)
with tab3: show_data("Diesel", 1.58, 1.60)

# --- DIE SUCHE BLEIBT AKTIV ---
st.write("---")
query = st.text_input("🔍 Welches Angebot suchst du heute?")
if query:
    st.link_button(f"👉 Deals für {query} prüfen", f"https://www.marktguru.de/search/{query}")
