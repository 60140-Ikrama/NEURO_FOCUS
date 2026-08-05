"""
Page 05: Mathematical Attention Analysis Workspace for NeuroLearn Research Suite.
"""

import sys
import os
import streamlit as st

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from segmentation.windowing import EEGSegmenter
from features.extractor import FeatureExtractionEngine
from attention.calculator import AttentionCalculator
from dashboard.components import render_header, render_kpi_card
from visualization.plots import VisualizationEngine

render_header("Attention Analysis", "Pure Mathematical Non-ML Cognitive State Quantification & Custom Formula Builder")

eeg_clean = st.session_state.clean_eeg

col_form1, col_form2 = st.columns([2, 1])

with col_form1:
    formula_choice = st.selectbox(
        "Choose Mathematical Attention Formula:",
        ["beta / theta", "(beta + gamma) / (theta + alpha)", "beta / alpha", "alpha / theta", "Custom Expression"]
    )
    if formula_choice == "Custom Expression":
        active_formula = st.text_input("Enter Custom Math Formula (variables: delta, theta, alpha, beta, gamma):", "(beta + gamma) / (theta + alpha)")
    else:
        active_formula = formula_choice

with col_form2:
    win_sec = st.selectbox("Sliding Window Size (seconds):", [2.0, 5.0, 10.0, 20.0, 30.0], index=1)
    overlap_val = st.slider("Window Overlap Ratio:", 0.0, 0.9, 0.5, 0.1)

if st.button("Calculate Attention Index Timeline", type="primary"):
    segmenter = EEGSegmenter(window_sec=win_sec, overlap_ratio=overlap_val)
    epochs = segmenter.segment(eeg_clean)

    fe = FeatureExtractionEngine(psd_method="welch")
    df_feat = fe.extract_features(epochs)

    calc = AttentionCalculator(formula_str=active_formula)
    df_att, summary = calc.compute_attention(df_feat)

    st.session_state.df_attention = df_att
    st.session_state.att_summary = summary
    st.success("Attention timeline computed successfully!")

st.markdown("---")

att_sum = st.session_state.att_summary
c1, c2, c3, c4 = st.columns(4)

with c1:
    render_kpi_card("Average Attention", f"{att_sum['average_attention']:.1f} / 100", f"Category: {att_sum['dominant_category']}")
with c2:
    render_kpi_card("Peak Attention", f"{att_sum['peak_attention']:.1f} / 100", "Maximum Score")
with c3:
    render_kpi_card("Minimum Attention", f"{att_sum['minimum_attention']:.1f} / 100", "Minimum Score")
with c4:
    render_kpi_card("Attention Stability", f"{att_sum['stability_index']:.1f} / 100", f"Drop Events: {att_sum['attention_drop_count']}")

fig_timeline = VisualizationEngine.plot_attention_timeline(st.session_state.df_attention)
st.plotly_chart(fig_timeline, use_container_width=True)

# Data Table
with st.expander("View Epoch-by-Epoch Attention Scores Data Table"):
    st.dataframe(st.session_state.df_attention[["epoch_id", "start_sec", "end_sec", "attention_raw", "attention_score", "attention_category"]], use_container_width=True)
