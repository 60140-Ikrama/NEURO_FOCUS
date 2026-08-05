"""
Page 07: Systematic Research Ablation Workspace for NeuroLearn Research Suite.
"""

import sys
import os
import streamlit as st

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from ablation.engine import AblationEngine
from dashboard.components import render_header
from visualization.plots import VisualizationEngine

render_header("Ablation Study Workspace", "Systematic Quantitative Evaluation of Processing Choices on Neurophysiological Attention Metrics")

eeg = st.session_state.current_eeg
ablation_eng = AblationEngine(eeg)

tab1, tab2, tab3, tab4 = st.tabs([
    "🛠️ Preprocessing Pipeline Ablation",
    "⏱️ Window Size Ablation (2s - 30s)",
    "📊 PSD Method Ablation",
    "🧮 Attention Formula Ablation"
])

with tab1:
    st.markdown("#### **Systematic Preprocessing Pipeline Evaluation**")
    if st.button("Run Preprocessing Pipeline Ablation", type="primary"):
        with st.spinner("Evaluating filter pipelines..."):
            df_ab_pre = ablation_eng.run_preprocessing_ablation()
            st.session_state.df_ab_pre = df_ab_pre

    if "df_ab_pre" in st.session_state:
        df_ab = st.session_state.df_ab_pre
        st.dataframe(df_ab, use_container_width=True)
        fig = VisualizationEngine.plot_ablation_matrix(df_ab, "Mean Attention Score Across Preprocessing Pipelines")
        st.plotly_chart(fig, use_container_width=True)

with tab2:
    st.markdown("#### **Window Size Sensitivity Analysis (2s to 30s Epochs)**")
    if st.button("Run Window Size Ablation", type="primary"):
        with st.spinner("Evaluating sliding window durations..."):
            df_ab_win = ablation_eng.run_window_size_ablation()
            st.session_state.df_ab_win = df_ab_win

    if "df_ab_win" in st.session_state:
        df_ab_w = st.session_state.df_ab_win
        st.dataframe(df_ab_w, use_container_width=True)
        fig_w = VisualizationEngine.plot_ablation_matrix(df_ab_w, "Attention Metrics vs Sliding Window Size")
        st.plotly_chart(fig_w, use_container_width=True)

with tab3:
    st.markdown("#### **PSD Estimation Method Comparison (Welch vs FFT vs Multitaper)**")
    if st.button("Run PSD Method Ablation", type="primary"):
        with st.spinner("Evaluating spectral estimation algorithms..."):
            df_ab_psd = ablation_eng.run_psd_method_ablation()
            st.session_state.df_ab_psd = df_ab_psd

    if "df_ab_psd" in st.session_state:
        df_ab_p = st.session_state.df_ab_psd
        st.dataframe(df_ab_p, use_container_width=True)
        fig_p = VisualizationEngine.plot_ablation_matrix(df_ab_p, "Mean Attention Score by PSD Method")
        st.plotly_chart(fig_p, use_container_width=True)

with tab4:
    st.markdown("#### **Neurophysiological Formula Formulation Comparison**")
    if st.button("Run Attention Formula Ablation", type="primary"):
        with st.spinner("Evaluating attention formula ratio formulations..."):
            df_ab_form = ablation_eng.run_formula_ablation()
            st.session_state.df_ab_form = df_ab_form

    if "df_ab_form" in st.session_state:
        df_ab_f = st.session_state.df_ab_form
        st.dataframe(df_ab_f, use_container_width=True)
        fig_f = VisualizationEngine.plot_ablation_matrix(df_ab_f, "Mean Attention Score Across Formulations")
        st.plotly_chart(fig_f, use_container_width=True)
