import streamlit as st
import requests
from streamlit_js_eval import streamlit_js_eval

# 1. ULTIMATIVES DESIGN (Filter-System & Premium Icons)
st.set_page_config(page_title="Wiesmoor Radar", layout="centered")

st.markdown("""
<style>
    /* Das Hauptbanner (Original-Look) */
    .hero-banner {
        width: 100%;
        height: 150px;
        background: linear-gradient(rgba(0,0,0,0.5), rgba(0,0,0,0.5)), 
                    url('https://images.unsplash.com/photo-1527018601619-a508a2be00cd?q=80&w=1000');
        background-size: cover;
        background-position: center;
        border-radius: 25px;
        display: flex;
        align-items: center;
        justify-content: center;
        box-shadow: 0 10px 30px rgba(0,0,0,0.2);
        margin-bottom: 5px;
        border: 1px solid rgba(255,255,255,0.2);
    }
    .hero-title {
        color: white;
        font-size: 2.2rem;
        font-weight: 900;
        text-shadow: 2px 2px 10px rgba(0,0,0,0.8);
    }
    
    /* Community Aufruf */
    .community-box {
        text-align: center;
        color: #d32f2f;
        font-size: 0.85rem;
        font-weight: 600;
        margin-bottom: 20px;
        padding: 5px;
    }

    /* Tankstellen Karte */
    .station-card {
        background: white;
        padding: 18px;
        border-radius: 22px;
        display: flex;
        align-items: center;
        border: 1px solid #f0f0f0;
        box-shadow: 0 5px 15px rgba(0,0,0,0.04);
        margin-bottom: 10px;
    }

    .brand-icon {
        width: 55px;
        height: 55px;
        border-radius: 15px;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 1.6rem;
        font-weight: 900;
        flex-shrink: 0;
    }

    .price-text {
        margin-left: auto;
        font-size: 2.1rem;
        font-weight: 900;
        color: #111;
        letter-spacing: -1px;
    }

    /* Neue moderne Foto-Badges */
    div.stButton > button {
        background-color: transparent !important;
        color: #666 !important;
        border: 1px solid #ddd !important;
        border-radius: 20px !important;
        padding: 2px 12px !important;
        font-size: 0.7rem !important;
        text-transform: uppercase !important;
        letter-spacing: 0.5px !important;
        margin-top: -15px !important;
        margin-bottom: 15px !important;
        transition: all 0.3s !important;
    }
    
    div.stButton > button:hover {
        border-color: #e2001a !important;
        color: #e2001a !important;
        background-color: #fff1f1 !important;
    }
</style>
""", unsafe_allow_html=True)

# --- UI START ---
st.markdown('<div class="hero-banner"><div class="hero-title">WIESMOOR RADAR</div></div>', unsafe_allow_html=True)
st.markdown('<div class="community-box">📸 Bitte Fotos für die Community machen, um Echtheit zu bestätigen!</div>', unsafe_allow_html=True)

# 2. STANDORT-FILTERUNG & SORTIERUNG
if 'lat' not in st.session_state: st.session_state.lat, st.session_state.lng = 53.414, 7.733

col1, col2 = st.columns([2, 1])
with col1:
    if st.button("📍 ME
