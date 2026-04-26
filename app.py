import streamlit as st

# --- KONFIGURATION ---
st.set_page_config(page_title="🚨 DEAL-RADAR 🚨", page_icon="💥", layout="centered")

# --- STYLE (Noch mehr Rot & Auffälliger) ---
st.markdown("""
<style>
    .stApp { background-color: #ffffff; }
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
    }
    /* Blinkender Alarm für Favoriten */
    .favoriten-alarm {
        background-color: #ff0000;
        color: white;
        padding: 15px;
        border-radius: 15px;
        text-align: center;
        font-weight: bold;
        animation: blinker 1s linear infinite;
        margin-bottom: 20px;
        border: 3px solid #fff000;
    }
    @keyframes blinker { 50% { opacity: 0.5; } }
    
    .fav-card {
        border: 2px dashed #e2001a;
        padding: 10px;
        border-radius: 15px;
        margin-bottom: 10px;
        background: #fff5f5;
    }
</style>
""", unsafe_allow_html=True)

# --- HEADER ---
st.markdown('<div class="header-bar">💥 DEIN DEAL-RADAR 💥</div>', unsafe_allow_html=True)

# --- NEU: FAVORITEN & BENACHRICHTIGUNGEN ---
if 'favs' not in st.session_state:
    st.session_state.favs = []

st.subheader("📌 MEIN FAVORITEN-RADAR")

# Alarm anzeigen, wenn Favoriten vorhanden sind
if st.session_state.favs:
    st.markdown(f'<div class="favoriten-alarm">🚨 ALARM: Checke jetzt Angebote für deine {len(st.session_state.favs)} Favoriten!</div>', unsafe_allow_html=True)
    
    cols = st.columns(len(st.session_state.favs) if len(st.session_state.favs) < 4 else 4)
    for idx, f in enumerate(st.session_state.favs):
        with cols[idx % 4]:
            st.markdown(f'<div class="fav-card"><b>{f}</b></div>', unsafe_allow_html=True)
            if st.button("Check", key=f"check_{idx}"):
                st.switch_page(f"https://www.marktguru.de/search/{f}") # Direkter Prospekt-Check
    
    if st.button("🗑️ Alle Favoriten löschen"):
        st.session_state.favs = []
        st.rerun()
else:
    st.info("Noch keine Favoriten gespeichert. Nutze die Suche unten!")

# --- ACTION AREA ---
st.markdown("---")
c1, c2 = st.columns(2)
with c1:
    st.link_button("🔵 LIDL PLUS", "https://www.lidl.de/c/online-prospekte/s10005610")
with c2:
    st.link_button("🅿️ PAYBACK", "https://www.payback.de/coupons")

# --- SUCHE & NEU: ALS FAVORIT SPEICHERN ---
st.markdown("---")
st.subheader("🚀 PRODUKT-SUCHE")
query = st.text_input("", placeholder="z.B. Cola, Kaffee, Werkzeug...")

if query:
    search_term = query.replace(" ", "+")
    
    # Button um Favoriten hinzuzufügen
    if st.button(f"⭐ '{query.upper()}' ALS FAVORIT SPEICHERN"):
        if query not in st.session_state.favs:
            st.session_state.favs.append(query)
            st.success(f"{query} zum Radar hinzugefügt!")
            st.rerun()

    st.markdown(f"### Ergebnisse für: {query.upper()}")
    c1, c2, c3 = st.columns(3)
    with c1:
        st.markdown(f"[🛒 Lidl Shop](https://www.lidl.de/q/search?q={search_term})")
    with c2:
        st.markdown(f"[🅿️ Payback](https://www.google.com/search?q=Payback+{search_term})")
    with c3:
        st.markdown(f"[⚖️ Idealo](https://www.idealo.de/preisvergleich/MainSearchProductCategory.html?q={search_term})")
