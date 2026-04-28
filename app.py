import streamlit as st
import requests
import folium
from streamlit_folium import st_folium
from streamlit_js_eval import streamlit_js_eval
from datetime import datetime
from PIL import Image

# 1. SETUP & MODERNES DESIGN
st.set_page_config(page_title="Wiesmoor Radar", page_icon="⛽", layout="centered")

st.markdown("""
    <style>
    .header-container {
        position: relative;
        width: 100%;
        height: 150px;
        background: #e2001a;
        background-image: url('https://images.unsplash.com/photo-1527018601619-a508a2be00cd?q=80&w=1000&auto=format&fit=crop');
        background-size: cover;
        background-position: center;
        border-radius: 15px;
        display: flex;
        align-items: center;
        justify-content: center;
        margin-bottom: 5px;
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
        text-align: center;
        text-shadow: 3px 3px 6px rgba(0,0,0,0.7);
        letter-spacing: 1px;
    }
    .community-info {
