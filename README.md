# Vehicle Tracking & Hotlist Alert System

A license plate recognition (ANPR) system that detects vehicle plates from images, checks them against a hotlist database, and plots detection locations on an interactive map. Built for urban surveillance and security applications.

## Features

- License plate detection using EasyOCR (deep learning-based OCR)
- Real-time hotlist matching with visual alerts
- SQLite database for storing hotlist plates and detection history
- Interactive Folium map showing detection locations
- Streamlit dashboard with three tabs: Scan, Hotlist Manager, Tracking Map
- Synthetic Pakistani-style plate dataset generator

## How It Works

1. Upload a vehicle image → system scans for license plate using OCR
2. Plate text is extracted and checked against the hotlist database
3. If plate is hotlisted → red alert with warning
4. Detection location is logged and plotted on an interactive map

## Quick Start

```bash
# Install dependencies
pip install -r requirements.txt

# Generate synthetic plate dataset (200 images)
python generate_plates.py

# Initialize hotlist database
python hotlist_db.py

# Launch the dashboard
streamlit run tracking_app.py
```

## Project Structure

| File | Purpose |
|------|---------|
| `tracking_app.py` | Streamlit dashboard (scan, hotlist, map) |
| `plate_scanner.py` | EasyOCR-based plate reading pipeline |
| `hotlist_db.py` | SQLite database management |
| `generate_plates.py` | Creates synthetic Pakistani-style plate images |
| `paper.tex` | LaTeX research paper |
| `samples/` | 200 generated plate images (20 hotlisted) |
| `requirements.txt` | Python dependencies |

## Tech Stack

- **Python 3.12** — core language
- **EasyOCR** — deep learning OCR library (PyTorch backend)
- **Streamlit** — web dashboard
- **Folium** — interactive map visualization
- **SQLite** — database
- **Pillow** — image generation

## Dataset

200 synthetic Pakistani-style license plates following the format: `[2-3 letters]-[3-4 digits]` (e.g., `LEG-456`, `ISB-1234`). 20 plates (10%) are randomly assigned to the hotlist for demo purposes.

## Paper

A LaTeX research paper is included at `paper.tex`. Compile with pdflatex or upload to Overleaf.

## Author

**Basit Ali** — Abdul Wali Khan University Mardan, Pakistan
