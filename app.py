import streamlit as st
import pandas as pd

st.set_page_config(page_title="Preis-Profi AI", page_icon="💰", layout="centered")

st.title("💰 Preis-Profi AI")
st.markdown("---")

# Suchfeld
query = st.text_input("Was möchtest du heute günstig finden?", placeholder="z.B. iPhone 15, Kaffeemaschine...")

if query:
    st.subheader(f"Ergebnisse für '{query}'")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.info("🔍 Preisvergleich")
        # Direkter Link zu Idealo
        idealo_url = f"https://www.idealo.de/preisvergleich/MainSearchProductCategory.html?q={query.replace(' ', '+')}"
        st.markdown(f"[👉 Beste Preise auf Idealo]({idealo_url})")
        
    with col2:
        st.success("🛒 Direkt-Angebote")
        # Direkter Link zu Google Shopping
        google_url = f"https://www.google.com/search?tbm=shop&q={query.replace(' ', '+')}"
        st.markdown(f"[👉 Angebote bei Google Shopping]({google_url})")

    st.markdown("---")
    st.write("💡 *Tipp: Klicke auf die Links oben, um die tagesaktuellen Bestpreise der größten Händler zu sehen.*")

# Einkaufsliste in der Seitenleiste
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
