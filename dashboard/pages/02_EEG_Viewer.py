"""
Page 02: EEG Waveform Hub & Clinical Workspace (Dashboard 2).
High-density multi-channel EEG waveform visualizer, Montage Referencing (CAR / Bipolar Double Banana),
Welch Power Spectral Density (PSD), Time-Frequency Spectrogram (STFT), and Quality Audit Matrix.
"""

import sys
import os
import tempfile
import json
import streamlit as st
import numpy as np
import pandas as pd

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from dashboard.components import render_header, render_kpi_card
from visualization.plots import VisualizationEngine
from preprocessing.cleaner import EEGPreprocessor
from features.extractor import FeatureExtractionEngine

render_header("EEG Waveform Hub & Clinical Workspace (Dashboard 2)", "Multi-Channel EEG Waveforms, Montage Referencing (CAR/Bipolar), Welch PSD, STFT Spectrogram, & SQI Matrix")

eeg_raw = st.session_state.current_eeg
eeg_clean = st.session_state.clean_eeg
sqi_report = st.session_state.sqi_report

# TOP CONTROL BAR: MONTAGE & VIEW MODES
ctrl_col1, ctrl_col2, ctrl_col3, ctrl_col4 = st.columns([2, 1, 1, 1])

with ctrl_col1:
    selected_chs = st.multiselect(
        "Select Channels to Inspect:",
        options=eeg_raw.channel_names,
        default=eeg_raw.channel_names[:min(8, eeg_raw.n_channels)]
    )

with ctrl_col2:
    view_sec = st.slider("Time Window (sec):", 1.0, 60.0, 10.0, 1.0)

with ctrl_col3:
    sig_mode = st.radio("Signal Mode:", ["Preprocessed Filtered", "Raw Unfiltered"], horizontal=True)

with ctrl_col4:
    montage_opt = st.selectbox("Montage Referencing:", ["Monopolar (Raw)", "CAR (Common Average)", "Bipolar (Double Banana)"])

# Process Montage Referencing dynamically
cleaner = EEGPreprocessor(
    lowcut=1.0, highcut=40.0, notch_freq=50.0,
    montage_ref="car" if montage_opt.startswith("CAR") else ("bipolar" if montage_opt.startswith("Bipolar") else "raw")
)
target_eeg, _ = cleaner.process(eeg_clean if sig_mode == "Preprocessed Filtered" else eeg_raw)

st.markdown("---")

# MIDDLE MAIN CANVAS: STACKED WAVEFORMS
if selected_chs:
    # Filter selected channels present in montage
    display_chs = [ch for ch in selected_chs if ch in target_eeg.channel_names] or target_eeg.channel_names[:min(8, target_eeg.n_channels)]
    fig_wave = VisualizationEngine.plot_eeg_signals(
        target_eeg,
        selected_channels=display_chs,
        max_seconds=view_sec,
        title=f"Multi-Channel EEG Waveforms ({sig_mode} - {montage_opt})"
    )
    st.plotly_chart(fig_wave, width="stretch")
else:
    st.warning("Please select at least one channel to display waveforms.")

st.markdown("<br/>", unsafe_allow_html=True)

# TABBED SPECTRAL & DIAGNOSTIC WORKSPACE
t_psd, t_stft, t_topo, t_sqi, t_export = st.tabs([
    "🌊 Welch PSD Curves", "⚡ Time-Frequency Spectrogram (STFT)", "🧠 2D Scalp Topomap", "🛡️ SQI Audit Matrix", "💾 Data & BIDS Export"
])

with t_psd:
    st.markdown("### Welch Power Spectral Density (PSD) Curves")
    try:
        fig_psd = VisualizationEngine.plot_psd_curves(target_eeg, selected_channels=selected_chs[:min(4, len(selected_chs))])
        st.plotly_chart(fig_psd, width="stretch")
    except Exception as e:
        st.error(f"Unable to render Welch PSD curves: {str(e)}")

with t_stft:
    st.markdown("### Short-Time Fourier Transform (STFT) Spectrogram")
    stft_ch = st.selectbox("Select Spectrogram Channel:", options=target_eeg.channel_names)
    try:
        fig_spec = VisualizationEngine.plot_spectrogram(target_eeg, channel_name=stft_ch)
        st.plotly_chart(fig_spec, width="stretch")
    except Exception as e:
        st.error(f"Unable to render Spectrogram: {str(e)}")

with t_topo:
    st.markdown("### 2D Topographic Scalp Power Heatmap")
    try:
        # Calculate channel power band averages
        band_pwr_map = {ch: float(np.var(target_eeg.signals[i])) for i, ch in enumerate(target_eeg.channel_names)}
        fig_topo = VisualizationEngine.plot_topomap(band_pwr_map, title="2D Topographic Scalp Power Heatmap")
        st.plotly_chart(fig_topo, width="stretch")
    except Exception as e:
        st.error(f"Unable to render 2D Topomap: {str(e)}")

with t_sqi:
    st.markdown("### Channel Quality Audit & SNR Matrix")
    ch_rows = []
    for ch in eeg_raw.channel_names:
        snr = sqi_report["channel_snr_db"].get(ch, 0.0)
        status = "PASSED" if ch not in sqi_report["bad_channels"] else "EXCLUDED"
        ch_rows.append({
            "Channel": ch,
            "SNR (dB)": f"{snr:.2f} dB",
            "SQI Status": status,
            "Contamination": "Clean" if status == "PASSED" else "High Artifact Contamination"
        })
    st.dataframe(ch_rows, width="stretch", height=320)

with t_export:
    st.markdown("### Export Derived Features & BIDS Metadata")
    exp_col1, exp_col2 = st.columns(2)
    
    with exp_col1:
        st.markdown("#### Export Preprocessed CSV Dataset")
        df_export = pd.DataFrame(target_eeg.signals.T, columns=target_eeg.channel_names)
        csv_data = df_export.to_csv(index=False).encode('utf-8')
        st.download_button(
            "📥 Download Preprocessed Signals (CSV)",
            data=csv_data,
            file_name=f"preprocessed_{target_eeg.subject_id}.csv",
            mime="text/csv"
        )
        
    with exp_col2:
        st.markdown("#### Export Standardized BIDS Metadata")
        bids_meta = {
            "SubjectID": target_eeg.subject_id,
            "SamplingFrequency": target_eeg.sampling_rate,
            "EEGChannelCount": target_eeg.n_channels,
            "RecordingDurationSec": target_eeg.duration_sec,
            "PowerlineFrequency": 50.0,
            "EEGReference": montage_opt,
            "Manufacturer": target_eeg.source_type
        }
        bids_json = json.dumps(bids_meta, indent=2).encode('utf-8')
        st.download_button(
            "📥 Download BIDS Sidecar Metadata (JSON)",
            data=bids_json,
            file_name=f"sub-{target_eeg.subject_id}_eeg.json",
            mime="application/json"
        )
