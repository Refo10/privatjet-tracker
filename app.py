import streamlit as st
from src.styles import apply_global_style

st.set_page_config(
    page_title="Privatjet-Tracker",
    page_icon="✈️",
    layout="wide"
)

apply_global_style()

# =======================
# Titel
# =======================
st.markdown('<div class="title-big">✈️ Privatjet-Tracker</div>', unsafe_allow_html=True)

st.markdown(
    '<div class="subtle">'
    'Data-Science-Bonusprojekt – interaktive Web-App zur Analyse von Privatjetflügen '
    'und deren CO₂-Emissionen'
    '</div>',
    unsafe_allow_html=True
)

st.divider()

# =======================
# Einleitung
# =======================
st.markdown(
    """
    **Willkommen im Privatjet-Tracker.**

    Diese Anwendung visualisiert Privatjet-Flüge anhand eines strukturierten Datensatzes
    und stellt deren ökologische Auswirkungen über Karten, Kennzahlen und Diagramme dar.
    """
)

st.info(
    "👉 **Nutze die Navigation links**, um zum **Dashboard** oder zu den **Datenquellen** zu gelangen."
)

st.markdown(
    """
    **Funktionen im Überblick:**
    - 📊 Interaktive Kennzahlen zu Flügen und CO₂-Emissionen  
    - 🗺️ Weltweite Flugrouten auf einer interaktiven Karte  
    - 🔄 Umschaltung zwischen Standard-Datensatz und hochgeladenen CSV-Dateien  
    - 🗂️ Transparente Darstellung der verwendeten Daten  
    """
)
