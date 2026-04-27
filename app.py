import streamlit as st
import requests

# 1. SETUP
st.set_page_config(page_title="Wiesmoor Radar", page_icon="⛽")
API_KEY = "616cbb8e-9dde-4eb7-91f1-21a1663fa495"

st.markdown('<div style="background:#e2001a;color:white;padding:20px;text-align:center;border-radius:15px;font-weight:bold;font-size:1.4rem;">⛽ WIESMOOR LIVE-RADAR</div>', unsafe_allow_html=True)

# 2. EINFACHE DATEN-FUNKTION (Ohne kompliziertes Caching)
def get_data():
    url = f"https://creativecommons.tankerkoenig.de/json/list.php?lat=53.414&lng=7.733&rad=15&sort=dist&type=all&apikey={API_KEY}"
    try:
        r = requests.get(url, timeout=8)
        return r.json().get("stations")
    except:
        return None

stations = get_data()

if stations:
    t1, t2, t3 = st.tabs(["Super E5", "Super E10", "Diesel"])
    modes = {"Super E5": "e5", "Super E10": "e10", "Diesel": "diesel"}
    
    for tab, (label, key) in zip([t1, t2, t3], modes.items()):
        with tab:
            # Sortieren nach Preis
            valid = sorted([s for s in stations if s.get(key)], key=lambda x: x[key])
            
            for s in valid:
                name = s["brand"] if s["brand"] else s["name"]
                # Decker Check
                is_decker = "decker" in (name + s["street"]).lower()
                
                # Design-Box
                bg = "#eef6ff" if is_decker else "white"
                border = "#004a99" if is_decker else "#e2001a"
                
                st.markdown(f'''
                <div style="background:{bg}; padding:12px; border-radius:10px; margin-top:8px; border-left:6px solid {border}; display:flex; justify-content:space-between; align-items:center; box-shadow: 1px 1px 3px rgba(0,0,0,0.1);">
                    <div><b>{"⭐ " if is_decker else ""}{name}</b><br><small>{s["place"]}</small></div>
                    <div style="font-weight:bold; font-size:1.2rem;">{s[key]:.2f} €</div>
                </div>
                ''', unsafe_allow_html=True)
                
                # Öffnungszeiten OHNE Button (direkt beim Aufklappen)
                with st.expander("🕒 Status & Info"):
                    st.write(f"**Aktuell:** {'🟢 OFFEN' if s['isOpen'] else '🔴 GESCHLOSSEN'}")
                    st.write(f"**Adresse:** {s['street']}, {s['place']}")
                    st.caption("Detail-Wochenpläne sind bei Automaten-Stationen oft nicht verfügbar.")

else:
    st.error("Daten konnten nicht geladen werden. Bitte Seite neu laden.")

st.write("---")
if st.button("📞 Gebr. Decker anrufen"):
    st.success("Tel: 04948 91990")
