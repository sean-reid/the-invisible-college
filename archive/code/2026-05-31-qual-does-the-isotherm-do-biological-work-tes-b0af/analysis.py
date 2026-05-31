"""
Does the Isotherm Do Biological Work?
Full analysis: GBIF occurrences + elevation API + ERA5 lapse rates
+ Bray-Curtis assemblage turnover + isotherm vs altitude test.

Mountains:
  Wet regime (Ecuador): Chimborazo, Cotopaxi
  Dry regime (Peru):    Misti,      Chachani

Author: Alexander von Humboldt, Invisible College
Date:   2026-05-31
"""

import requests, time, json, math, random, os
import numpy as np
import pandas as pd

# ─── CONFIG ───────────────────────────────────────────────────────────────────

MOUNTAINS = [
    {"name": "Chimborazo", "lat": -1.47,  "lon": -78.82, "regime": "wet",  "max_elev": 6268},
    {"name": "Cotopaxi",   "lat": -0.68,  "lon": -78.44, "regime": "wet",  "max_elev": 5897},
    {"name": "Misti",      "lat": -16.29, "lon": -71.41, "regime": "dry",  "max_elev": 5822},
    {"name": "Chachani",   "lat": -16.19, "lon": -71.53, "regime": "dry",  "max_elev": 6075},
]

RADIUS_KM        = 40
MAX_GBIF_RECORDS = 2000
ELEV_BAND_M      = 100   # 100m bands for Bray-Curtis
MIN_BAND_RECORDS = 8     # minimum records in a band to include it
BRAY_THRESH_PCT  = 80    # percentile above which a band boundary is a candidate zone boundary

RANDOM_SEED = 42
random.seed(RANDOM_SEED)
np.random.seed(RANDOM_SEED)

# ─── UTILITIES ────────────────────────────────────────────────────────────────

def haversine(lat1, lon1, lat2, lon2):
    R = 6371.0
    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)
    a = (math.sin(dlat/2)**2
         + math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * math.sin(dlon/2)**2)
    return R * 2 * math.asin(min(1.0, math.sqrt(a)))

def random_point_in_circle(center_lat, center_lon, radius_km):
    """Uniform random sample inside a circle."""
    r = radius_km * math.sqrt(random.random())
    theta = random.uniform(0, 2 * math.pi)
    dlat = r * math.cos(theta) / 111.0
    dlon = r * math.sin(theta) / (111.0 * math.cos(math.radians(center_lat)))
    return center_lat + dlat, center_lon + dlon

def save_json(data, path):
    with open(path, "w") as f:
        json.dump(data, f)

def load_json(path):
    with open(path) as f:
        return json.load(f)

# ─── PHASE 1: GBIF OCCURRENCE RECORDS ─────────────────────────────────────────

def fetch_gbif_for_mountain(m):
    cache = f"cache_gbif_{m['name']}.json"
    if os.path.exists(cache):
        print(f"  {m['name']}: loading from cache")
        return load_json(cache)

    print(f"  {m['name']}: querying GBIF ...")
    radius_deg = RADIUS_KM / 111.0
    records = []
    offset = 0
    limit = 300

    while len(records) < MAX_GBIF_RECORDS:
        params = {
            'decimalLatitude':  f"{m['lat']-radius_deg},{m['lat']+radius_deg}",
            'decimalLongitude': f"{m['lon']-radius_deg},{m['lon']+radius_deg}",
            'kingdomKey': 6,           # Plantae
            'hasCoordinate': 'true',
            'hasGeospatialIssue': 'false',
            'limit': limit,
            'offset': offset,
        }
        try:
            r = requests.get('https://api.gbif.org/v1/occurrence/search',
                             params=params, timeout=30)
            data = r.json()
        except Exception as e:
            print(f"    GBIF error at offset {offset}: {e}")
            break

        batch = data.get('results', [])
        # Filter to strict circle
        batch = [
            rec for rec in batch
            if rec.get('decimalLatitude') is not None
            and haversine(m['lat'], m['lon'],
                          rec['decimalLatitude'], rec['decimalLongitude']) <= RADIUS_KM
        ]
        records.extend(batch)

        if len(data.get('results', [])) < limit:
            break  # exhausted
        offset += limit
        time.sleep(0.4)

    print(f"    → {len(records)} records after circle filter")
    # Keep only what we need
    slim = [
        {'lat': rec['decimalLatitude'],
         'lon': rec['decimalLongitude'],
         'speciesKey': rec.get('speciesKey') or rec.get('taxonKey'),
         'species': rec.get('species') or rec.get('scientificName', 'unknown')}
        for rec in records
        if rec.get('speciesKey') or rec.get('taxonKey')
    ]
    save_json(slim, cache)
    return slim

