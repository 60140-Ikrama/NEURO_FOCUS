"""
Page 01: Dataset Manager Workspace for NeuroLearn Research Suite.
"""

import sys
import os
import streamlit as st
import tempfile

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from data.loader import EEGDataLoader
from data.biopac import BiopacImportManager
from data.physionet import PhysioNetManager
from data.sample_generator import generate_synthetic_eeg
from dashboard.components import render_header, render_kpi_card
from preprocessing.quality import SignalQualityAssessment

render_header("Dataset Manager", "Import & Metadata Auto-Detection for PhysioNet, Biopac, MAT, EDF, CSV, TXT Datasets")

st.markdown("### Select Data Source")
source_option = st.radio(
    "Choose Dataset Type:",
    ["Synthetic Sample (Focused/Resting)", "PhysioNet (eegmmidb)", "Import Biopac File (MAT/CSV/EDF)", "Upload Custom EEG File"],
    horizontal=True
)

if source_option == "Synthetic Sample (Focused/Resting)":
    state = st.selectbox("Simulated Cognitive State:", ["focused", "resting", "drowsy", "artifact_heavy"])
    duration = st.slider("Duration (seconds):", 10.0, 120.0, 30.0, 10.0)
    if st.button("Generate Synthetic Recording", type="primary"):
        eeg_data = generate_synthetic_eeg(duration_sec=duration, state=state)
        st.session_state.current_eeg = eeg_data
        sqa = SignalQualityAssessment()
        st.session_state.sqi_report = sqa.evaluate(eeg_data)
        st.success(f"Generated synthetic {state} recording ({eeg_data.n_channels} channels, {eeg_data.sampling_rate} Hz).")

elif source_option == "PhysioNet (eegmmidb)":
    subj_id = st.number_input("PhysioNet Subject ID (1-109):", min_value=1, max_value=109, value=1)
    run_id = st.selectbox("Task Run:", [1, 2, 3])
    if st.button("Fetch PhysioNet Dataset", type="primary"):
        with st.spinner("Fetching PhysioNet recording..."):
            try:
                eeg_data = PhysioNetManager.load_physionet_subject(subject_id=subj_id, runs=[run_id])
                st.session_state.current_eeg = eeg_data
                sqa = SignalQualityAssessment()
                st.session_state.sqi_report = sqa.evaluate(eeg_data)
                st.success(f"Fetched PhysioNet Subject {subj_id} Run {run_id}!")
            except Exception as e:
                st.error(f"Failed to fetch PhysioNet dataset: {e}")

elif source_option == "Import Biopac File (MAT/CSV/EDF)":
    uploaded_biopac = st.file_uploader("Upload Biopac AcqKnowledge Export File:", type=["mat", "csv", "txt", "edf"])
    if uploaded_biopac is not None:
        with tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(uploaded_biopac.name)[1]) as tmp:
            tmp.write(uploaded_biopac.getbuffer())
            tmp_path = tmp.name

        if st.button("Import Biopac Recording", type="primary"):
            try:
                eeg_data = BiopacImportManager.import_biopac_recording(tmp_path)
                st.session_state.current_eeg = eeg_data
                sqa = SignalQualityAssessment()
                st.session_state.sqi_report = sqa.evaluate(eeg_data)
                st.success("Biopac recording normalized and loaded into processing pipeline!")
            except Exception as e:
                st.error(f"Biopac import error: {e}")

elif source_option == "Upload Custom EEG File":
    uploaded_file = st.file_uploader("Upload EEG Recording (EDF, MAT, CSV, TXT):", type=["edf", "mat", "csv", "txt"])
    if uploaded_file is not None:
        with tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(uploaded_file.name)[1]) as tmp:
            tmp.write(uploaded_file.getbuffer())
            tmp_path = tmp.name

        if st.button("Load File", type="primary"):
            try:
                eeg_data = EEGDataLoader.load_file(tmp_path)
                st.session_state.current_eeg = eeg_data
                sqa = SignalQualityAssessment()
                st.session_state.sqi_report = sqa.evaluate(eeg_data)
                st.success(f"Successfully loaded {uploaded_file.name}!")
            except Exception as e:
                st.error(f"Loader error: {e}")

st.markdown("---")
st.markdown("### Automatically Detected Metadata")
eeg = st.session_state.current_eeg

c1, c2, c3, c4 = st.columns(4)
with c1:
    render_kpi_card("Sampling Frequency", f"{eeg.sampling_rate} Hz", "Auto-Detected")
with c2:
    render_kpi_card("Channel Count", f"{eeg.n_channels}", f"Labels: {', '.join(eeg.channel_names[:4])}...")
with c3:
    render_kpi_card("Recording Duration", f"{eeg.duration_sec:.1f} s", f"Total Samples: {eeg.n_samples}")
with c4:
    render_kpi_card("Signal Units", f"{eeg.units}", f"Source: {eeg.source_type}")

st.markdown("#### Detected Channel Labels")
st.code(", ".join(eeg.channel_names))
