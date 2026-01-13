import streamlit as st
import pandas as pd

from src.styles import apply_global_style

# Seiten-Config
st.set_page_config(
    page_title="Datenquellen – Privatjet-Tracker",
    page_icon="🗂️",
    layout="wide"
)

apply_global_style()

# =======================
# Titel
# =======================
st.markdown('<div class="title-big">🗂️ Datenquellen</div>', unsafe_allow_html=True)

st.write(
    """
    Die in dieser Anwendung verwendeten Flugdaten basieren auf **öffentlich zugänglichen Informationen**
    und wurden für Analyse- und Visualisierungszwecke strukturiert aufbereitet.
    """
)

st.divider()

# =======================
# CSV laden
# =======================
CSV_PATH = "data/drake_flights.csv"

try:
    df = pd.read_csv(CSV_PATH)

    st.success("Standard-Datensatz erfolgreich geladen.")

    st.markdown("### Inhalt des verwendeten Datensatzes")

    st.caption(
        "Der folgende Tabellenausschnitt zeigt die Rohdaten, die im Dashboard "
        "für die Berechnung von Kennzahlen, Karten und Diagrammen verwendet werden."
    )

    # Tabelle anzeigen
    st.dataframe(
        df,
        use_container_width=True,
        height=600
    )

    st.markdown("### Beschreibung der Spalten")

    st.markdown(
        """
        - **date** – Flugdatum  
        - **origin** – Startflughafen  
        - **destination** – Zielflughafen  
        - **distance_km** – Flugdistanz in Kilometern  
        - **flight_time_min** – Flugdauer in Minuten  
        - **co2_kg** – Geschätzte CO₂-Emissionen in Kilogramm  
        - **orig_lat / orig_lon** – Koordinaten des Startflughafens  
        - **dest_lat / dest_lon** – Koordinaten des Zielflughafens  
        """
    )

except FileNotFoundError:
    st.error(
        "Die CSV-Datei konnte nicht gefunden werden. "
        "Bitte stelle sicher, dass sich die Datei unter `data/drake_flights.csv` befindet."
    )
