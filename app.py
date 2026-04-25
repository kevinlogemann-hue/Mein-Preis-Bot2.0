import streamlit as st
import pandas as pd

st.set_page_config(page_title="Preis-Profi AI", page_icon="💰", layout="centered")

st.title("💰 Preis-Profi AI")
st.markdown("---")

# Suchfeld
query = st.text_input("Was suchst du heute?", placeholder="z.B. Butter, Akkuschrauber, Fernseher...")

if query:
    st.subheader(f"Ergebnisse für '{query}'")
    
    # Drei Spalten für verschiedene Such-Typen
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.info("🌐 Online")
        idealo_url = f"https://www.idealo.de/preisvergleich/MainSearchProductCategory.html?q={query.replace(' ', '+')}"
        st.markdown(f"[Idealo Preischeck]({idealo_url})")
        
    with col2:
        st.success("🛒 Shopping")
        google_url = f"https://www.google.com/search?tbm=shop&q={query.replace(' ', '+')}"
        st.markdown(f"[Google Angebote]({google_url})")

    with col3:
        st.warning("🏠 Lokal")
        # Suche in Prospekten (Kaufda)
        kaufda_url = f"https://www.kaufda.de/suche/{query.replace(' ', '%20')}"
        st.markdown(f"[Prospekt-Check]({kaufda_url})")

    st.markdown("---")
    
    # Interaktive Karte für Läden in der Nähe
    st.write("📍 **Läden in deiner Umgebung:**")
    maps_url = f"https://www.google.com/maps/search/{query.replace(' ', '+')}+in+der+Nähe"
    st.markdown(f"[Auf Google Maps anzeigen]({maps_url})")

# Einkaufsliste bleibt erhalten
with st.sidebar:
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
