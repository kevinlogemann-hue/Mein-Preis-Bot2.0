import streamlit as st
import random

# --- KONFIGURATION (Lidl Farben) ---
st.set_page_config(
    page_title="DEIN PREIS-PLUS",
    page_icon="💙",
    layout="centered"
)

# --- LIDL-STYLE CSS ---
st.markdown("""
<style>
    /* Hintergrund in hellem Lidl-Grau/Blau */
    .stApp {
        background-color: #f0f4f8;
        color: #0050aa;
    }
    
    /* Die typische Lidl-Blaue Kopfzeile */
    h1 {
        background-color: #0050aa;
        color: #fff !important;
        padding: 20px;
        border-radius: 0 0 20px 20px;
        text-align: center;
        font-family: 'Arial Black', sans-serif;
        box-shadow: 0 4px 10px rgba(0,0,0,0.1);
    }

    /* Coupon-Karten-Design */
    .coupon-card {
        background-color: white;
        border-left: 10px solid #e2001a; /* Lidl Rot */
        padding: 15px;
        border-radius: 10px;
        box-shadow: 2px 2px 10px rgba(0,0,0,0.05);
        margin-bottom: 15px;
    }
    
    .coupon-title {
        color: #e2001a;
        font-weight: bold;
        font-size: 1.2rem;
    }

    /* Sidebar-Styling */
    [data-testid="stSidebar"] {
        background-color: #0050aa !important;
    }
    [data-testid="stSidebar"] * {
        color: white !important;
    }
    
    /* Gelber Lidl-Button */
    .stButton>button {
        background-color: #fff000 !important;
        color: #0050aa !important;
        border-radius: 25px;
        border: none;
        font-weight: bold;
        width: 100%;
    }
</style>
""", unsafe_allow_html=True)

# --- SEITENLEISTE (Profil & Karte) ---
with st.sidebar:
    st.markdown("## 👤 MEIN PROFIL")
    st.write("Hallo, Spar-Profi!")
    st.markdown("---")
    
    # Simulierte digitale Kundenkarte
    st.markdown("""
    <div style="background: white; padding: 10px; border-radius: 10px; text-align: center;">
        <img src="https://api.qrserver.com/v1/create-qr-code/?size=150x150&data=PREIS-PROFI-MEMBER" width="120">
        <p style="color: #0050aa; font-weight: bold;">MEIN SCAN-CODE</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    plz = st.text_input("📍 MEIN MARKT (PLZ):", value="26639")
    
    st.header("📋 EINKAUFSLISTE")
    item = st.text_input("Artikel hinzufügen:")
    if st.button("SPEICHERN"):
        if 'liste' not in st.session_state: st.session_state.liste = []
        if item: st.session_state.liste.append(item)
    
    if 'liste' in st.session_state:
        for i in st.session_state.liste:
            st.write(f"🛒 {i}")

# --- HAUPTBEREICH ---
st.title("💙 PREIS-PLUS")

# --- COUPON DER WOCHE ---
st.markdown("""
<div class="coupon-card">
    <p class="coupon-title">🔥 COUPON-HIGHLIGHT</p>
    <p style="color: #555;">Gültig in Wiesmoor & Umzu</p>
    <h2 style="color: #0050aa;">-25% AUF ALLES</h2>
    <p>Aktiviere diesen Coupon bei deiner nächsten Suche!</p>
</div>
""", unsafe_allow_html=True)

# --- SUCHE ---
query = st.text_input("Welches Produkt suchst du heute?", placeholder="z.B. Milch, Werkzeug...")

if query:
    st.markdown(f"### 🔍 ERGEBNISSE FÜR '{query.upper()}'")
    
    col1, col2, col3 = st.columns(3)
    search_term = query.replace(" ", "+")
    
    with col1:
        st.markdown(f'''<div style="background: white; padding: 15px; border-radius: 10px; text-align: center; border-bottom: 5px solid #0050aa;">
            <p style="font-weight: bold;">ONLINE</p>
            <a href="https://www.idealo.de/preisvergleich/MainSearchProductCategory.html?q={search_term}" target="_blank" style="color: #0050aa; text-decoration: none;">CHECK</a>
        </div>''', unsafe_allow_html=True)
        
    with col2:
        st.markdown(f'''<div style="background: white; padding: 15px; border-radius: 10px; text-align: center; border-bottom: 5px solid #fff000;">
            <p style="font-weight: bold;">SHOPPING</p>
            <a href="https://www.google.com/search?tbm=shop&q={search_term}" target="_blank" style="color: #0050aa; text-decoration: none;">PREISE</a>
        </div>''', unsafe_allow_html=True)

    with col3:
        st.markdown(f'''<div style="background: white; padding: 15px; border-radius: 10px; text-align: center; border-bottom: 5px solid #e2001a;">
            <p style="font-weight: bold;">LOKAL</p>
            <a href="https://www.marktguru.de/search/{search_term}" target="_blank" style="color: #0050aa; text-decoration: none;">PROSPEKTE</a>
        </div>''', unsafe_allow_html=True)

    st.markdown("---")
    st.info(f"📍 Route zum nächsten Markt mit '{query}' in {plz}")
    st.markdown(f"[**AUF DER KARTE ANZEIGEN**](https://www.google.com/maps/search/{search_term}+{plz})")

else:
    # Begrüßung wie in der App
    st.image("https://img.icons8.com/clouds/200/shopping-basket-2.png", width=150)
    st.write("Wähle einen Markt aus, um die besten Coupons in deiner Nähe zu sehen.")
