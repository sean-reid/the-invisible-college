"""Check GBIF counts for additional dry Andean mountains to replace Coropuna."""
import requests, time

candidates = [
    {"name": "Chachani",   "lat": -16.19, "lon": -71.53, "regime": "dry"},
    {"name": "Ampato",     "lat": -15.80, "lon": -71.86, "regime": "dry"},
    {"name": "Ubinas",     "lat": -16.36, "lon": -70.90, "regime": "dry"},
    {"name": "Pichu Pichu","lat": -16.35, "lon": -71.21, "regime": "dry"},
    {"name": "Huascaran",  "lat":  -9.12, "lon": -77.60, "regime": "wet?"},
    {"name": "El Misti2",  "lat": -16.29, "lon": -71.41, "regime": "dry"},  # sanity check
]

RADIUS_KM = 40
DEG_PER_KM = 1/111.0

for m in candidates:
    radius_deg = RADIUS_KM * DEG_PER_KM
    params = {
        'decimalLatitude':  f"{m['lat']-radius_deg},{m['lat']+radius_deg}",
        'decimalLongitude': f"{m['lon']-radius_deg},{m['lon']+radius_deg}",
        'kingdomKey': 6,
        'hasCoordinate': 'true',
        'hasGeospatialIssue': 'false',
        'limit': 1,
    }
    try:
        r = requests.get('https://api.gbif.org/v1/occurrence/search', params=params, timeout=20)
        count = r.json().get('count', 0)
        print(f"{m['name']:12s} ({m['regime']:8s}): {count:6d} records")
    except Exception as e:
        print(f"{m['name']:12s}: ERROR - {e}")
    time.sleep(0.5)
