import pandas as pd

from app.models import SearchRequest

REQUIRED_COLUMNS = {
    "ad_id",
    "manufacturer",
    "model",
    "year",
    "price",
    "km",
    "gearbox",
    "fuel_type",
    "area",
    "owners",
    "title",
    "url",
}


def load_ads(csv_path: str) -> pd.DataFrame:
    df = pd.read_csv(csv_path)

    missing = REQUIRED_COLUMNS - set(df.columns)
    if missing:
        raise ValueError(f"CSV missing required columns: {sorted(missing)}")

    for col in ["manufacturer", "model", "gearbox", "fuel_type", "area", "title", "url"]:
        df[col] = df[col].astype(str).str.strip()

    for col in ["year", "price", "km", "owners"]:
        df[col] = pd.to_numeric(df[col], errors="coerce")
    if "engine_volume" in df.columns:
        df["engine_volume"] = pd.to_numeric(df["engine_volume"], errors="coerce")

    return df.dropna(subset=["year", "price", "km"])


def apply_hard_filters(df: pd.DataFrame, req: SearchRequest) -> pd.DataFrame:
    hf = req.hard_filters
    out = df[
        (df["manufacturer"].str.lower() == hf.manufacturer.strip().lower())
        & (df["model"].str.lower() == hf.model.strip().lower())
    ]

    if hf.gearbox:
        out = out[out["gearbox"].str.lower() == hf.gearbox.strip().lower()]

    if hf.fuel_type:
        out = out[out["fuel_type"].str.lower() == hf.fuel_type.strip().lower()]

    # Apply this filter only when the source CSV provides engine_volume.
    if hf.engine_volume is not None and "engine_volume" in out.columns:
        out = out[(out["engine_volume"] - hf.engine_volume).abs() <= 0.2]

    return out


def apply_range_filters(df: pd.DataFrame, req: SearchRequest) -> pd.DataFrame:
    rf = req.range_filters
    out = df.copy()

    if rf.year_min is not None:
        out = out[out["year"] >= rf.year_min]
    if rf.year_max is not None:
        out = out[out["year"] <= rf.year_max]

    if rf.price_min is not None:
        out = out[out["price"] >= rf.price_min]
    if rf.price_max is not None:
        out = out[out["price"] <= rf.price_max]

    if rf.km_min is not None:
        out = out[out["km"] >= rf.km_min]
    if rf.km_max is not None:
        out = out[out["km"] <= rf.km_max]

    if rf.owners_max is not None:
        out = out[out["owners"] <= rf.owners_max]

    return out


def _safe_norm(value: float, min_v: float, max_v: float) -> float:
    if max_v <= min_v:
        return 1.0
    return (value - min_v) / (max_v - min_v)


def score_ads(df: pd.DataFrame, req: SearchRequest) -> pd.DataFrame:
    if df.empty:
        return df

    scored = df.copy()

    y_min, y_max = scored["year"].min(), scored["year"].max()
    scored["year_score"] = scored["year"].apply(lambda v: _safe_norm(v, y_min, y_max))

    k_min, k_max = scored["km"].min(), scored["km"].max()
    scored["km_score"] = scored["km"].apply(lambda v: 1 - _safe_norm(v, k_min, k_max))

    owners_series = scored["owners"].fillna(scored["owners"].max())
    o_min, o_max = owners_series.min(), owners_series.max()
    scored["owners_score"] = owners_series.apply(lambda v: 1 - _safe_norm(v, o_min, o_max))

    scored["similarity_score"] = (
        0.45 * scored["km_score"]
        + 0.35 * scored["year_score"]
        + 0.20 * scored["owners_score"]
    )

    return scored.sort_values("similarity_score", ascending=False)


def search_ads(csv_path: str, req: SearchRequest) -> list[dict]:
    df = load_ads(csv_path)
    df = apply_hard_filters(df, req)
    df = apply_range_filters(df, req)
    df = score_ads(df, req)

    limit = max(1, min(req.result_limit, 50))
    df = df.head(limit)

    fields = [
        "ad_id",
        "title",
        "manufacturer",
        "model",
        "year",
        "price",
        "km",
        "gearbox",
        "fuel_type",
        "area",
        "owners",
        "url",
        "similarity_score",
    ]

    for field in fields:
        if field not in df.columns:
            df[field] = None

    out = df[fields].copy()
    out["similarity_score"] = out["similarity_score"].round(4)
    return out.to_dict(orient="records")
