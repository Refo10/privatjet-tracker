import pandas as pd

def compute_kpis(df: pd.DataFrame):
    flights = len(df)
    avg_distance = float(df["distance_km"].mean()) if flights else 0.0
    total_co2_t = float(df["co2_kg"].sum()) / 1000 if flights else 0.0
    avg_duration = float(df["flight_time_min"].mean()) if flights else 0.0
    return flights, avg_distance, total_co2_t, avg_duration

def compare_to_small_city(total_co2_t: float):
    # Platzhalterwert – später ersetzen wir das mit echter Quelle
    small_city_t_per_year = 50_000.0
    share = (total_co2_t / small_city_t_per_year * 100) if small_city_t_per_year else 0.0
    return small_city_t_per_year, share
