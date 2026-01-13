import streamlit as st
from src.styles import apply_global_style

st.set_page_config(
    page_title="Privatjet-Tracker",
    page_icon="✈️",
    layout="wide"
)

apply_global_style()

st.title("✈️ Privatjet-Tracker")
st.caption("Data Science Bonusprojekt – interaktive Web-App für Privatjetflüge und CO₂-Kennzahlen")

st.info(
    "Nutze links die Navigation (Streamlit Pages):\n"
    "- 📊 Dashboard\n"
    "- 🧪 Methodik\n"
    "- 🗂️ Datenquellen\n"
    "- ℹ️ About\n\n"
    "Inhalt und echte Daten fügen wir später ein – aktuell sind Platzhalter aktiv."
)
