import streamlit as st
from src.styles import apply_global_style

st.set_page_config(page_title="Datenquellen – Privatjet-Tracker", page_icon="🗂️", layout="wide")
apply_global_style()

st.markdown('<div class="title-big">🗂️ Datenquellen</div>', unsafe_allow_html=True)
st.write(
    """
    **Hier kommen später rein:**
    - Quelle(n) für Flugdaten (API/CSV, Lizenz, Abdeckung)
    - Variablenbeschreibung (Start/Ziel, Distanz, CO₂ etc.)
    - Aktualisierungsfrequenz
    - Datenschutz / Transparenzhinweise
    """
)
