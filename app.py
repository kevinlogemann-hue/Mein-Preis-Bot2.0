import streamlit as st

# --- KONFIGURATION ---
st.set_page_config(page_title="🚨 DEAL-RADAR 🚨", page_icon="💥", layout="centered")

# --- STYLE ---
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
    .favoriten-alarm {
        background-color: #ff0000;
        color: white;
        padding: 15px;
        border-radius: 15px;
        text-align: center;
        font-weight: bold;
        animation: blinker 1s linear infinite;
        margin-bottom: 20px;
    }
    @keyframes blinker { 50% { opacity: 0.5; } }
</style>
""", unsafe_allow_html=True)

# --- FUNKTION: SYMBOLFINDER ---
def get_icon(word):
    word = word.lower()
    icons = {
        "würst": "🌭", "wiener": "🌭", "fleisch": "🥩",
        "kaffee": "☕", "bohnen": "🫘",
        "bier": "🍺", "cola": "🥤", "getränk": "🍹",
        "brot": "🍞", "brötchen": "🥖",
        "käse": "🧀", "milch": "🥛",
        "werkzeug": "🛠️", "bohrer": "⚙️",
        "obst": "🍎", "gemüse": "🥦", "pizza": "🍕",
        "schokolade": "🍫", "eis": "🍦"
    }
    for key in icons:
        if key in word:
            return icons[key]
    return "🔍" # Standard-Lupe, wenn nichts passt

# --- HEADER ---
st.markdown('<div class="header-bar">💥 DEIN DEAL-RADAR 💥</div>', unsafe_allow_html=True)

# --- FAVORITEN-RADAR ---
if 'favs' not in st.session_state:
    st.session_state.favs = []

if st.session_state.favs:
    st.markdown(f'<div class="favoriten-alarm">🚨 ALARM: Checke deine Favoriten!</div>', unsafe_allow_html=True)
    cols = st.columns(len(st.session_state.favs) if len(st.session_state.favs) < 4 else 4)
    for idx, f in enumerate(st.session_state.favs):
        with cols[idx % 4]:
            st.info(f"{get_icon(f)} {f}")
            if st.button("Check", key=f"check_{idx}"):
                st.markdown(f'<meta http-equiv="refresh" content="0;URL=https://www.marktguru.de/search/{f}">', unsafe_allow_html=True)

# --- SUCHE MIT AUTO-SYMBOL ---
st.markdown("---")
query = st.text_input("Was suchst du heute?", placeholder="z.B. Wiener Würstchen...")

if query:
    current_icon = get_icon(query)
    st.markdown(f"### {current_icon} Deine Suche: {query.upper()}")
    
    search_term = query.replace(" ", "+")
    
    if st.button(f"⭐ '{query.upper()}' ZUM RADAR HINZUFÜGEN"):
        if query not in st.session_state.favs:
            st.session_state.favs.append(query)
            st.rerun()

    c1, c2, c3 = st.columns(3)
    with c1:
        st.markdown(f"[🛒 Lidl Shop](https://www.lidl.de/q/search?q={search_term})")
    with c2:
        st.markdown(f"[🅿️ Payback](https://www.google.com/search?q=Payback+{search_term})")
    with c3:
        st.markdown(f"[⚖️ Idealo](https://www.idealo.de/preisvergleich/MainSearchProductCategory.html?q={search_term})")
