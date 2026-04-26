import streamlit as st

# --- KONFIGURATION ---
st.set_page_config(page_title="WIESMOOR GAS-RADAR", page_icon="💨")

# --- STYLE ---
st.markdown("""
<style>
    .header { background: #0050aa; color: white; padding: 20px; text-align: center; border-radius: 15px; font-weight: bold; }
    .card { background: #f0f2f6; padding: 15px; border-radius: 10px; margin-top: 10px; border-left: 5px solid #0050aa; }
    .price { float: right; color: #0050aa; font-weight: bold; }
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="header">💨 CNG & LPG RADAR</div>', unsafe_allow_html=True)

# --- GASPREISE ---
st.subheader("💎 CNG (Erdgas)")
st.markdown('<div class="card">Stadtwerke Aurich <span class="price">1.39 €/kg</span></div>', unsafe_allow_html=True)
st.markdown('<div class="card">Raiffeisen Wiesmoor <span class="price">1.45 €/kg</span></div>', unsafe_allow_html=True)

st.subheader("⛽ LPG (Autogas)")
st.markdown('<div class="card">Raiffeisen Wiesmoor <span class="price">0.98 €/l</span></div>', unsafe_allow_html=True)
st.markdown('<div class="card">Classic Wiesmoor <span class="price">1.02 €/l</span></div>', unsafe_allow_html=True)

# --- SUCHE ---
st.write("---")
query = st.text_input("Suche nach Deals:")
if query:
    st.link_button(f"🔍 '{query}' Preisvergleich", f"https://www.idealo.de/preisvergleich/MainSearchProductCategory.html?q={query}")

# --- WICHTIG ---
st.info("Hinweis: Falls die App nicht lädt, stelle sicher, dass 'pandas' in deiner requirements.txt Datei steht!")
