import streamlit as st
from src.styles import apply_global_style

st.set_page_config(page_title="Methodik – Privatjet-Tracker", page_icon="🧪", layout="wide")
apply_global_style()

st.markdown('<div class="title-big">🧪 Methodik</div>', unsafe_allow_html=True)
st.write(
    """
    **Hier kommt später rein:**
    - Datenaufbereitung (Cleaning, Missing Values, Outlier)
    - Berechnung von Distanz, Flugzeit, CO₂ (Formeln/Annahmen)
    - Aggregationen (Monat/Jahr)
    - Grenzen & Unsicherheiten der Daten
    """
)
