import streamlit as st

# --- KONFIGURATION ---
st.set_page_config(page_title="🚨 SPARE JETZT! 🚨", page_icon="💥", layout="centered")

# --- HIGH-ATTENTION CSS ---
st.markdown("""
<style>
    .stApp { background-color: #ffffff; color: #333; }
    .header-bar {
        background: linear-gradient(135deg, #e2001a, #ff4b4b);
        color: white;
        padding: 25px;
        text-align: center;
        border-radius: 0 0 30px 30px;
        font-weight: bold;
        font-size: 1.8rem;
        text-transform: uppercase;
        box-shadow: 0 10px 20px rgba(226,0,26,0.3);
        margin-bottom: 30px;
    }
    .coupon-box {
        border: 3px solid #e2001a;
        border-radius: 20px;
        padding: 20px;
        margin-bottom: 20px;
        background: rgba(226,0,26,0.05);
    }
    .stButton>button {
        background-color: #e2001a !important;
        color: white !important;
        border-radius: 50px !important;
        font-weight: bold !important;
        width: 100% !important;
    }
</style>
""", unsafe_allow_html=True)

# --- HEADER ---
st.markdown('<div class="header-bar">💥 DEIN DEAL-ALARM 💥</div>', unsafe_allow_html=True)

# --- ACTION AREA ---
st.error("⚠️ ACHTUNG: VERPASSE KEINE PUNKTE MEHR!")

col_a, col_b = st.columns(2)
with col_a:
    st.link_button("🔵 LIDL PLUS (Wiesmoor)", "https://www.lidl.de/c/online-prospekte/s10005610")
with col_b:
    st.link_button("🅿️ PAYBACK COUPONS", "https://www.payback.de/coupons")

st.markdown("""
<div class="coupon-box">
    <h3 style="color:#e2001a; margin:0;">🔥 MEINPROSPEKT CHECK</h3>
    <p>Alle Prospekte in deiner Nähe auf einen Blick.</p>
</div>
""", unsafe_allow_html=True)
st.link_button("LOKALE PROSPEKTE ÖFFNEN", "https://www.meinprospekt.de/")

# --- SUCHE ---
st.markdown("---")
st.subheader("🚀 WAS SUCHST DU HEUTE GÜNSTIGER?")
query = st.text_input("", placeholder="z.B. Cola, Kaffee, Werkzeug...")

if query:
    st.balloons()
    search_term = query.replace(" ", "+")
    
    st.success(f"SUCHE LÄUFT FÜR: {query.upper()}")
    
    c1, c2, c3 = st.columns(3)
    
    # Vereinfachte Links ohne HTML-Verschachtelung für maximale Stabilität
    with c1:
        st.info("🛒 LIDL SHOP")
        st.markdown(f"[Hier klicken](https://www.lidl.de/q/search?q={search_term})")
    with c2:
        st.info("🅿️ PAYBACK")
        st.markdown(f"[Hier klicken](https://www.google.com/search?q=Payback+{search_term})")
    with c3:
        st.info("⚖️ IDEALO")
        st.markdown(f"[Hier klicken](https://www.idealo.de/preisvergleich/MainSearchProductCategory.html?q={search_term})")

st.markdown("---")
st.warning("📍 Tipp: Nutze die App am Handy!")
