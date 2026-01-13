import streamlit as st
from src.styles import apply_global_style
from src.data import (
    load_flights_placeholder,
    read_csv_any,
    normalize_column_names,
    auto_map_columns,
    apply_mapping,
    validate_flights_df,
    finalize_df,
)
from src.metrics import compute_kpis, compare_to_small_city
from src.viz import make_map, chart_flights_per_month, chart_co2_by_year

st.set_page_config(page_title="Dashboard – Privatjet-Tracker", page_icon="📊", layout="wide")
apply_global_style()

# Header
left, right = st.columns([3, 1])
with left:
    st.markdown('<div class="title-big">✈️ Privatjet-Tracker – Dashboard</div>', unsafe_allow_html=True)
    st.markdown('<div class="subtle">Interaktive Visualisierung von Privatjetflügen & CO₂-Kennzahlen</div>', unsafe_allow_html=True)
with right:
    st.markdown('<div class="pill">Python • Pandas • Streamlit</div>', unsafe_allow_html=True)

# Sidebar
st.sidebar.header("Daten & Filter")

uploaded = st.sidebar.file_uploader("CSV hochladen", type=["csv"])

use_demo = st.sidebar.toggle("Demo-Daten verwenden", value=(uploaded is None))

df_all = None

if uploaded is not None and not use_demo:
    try:
        raw = read_csv_any(uploaded)
        raw = normalize_column_names(raw)

        # Auto-Mapping
        mapping_guess = auto_map_columns(raw)

        st.sidebar.subheader("Spalten-Mapping (optional anpassen)")
        mapping = {}
        for target in [
            "date", "origin", "destination", "distance_km", "flight_time_min", "co2_kg",
            "orig_lat", "orig_lon", "dest_lat", "dest_lon"
        ]:
            options = ["— nicht zugeordnet —"] + list(raw.columns)
            default = mapping_guess.get(target, "— nicht zugeordnet —")
            default_index = options.index(default) if default in options else 0
            choice = st.sidebar.selectbox(f"{target}  →", options, index=default_index)
            if choice != "— nicht zugeordnet —":
                mapping[target] = choice

        mapped = apply_mapping(raw, mapping)
        ok, errors = validate_flights_df(mapped)

        if not ok:
            st.sidebar.error("CSV erkannt, aber noch nicht valide.")
            for e in errors:
                st.sidebar.write(f"• {e}")
            st.warning("Bitte Mapping/CSV korrigieren – oder Demo-Daten aktivieren.")
            df_all = load_flights_placeholder()
        else:
            df_all = finalize_df(mapped)
            st.sidebar.success(f"CSV geladen: {len(df_all):,} Flüge".replace(",", "."))

    except Exception as e:
        st.sidebar.error(f"Fehler beim Laden: {e}")
        df_all = load_flights_placeholder()
else:
    df_all = load_flights_placeholder()
    st.sidebar.caption("Aktuell Demo-Daten aktiv.")
