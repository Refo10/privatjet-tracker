import streamlit as st
from src.styles import apply_global_style

st.set_page_config(page_title="About – Privatjet-Tracker", page_icon="ℹ️", layout="wide")
apply_global_style()

st.markdown('<div class="title-big">ℹ️ About</div>', unsafe_allow_html=True)
st.write(
    """
    **Projektziel:** Privatjet-Flugaktivitäten visualisieren und ökologische Auswirkungen verständlich machen.  
    **Tech-Stack:** Python, Pandas, Streamlit, PyDeck, Altair  
    **Status:** UI steht, Daten & Inhalte folgen.
    """
)
