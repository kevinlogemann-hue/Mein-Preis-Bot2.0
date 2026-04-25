import streamlit as st
import pandas as pd

# --- KONFIGURATION & STYLING ---
st.set_page_config(
    page_title="Preis-Profi AI",
    page_icon="💰",
    layout="centered",
    initial_sidebar_state="expanded"
)

# Eigenes CSS für das Design
st.markdown("""
<style>
    .main {
        background-color: #f0f2f6;
    }
    h1 {
        color: #1E3A8A;
    }
</style>
""", unsafe_allow_html=True)

# --- SEITENLEISTE ---
with st.sidebar:
    # Logo-Platzhalter
    logo_url = "https://img.icons8.com/fluency/144/money-bag.png"
    st.image(logo_url, width=100)
    
    st.title("Preis-Profi AI")
    st.markdown("---")
    
    st.header("📍 Standort")
    plz = st.text_input("Deine PLZ:", placeholder="z.B. 26639", value="26639")
    st.markdown("---")
    
    st.header("📋 Meine Liste")
    item = st.text_input("Artikel merken:")
    if st.button("Hinzufügen"):
        if 'liste' not in st.session_state:
            st.session_state.liste = []
        if item:
            st.session_state.liste.append(item)
    
    if 'liste' in st.session_state:
        for i in st.session_state.liste:
            st.write(f"✅ {i}")
        if st.button("Liste löschen"):
            st.session_state.liste = []
            st.rerun()

# --- HAUPTBEREICH ---
col1, col2 = st.columns([1, 4])
with col1:
    st.image(logo_url, width=80)
with col2:
    st.title("💰 Preis-Profi AI")
    st.subheader(f"Günstig finden in {plz}")

st.markdown("---")

query = st.text_input("Was suchst du heute?", placeholder="z.B. Butter, Akkuschrauber...")

if query:
    st.subheader(f"Ergebnisse für '{query}'")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.info("🌐 Online")
        idealo_url = f"https://www.idealo.de/preisvergleich/MainSearchProductCategory.html?q={query.replace(' ', '+')}"
        st.markdown(f"[Idealo Check]({idealo_url})")
        
    with col2:
        st.success("🛒 Shopping")
        google_url = f"https://www.google.com/search?tbm=shop&q={query.replace(' ', '+')}"
        st.markdown(f"[Google Preis]({google_url})")

    with col3:
        st.warning("🏠 Lokal")
        kaufda_url = f"https://www.kaufda.de/suche/{query.replace(' ', '%20')}?zip={plz}"
        st.markdown(f"[Prospekte in {plz}]({kaufda_url})")

    st.markdown("---")
    st.write(f"📍 **Geschäfte mit '{query}' nahe {plz}:**")
    maps_url = f"https://www.google.com/maps/search/{query.replace(' ', '+')}+{plz}"
    st.markdown(f"[Auf Google Maps öffnen]({maps_url})")
