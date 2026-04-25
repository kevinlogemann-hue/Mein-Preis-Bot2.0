import streamlit as st
import pandas as pd

# --- KONFIGURATION ---
st.set_page_config(
    page_title="PREIS-PROFI AI 2.0",
    page_icon="⚡",
    layout="centered"
)

# --- HYPER-STYLING (Neon-Cyber-Look) ---
st.markdown("""
<style>
    /* Globaler Hintergrund mit animiertem Verlauf */
    .stApp {
        background: linear-gradient(270deg, #0f172a, #1e1b4b, #581c87);
        background-size: 600% 600%;
        animation: GradientAnimation 15s ease infinite;
        color: #00f2ff;
    }
    
    @keyframes GradientAnimation {
        0%{background-position:0% 50%}
        50%{background-position:100% 50%}
        100%{background-position:0% 50%}
    }

    /* Neon-Karten für Ergebnisse */
    .result-card {
        background: rgba(0, 0, 0, 0.6);
        padding: 25px;
        border-radius: 20px;
        border: 2px solid #ff00ff;
        box-shadow: 0 0 15px #ff00ff, inset 0 0 10px #ff00ff;
        margin-bottom: 20px;
        text-align: center;
    }

    /* Pulsierender Titel */
    h1 {
        font-family: 'Courier New', Courier, monospace;
        color: #fff;
        text-align: center;
        text-transform: uppercase;
        letter-spacing: 5px;
        text-shadow: 0 0 10px #00f2ff, 0 0 20px #00f2ff, 0 0 40px #00f2ff;
        font-size: 3.5rem !important;
    }

    /* Sidebar-Styling */
    [data-testid="stSidebar"] {
        background-color: rgba(15, 23, 42, 0.95) !important;
        border-right: 2px solid #00f2ff;
    }

    /* Input Felder */
    .stTextInput>div>div>input {
        background-color: rgba(255, 255, 255, 0.1);
        border: 1px solid #00f2ff;
        color: white !important;
        border-radius: 10px;
    }
</style>
""", unsafe_allow_html=True)

# --- SEITENLEISTE ---
with st.sidebar:
    st.image("https://img.icons8.com/clouds/200/flash-light.png", width=150)
    st.markdown("## ⚡ STEUERZENTRALE")
    plz = st.text_input("📍 DEIN STANDORT:", value="26639")
    st.markdown("---")
    
    st.header("🛒 SHOP-LISTE")
    item = st.text_input("Artikel merken:")
    if st.button("HINZUFÜGEN"):
        if 'liste' not in st.session_state: st.session_state.liste = []
        if item: st.session_state.liste.append(item)
    
    if 'liste' in st.session_state and st.session_state.liste:
        for i in st.session_state.liste:
            st.write(f"🔹 {i}")

# --- HAUPTBEREICH ---
st.write("### 🚀 DER ULTIMATIVE")
st.title("PREIS-PROFI")
st.write("---")

query = st.text_input("", placeholder="WELCHEN DEAL SUCHST DU?", help="Eingeben und sparen!")

if query:
    st.snow() # Mal was anderes als Ballons!
    st.markdown(f"## 💎 DEALS GEFUNDEN FÜR: {query.upper()}")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown(f'''<div class="result-card">
            <h3 style="color: #00f2ff;">🌐 WEB</h3>
            <p style="color: #fff;">Online Bestpreis</p>
            <a href="https://www.idealo.de/preisvergleich/MainSearchProductCategory.html?q={query.replace(' ', '+')}" target="_blank" style="color: #00f2ff; text-decoration: none; border: 1px solid #00f2ff; padding: 5px; border-radius: 5px;">IDEALO</a>
        </div>''', unsafe_allow_html=True)
        
    with col2:
        st.markdown(f'''<div class="result-card">
            <h3 style="color: #ff00ff;">🛒 SHOP</h3>
            <p style="color: #fff;">Google Check</p>
            <a href="https://www.google.com/search?tbm=shop&q={query.replace(' ', '+')}" target="_blank" style="color: #ff00ff; text-decoration: none; border: 1px solid #ff00ff; padding: 5px; border-radius: 5px;">GOOGLE</a>
        </div>''', unsafe_allow_html=True)

    with col3:
        st.markdown(f'''<div class="result-card">
            <h3 style="color: #39ff14;">🏠 LOKAL</h3>
            <p style="color: #fff;">Wiesmoor & Umzu</p>
            <a href="https://www.kaufda.de/suche/{query.replace(' ', '%20')}?zip={plz}" target="_blank" style="color: #39ff14; text-decoration: none; border:
