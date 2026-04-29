import streamlit as st
import requests
from streamlit_js_eval import streamlit_js_eval

# 1. DESIGN-SETUP (Maximale Stabilität ohne f-Strings im CSS)
st.set_page_config(page_title="Wiesmoor Radar", layout="centered")

STYLE = """
<style>
    .hero-banner {
        width: 100%; height: 140px;
        background: linear-gradient(rgba(0,0,0,0.5), rgba(0,0,0,0.7)), 
                    url('https://images.unsplash.com/photo-1527018601619-a508a2be00cd?q=80&w=1000');
        background-size: cover; background-position: center; border-radius: 20px;
        display: flex; flex-direction: column; align-items: center; justify-content: center; margin-bottom: 20px;
    }
    .hero-title { color: white; font-size: 2rem; font-weight: 900; margin: 0; }
    .hero-subtitle { color: #d1ffcd; font-size: 0.9rem; font-weight: 600; text-align: center; }

    .station-card {
        background: white; padding: 16px; border-radius: 20px;
        display: flex; align-items: center; border: 1px solid #eee;
        box-shadow: 0 4px 10px rgba(0,0,0,0.03); margin-bottom: 8px;
    }
    .brand-logo {
        width: 50px; height: 50px; border-radius: 12px;
        display: flex; align-items: center; justify-content: center;
        font-size: 1.4rem; font-weight: bold; flex-shrink: 0;
    }
    .price-tag { margin-left: auto; font-size: 1.9rem; font-weight: 900
