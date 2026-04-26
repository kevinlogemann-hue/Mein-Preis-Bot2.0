import streamlit as st

# --- KONFIGURATION ---
st.set_page_config(page_title="SPAR-CENTER PRO", page_icon="💳", layout="centered")

# --- APP-STYLE (Dein Screenshot-Look) ---
st.markdown("""
<style>
    .stApp { background-color: #ffffff; }
    
    /* Blaue Header-Bar */
    .header-bar {
        background-color: #0050aa;
        color: white;
        padding: 15px;
        text-align: center;
        border-radius: 0 0 15px 15px;
        font-weight: bold;
        margin-bottom: 20px;
    }

    /* Coupon-Karten wie im Screenshot */
    .coupon-box {
        border: 1px solid #e0e0e0;
        border-radius: 12px;
        padding: 15px;
        margin-bottom: 10px;
        background: white;
        display: flex;
        justify-content: space-between;
        align-items: center;
    }

    /* Untere Navigationsleiste Simulation */
    .nav-bar {
        position: fixed;
        bottom: 0;
        left: 0;
        width: 100%;
        background: white;
        border-top: 1px solid #ddd;
        display: flex;
        justify-content: space-around;
        padding: 10px 0;
        z-index: 100;
    }
    .nav-item { text-align: center; color: #666; font-size: 0.7rem; }
</style>
""", unsafe_allow_html=True)

# --- HEADER ---
st.markdown('<div class="header-bar">MEIN SPAR-CENTER 2.0</div>', unsafe_allow_html=True)

# --- COUPON BEREICH (Nachbau deines Bildes) ---
st.subheader("Deine Top-Coupons")

col1, col2 = st.columns(2)
with col1:
    st.link_button("🔵 LIDL PLUS AKTIVIEREN", "https://www.lidl.de/c/online-prospekte/s10005610", use_container_width=True)
with col2:
    st.link_button("🅿️ PAYBACK COUPONS", "https://www.payback.de/coupons", use_container_width=True)

st.markdown("""
<div class="coupon-box">
    <div>
        <b style="color:#e2001a;">OTTO DEAL</b><br>
        <small>Extra-Punkte auf Mode & Technik</small>
    </div>
    <div style="color:#0050aa; font-weight:bold;">AKTIV</div>
</div>
""", unsafe_allow_html=True)

# --- SUCHE ---
st.markdown("---")
query = st.text_input("🔍 Produkt suchen:", placeholder="Was möchtest du heute sparen?")

if query:
    search_term = query.replace(" ", "+")
    c1, c2, c3 = st.columns(3)
    with c1: st.markdown(f"[🛒 Lidl Shop](https://www.lidl.de/q/search?q={search_term})")
    with c2: st.markdown(f"[🅿️ Payback Suche](https://www.google.com/search?q=Payback+{search_term})")
    with c3: st.markdown(f"[⚖️ Idealo](https://www.idealo.de/preisvergleich/MainSearchProductCategory.html?q={search_term})")

# --- UNTERE NAVI (Optik) ---
st.markdown("""
<div class="nav-bar">
    <div class="nav-item">🕒<br>Aktuell</div>
    <div class="nav-item" style="color:#0050aa;">🎟️<br>Coupons</div>
    <div class="nav-item">💳<br>Karte</div>
    <div class="nav-item">🛒<br>Shops</div>
</div>
<br><br>
""", unsafe_allow_html=True)
