import streamlit as st
import pandas as pd

# --- KONFIGURATION ---
st.set_page_config(
    page_title="Preis-Profi AI",
    page_icon="💰",
    layout="centered"
)

# --- STYLING (Der "Memory"-Effekt) ---
st.markdown("""
<style>
    /* Hintergrund und Schrift */
    .main {
        background: linear-gradient(135deg, #1e3a8a 0%, #1e1b4b 100%);
        color: white;
    }
    
    /* Karten-Design für die Ergebnisse */
    .result-card {
        background-color: rgba(255, 255, 255, 0.1);
        padding: 20px;
        border-radius: 15px;
        border: 1px solid rgba(255, 255, 255, 0.2);
        margin-bottom: 10px;
        transition: transform 0.3s;
    }
    
    /* Titel-Styling */
    h1 {
        font-family: 'Trebuchet MS', sans-serif;
        text-shadow: 2px 2px 4px #000000;
        background: -webkit-linear-gradient(#fcd34d, #fbbf24);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-size: 3rem !important;
    }

    /* Buttons schöner machen */
    .stButton>button {
        border-radius: 20px;
        background-color: #fbbf24;
        color: #1e3a8a;
        font-weight: bold;
        border: none;
    }
</style>
""", unsafe_allow_html=True)

# --- SEITENLEISTE ---
with st.sidebar:
    st.image("https://img.icons8.com/fluency/144/money-box.png", width=120)
    st.title("Dein Spar-Assistent")
    plz = st.text_input("📍 Standort (PLZ):", value="26639")
    st.markdown("---")
    
    st.header("📋 Merkzettel")
    item = st.text_input("Was fehlt noch?")
    if st.button("Auf die Liste"):
        if 'liste' not in st.session_state: st.session_state.liste = []
        if item: st.session_state.liste.append(item)
    
    if 'liste' in st.session_state and st.session_state.liste:
        for i in st.session_state.liste:
            st.write(f"✅ {i}")
        if st.button("Liste leeren"):
            st.session_state.liste = []
            st.rerun()

# --- HAUPTBEREICH ---
st.title("Preis-Profi AI")
st.markdown("### *Schluss mit teuer. Finden statt suchen!*")

query = st.text_input("", placeholder="Suche eingeben, z.B. Kaffee oder iPhone...", help="Tippe hier, um bares Geld zu sparen!")

if query:
    st.balloons() # Ein kleiner Effekt zur Feier der Suche!
    
    st.markdown(f"### 🔥 Top-Deals für '{query}'")
    
    # Kachel-Layout
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown(f'''<div class="result-card">
            <h4>🌐 Online</h4>
            <p>Bester Netz-Preis</p>
            <a href="https://www.idealo.de/preisvergleich/MainSearchProductCategory.html?q={query.replace(' ', '+')}" target="_blank" style="color: #fbbf24; text-decoration: none; font-weight: bold;">→ Idealo Check</a>
        </div>''', unsafe_allow_html=True)
        
    with col2:
        st.markdown(f'''<div class="result-card">
            <h4>🛒 Shopping</h4>
            <p>Direkt-Angebote</p>
            <a href="https://www.google.com/search?tbm=shop&q={query.replace(' ', '+')}" target="_blank" style="color: #fbbf24; text-decoration: none; font-weight: bold;">→ Google Preise</a>
        </div>''', unsafe_allow_html=True)

    with col3:
        st.markdown(f'''<div class="result-card">
            <h4>🏠 Lokal</h4>
            <p>In {plz} & Umgebung</p>
            <a href="https://www.kaufda.de/suche/{query.replace(' ', '%20')}?zip={plz}" target="_blank" style="color: #fbbf24; text-decoration: none; font-weight: bold;">→ Prospekte</a>
        </div>''', unsafe_allow_html=True)

    st.markdown("---")
    st.markdown(f"📍 [**Hier klicken, um alle Läden in der Nähe auf der Karte zu sehen**](https://www.google.com/maps/search/{query.replace(' ', '+')}+{plz})")

else:
    st.info("💡 **Pro-Tipp:** Nutze die lokale Suche für Lebensmittel und die Online-Suche für Technik!")
