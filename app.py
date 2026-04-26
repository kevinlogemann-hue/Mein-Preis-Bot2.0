import streamlit as st

# --- KONFIGURATION ---
st.set_page_config(page_title="DEAL-RADAR 3.0", page_icon="🧀", layout="centered")

# --- STYLE UPDATE (Moderner & Kontrastreicher) ---
st.markdown("""
<style>
    .stApp { background-color: #f4f7f6; }
    .header-bar {
        background: linear-gradient(135deg, #e2001a, #b30014);
        color: white;
        padding: 30px;
        text-align: center;
        border-radius: 0 0 40px 40px;
        font-weight: bold;
        font-size: 2rem;
        box-shadow: 0 10px 30px rgba(226,0,26,0.4);
    }
    .quick-btn {
        background: white;
        border: 2px solid #e2001a;
        border-radius: 15px;
        padding: 10px;
        text-align: center;
        margin: 5px;
    }
</style>
""", unsafe_allow_html=True)

# --- FUNKTION: SYMBOL-AUTO-PILOT ---
def get_icon(word):
    word = word.lower()
    icons = {
        "käse": "🧀", "milch": "🥛", "fleisch": "🥩", "wurst": "🌭",
        "kaffee": "☕", "bier": "🍺", "cola": "🥤", "pizza": "🍕",
        "tanken": "⛽", "benzin": "⛽", "brot": "🍞", "ei": "🥚"
    }
    for key in icons:
        if key in word: return icons[key]
    return "🔎"

# --- HEADER ---
st.markdown('<div class="header-bar">💥 DEAL-RADAR 3.0</div>', unsafe_allow_html=True)

# --- NEU: SCHNELLWAHL-LEISTE ---
st.write("### ⚡ SCHNELL-CHECK")
col_s1, col_s2, col_s3, col_s4 = st.columns(4)
with col_s1: st.link_button("☕ Kaffee", "https://www.marktguru.de/search/Kaffee")
with col_s2: st.link_button("🍺 Bier", "https://www.marktguru.de/search/Bier")
with col_s3: st.link_button("⛽ Sprit", "https://www.clever-tanken.de/tankstelle_liste?ort=26639")
with col_s4: st.link_button("🥩 Grillen", "https://www.marktguru.de/search/Fleisch")

# --- HAUPTSUCHE ---
st.markdown("---")
query = st.text_input("Was suchst du?", placeholder="z.B. Käse...")

if query:
    icon = get_icon(query)
    st.markdown(f"## {icon} {query.upper()}")
    
    # Automatische Buttons für die Suche
    st.link_button(f"👉 {query} bei Lidl prüfen", f"https://www.lidl.de/q/search?q={query}")
    st.link_button(f"👉 {query} im Prospekt finden", f"https://www.marktguru.de/search/{query}")

# --- FAVORITEN SPEICHER ---
if 'favs' not in st.session_state: st.session_state.favs = []
if query and st.button("⭐ Produkt merken"):
    if query not in st.session_state.favs:
        st.session_state.favs.append(query)
        st.rerun()

if st.session_state.favs:
    st.write("---")
    st.write("### 📌 DEIN RADAR")
    st.write(", ".join([f"{get_icon(f)} {f}" for f in st.session_state.favs]))
