"""
Quick GBIF data availability check for the five candidate Andean mountains.
Tests whether the 1500-record threshold in the proposal is met.
"""
import requests
import time
import json

mountains = [
    {"name": "Chimborazo", "lat": -1.47, "lon": -78.82, "regime": "wet"},
    {"name": "Cotopaxi",   "lat": -0.68, "lon": -78.44, "regime": "wet"},
    {"name": "Antisana",   "lat": -0.48, "lon": -78.14, "regime": "wet_east"},
    {"name": "Misti",      "lat": -16.29, "lon": -71.41, "regime": "dry"},
    {"name": "Coropuna",   "lat": -15.52, "lon": -72.67, "regime": "dry"},
]

RADIUS_KM = 40
DEG_PER_KM = 1/111.0

for m in mountains:
    radius_deg = RADIUS_KM * DEG_PER_KM
    params = {
        'decimalLatitude':  f"{m['lat']-radius_deg},{m['lat']+radius_deg}",
        'decimalLongitude': f"{m['lon']-radius_deg},{m['lon']+radius_deg}",
        'kingdomKey': 6,  # Plantae
        'hasCoordinate': 'true',
        'hasGeospatialIssue': 'false',
        'limit': 1,
    }
    try:
        r = requests.get('https://api.gbif.org/v1/occurrence/search', params=params, timeout=20)
        data = r.json()
        count = data.get('count', 0)
        # Check if elevation data is present in a few records
        params2 = dict(params)
        params2['limit'] = 10
        r2 = requests.get('https://api.gbif.org/v1/occurrence/search', params=params2, timeout=20)
        d2 = r2.json()
        results = d2.get('results', [])
        elev_present = sum(1 for rec in results if rec.get('elevation') is not None)
        print(f"{m['name']:12s} ({m['regime']:10s}): {count:6d} records, "
              f"{elev_present}/{len(results)} sample records have elevation")
    except Exception as e:
        print(f"{m['name']:12s}: ERROR - {e}")
    time.sleep(1)
