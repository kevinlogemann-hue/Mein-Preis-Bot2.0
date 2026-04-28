import streamlit as st
import requests
from streamlit_js_eval import streamlit_js_eval

# 1. ULTIMATIVES PREMIUM DESIGN (Banner zurück + Schicke Foto-Buttons)
st.set_page_config(page_title="Wiesmoor Radar", layout="centered")

st.markdown("""
<style>
    /* Das markante Hauptbanner (Blickfang) */
    .hero-banner {
        width: 100%;
        height: 140px;
        background: linear-gradient(rgba(180,0,0,0.6), rgba(0,0,0,0.7)), 
                    url('https://images.unsplash.com/photo-1527018601619-a508a2be00cd?q=80&w=1000');
        background-size: cover;
        background-position: center;
        border-radius: 24px;
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        box-shadow: 0 12px 24px rgba(0,0,0,0.2);
        margin-bottom: 8px;
        border: 2px solid #e2001a;
    }
    .hero-title {
        color: white;
        font-size: 2.1rem;
        font-weight: 900;
        text-shadow: 2px 2px 8px rgba(0,0,0,0.8);
        letter-spacing: 1px;
        margin: 0;
    }
    
    /* Community Text */
    .community-text {
        text-align: center;
        font-size: 0.85rem;
        color: #666;
        margin-bottom: 20px;
        padding: 0 20px;
        font-style: italic;
    }

    /* Station Card */
    .station-card {
        background: white;
        padding: 18px;
        border-radius: 20px;
        display: flex;
        align-items: center;
        border: 1px solid #f0f0f0;
        box-shadow: 0 4px 15px rgba(0,0,0,0.04);
        margin-bottom: 4px;
    }

    .brand-icon {
        width: 55px;
        height: 55px;
        border-radius: 14px;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 1.6rem;
        font-weight: 800;
        flex-shrink: 0;
    }

    .price-tag {
        margin-left: auto;
        font-size: 2.1rem;
        font-weight: 900;
        color: #000;
        letter-spacing: -1px;
    }

    /* Styling für den Foto-Button (Dezent & Schick) */
    div.stButton > button {
        background-color: transparent !important;
        color: #e2001a !important;
        border: 1px solid #ffccd1 !important;
        border-radius: 12px !important;
        font-size: 0.8rem !important;
        padding: 4px 12px !important;
        margin-top: -10px !important;
        margin-bottom: 20px !important;
        transition: all 0.3s !important;
    }
    
    div.stButton > button:hover {
        background-color: #fdf2f2 !important;
        border-color: #e2001a !important;
        transform: translateY(-1px);
    }
</style>
""", unsafe_allow_html=True)

# --- UI ELEMENTE ---
st.markdown('<div class="hero-banner"><h1 class="hero-title">WIESMOOR RADAR</h1></div>', unsafe_allow_html=True)
st.markdown('<div class="community-text">📸 Community-Power: Lade ein Foto hoch, um die Preise aktuell zu halten!</div>', unsafe_allow_html=True)

# Logik-States
if 'lat' not in st.session_state: st.session_state.lat, st.session_state.lng = 53.414, 7.733

c1, c2 = st.columns(2)
with c1:
    if st.button("📍
