import pandas as pd

def compute_kpis(df: pd.DataFrame):
    flights = len(df)
    avg_distance = float(df["distance_km"].mean()) if flights else 0.0
    total_co2_t = float(df["co2_kg"].sum()) / 1000 if flights else 0.0
    avg_duration = float(df["flight_time_min"].mean()) if flights else 0.0
    return flights, avg_distance, total_co2_t, avg_duration

def compare_to_small_city(total_co2_t: float, population: int = 15000, per_capita_t: float = 8.5):
    """
    Vergleich: Privatjet-CO₂ (in Tonnen) vs. jährliche CO₂-Emissionen einer deutschen Kleinstadt.
    Kleinstadt: typischerweise 5.000–20.000 Einwohner.
    """
    small_city_total_t = population * per_capita_t
    share_percent = (total_co2_t / small_city_total_t * 100) if small_city_total_t > 0 else 0.0
    return small_city_total_t, share_percent
