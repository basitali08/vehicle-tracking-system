<div align="center">
  <h1>🚗 Vehicle Tracking & Hotlist Alert System</h1>
  <p><b>License Plate Recognition (ANPR) with Real-Time Hotlist Alerts & Interactive Mapping</b></p>
</div>

<br>

<div align="center">
  <img src="https://img.shields.io/badge/Python-3.12+-3776AB?style=for-the-badge&logo=python&logoColor=white">
  <img src="https://img.shields.io/badge/EasyOCR-1.7+-FF6F00?style=for-the-badge&logo=openai&logoColor=white">
  <img src="https://img.shields.io/badge/Streamlit-1.28+-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white">
  <img src="https://img.shields.io/badge/Folium-0.14+-228B22?style=for-the-badge&logo=python&logoColor=white">
  <img src="https://img.shields.io/badge/SQLite-3+-003B57?style=for-the-badge&logo=sqlite&logoColor=white">
  <img src="https://img.shields.io/badge/License-MIT-yellow?style=for-the-badge">
</div>

<br>

<div align="center">
  <i>A license plate recognition (ANPR) system that detects vehicle plates from images, checks them against a hotlist database, and plots detection locations on an interactive map.</i>
</div>

<br>

---

## 📋 Table of Contents

- [Features](#features)
- [How It Works](#how-it-works)
- [Quick Start](#quick-start)
- [Project Structure](#project-structure)
- [Tech Stack](#tech-stack)
- [Dataset](#dataset)
- [Paper](#paper)
- [Author](#author)

---

## ✨ Features

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
| `generate_plates.py` | Synthetic Pakistani-style plate image generator |
| `paper.tex` | LaTeX research paper |
| `requirements.txt` | Python dependencies |
| `.gitignore` | Git ignore rules |
| `samples/` | 200 generated plate images (20 hotlisted) |

## Tech Stack

- **Python 3.12** — core language
- **EasyOCR** — deep learning OCR library (PyTorch backend)
- **Streamlit** — web dashboard
- **Folium** — interactive map visualization
- **SQLite** — database
- **Pillow** — image generation

## Dataset

200 synthetic Pakistani-style license plates following the format: `[2-3 letters]-[3-4 digits]` (e.g., `LEG-456`, `ISB-1234`). 20 plates (10%) are randomly assigned to the hotlist for demo purposes.

## 📄 Paper

A LaTeX research paper is included at `paper.tex`. Compile with pdflatex or upload to Overleaf.

---

<p align="center">
<b>Built by Basit Ali</b> · <a href="https://github.com/basitali08">GitHub</a> · <a href="mailto:whoisbasit@gmail.com">Email</a><br>
<sub>Computer Vision & Surveillance · MS Data Science Portfolio</sub>
</p>
