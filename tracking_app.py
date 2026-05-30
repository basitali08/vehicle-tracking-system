"""
Streamlit dashboard: Vehicle Tracking & Hotlist Alert System
- Upload images/videos
- Auto-detect and read license plates
- Check against hotlist database
- Log detections with location
- Show tracking trail on map
"""
import streamlit as st
import os
import tempfile
from datetime import datetime
import pandas as pd
import folium
from streamlit_folium import st_folium
import random

from hotlist_db import (
    init_db, get_hotlist, add_to_hotlist, remove_from_hotlist,
    is_hotlisted, log_detection, get_detection_history, get_alert_count, seed_from_file
)
from plate_scanner import scan_image

st.set_page_config(page_title="Vehicle Tracker", page_icon="🚗", layout="wide")
init_db()
seed_from_file()

st.title("🚗 Vehicle Tracking & Hotlist Alert System")
st.markdown("Upload a vehicle image or video. The system reads the license plate and checks if it's on the hotlist.")

tab1, tab2, tab3 = st.tabs(["📸 Scan & Track", "📋 Hotlist Manager", "🗺️ Tracking Map"])

with tab1:
    col1, col2 = st.columns([1, 1])

    with col1:
        uploaded_file = st.file_uploader(
            "Upload vehicle image",
            type=['png', 'jpg', 'jpeg'],
            help="Upload a clear image showing the license plate"
        )
        manual_plate = st.text_input("Or enter plate number manually:", placeholder="e.g., LEG-456")

        lat = st.number_input("Latitude", value=33.6844, format="%.4f", help="GPS latitude of detection location")
        lng = st.number_input("Longitude", value=73.0479, format="%.4f", help="GPS longitude of detection location")
        loc_name = st.text_input("Location name", value="Islamabad", help="e.g., Street name, area")

    with col2:
        if uploaded_file:
            with tempfile.NamedTemporaryFile(delete=False, suffix='.png') as tmp:
                tmp.write(uploaded_file.read())
                tmp_path = tmp.name

            st.image(uploaded_file, caption="Uploaded vehicle image", use_container_width=True)

            with st.spinner("Scanning license plate..."):
                detections = scan_image(tmp_path)

            os.unlink(tmp_path)

            plate_to_use = None
            if detections:
                best = detections[0]
                plate_to_use = best['plate']
                st.success(f"Detected plate: **{best['plate']}** (confidence: {best['confidence']:.2%})")
            elif manual_plate:
                plate_to_use = manual_plate.strip().upper()
                st.info(f"Using manual plate: **{plate_to_use}**")
            else:
                st.warning("No plate detected. Enter plate manually above.")

            if plate_to_use:
                if is_hotlisted(plate_to_use):
                    st.error(f"🚨 **ALERT!** Plate **{plate_to_use}** is on the HOTLIST!")
                else:
                    st.success(f"Plate **{plate_to_use}** is clean.")

                if st.button("Log Detection", type="primary"):
                    log_detection(plate_to_use, uploaded_file.name, lat, lng, loc_name)
                    st.toast(f"Detection logged for {plate_to_use} at {loc_name}")

        elif manual_plate:
            plate = manual_plate.strip().upper()
            if is_hotlisted(plate):
                st.error(f"🚨 **ALERT!** Plate **{plate}** is on the HOTLIST!")
            else:
                st.success(f"Plate **{plate}** is clean.")

            if st.button("Log Detection", type="primary"):
                log_detection(plate, '', lat, lng, loc_name)
                st.toast(f"Detection logged for {plate} at {loc_name}")
        else:
            st.info("Upload an image or enter a plate number to begin.")

with tab2:
    st.subheader("Hotlist Management")
    alert_count = get_alert_count()
    st.metric("Total Alerts", alert_count)

    new_plate = st.text_input("Add plate to hotlist:", placeholder="e.g., LEG-456", key="add_plate")
    reason = st.text_input("Reason (optional):", placeholder="Suspicious activity", key="reason")
    if st.button("Add to Hotlist"):
        if new_plate.strip():
            add_to_hotlist(new_plate.strip().upper(), reason)
            st.success(f"Added {new_plate.strip().upper()} to hotlist")
            st.rerun()

    st.divider()
    st.subheader("Current Hotlist")
    hotlist = get_hotlist()
    if hotlist:
        for h in hotlist:
            c1, c2, c3, c4 = st.columns([3, 3, 2, 1])
            c1.write(h['plate'])
            c2.write(h['reason'] or '-')
            c3.write(h['added_at'][:10])
            if c4.button("Remove", key=f"rem_{h['id']}"):
                remove_from_hotlist(h['plate'])
                st.rerun()
    else:
        st.info("Hotlist is empty. Add plates above.")

with tab3:
    st.subheader("Tracking Trail Map")
    history = get_detection_history(limit=200)

    if history:
        center_lat = sum(h['latitude'] for h in history) / len(history)
        center_lng = sum(h['longitude'] for h in history) / len(history)

        m = folium.Map(location=[center_lat, center_lng], zoom_start=12)

        hotlist_plates = {h['plate'] for h in get_hotlist()}

        for det in history:
            color = 'red' if det['plate'] in hotlist_plates else 'blue'
            icon = folium.Icon(color=color, icon='flag' if color == 'red' else 'info-sign')

            folium.Marker(
                [det['latitude'], det['longitude']],
                popup=f"<b>{det['plate']}</b><br>{det['location_name']}<br>{det['detected_at']}",
                icon=icon,
                tooltip=det['plate']
            ).add_to(m)

        st_folium(m, width=1000, height=600)

        st.divider()
        st.subheader("Detection History")
        df = pd.DataFrame(history)
        df['alert'] = df['plate'].apply(lambda p: '🔴 ALERT' if p in hotlist_plates else '✅ Clean')
        st.dataframe(
            df[['detected_at', 'plate', 'location_name', 'alert']].rename(
                columns={'detected_at': 'Time', 'plate': 'Plate', 'location_name': 'Location', 'alert': 'Status'}
            ),
            hide_index=True,
            use_container_width=True
        )
    else:
        st.info("No detections yet. Go to Scan & Track tab to start logging.")

st.divider()
st.caption("🚗 Vehicle Tracking System | ANPR + Hotlist Alert | Abdul Wali Khan University Mardan")
