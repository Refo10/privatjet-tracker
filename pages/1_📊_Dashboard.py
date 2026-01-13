import streamlit as st
from src.styles import apply_global_style
from src.data import load_flights_placeholder
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

st.sidebar.header("Filter & Ansicht")

df_all = load_flights_placeholder()

year_min, year_max = int(df_all["year"].min()), int(df_all["year"].max())
year_mode = st.sidebar.radio("Jahresauswahl", ["Alle Jahre", "Ein Jahr"], index=0)

if year_mode == "Ein Jahr":
    year_selected = st.sidebar.slider("Jahr", year_min, year_max, year_max)
    df = df_all[df_all["year"] == year_selected].copy()
else:
    year_selected = None
    df = df_all.copy()

st.sidebar.caption("Aktuell Demo-Daten. Echte Daten kommen später.")

# KPIs
flights, avg_distance, total_co2_t, avg_duration = compute_kpis(df)
k1, k2, k3, k4 = st.columns(4)
k1.metric("Flüge", f"{flights:,}".replace(",", "."))
k2.metric("Ø Distanz", f"{avg_distance:,.0f} km".replace(",", "."))
k3.metric("Gesamt-CO₂", f"{total_co2_t:,.0f} t".replace(",", "."))
k4.metric("Ø Flugdauer", f"{avg_duration:,.0f} min".replace(",", "."))

st.divider()

# Map
st.markdown('<div class="section-title">Flugroutenkarte (interaktiv)</div>', unsafe_allow_html=True)
deck = make_map(df)
st.pydeck_chart(deck, use_container_width=True)

st.divider()

# Charts
c1, c2 = st.columns(2)
with c1:
    st.markdown('<div class="section-title">Diagramm: Flüge pro Monat</div>', unsafe_allow_html=True)
    st.altair_chart(chart_flights_per_month(df), use_container_width=True)

with c2:
    st.markdown('<div class="section-title">Diagramm: CO₂-Trend über Jahre</div>', unsafe_allow_html=True)
    st.altair_chart(chart_co2_by_year(df), use_container_width=True)

st.divider()

# Comparison
st.markdown('<div class="section-title">Vergleich: Emissionen vs. Kleinstadt</div>', unsafe_allow_html=True)
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

with st.expander("🔎 Datenvorschau (Debug)"):
    st.dataframe(df.head(30), use_container_width=True)
