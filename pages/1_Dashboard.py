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
    load_default_csv,
)
from src.metrics import compute_kpis, compare_to_small_city
from src.viz import make_map, chart_flights_per_month, chart_co2_by_year

# ✅ Muss ganz oben stehen
st.set_page_config(page_title="Dashboard – Privatjet-Tracker", page_icon="📊", layout="wide")
apply_global_style()

# =======================
# Header
# =======================
left, right = st.columns([3, 1])
with left:
    st.markdown('<div class="title-big">✈️ Privatjet-Tracker – Dashboard</div>', unsafe_allow_html=True)
    st.markdown('<div class="subtle">Interaktive Visualisierung von Privatjetflügen & CO₂-Kennzahlen</div>', unsafe_allow_html=True)
    st.caption("Datensatz: Privatjet-Flüge von Drake (N767CJ) – basierend auf öffentlich zugänglichen Informationen.")
with right:
    st.markdown('<div class="pill">Python • Pandas • Streamlit</div>', unsafe_allow_html=True)

# =======================
# Sidebar (Daten & Filter)
# =======================
st.sidebar.header("Daten & Filter")
uploaded = st.sidebar.file_uploader("CSV hochladen", type=["csv"])
use_demo = st.sidebar.toggle("Demo-Daten verwenden", value=(uploaded is None))

df_all = None

if uploaded is not None and not use_demo:
    try:
        raw = read_csv_any(uploaded)
        raw = normalize_column_names(raw)

        # Auto-Mapping Vorschlag
        mapping_guess = auto_map_columns(raw)

        st.sidebar.subheader("Spalten-Mapping (optional anpassen)")
        mapping = {}
        targets = [
            "date", "origin", "destination",
            "distance_km", "flight_time_min", "co2_kg",
            "orig_lat", "orig_lon", "dest_lat", "dest_lon"
        ]

        for target in targets:
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
    try:
        df_all = load_default_csv()
        st.sidebar.caption("Standard-Datensatz: Drake (N767CJ)")
    except Exception as e:
        st.warning("Standard-CSV konnte nicht geladen werden – Demo-Daten aktiv.")
        df_all = load_flights_placeholder()


# =======================
# Absicherung
# =======================
if df_all is None or len(df_all) == 0:
    st.warning("Keine Daten verfügbar – Demo-Daten werden geladen.")
    df_all = load_flights_placeholder()

df = df_all.copy()

# Optional: Debug (wenn es läuft, kannst du die nächsten 2 Zeilen löschen)
# st.write("DEBUG: Anzahl Zeilen:", len(df))
# st.dataframe(df.head(), use_container_width=True)

# =======================
# Jahresfilter (optional)
# =======================
year_min, year_max = int(df["year"].min()), int(df["year"].max())
year_mode = st.sidebar.radio("Jahresauswahl", ["Alle Jahre", "Ein Jahr"], index=0)

if year_mode == "Ein Jahr":
    year_selected = st.sidebar.slider("Jahr", year_min, year_max, year_max)
    df = df[df["year"] == year_selected].copy()

# =======================
# KPI-Kacheln
# =======================
flights, avg_distance, total_co2_t, avg_duration = compute_kpis(df)

k1, k2, k3, k4 = st.columns(4)
k1.metric("Flüge", f"{flights:,}".replace(",", "."))
k2.metric("Ø Distanz", f"{avg_distance:,.0f} km".replace(",", "."))
k3.metric("Gesamt-CO₂", f"{total_co2_t:,.0f} t".replace(",", "."))
k4.metric("Ø Flugdauer", f"{avg_duration:,.0f} min".replace(",", "."))

st.divider()

# =======================
# Karte (PyDeck)
# =======================
st.markdown("### Flugroutenkarte (interaktiv)")
deck = make_map(df)
st.pydeck_chart(deck, use_container_width=True)

st.divider()

# =======================
# Diagramme
# =======================
c1, c2 = st.columns(2)

with c1:
    st.markdown("### Flüge pro Monat")
    st.altair_chart(chart_flights_per_month(df), use_container_width=True)

with c2:
    st.markdown("### CO₂-Trend über Jahre")
    st.altair_chart(chart_co2_by_year(df), use_container_width=True)

st.divider()

# =======================
# Vergleich: Emissionen vs. Kleinstadt
# =======================
st.markdown("### Vergleich: Emissionen vs. Kleinstadt")
small_city_t, share = compare_to_small_city(total_co2_t)

colA, colB = st.columns([2, 1])
with colA:
    st.write("Platzhalter: später kommt hier ein sauber belegter Vergleich inkl. Quelle.")
    st.info(
        f"Demo: Kleinstadt = {small_city_t:,.0f} t CO₂/Jahr → Privatjet-Flüge ~{share:,.2f}% davon."
        .replace(",", ".")
    )
with colB:
    st.progress(min(max(share / 100, 0), 1), text=f"Anteil: {share:,.2f}%".replace(",", "."))

# =======================
# Datenvorschau
# =======================
with st.expander("🔎 Datenvorschau (Debug)"):
    st.dataframe(df.head(50), use_container_width=True)
