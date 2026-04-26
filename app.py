import streamlit as st

# --- KONFIGURATION (Titel angepasst) ---
st.set_page_config(page_title="🚨 SPARE JETZT! 🚨", page_icon="💥", layout="centered")

# --- HIGH-ATTENTION CSS (Rot, Neon, Groß) ---
st.markdown("""
<style>
    /* Heller Hintergrund, um das Rot knallen zu lassen */
    .stApp { background-color: #ffffff; color: #333; }
    
    /* Aggressive Rote Header-Bar mit Schatten */
    .header-bar {
        background: linear-gradient(135deg, #e2001a, #ff4b4b);
        color: white;
        padding: 25px;
        text-align: center;
        border-radius: 0 0 30px 30px;
        font-weight: bold;
        font-size: 2rem;
        text-transform: uppercase;
        letter-spacing: 2px;
        box-shadow: 0 10px 20px rgba(226,0,26,0.3);
        margin-bottom: 30px;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
    }

    /* Rote, auffällige Coupon-Karten */
    .coupon-box {
        border: 3px solid #e2001a;
        border-radius: 20px;
        padding: 20px;
        margin-bottom: 20px;
        background: rgba(226,0,26,0.05);
        display: flex;
        justify-content: space-between;
        align-items: center;
        transition: transform 0.2s;
    }
    .coupon-box:hover {
        transform: scale(1.02);
        box-shadow: 0 5px 15px rgba(226,0,26,0.2);
    }

    /* Große, leuchtende Suchleiste */
    .stTextInput>div>div>input {
        border: 3px solid #0050aa !important;
        border-radius: 50px !important;
        font-size: 1.2rem !important;
        padding: 15px !important;
        box-shadow: 0 0 10px rgba(0,80,170,0.1);
    }

    /* Rote Buttons mit Hover-Effekt */
    .stButton>button {
        background-color: #e2001a !important;
        color: white !important;
        border-radius: 50px !important;
        border: none !important;
        font-weight: bold !important;
        font-size: 1.1rem !important;
        padding: 10px 20px !important;
        width: 100% !important;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1) !important;
    }
    .stButton>button:hover {
        background-color: #ff4b4b !important;
        box-shadow: 0 6px 12px rgba(226,0,26,0.3) !important;
    }
</style>
""", unsafe_allow_html=True)

# --- HEADER (Knallrot) ---
st.markdown('<div class="header-bar">💥 DEIN DEAL-ALARM 💥</div>', unsafe_allow_html=True)

# --- ACTION AREA (Coupons) ---
st.error("⚠️ ACHTUNG: VERPASSE KEINE PUNKTE MEHR!")

c1, c2 = st.columns(2)
with c1:
    st.link_button("🔵 ZU LIDL PLUS (Wiesmoor)", "https://www.lidl.de/c/online-prospekte/s10005610")
with c2:
    st.link_button("🅿️ ZU PAYBACK COUPONS", "https://www.payback.de/coupons")

st.markdown("""
<div class="coupon-box">
    <div>
        <h3 style="color:#e2001a; margin:0;">🔥 MEINPROSPEKT CHECK</h3>
        <p style="margin:5px 0;">Alle Prospekte in deiner Nähe auf einen Blick.</p>
    </div>
    <a href="https://www.meinprospekt.de/" target="_blank" style="background:#e2001a; color:white; padding:10px 20px; border-radius:50px; text-decoration:none; font-weight:bold;">ÖFFNEN</a>
</div>
""", unsafe_allow_html=True)

# --- SUCHE (Mit blauer Akzentfarbe) ---
st.markdown("---")
st.subheader("🚀 WAS SUCHST DU HEUTE GÜNSTIGER?")
query = st.text_input("", placeholder="z.B. Cola, Kaffee, Werkzeug...")

if query:
    search_term = query.replace(" ", "+")
    
    # Rote Info-Box für die Ergebnisse
    st.success(f"Deals gefunden für: {query.upper()}")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown(f'''<div style="background:#0050aa; color:white; padding:15px; border-radius:10px; text-align:center; box-shadow: 0 4px 6px rgba(0,0,0,0.1);">
            <h4 style="margin:0; color:white;">🛒 Lidl Shop</h4>
            <a href="https://www.lidl.de/q/search?q={search_term}" target="_blank" style="color:#fff000; font-weight:bold; text-decoration:none;">PREISE</a>
        </div>''', unsafe_allow_html=True)
    with col2:
        st.markdown(f'''<div style="background:#0091ff; color:white; padding:15px; border-radius:10px; text-align:center; box-shadow: 0 4px 6px rgba(0,0,0,0.1);">
            <h4 style="margin:0; color:white;">🅿️ Payback</h4>
            <a href="https://www.google.com/search?q=Payback+{search_term}" target="_
