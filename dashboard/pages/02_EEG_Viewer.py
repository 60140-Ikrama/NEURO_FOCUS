"""
Page 02: EEG Waveform Hub & Spectral Workspace (Dashboard 2).
High-density multi-channel EEG waveform visualizer, Welch PSD curves, and SQI Quality Audit Table.
"""

import sys
import os
import streamlit as st
import numpy as np

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from dashboard.components import render_header, render_kpi_card
from visualization.plots import VisualizationEngine
from features.extractor import FeatureExtractionEngine

render_header("EEG Waveform Hub & Spectral Workspace (Dashboard 2)", "Stacked Multi-Channel Waveform Plotter, Welch Power Spectral Density (PSD), & Channel SQI Audit")

eeg_raw = st.session_state.current_eeg
eeg_clean = st.session_state.clean_eeg
sqi_report = st.session_state.sqi_report

# TOP CONTROL BAR
ctrl_col1, ctrl_col2, ctrl_col3 = st.columns([2, 1, 1])

with ctrl_col1:
    selected_chs = st.multiselect(
        "Select Channels to Inspect:",
        options=eeg_raw.channel_names,
        default=eeg_raw.channel_names[:min(8, eeg_raw.n_channels)]
    )

with ctrl_col2:
    view_sec = st.slider("Time Window (sec):", 2.0, 30.0, 10.0, 2.0)

with ctrl_col3:
    sig_mode = st.radio("Signal View Mode:", ["Preprocessed Filtered", "Raw Unfiltered"], horizontal=True)

target_eeg = eeg_clean if sig_mode == "Preprocessed Filtered" else eeg_raw

st.markdown("---")

# MIDDLE MAIN CANVAS: STACKED WAVEFORMS
if selected_chs:
    fig_wave = VisualizationEngine.plot_eeg_signals(
        target_eeg,
        selected_channels=selected_chs,
        max_seconds=view_sec,
        title=f"Multi-Channel EEG Waveforms ({sig_mode})"
    )
    st.plotly_chart(fig_wave, width="stretch")
else:
    st.warning("Please select at least one channel to display waveforms.")

st.markdown("<br/>", unsafe_allow_html=True)

# BOTTOM SECTION: 50 / 50 SPLIT (PSD SPECTRAL CURVES & CHANNEL SQI AUDIT TABLE)
btm_left, btm_right = st.columns(2)

with btm_left:
    st.markdown("### 🌊 Welch Power Spectral Density (PSD)")
    fig_psd = VisualizationEngine.plot_psd_curves(target_eeg, selected_channels=selected_chs[:min(4, len(selected_chs))])
    st.plotly_chart(fig_psd, width="stretch")

with btm_right:
    st.markdown("### 🛡️ Channel Quality Audit & SNR Matrix")
    
    # Construct Channel Audit Dataframe
    ch_rows = []
    for ch in eeg_raw.channel_names:
        snr = sqi_report["channel_snr_db"].get(ch, 0.0)
        status = "PASSED" if ch not in sqi_report["bad_channels"] else "EXCLUDED"
        ch_rows.append({
            "Channel": ch,
            "SNR (dB)": f"{snr:.2f} dB",
            "SQI Status": status,
            "Contamination": "Clean" if status == "PASSED" else "High Artifact Noise"
        })
    
    st.dataframe(ch_rows, width="stretch", height=320)
