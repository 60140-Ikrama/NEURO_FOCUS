"""
Page 04: Frequency & Spectral Analysis Workspace for NeuroLearn Research Suite.
"""

import sys
import os
import streamlit as st
import numpy as np

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from features.frequency_domain import FrequencyDomainExtractor
from dashboard.components import render_header, render_kpi_card
from visualization.plots import VisualizationEngine

render_header("Frequency Analysis", "Power Spectral Density (Welch/Multitaper), Band Powers, & SEF95 Metrics")

eeg = st.session_state.clean_eeg

c_ctrl1, c_ctrl2 = st.columns(2)
with c_ctrl1:
    selected_ch = st.selectbox("Select Target Channel:", eeg.channel_names)
with c_ctrl2:
    psd_method = st.selectbox("PSD Estimation Method:", ["welch", "fft", "multitaper"])

extractor = FrequencyDomainExtractor(psd_method=psd_method)
sig = eeg.get_channel_data(selected_ch)
freqs, psd = extractor.compute_psd(sig, eeg.sampling_rate)

st.markdown("---")

fig_psd = VisualizationEngine.plot_psd(freqs, psd, channel_name=selected_ch, psd_method=psd_method.capitalize())
st.plotly_chart(fig_psd, width="stretch")

# Band Power Breakdown Metrics
st.markdown("### Band Power Breakdown")

bands = {
    "Delta (0.5-4Hz)": (0.5, 4.0),
    "Theta (4-8Hz)": (4.0, 8.0),
    "Alpha (8-13Hz)": (8.0, 13.0),
    "Beta (13-30Hz)": (13.0, 30.0),
    "Gamma (30-40Hz)": (30.0, 40.0)
}

trapz_func = getattr(np, 'trapezoid', None) or getattr(np, 'trapz', None)
tot_p = trapz_func(psd, freqs) if len(psd) > 0 else 1.0
tot_p = tot_p if tot_p > 0 else 1e-6

cols = st.columns(5)
for i, (b_name, (l_f, h_f)) in enumerate(bands.items()):
    idx = np.where((freqs >= l_f) & (freqs <= h_f))[0]
    p_val = float(trapz_func(psd[idx], freqs[idx])) if len(idx) > 0 else 0.0
    rel_p = (p_val / tot_p) * 100.0

    with cols[i]:
        render_kpi_card(b_name.split()[0], f"{rel_p:.1f}%", f"Abs: {p_val:.2e}")
