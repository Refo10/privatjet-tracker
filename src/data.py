import pandas as pd
import numpy as np

def load_flights_placeholder(seed: int = 42) -> pd.DataFrame:
    rng = np.random.default_rng(seed)
    n = 800

    df = pd.DataFrame({
        "date": pd.to_datetime(
            rng.choice(pd.date_range("2019-01-01", "2025-12-31", freq="D"), size=n)
        ),
        "origin": rng.choice(["FRA", "MUC", "BER", "HAM", "CGN"], size=n),
        "destination": rng.choice(["LHR", "CDG", "ZRH", "AMS", "BCN", "FCO"], size=n),
        "distance_km": rng.normal(900, 350, size=n).clip(80, 3500).round(0),
        "flight_time_min": rng.normal(120, 50, size=n).clip(25, 420).round(0),
        "co2_kg": rng.normal(2500, 1200, size=n).clip(200, 12000).round(0),
        "orig_lat": rng.normal(50.0, 2.0, size=n),
        "orig_lon": rng.normal(10.0, 3.0, size=n),
        "dest_lat": rng.normal(48.0, 3.0, size=n),
        "dest_lon": rng.normal(8.0, 4.0, size=n),
    })

    df["year"] = df["date"].dt.year
    df["month"] = df["date"].dt.to_period("M").astype(str)
    return df

# Später: def load_flights_from_csv(path): ...
# Später: def load_flights_from_api(...): ...
