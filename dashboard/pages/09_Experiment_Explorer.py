"""
Page 09: Experiment Explorer & 100% Reproducibility Workspace for NeuroLearn Research Suite.
"""

import sys
import os
import streamlit as st

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from experiments.tracker import ExperimentTracker
from dashboard.components import render_header

render_header("Experiment Explorer", "100% Reproducibility Tracker, Parameter Snapshotting, & Audit Logging")

tracker = ExperimentTracker("EEG_Attention_Study_2026")

eeg = st.session_state.current_eeg
log = st.session_state.preproc_log
att = st.session_state.att_summary

if st.button("Generate Experiment Reproducibility Snapshot", type="primary"):
    snapshot = tracker.create_reproducibility_snapshot(
        dataset_name=eeg.subject_id,
        n_channels=eeg.n_channels,
        fs=eeg.sampling_rate,
        duration_sec=eeg.duration_sec,
        preproc_config=log,
        window_sec=5.0,
        attention_formula="beta / theta",
        results_summary=att
    )
    st.session_state.current_snapshot = snapshot
    st.success(f"Snapshot created: ID `{snapshot['experiment_id']}` (Hash: `{snapshot['parameter_hash']}`)")

if "current_snapshot" in st.session_state:
    st.markdown("### Reproducibility Snapshot Details")
    st.json(st.session_state.current_snapshot)
