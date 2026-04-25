import streamlit as st
import pandas as pd

st.set_page_config(page_title="LokalFinder AI", page_icon="🛒")

st.title("🛒 LokalFinder AI")
st.subheader("Dein smarter Preisvergleich")

# Suchfeld
query = st.text_input("Was suchst du?", placeholder="z.B. Milch, Bohrmaschine...")

if query:
    st.write(f"### Angebote für '{query}' in der Nähe:")
    # Platzhalter für echte Daten
    data = {
        "Laden": ["Baumarkt Hornbach", "Lidl Express", "Edeka"],
        "Preis": ["89.99 €", "1.29 €", "1.49 €"],
        "Status": ["Geöffnet", "Schließt um 20h", "Geöffnet"]
    }
    st.table(pd.DataFrame(data))
    st.markdown(f"[📍 Route in Google Maps öffnen](https://www.google.com/maps/search/{query.replace(' ', '+')})")

# Einkaufsliste
with st.sidebar:
    st.header("Einkaufsliste")
    item = st.text_input("Hinzufügen:")
    if st.button("Speichern"):
        if 'liste' not in st.session_state:
            st.session_state.liste = []
        if item:
            st.session_state.liste.append(item)
    
    if 'liste' in st.session_state:
        for i in st.session_state.liste:
            st.write(f"- {i}")
