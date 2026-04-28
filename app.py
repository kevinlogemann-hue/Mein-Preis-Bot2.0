import streamlit as st
import requests
from streamlit_js_eval import streamlit_js_eval
from datetime import datetime
from PIL import Image

# 1. KONFIGURATION & STYLING
st.set_page_config(page_title="Wiesmoor Radar", page_icon="⛽", layout="centered")

st.markdown("""
<style>
    .header-container {
        position: relative;
        width: 100%;
        height: 150px;
        background-color: #e2001a;
        background-image: url('https://images.unsplash.com/photo-1527018601619-a508a2be00cd?q=80&w=1000&auto=format&fit=crop');
        background-size: cover;
        background-position: center;
        border-radius: 15px;
        display: flex;
        align-items: center;
        justify-content: center;
        border: 2px solid #c10016;
    }
    .header-overlay {
        background: rgba(180, 0, 0, 0.4); 
        width: 100%;
        height: 100%;
        border-radius: 13px;
        display: flex;
        align-items: center;
        justify-content: center;
    }
    .header-title {
        color: white;
        font-size: 1.8rem;
        font-weight: 900;
        text-shadow: 3px 3px 6px rgba(0,0,0,0.7);
    }
    .community-info {
        text-align: center; 
        color: #555; 
        font-size: 0.95rem; 
        margin: 15px 0;
        line-height: 1.4;
    }
</style>
""", unsafe_allow_html=True)

# 2. HEADER ANZEIGEN
st.markdown('<div class="header-container"><div class="header-overlay"><div class="header-title">WIESMOOR LIVE-RADAR</div></div></div>', unsafe_allow_html=True)

st.markdown('<div class="community-info">📸 <b>Mache Fotos für die Community für die Echtzeit-Preisangaben.</b><br>Umso mehr mitmachen, desto genauer werden die Preise werden!</div>', unsafe_allow_html=True)

# 3. LOGIK & API
API_KEY = "616cbb8e-9dde-4eb7-91f1-21a1663fa495"

if 'user_reports' not in st.session_state:
    st.session_state.user_reports = {}
if 'lat' not in st.session_state:
    st.session_state.lat, st.session_state.lng = 53.414, 7.733

# Buttons
col1, col2 = st.columns(2)
with col1:
    loc = streamlit_js_eval(js_expressions='navigator.geolocation ? new Promise((resolve) => { navigator.geolocation.getCurrentPosition(pos => resolve({lat: pos.coords.latitude, lon: pos.coords.longitude})) }) : null', key='gps_final')
    if st.button("📍 Standort"):
        if loc:
            st.session_state.lat, st.session_state.
