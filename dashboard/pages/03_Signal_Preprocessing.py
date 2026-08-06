"""
Page 03: Signal Preprocessing & Quality Audit Workspace for NeuroLearn Research Suite.
"""

import sys
import os
import streamlit as st

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from preprocessing.cleaner import EEGPreprocessor
from preprocessing.quality import SignalQualityAssessment
from dashboard.components import render_header, render_kpi_card
from visualization.plots import VisualizationEngine

render_header("Signal Preprocessing & SQI Audit", "Configure Bandpass, Notch, ICA Cleaning, Montage Referencing, & Quality Audit")

c_cfg1, c_cfg2 = st.columns(2)

with c_cfg1:
    st.markdown("#### **Filter Parameters**")
    low_f = st.number_input("Bandpass Low Cutoff (Hz):", 0.1, 10.0, 1.0, 0.5)
    high_f = st.number_input("Bandpass High Cutoff (Hz):", 15.0, 70.0, 40.0, 5.0)
    notch_f = st.selectbox("Notch Frequency (Powerline):", [50.0, 60.0, 0.0])
    montage_ref = st.selectbox("Montage Referencing:", ["raw", "car", "bipolar"])

with c_cfg2:
    st.markdown("#### **Standardization & ICA Rejection**")
    norm_type = st.selectbox("Normalization Method:", ["zscore", "minmax", "robust", "none"])
    use_ica = st.checkbox("FastICA Artifact Rejection (Ocular & EMG)", value=True)
    detrend_flag = st.checkbox("Baseline Detrending", value=True)
    dc_flag = st.checkbox("DC Offset Removal", value=True)
    auto_exclude = st.checkbox("Auto-Exclude Bad Channels (SQI < 40%)", value=True)

if st.button("Apply Preprocessing Pipeline", type="primary"):
    cleaner = EEGPreprocessor(
        lowcut=low_f, highcut=high_f,
        notch_freq=notch_f,
        detrend=detrend_flag, dc_offset_removal=dc_flag,
        normalization=norm_type,
        montage_ref=montage_ref,
        use_ica=use_ica
    )
    clean_data, log = cleaner.process(st.session_state.current_eeg)

    sqa = SignalQualityAssessment()
    sqi_report = sqa.evaluate(clean_data)

    if auto_exclude and sqi_report["bad_channels"]:
        clean_data = sqa.exclude_bad_channels(clean_data, sqi_report["bad_channels"])

    st.session_state.clean_eeg = clean_data
    st.session_state.preproc_log = log
    st.session_state.sqi_report = sqi_report
    st.success("Preprocessing pipeline executed and stored!")

st.markdown("---")
st.markdown("### Signal Quality Index (SQI) Audit Results")

sqi = st.session_state.sqi_report
c1, c2, c3 = st.columns(3)
with c1:
    render_kpi_card("Overall SQI Score", f"{sqi['overall_sqi']}%", "Average Quality Score")
with c2:
    render_kpi_card("Valid Channels", f"{sqi['good_channel_count']}", f"Total: {sqi['total_channel_count']}")
with c3:
    render_kpi_card("Excluded Channels", f"{len(sqi['bad_channels'])}", ", ".join(sqi['bad_channels']) if sqi['bad_channels'] else "None")

fig_sqi = VisualizationEngine.plot_signal_quality(sqi)
st.plotly_chart(fig_sqi, width="stretch")
