import pandas as pd
import numpy as np

REQUIRED_COLUMNS = [
    "date",
    "origin", "destination",
    "distance_km",
    "flight_time_min",
    "co2_kg",
    "orig_lat", "orig_lon",
    "dest_lat", "dest_lon",
]

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

    df = enrich_time_cols(df)
    return df

def enrich_time_cols(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    df["date"] = pd.to_datetime(df["date"], errors="coerce")
    df = df.dropna(subset=["date"])
    df["date_str"] = df["date"].dt.strftime("%Y-%m-%d")  # ✅ neu
    df["year"] = df["date"].dt.year
    df["month"] = df["date"].dt.to_period("M").astype(str)
    return df

def read_csv_any(uploaded_file) -> pd.DataFrame:
    """
    Liest CSV robust ein (Delimiter/Encoding wird grob abgefedert).
    """
    # Versuch 1: Standard
    try:
        return pd.read_csv(uploaded_file)
    except Exception:
        pass

    # Versuch 2: Semikolon (deutsche CSV)
    uploaded_file.seek(0)
    try:
        return pd.read_csv(uploaded_file, sep=";")
    except Exception as e:
        raise ValueError(f"CSV konnte nicht gelesen werden: {e}")

def normalize_column_names(df: pd.DataFrame) -> pd.DataFrame:
    """
    Normalisiert Spaltennamen (klein, trim, spaces->underscore)
    """
    df = df.copy()
    df.columns = (
        df.columns.astype(str)
        .str.strip()
        .str.lower()
        .str.replace(" ", "_")
        .str.replace("-", "_")
    )
    return df

def auto_map_columns(df: pd.DataFrame) -> dict:
    """
    Einfaches Auto-Mapping gängiger Varianten -> Zielspalten.
    Du kannst später weitere Synonyme ergänzen.
    """
    candidates = {
        "date": ["date", "datetime", "timestamp", "flight_date", "time"],
        "origin": ["origin", "from", "dep", "departure", "departure_airport", "orig"],
        "destination": ["destination", "to", "arr", "arrival", "arrival_airport", "dest"],
        "distance_km": ["distance_km", "distance", "km", "great_circle_km"],
        "flight_time_min": ["flight_time_min", "duration_min", "duration", "minutes", "flight_minutes"],
        "co2_kg": ["co2_kg", "co2", "emissions_kg", "emission_kg", "co2e_kg", "co2e"],
        "orig_lat": ["orig_lat", "origin_lat", "from_lat", "dep_lat", "latitude_origin"],
        "orig_lon": ["orig_lon", "origin_lon", "from_lon", "dep_lon", "longitude_origin"],
        "dest_lat": ["dest_lat", "destination_lat", "to_lat", "arr_lat", "latitude_destination"],
        "dest_lon": ["dest_lon", "destination_lon", "to_lon", "arr_lon", "longitude_destination"],
    }

    mapping = {}
    cols = set(df.columns)
    for target, syns in candidates.items():
        for s in syns:
            if s in cols:
                mapping[target] = s
                break
    return mapping

def apply_mapping(df: pd.DataFrame, mapping: dict) -> pd.DataFrame:
    """
    Benennt Spalten gemäß mapping um.
    mapping: {zielspalte: aktuelle_spalte}
    """
    rename_dict = {v: k for k, v in mapping.items()}
    out = df.rename(columns=rename_dict).copy()
    return out

def validate_flights_df(df: pd.DataFrame) -> tuple[bool, list[str]]:
    errors = []
    missing = [c for c in REQUIRED_COLUMNS if c not in df.columns]
    if missing:
        errors.append(f"Fehlende Spalten: {', '.join(missing)}")

    if "date" in df.columns:
        tmp = pd.to_datetime(df["date"], errors="coerce")
        if tmp.isna().mean() > 0.2:
            errors.append("Viele ungültige Datumswerte in 'date' (mehr als 20%).")

    # Plausibilitäten (nur leicht, um Nutzer nicht zu nerven)
    for col, low, high in [
        ("distance_km", 1, 20000),
        ("flight_time_min", 1, 2000),
        ("co2_kg", 0, 500000),
    ]:
        if col in df.columns:
            numeric = pd.to_numeric(df[col], errors="coerce")
            if numeric.isna().mean() > 0.3:
                errors.append(f"Viele ungültige Werte in '{col}' (mehr als 30%).")
            else:
                if (numeric < low).mean() > 0.1:
                    errors.append(f"Unplausible Werte: '{col}' häufig < {low}.")
                if (numeric > high).mean() > 0.05:
                    errors.append(f"Unplausible Werte: '{col}' teils > {high}.")

    ok = len(errors) == 0
    return ok, errors

def finalize_df(df: pd.DataFrame) -> pd.DataFrame:
    """
    Typen setzen, Zeitspalten erzeugen.
    """
    df = df.copy()
    df["distance_km"] = pd.to_numeric(df["distance_km"], errors="coerce")
    df["flight_time_min"] = pd.to_numeric(df["flight_time_min"], errors="coerce")
    df["co2_kg"] = pd.to_numeric(df["co2_kg"], errors="coerce")

    for c in ["orig_lat", "orig_lon", "dest_lat", "dest_lon"]:
        df[c] = pd.to_numeric(df[c], errors="coerce")

    df = enrich_time_cols(df)
    df = df.dropna(subset=["orig_lat", "orig_lon", "dest_lat", "dest_lon"])
    return df

def load_default_csv() -> pd.DataFrame:
    df = pd.read_csv("data/drake_flights.csv")
    df = normalize_column_names(df)
    df = finalize_df(df)
    return df

