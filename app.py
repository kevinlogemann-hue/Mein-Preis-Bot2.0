import streamlit as st

# --- KONFIGURATION ---
st.set_page_config(
    page_title="PREIS-PROFI AI 2.0",
    page_icon="⚡",
    layout="centered"
)

# --- HYPER-STYLING ---
st.markdown("""
<style>
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
    .result-card {
        background: rgba(0, 0, 0, 0.6);
        padding: 20px;
        border-radius: 20px;
        border: 2px solid #ff00ff;
        box-shadow: 0 0 15px #ff00ff;
        margin-bottom: 20px;
        text-align: center;
    }
    h1 {
        color: #fff;
        text-shadow: 0 0 10px #00f2ff, 0 0 20px #00f2ff;
        text-align: center;
    }
</style>
""", unsafe_allow_html=True)

# --- SEITENLEISTE ---
with st.sidebar:
    st.image("https://img.icons8.com/clouds/200/flash-light.png", width=120)
    st.title("Spar-Cockpit")
    plz = st.text_input("📍 PLZ:", value="26639")
    
    st.header("🛒 SHOP-LISTE")
    item = st.text_input("Merken:")
    if st.button("HINZUFÜGEN"):
        if 'liste' not in st.session_state: st.session_state.liste = []
        if item: st.session_state.liste.append(item)
    
    if 'liste' in st.session_state:
        for i in st.session_state.liste:
            st.write(f"🔹 {i}")

# --- HAUPTBEREICH ---
st.title("⚡ PREIS-PROFI")
query = st.text_input("", placeholder="WELCHEN DEAL SUCHST DU?")

if query:
    st.snow()
    st.markdown(f"### Ergebnisse für: {query.upper()}")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown(f'<div class="result-card"><h3 style="color: #00f2ff;">🌐 WEB</h3><a href="https://www.idealo.de/preisvergleich/MainSearchProductCategory.html?q={query}" target="_blank" style="color: #00f2ff; text-decoration: none;">IDEALO</a></div>', unsafe_allow_html=True)
        
    with col2:
        st.markdown(f'<div class="result-card"><h3 style="color: #ff00ff;">🛒 SHOP</h3><a href="https://www.google.com/search?tbm=shop&q={query}" target="_blank" style="color: #ff00ff; text-decoration: none;">GOOGLE</a></div>', unsafe_allow_html=True)

    with col3:
        st.markdown(f'<div class="result-card"><h3 style="color: #39ff14;">🏠 LOKAL</h3><a href="https://www.kaufda.de/suche/{query}?zip={plz}" target="_blank" style="color: #39ff14; text-decoration: none;">PROSPEKTE</a></div>', unsafe_allow_html=True)

    st.markdown(f"📍 [**LÄDEN IN DER NÄHE AUF DER KARTE**](https://www.google.com/maps/search/{query}+{plz})")
