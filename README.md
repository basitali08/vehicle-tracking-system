# 🚗 Vehicle Tracking & Hotlist Alert System

A license plate recognition system that detects vehicles, checks against a hotlist database, and tracks detections on a map.

## How it works

1. **Upload image** → system scans for license plate using OCR
2. **Plate read** → checks against hotlist database in real-time
3. **Alert** → if plate is hotlisted, a red alert shows
4. **Map** → all detections are plotted on an interactive map

## Quick Start

```bash
pip install -r requirements.txt
python generate_plates.py     # creates 200 synthetic plate images
python hotlist_db.py           # initializes database with hotlist
streamlit run tracking_app.py  # launches dashboard
```

## Files

| File | Purpose |
|------|---------|
| `generate_plates.py` | Creates synthetic Pakistani plate images |
| `hotlist_db.py` | SQLite database for hotlist + detections |
| `plate_scanner.py` | EasyOCR-based plate reading |
| `tracking_app.py` | Streamlit dashboard with map |
| `test_scan.py` | Quick test for the scanner |
| `samples/` | Generated plate images |
