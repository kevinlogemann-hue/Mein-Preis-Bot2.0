import streamlit as st
import requests
from streamlit_js_eval import streamlit_js_eval

# 1. STABILE UI-KONFIGURATION
st.set_page_config(page_title="Wiesmoor Radar", layout="centered")

st.markdown("""
<style>
    .hero-banner {
        width: 100%; height: 140px;
        background: linear-gradient(rgba(0,0,0,0.5), rgba(0,0,0,0.7)), 
                    url('https://images.unsplash.com/photo-1527018601619-a508a2be00cd?q=80&w=1000');
        background-size: cover; background-position: center; border-radius: 20px;
        display: flex; flex-direction: column; align-items: center; justify-content: center; margin-bottom: 20px;
    }
    .hero-title { color: white; font-size: 2.1rem; font-weight: 900; margin: 0; text-shadow: 2px 2px 4px rgba(0,0,0,0.5); }
    .hero-subtitle { color: #d1ffcd; font-size: 0.9rem; font-weight: 600; text-align: center; }

    .station-card {
        background: white; padding: 16px; border-radius: 20px;
        display: flex; align-items: center; border: 1px solid #eee;
        box-shadow: 0 4px 10px rgba(0,0,0,0.03); margin-bottom: 8px;
    }
    .brand-logo {
        width: 52px; height: 52px; border-radius: 14px;
        display: flex; align-items: center; justify-content: center;
        font-size: 1.4rem; font-weight: bold; flex-shrink: 0;
    }
    .price-tag { margin-left: auto; font-size: 1.9rem; font-weight: 900; color: #000; letter-spacing: -1px; }

    /* Community Button */
    div.stButton > button {
        background-color: #f0f7ff !important; color: #007bff !important;
        border: 2px solid #007bff !important; border-radius: 12px !important;
        padding: 5px 15px !important; font-size: 0.8rem !important;
        font-weight: 700 !important; margin-top: -12px !important; margin-bottom: 25px !important;
    }
    div.stButton > button:hover { background-color: #007bff !important; color: white !important; }
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="