# ─── PHASE 2: ELEVATION VIA OPEN-ELEVATION API ─────────────────────────────────

def fetch_elevations(points, batch_size=100):
    """
    points: list of {"lat": x, "lon": y, ...}
    Returns same list with "elev" added (or None on failure).
    Uses open-elevation.com SRTM API.
    """
    results = list(points)  # copy to avoid mutation
    for i in range(0, len(results), batch_size):
        batch = results[i : i + batch_size]
        locations = [{"latitude": p["lat"], "longitude": p["lon"]} for p in batch]
        try:
            r = requests.post(
                "https://api.open-elevation.com/api/v1/lookup",
                json={"locations": locations},
                timeout=45
            )
            resp = r.json()
            for j, item in enumerate(resp.get("results", [])):
                results[i + j]["elev"] = item.get("elevation")
        except Exception as e:
            print(f"    elevation API error (batch {i//batch_size}): {e}")
            for j in range(len(batch)):
                results[i + j]["elev"] = None
        time.sleep(0.5)
    return results

def add_elevations_to_records(m, records):
    cache = f"cache_elev_{m['name']}.json"
    if os.path.exists(cache):
        print(f"  {m['name']}: loading elevations from cache")
        return load_json(cache)

    print(f"  {m['name']}: fetching elevations for {len(records)} records ...")
    enriched = fetch_elevations(records, batch_size=100)
    # Drop records without elevation or with unreasonable values
    enriched = [r for r in enriched
                if r.get("elev") is not None and 0 < r["elev"] < 7000]
    print(f"    → {len(enriched)} records with valid elevation")
    save_json(enriched, cache)
    return enriched

# ─── PHASE 3: EMPIRICAL LAPSE RATE ────────────────────────────────────────────

def fetch_annual_mean_temp(lat, lon):
    """
    Get mean annual temperature at (lat, lon) using ERA5 via open-meteo archive.
    Uses 2010-2019 for computational tractability.
    """
    try:
        r = requests.get(
            "https://archive-api.open-meteo.com/v1/archive",
            params={
                'latitude': lat,
                'longitude': lon,
                'start_date': '2010-01-01',
                'end_date': '2019-12-31',
                'daily': 'temperature_2m_mean',
                'timezone': 'UTC',
            },
            timeout=60
        )
        data = r.json()
        temps = data.get('daily', {}).get('temperature_2m_mean', [])
        temps = [t for t in temps if t is not None]
        if temps:
            return float(np.mean(temps))
    except Exception as e:
        print(f"    ERA5 error at ({lat:.2f},{lon:.2f}): {e}")
    return None

