import streamlit as st
import requests
from datetime import datetime

# --- 1. CONFIG & ICON ---
st.set_page_config(
    page_title="Wiesmoor Live-Radar", 
    page_icon="⛽",
    layout="centered"
)

# --- 2. DEIN AKTIVIERTER API-KEY ---
API_KEY = "616cbb8e-9dde-4eb7-91f1-21a1663fa495" 

# Koordinaten für Wiesmoor (Zentrum)
LAT = "53.414"
LNG = "7.733"

# --- 3. DESIGN ---
st.markdown("""
<style>
    .main-header { 
        background: linear-gradient(135deg, #e2001a, #b30014); 
        color: white; padding: 20px; text-align: center; border-radius: 15px; 
        font-weight: bold; margin-bottom: 20px;
    }
    .card { 
        background: white; padding: 15px; border-radius: 12px; margin-top: 10px; 
        border-left: 6px solid #e2001a; display: flex; justify-content: space-between; 
        align-items: center; box-shadow: 2px 2px 10px rgba(0,0,0,0.05);
    }
    .best-card { border-left-color: #28a745; background-color: #f0fff4; }
    .price-text { font-weight: 900; color: #333; font-size: 1.2rem; }
    .status-tag { font-size: 0.8rem; font-weight: bold; }
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="main-header">⛽ WIESMOOR LIVE-RADAR</div>', unsafe_allow_html=True)

# --- 4. FUNKTION ZUM PREISE LADEN ---
@st.cache_data(ttl=300) # Aktualisiert alle 5 Minuten
def get_tankerkoenig_data():
    url = f"https://creativecommons.tankerkoenig.de/json/list.php?lat={LAT}&lng={LNG}&rad=10&sort=dist&type=all&apikey={API_KEY}"
    try:
        response = requests.get(url)
        return response.json()
    except:
        return None

# --- 5. ANZEIGE DER PREISE ---
data = get_tankerkoenig_data()

if data and data.get("ok"):
    stations = data["stations"]
    
    # Tabs für die Übersicht
    tabs = st.tabs(["🟢 Super E5", "🟡 Super E10", "⚫ Diesel"])
    
    fuel_map = {"e5": tabs[0], "e10": tabs[1],
