import streamlit as st

# --- KONFIGURATION ---
st.set_page_config(page_title="MEIN SPAR-CENTER", page_icon="💳")

# --- STYLE ---
st.markdown("""
<style>
    .stApp { background-color: #f8f9fa; }
    .card {
        background: white;
        padding: 20px;
        border-radius: 15px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        margin-bottom: 20px;
        border-top: 5px solid #0050aa;
    }
    .payback { border-top: 5px solid #0091ff; }
    .lidl { border-top: 5px solid #e2001a; }
</style>
""", unsafe_allow_html=True)

# --- HAUPTBEREICH ---
st.title("💳 MEIN SPAR-CENTER")
st.write("Deine Schaltzentrale für Lidl Plus & Payback")

# --- VERKNÜPFUNGS-SECTION ---
col1, col2 = st.columns(2)

with col1:
    st.markdown("""
    <div class="card lidl">
        <h3 style="color: #0050aa;">💙 Lidl Plus</h3>
        <p style="font-size: 0.8rem; color: #666;">Coupons & Prospekte</p>
    </div>
    """, unsafe_allow_html=True)
    # Stabiler Link zur offiziellen Prospekt-Übersicht
    st.link_button("Lidl Prospekte öffnen", "https://www.lidl.de/c/prospekte/s10007572")

with col2:
    st.markdown("""
    <div class="card payback">
        <h3 style="color: #0091ff;">🅿️ Payback</h3>
        <p style="font-size: 0.8rem; color: #666;">Punkte & Aktivierung</p>
    </div>
    """, unsafe_allow_html=True)
    st.link_button("Payback Coupons", "https://www.payback.de/coupons")

st.markdown("---")

# --- INTELLIGENTE SUCHE ---
query = st.text_input("Produkt suchen:", placeholder="z.B. Kaffee, Werkzeug...")

if query:
    search_term = query.replace(" ", "+")
    st.subheader(f"Ergebnisse für {query}:")
    
    c1, c2, c3 = st.columns(3)
    
    with c1:
        # Direktsuche im Lidl Onlineshop
        st.markdown(f"[🛒 Im Lidl Shop](https://www.lidl.de/q/search?q={search_term})")
        
    with c2:
        # Payback Partner Suche via Google
        st.markdown(f"[🅿️ Payback Deals](https://www.google.com/search?q=Payback+Punkte+{search_term})")

    with c3:
        # Preisvergleich
        st.markdown(f"[⚖️ Idealo Check](https://www.idealo.de/preisvergleich/MainSearchProductCategory.html?q={search_term})")

st.markdown("---")
st.caption("Tipp: Nutze diese App am Handy, um direkt in die installierten Apps zu springen.")