def compute_lapse_rate(m):
    """
    Sample 50 random points in the circle, get their elevation,
    pick 12 that span the widest elevation range, get ERA5 temperature,
    regress T ~ elevation to get lapse rate.
    """
    cache = f"cache_lapse_{m['name']}.json"
    if os.path.exists(cache):
        print(f"  {m['name']}: loading lapse rate from cache")
        return load_json(cache)

    print(f"  {m['name']}: computing empirical lapse rate ...")

    # Sample 50 candidate points (include the peak itself)
    candidates = [{"lat": m["lat"], "lon": m["lon"]}]
    for _ in range(49):
        la, lo = random_point_in_circle(m["lat"], m["lon"], RADIUS_KM)
        candidates.append({"lat": la, "lon": lo})

    # Get elevations
    candidates = fetch_elevations(candidates, batch_size=50)
    valid = [c for c in candidates if c.get("elev") is not None]

    # Sort by elevation and pick 12 spanning the range
    valid.sort(key=lambda x: x["elev"])
    if len(valid) < 5:
        print(f"    WARNING: only {len(valid)} valid elevation points")
        result = {"lr": None, "n": 0, "r2": None, "points": []}
        save_json(result, cache)
        return result

    # Pick 12 evenly spaced by elevation rank
    n_sample = min(12, len(valid))
    indices = np.linspace(0, len(valid)-1, n_sample, dtype=int)
    selected = [valid[i] for i in indices]

    # Get annual mean temperature for each
    print(f"    fetching ERA5 temperatures for {n_sample} points ...")
    for pt in selected:
        pt["temp"] = fetch_annual_mean_temp(pt["lat"], pt["lon"])
        time.sleep(1.0)

    # Regress T ~ elevation
    pts = [(p["elev"], p["temp"]) for p in selected if p.get("temp") is not None]
    if len(pts) < 4:
        print(f"    WARNING: only {len(pts)} temperature points")
        result = {"lr": None, "n": len(pts), "r2": None, "points": pts}
        save_json(result, cache)
        return result

    elevs = np.array([p[0] for p in pts])
    temps = np.array([p[1] for p in pts])
    # np.polyfit: T = slope_per_m * elev + intercept
    coeffs = np.polyfit(elevs, temps, 1)
    slope_per_m = coeffs[0]
    intercept = coeffs[1]
    residuals = temps - (slope_per_m * elevs + intercept)
    ss_res = np.sum(residuals**2)
    ss_tot = np.sum((temps - np.mean(temps))**2)
    r2 = 1 - ss_res/ss_tot if ss_tot > 0 else 0

    lr_per_1000m = -slope_per_m * 1000  # positive: temperature drops with elevation
    # Standard error on slope from regression
    n = len(pts)
    mse = ss_res / max(n - 2, 1)
    sx2 = np.sum((elevs - elevs.mean())**2)
    se_slope = math.sqrt(mse / sx2) if sx2 > 0 else 0
    se_per_1000m = se_slope * 1000

    print(f"    lapse rate = {lr_per_1000m:.2f} ± {se_per_1000m:.2f} °C/1000m, R²={r2:.3f}")

    result = {
        "lr": lr_per_1000m,
        "se": se_per_1000m,
        "intercept": intercept,
        "r2": r2,
        "n": len(pts),
        "points": pts,
    }
    save_json(result, cache)
    return result

# ─── PHASE 4: BRAY-CURTIS DISSIMILARITY ──────────────────────────────────────

def bray_curtis(u, v):
    """Bray-Curtis dissimilarity between two presence-absence vectors."""
    u = np.array(u, dtype=float)
    v = np.array(v, dtype=float)
    if u.sum() + v.sum() == 0:
        return 0.0
    return 1.0 - 2.0 * np.dot(u, v) / (u.sum() + v.sum())

