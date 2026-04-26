import streamlit as st

# 1. SETUP
st.set_page_config(page_title="WIESMOOR RADAR", page_icon="⛽")

# 2. DESIGN
st.markdown("""
<style>
    .header { background: #e2001a; color: white; padding: 20px; text-align: center; border-radius: 15px; font-weight: bold; font-size: 1.5rem; }
    .card { background: #f0f2f6; padding: 12px; border-radius: 10px; margin-top: 10px; border-left: 5px solid #e2001a; display: flex; justify-content: space-between; }
    .top { border-left-color: #28a745; background-color: #e8f5e9; }
    .price { font-weight: bold; color: #333; }
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="header">⛽ SPRIT-RADAR WIESMOOR</div>', unsafe_allow_html=True)

# 3. REITER (TABS)
t1, t2, t3, t4, t5 = st.tabs(["E5", "E10", "Diesel", "LPG", "CNG"])

with t1:
    st.markdown('**Super E5 - Günstigste zuerst**')
    st.markdown('<div class="card top">JET (Aurich) <span class="price">1.76 €</span></div>', unsafe_allow_html=True)
    st.markdown('<div class="card">SCORE (Friedeburg) <span class="price">1.78 €</span></div>', unsafe_allow_html=True)
    st.markdown('<div class="card">CLASSIC (Wiesmoor) <span class="price">1.79 €</span></div>', unsafe_allow_html=True)
    st.markdown('<div class="card">ARAL (Uplengen) <span class="price">1.85 €</span></div>', unsafe_allow_html=True)

with t2:
    st.markdown('**Super E10 - Günstigste zuerst**')
    st.markdown('<div class="card top">JET (Aurich) <span class="price">1.70 €</span></div>', unsafe_allow_html=True)
    st.markdown('<div class="card">SCORE (Friedeburg) <span class="price">1.72 €</span></div>', unsafe_allow_html=True)
    st.markdown('<div class="card">CLASSIC (Wiesmoor) <span class="price">1.73 €</span></div>', unsafe_allow_html=True)

with t3:
    st.markdown('**Diesel - Günstigste zuerst**')
    st.markdown('<div class="card top">JET (Aurich) <span class="price">1.58 €</span></div>', unsafe_allow_html=True)
    st.markdown('<div class="card">SCORE (Friedeburg) <span class="price">1.60 €</span></div>', unsafe_allow_html=True)
    st.markdown('<div class="card">RAIFFEISEN (Wiesmoor) <span class="price">1.64 €</span></div>', unsafe_allow_html=True)

with t4:
    st.markdown('**LPG (Autogas) - Günstigste zuerst**')
    st.markdown('<div class="card top">JET (Aurich) <span class="price">0.94 €</span></div>', unsafe_allow_html=True)
    st.markdown('<div class="card">RAIFFEISEN (Wiesmoor) <span class="price">0.98 €</span></div>', unsafe_allow_html=True)
    st.markdown('<div class="card">CLASSIC (Wiesmoor) <span class="price">1.02 €</span></div>', unsafe_allow_html=True)

with t5:
    st.markdown('**CNG (Erdgas) - Günstigste zuerst**')
    st.markdown('<div class="card top">STADTWERKE (Aurich) <span class="price">1.39 €/kg</span></div>', unsafe_allow_html=True)
    st.markdown('<div class="card">SCORE (Friedeburg) <span class="price">1.42 €/kg</span></div>', unsafe_allow_html=True)
    st.markdown('<div class="card">RAIFFEISEN (Wiesmoor) <span class="price">1.45 €/kg</span></div>', unsafe_allow_html=True)

# 4. SUCHE
st.write("---")
q = st.text_input("🔍 Suchbegriff:")
if q:
    st.link_button(f"Deals für {q} suchen", f"https://www.marktguru.de/search/{q}")
