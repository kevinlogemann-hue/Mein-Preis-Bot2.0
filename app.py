import streamlit as st
import pandas as pd

# --- KONFIGURATION ---
st.set_page_config(page_title="WIESMOOR SUPER-APP", page_icon="⛽", layout="centered")

# --- DESIGN (Einfach & Stabil) ---
st.markdown("""
<style>
    .header-bar {
        background: #e2001a;
        color: white; padding: 20px; text-align: center;
        border-radius: 0 0 20px 20px; font-weight: bold; font-size: 1.5rem;
        margin-bottom: 20px;
    }
    .best-deal {
        background-color: #28a745; color: white;
        padding: 15px; border-radius: 10px; font-weight: bold;
        display: flex; justify-content: space-between; margin-bottom: 10px;
    }
    .other-deal {
        background-color: #f1f1f1; color: #333;
        padding: 10px; border-radius: 10px;
        display: flex; justify-content: space-between; margin-bottom: 8px;
        border-left: 5px solid #e2001a;
    }
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="header-bar">⛽ SPRIT- & DEAL-RADAR</div>', unsafe_allow_html=True)

# --- TANKSTELLEN-DATEN ---
tanks = [
    {"Marke": "JET", "Ort": "Aurich", "E5": 1.76, "E10": 1.70, "Diesel": 1.58},
    {"Marke": "SCORE", "Ort": "Friedeburg", "E5": 1.78, "E10": 1.72, "Diesel": 1.60},
    {"Marke": "CLASSIC", "Ort": "Wiesmoor", "E5": 1.79, "E10": 1.73, "Diesel": 1.62},
    {"Marke": "RAIFFEISEN", "Ort": "Wiesmoor", "E5": 1.80, "E10": 1.74, "Diesel": 1.64},
    {"Marke": "AVIA", "Ort": "Wiesmoor", "E5": 1.82, "E10": 1.76, "Diesel": 1.65},
    {"Marke": "ARAL", "Ort": "Uplengen", "E5": 1.85, "E10": 1.79, "Diesel": 1.69},
    {"Marke": "SHELL", "Ort": "Remels", "E5": 1.87, "E10": 1.81, "Diesel": 1.71},
]
df = pd.DataFrame(tanks)

# --- SPRIT-REITER ---
tab1, tab2, tab3 = st.tabs(["🟢 E5", "🟡 E10", "⚫ Diesel"])

def liste_anzeigen(kraftstoff):
    sorted_df = df.sort_values(by=kraftstoff)
    for i, row in sorted_df.iterrows():
        if i == sorted_df.index[0]: # Günstigster
            st.markdown(f'<div class="best-deal"><span>🏆 {row["Marke"]} ({row["Ort"]})</span><span>{row[kraftstoff]:.2f} €</span></div>', unsafe_allow_html=True)
        else:
            st.markdown(f'<div class="other-deal"><span>📍 {row["Marke"]} ({row["Ort"]})</span><span>{row[kraftstoff]:.2f} €</span></div>', unsafe_allow_html=True)

with tab1: liste_anzeigen("E5")
with tab2: liste_anzeigen("E10")
with tab3: liste_anzeigen("Diesel")

# --- SUCHE MIT SYMBOLEN ---
st.write("---")
st.subheader("🔍 Produktsuche & Spar-Check")

def get_icon(txt):
    txt = txt.lower()
    if "würst" in txt or "wiener" in txt: return "🌭"
    if "käse" in txt: return "🧀"
    if "kaffee" in txt: return "☕"
    if "bier" in txt: return "🍺"
    if "fleisch" in txt: return "🥩"
    return "🔎"

query = st.text_input("Was suchst du heute?")
if query:
    icon = get_icon(query)
    st.markdown(f"### {icon} {query.upper()}")
    c1, c2 = st.columns(2)
    with c1: st.link_button("🔵 Lidl Shop", f"https://www.lidl.de/q/search?q={query}")
    with c2: st.link_button("🅿️ Payback", f"https://www.google.com/search?q=Payback+{query}")

# --- FAVORITEN ---
if 'favs' not in st.session_state: st.session_state.favs = []
if query and st.button("⭐ Merken"):
    if query not in st.session_state.favs:
        st.session_state.favs.append(query)
        st.rerun()

if st.session_state.favs:
    st.write("📌 Merkliste:", ", ".join(st.session_state.favs))
