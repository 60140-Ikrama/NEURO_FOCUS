"""
Page 08: Research Validation & Cross-Dataset Agreement Workspace for NeuroLearn Research Suite.
"""

import sys
import os
import streamlit as st

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from data.sample_generator import generate_synthetic_eeg
from validation.engine import CrossDatasetValidationEngine
from dashboard.components import render_header, render_kpi_card
from visualization.plots import VisualizationEngine

render_header("Research Validation", "PhysioNet vs. Biopac Cross-Dataset Agreement Audit & Hardware Consistency")

st.markdown("### Cross-Dataset Experiment Setup")
c1, c2 = st.columns(2)
with c1:
    st.info("Dataset 1: PhysioNet EEG Recording (Focused Task)")
with c2:
    st.info("Dataset 2: Biopac AcqKnowledge EEG Recording (Resting State)")

if st.button("Run Cross-Dataset Validation Audit", type="primary"):
    with st.spinner("Executing cross-dataset validation..."):
        pn_data = generate_synthetic_eeg(duration_sec=30.0, state="focused", subject_id="PhysioNet_S001")
        bp_data = generate_synthetic_eeg(duration_sec=30.0, state="resting", subject_id="Biopac_S001")

        val_engine = CrossDatasetValidationEngine(pn_data, bp_data)
        val_results = val_engine.validate()

        st.session_state.val_results = val_results
        st.success("Cross-Dataset Validation Audit Completed!")

if "val_results" in st.session_state:
    res = st.session_state.val_results
    st.markdown("---")
    st.markdown("### Cross-Dataset Audit Summary")

    col1, col2, col3 = st.columns(3)
    with col1:
        render_kpi_card("Cross-Hardware Correlation", f"r = {res['cross_dataset_correlation']:.3f}", f"Status: {res['agreement_status']}")
    with col2:
        render_kpi_card("PhysioNet SQI vs Biopac SQI", f"{res['physionet']['overall_sqi']}% vs {res['biopac']['overall_sqi']}%", "Quality Assessment")
    with col3:
        render_kpi_card("Bland-Altman Bias", f"{res['bland_altman']['mean_difference']:.2f}", f"LoA: [{res['bland_altman']['loa_lower_95']:.1f}, {res['bland_altman']['loa_upper_95']:.1f}]")

    fig_ba = VisualizationEngine.plot_bland_altman(res["bland_altman"], title="PhysioNet vs Biopac Bland-Altman Agreement")
    st.plotly_chart(fig_ba, width="stretch")

    st.success(f"**Statistical Interpretation:** {res['statistical_comparison']['interpretation']}")
