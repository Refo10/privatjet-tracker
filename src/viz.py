import pydeck as pdk
import altair as alt
import pandas as pd

def make_map(df: pd.DataFrame):
    layer = pdk.Layer(
    "ArcLayer",
    data=df.sample(min(len(df), 300), random_state=1),
    get_source_position=["orig_lon", "orig_lat"],
    get_target_position=["dest_lon", "dest_lat"],

    # ✅ Farbe: Grün (RGB + Alpha)
    get_source_color=[0, 200, 0, 160],
    get_target_color=[0, 200, 0, 160],

    get_width=2,
    pickable=True,
    auto_highlight=True,
)


    view_state = pdk.ViewState(latitude=50.5, longitude=10.5, zoom=3.4, pitch=30)

    tooltip = {
        "html": "<b>{origin}</b> → <b>{destination}</b><br/>"
                "Distanz: {distance_km} km<br/>"
                "CO₂: {co2_kg} kg<br/>"
                "Datum: {date_str}",
        "style": {"fontSize": "12px"},
    }

    return pdk.Deck(layers=[layer], initial_view_state=view_state, tooltip=tooltip)

def chart_flights_per_month(df: pd.DataFrame):
    flights_month = df.groupby("month").size().reset_index(name="flights")
    return (
        alt.Chart(flights_month)
        .mark_line(point=True)
        .encode(
            x=alt.X("month:N", title="Monat", sort=None),
            y=alt.Y("flights:Q", title="Anzahl Flüge"),
            tooltip=["month", "flights"],
        )
        .properties(height=280)
    )

def chart_co2_by_year(df: pd.DataFrame):
    co2_year = df.groupby("year")["co2_kg"].sum().reset_index()
    co2_year["co2_t"] = co2_year["co2_kg"] / 1000
    return (
        alt.Chart(co2_year)
        .mark_bar()
        .encode(
            x=alt.X("year:O", title="Jahr"),
            y=alt.Y("co2_t:Q", title="CO₂ (t)"),
            tooltip=["year", alt.Tooltip("co2_t:Q", format=",.0f")],
        )
        .properties(height=280)
    )
