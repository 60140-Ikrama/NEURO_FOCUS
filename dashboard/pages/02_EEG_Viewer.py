"""
Page 02: EEG Signal Viewer Workspace for NeuroLearn Research Suite.
"""

import sys
import os
import streamlit as st

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from dashboard.components import render_header
from visualization.plots import VisualizationEngine

render_header("EEG Signal Viewer", "Multi-Channel Raw & Filtered EEG Waveform Visualizer")

eeg_raw = st.session_state.current_eeg
eeg_clean = st.session_state.clean_eeg

col_ctrl1, col_ctrl2 = st.columns([2, 1])

with col_ctrl1:
    selected_chs = st.multiselect(
        "Select Channels to Display:",
        options=eeg_raw.channel_names,
        default=eeg_raw.channel_names[:min(8, eeg_raw.n_channels)]
    )

with col_ctrl2:
    view_sec = st.slider("Display Window (seconds):", 2.0, 30.0, 10.0, 2.0)
    sig_mode = st.radio("Signal View Mode:", ["Preprocessed Filtered", "Raw Unfiltered"], horizontal=True)

target_eeg = eeg_clean if sig_mode == "Preprocessed Filtered" else eeg_raw

st.markdown("---")

if selected_chs:
    fig = VisualizationEngine.plot_eeg_signals(
        target_eeg,
        selected_channels=selected_chs,
        max_seconds=view_sec,
        title=f"Multi-Channel EEG Waveforms ({sig_mode})"
    )
    st.plotly_chart(fig, use_container_width=True)
else:
    st.warning("Please select at least one channel to view signals.")
