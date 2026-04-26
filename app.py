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
st.write("Verwalte deine Karten und suche nach Deals.")

# --- VERKNÜPFUNGS-SECTION ---
col1, col2 = st.columns(2)

with col1:
    st.markdown("""
    <div class="card lidl">
        <h3 style="color: #0050aa;">💙 Lidl Plus</h3>
        <p style="font-size: 0.8rem; color: #666;">Exklusive Coupons & Kassenbons</p>
    </div>
    """, unsafe_allow_html=True)
    if st.button("Lidl App öffnen"):
        # Dieser Link versucht die App auf dem Handy zu starten
        st.markdown("[Hier klicken zum Öffnen](https://www.lidl.de/l/lidl-plus)", unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="card payback">
        <h3 style="color: #0091ff;">🅿️ Payback</h3>
        <p style="font-size: 0.8rem; color: #666;">Punkte sammeln & einlösen</p>
    </div>
    """, unsafe_allow_html=True)
    if st.button("Payback öffnen"):
        st.markdown("[Hier klicken zum Öffnen](https://www.payback.de/coupons)", unsafe_allow_html=True)

st.markdown("---")

# --- INTELLIGENTE SUCHE ---
query = st.text_input("Produkt suchen & Punkte optimieren:", placeholder="z.B. Windeln, Kaffee...")

if query:
    st.info(f"Suche läuft für: {query}")
    c1, c2 = st.columns(2)
    
    with c1:
        # Sucht direkt bei Payback Partnern
        url_pb = f"https://www.google.com/search?q=Payback+Punkte+{query}"
        st.markdown(f"🔍 [Payback Deals für {query}]({url_pb})")
        
    with c2:
        # Sucht direkt im Lidl Onlineshop
        url_lidl = f"https://www.lidl.de/q/search?q={query}"
        st.markdown(f"🛒 [Lidl Shop: {query}]({url_lidl})")