def assemblage_turnover(records, min_elev=None, max_elev=None):
    """
    Bin records into ELEV_BAND_M elevation bands, compute Bray-Curtis
    dissimilarity between adjacent bands.

    Returns a DataFrame with columns: [band_lower, band_upper, bc_dissimilarity]
    where bc_dissimilarity is the dissimilarity between this band and the next higher.
    """
    df = pd.DataFrame(records)
    df = df.dropna(subset=["elev", "speciesKey"])
    df["elev"] = df["elev"].astype(float)
    df["speciesKey"] = df["speciesKey"].astype(str)

    if min_elev is None:
        min_elev = max(0, df["elev"].min() // ELEV_BAND_M * ELEV_BAND_M)
    if max_elev is None:
        max_elev = (df["elev"].max() // ELEV_BAND_M + 1) * ELEV_BAND_M

    bands = np.arange(min_elev, max_elev, ELEV_BAND_M)
    band_labels = [int(b) for b in bands]

    # Build presence-absence matrices: band × species
    all_species = sorted(df["speciesKey"].unique())
    species_idx = {s: i for i, s in enumerate(all_species)}

    band_data = {}  # band_lower → set of species present
    for band_lo in band_labels:
        mask = (df["elev"] >= band_lo) & (df["elev"] < band_lo + ELEV_BAND_M)
        subset = df[mask]
        if len(subset) >= MIN_BAND_RECORDS:
            band_data[band_lo] = set(subset["speciesKey"].unique())

    # Compute Bray-Curtis between adjacent occupied bands
    occupied = sorted(band_data.keys())
    if len(occupied) < 2:
        return pd.DataFrame(columns=["band_lower", "band_upper", "mid_elev", "bc"])

    rows = []
    for i in range(len(occupied) - 1):
        b1, b2 = occupied[i], occupied[i+1]
        sp1 = band_data[b1]
        sp2 = band_data[b2]
        # Jaccard-style presence/absence Bray-Curtis: same formula but with 0/1
        intersection = len(sp1 & sp2)
        total = len(sp1) + len(sp2)
        bc = 1.0 - 2.0 * intersection / total if total > 0 else 0.0
        rows.append({
            "band_lower": b1,
            "band_upper": b2,
            "mid_elev": (b1 + b2) / 2,  # midpoint between adjacent bands
            "n_sp_lo": len(sp1),
            "n_sp_hi": len(sp2),
            "bc": bc,
        })

    return pd.DataFrame(rows)

def find_zone_boundaries(bc_df, percentile=BRAY_THRESH_PCT):
    """
    Find band transitions with BC dissimilarity above the percentile threshold.
    Returns list of (midpoint elevation, bc value) for candidate zone boundaries.
    """
    if bc_df.empty:
        return []
    threshold = np.percentile(bc_df["bc"], percentile)
    peaks = bc_df[bc_df["bc"] >= threshold]
    return [(row["mid_elev"], row["bc"]) for _, row in peaks.iterrows()]

# ─── PHASE 5: ISOTHERM TEST ───────────────────────────────────────────────────

def elev_to_temp(elev, lapse_data):
    """
    Convert elevation to temperature using lapse rate from ERA5.
    Uses: T(elev) = T_ref - lr * (elev - elev_ref) / 1000
    where T_ref and elev_ref come from the regression intercept.
    """
    if lapse_data["lr"] is None:
        return None, None
    # From the regression: T = intercept + slope * elev
    # slope = -lr/1000 (negative because T decreases with elev)
    slope_per_m = -lapse_data["lr"] / 1000.0
    intercept = lapse_data["intercept"]
    temp = intercept + slope_per_m * elev
    # Propagate uncertainty: σ_T = σ_lr/1000 * elev
    temp_se = (lapse_data["se"] / 1000.0) * elev
    return temp, temp_se

def run_isotherm_test(mountain_results):
    """
    For each mountain, convert zone boundary elevations to temperatures.
    Test: does temperature cluster more tightly than elevation across mountains?
    Returns summary dict with CV values and interpretation.
    """
    all_boundaries = []  # list of (mountain_name, regime, boundary_elev, boundary_temp, temp_se)

    for m_name, data in mountain_results.items():
        boundaries = data.get("boundaries", [])
        lapse = data.get("lapse", {})
        regime = data.get("regime", "?")

        for (elev, bc) in boundaries:
            temp, temp_se = elev_to_temp(elev, lapse)
            all_boundaries.append({
                "mountain": m_name,
                "regime": regime,
                "elev": elev,
                "bc": bc,
                "temp": temp,
                "temp_se": temp_se,
            })

    df = pd.DataFrame(all_boundaries)
    return df

# ─── MAIN ─────────────────────────────────────────────────────────────────────

def main():
    print("=" * 60)
    print("Does the Isotherm Do Biological Work?")
    print("=" * 60)

    mountain_results = {}

    # Phase 1 + 2: GBIF + elevation
    print("\n--- Phase 1-2: GBIF records + elevation ---")
    for m in MOUNTAINS:
        records = fetch_gbif_for_mountain(m)
        if not records:
            print(f"  {m['name']}: NO RECORDS - skipping")
            continue

        # Sample to MAX_GBIF_RECORDS if needed
        if len(records) > MAX_GBIF_RECORDS:
            records = random.sample(records, MAX_GBIF_RECORDS)

        enriched = add_elevations_to_records(m, records)
        mountain_results[m["name"]] = {
            "regime": m["regime"],
            "records": enriched,
        }

    # Phase 3: Lapse rates
    print("\n--- Phase 3: Empirical lapse rates ---")
    for m in MOUNTAINS:
        if m["name"] not in mountain_results:
            continue
        lapse = compute_lapse_rate(m)
        mountain_results[m["name"]]["lapse"] = lapse

    # Phase 4: Assemblage turnover
    print("\n--- Phase 4: Bray-Curtis assemblage turnover ---")
    for m_name, data in mountain_results.items():
        records = data["records"]
        if not records:
            print(f"  {m_name}: no records")
            continue

        bc_df = assemblage_turnover(records)
        boundaries = find_zone_boundaries(bc_df, percentile=BRAY_THRESH_PCT)

        print(f"  {m_name}: {len(bc_df)} band pairs, {len(boundaries)} candidate boundaries")
        if not bc_df.empty:
            print(f"    elevation range: {int(bc_df['band_lower'].min())}–"
                  f"{int(bc_df['band_upper'].max())} m")
        for elev, bc in sorted(boundaries):
            print(f"    boundary at {elev:.0f} m, BC={bc:.3f}")

        mountain_results[m_name]["bc_df"] = bc_df.to_dict('records')
        mountain_results[m_name]["boundaries"] = boundaries

    # Phase 5: Isotherm test
    print("\n--- Phase 5: Isotherm hypothesis test ---")
    boundary_df = run_isotherm_test(mountain_results)

    if boundary_df.empty:
        print("  No boundaries found across mountains - analysis fails.")
    else:
        print("\nAll zone boundaries:")
        print(boundary_df[["mountain","regime","elev","temp","temp_se","bc"]].to_string(index=False))

        # Compute CV of elevations and temperatures across mountains
        # Use only boundaries with valid temperature
        valid = boundary_df.dropna(subset=["temp"])
        if len(valid) >= 4:
            # For each mountain, take the most prominent boundary (highest BC)
            primary = valid.loc[valid.groupby("mountain")["bc"].idxmax()]
            elev_vals = primary["elev"].values
            temp_vals = primary["temp"].values

            cv_elev = np.std(elev_vals) / np.mean(elev_vals) * 100
            cv_temp = np.std(temp_vals) / abs(np.mean(temp_vals)) * 100

            print(f"\nPrimary boundaries (highest BC per mountain):")
            print(primary[["mountain","regime","elev","temp","bc"]].to_string(index=False))
            print(f"\nCV of boundary elevations: {cv_elev:.1f}%")
            print(f"CV of boundary temperatures: {cv_temp:.1f}%")

            if cv_temp < cv_elev:
                verdict = "ISOTHERM HYPOTHESIS SUPPORTED: temperatures cluster more tightly than elevations"
            elif cv_temp > cv_elev * 1.5:
                verdict = "ALTITUDE HYPOTHESIS SUPPORTED: elevations cluster more tightly than temperatures"
            else:
                verdict = "INCONCLUSIVE: difference in clustering not sufficiently large"
            print(f"\nVerdict: {verdict}")
        else:
            print(f"  Only {len(valid)} boundaries with valid temperature - insufficient for test")

    # Save full results
    # Convert non-serializable items for JSON
    serializable = {}
    for k, v in mountain_results.items():
        serializable[k] = {
            "regime": v.get("regime"),
            "n_records": len(v.get("records", [])),
            "lapse": v.get("lapse"),
            "boundaries": v.get("boundaries"),
            "bc_profile": v.get("bc_df"),
        }
    save_json(serializable, "results.json")
    save_json(boundary_df.to_dict('records') if not boundary_df.empty else [], "boundary_df.json")
    print("\nResults saved to results.json and boundary_df.json")


if __name__ == "__main__":
    main()
