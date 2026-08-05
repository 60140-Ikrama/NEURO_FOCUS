"""
NeuroLearn Research Suite - Main Streamlit Application Entrypoint.
Provides centralized session state, navigation bar, sample dataset auto-generation,
and unified research workflow routing.
"""

import sys
import os
import streamlit as st

# Add workspace directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config.manager import ConfigManager
from data.loader import EEGDataLoader, EEGData
from data.sample_generator import generate_synthetic_eeg, save_sample_datasets
from data.biopac import BiopacImportManager
from preprocessing.cleaner import EEGPreprocessor
from preprocessing.quality import SignalQualityAssessment
from segmentation.windowing import EEGSegmenter
from features.extractor import FeatureExtractionEngine
from attention.calculator import AttentionCalculator
from dashboard.components import apply_custom_css, render_header, render_kpi_card
from visualization.plots import VisualizationEngine

st.set_page_config(
    page_title="NeuroLearn Research Suite",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded"
)

apply_custom_css()

# Initialize Session State
if "config" not in st.session_state:
    st.session_state.config = ConfigManager()

if "current_eeg" not in st.session_state:
    # Auto-generate focused sample EEG for default state
    sample_files = save_sample_datasets()
    st.session_state.current_eeg = generate_synthetic_eeg(duration_sec=30.0, state="focused")

if "clean_eeg" not in st.session_state:
    cleaner = EEGPreprocessor(lowcut=1.0, highcut=40.0, notch_freq=50.0)
    clean_data, log = cleaner.process(st.session_state.current_eeg)
    st.session_state.clean_eeg = clean_data
    st.session_state.preproc_log = log

if "sqi_report" not in st.session_state:
    sqa = SignalQualityAssessment()
    st.session_state.sqi_report = sqa.evaluate(st.session_state.current_eeg)

if "df_attention" not in st.session_state:
    segmenter = EEGSegmenter(window_sec=5.0, overlap_ratio=0.5)
    epochs = segmenter.segment(st.session_state.clean_eeg)
    fe = FeatureExtractionEngine(psd_method="welch")
    df_feat = fe.extract_features(epochs)
    calc = AttentionCalculator(formula_str="beta / theta")
    df_att, summary = calc.compute_attention(df_feat)
    st.session_state.df_attention = df_att
    st.session_state.att_summary = summary


# Sidebar Navigation & System Status
with st.sidebar:
    st.image("https://img.icons8.com/isometric/100/brain.png", width=60)
    st.markdown("### **NeuroLearn Research Suite**")
    st.markdown("`v1.0.0 | Research Edition`")
    st.markdown("---")

    st.markdown("#### **Active Dataset**")
    eeg = st.session_state.current_eeg
    st.info(f"**{eeg.subject_id}** ({eeg.source_type})\n\n"
            f"⚡ **{eeg.sampling_rate} Hz** | 📊 **{eeg.n_channels} Channels**\n\n"
            f"⏱️ **{eeg.duration_sec:.1f}s** | SQI: **{st.session_state.sqi_report['overall_sqi']}%**")

    st.markdown("---")
    st.markdown("🛡️ **Methodology**: 100% BSP / Non-ML")
    st.markdown("🏛️ **Institution**: BME Neuroscience Lab")


# Main Page Home Hero Banner
render_header("NeuroLearn Research Suite", "Modular Platform for EEG-Based Attention Quantification & Biomedical Signal Processing")

col1, col2, col3, col4 = st.columns(4)

with col1:
    render_kpi_card(
        "Signal Quality Index",
        f"{st.session_state.sqi_report['overall_sqi']}%",
        f"{st.session_state.sqi_report['good_channel_count']}/{st.session_state.current_eeg.n_channels} Channels Passing",
        "SQI Audit"
    )

with col2:
    render_kpi_card(
        "Mean Attention Score",
        f"{st.session_state.att_summary['average_attention']:.1f} / 100",
        f"Category: {st.session_state.att_summary['dominant_category']}",
        "Attention"
    )

with col3:
    render_kpi_card(
        "Attention Stability",
        f"{st.session_state.att_summary['stability_index']:.1f} / 100",
        f"Attention Drops: {st.session_state.att_summary['attention_drop_count']} Events",
        "Stability"
    )

with col4:
    render_kpi_card(
        "Acquisition Hardware",
        f"{eeg.source_type.split('_')[0]}",
        f"Sampling: {eeg.sampling_rate} Hz",
        "Hardware"
    )

st.markdown("---")

# Quick Visual Preview
t1, t2 = st.tabs(["📊 Live EEG Signal Viewer", "📈 Attention Score Timeline"])

with t1:
    fig_eeg = VisualizationEngine.plot_eeg_signals(st.session_state.clean_eeg, max_seconds=10.0)
    st.plotly_chart(fig_eeg, use_container_width=True)

with t2:
    fig_att = VisualizationEngine.plot_attention_timeline(st.session_state.df_attention)
    st.plotly_chart(fig_att, use_container_width=True)

st.markdown("""
### 🔬 Quick Navigation Guide
Use the **sidebar menu** to access specialized research workspaces:
- **01 Dataset Manager**: Import EDF, MAT, CSV, TXT files or Biopac AcqKnowledge exports.
- **02 EEG Viewer**: Interactive scrollable multi-channel signal viewer with zoom & pan.
- **03 Signal Preprocessing**: Configure 1-40Hz Bandpass, 50Hz Notch, and channel quality filters.
- **04 Frequency Analysis**: Welch & Multitaper PSD curves, Spectrograms, and SEF95 metrics.
- **05 Attention Analysis**: Mathematical ratio formulations, custom formula builder, and 5-level state classification.
- **06 Statistical Analysis**: Hypothesis testing (t-tests, Mann-Whitney), CIs, and Bland-Altman agreement.
- **07 Ablation Study**: Systematic comparative evaluation across filter pipelines, window sizes, and PSD methods.
- **08 Research Validation**: Direct cross-dataset agreement audit (PhysioNet vs. Biopac).
- **09 Experiment Explorer**: View, restore, and audit 100% reproducible experiment snapshots.
- **10 Report Center**: Generate IEEE/Frontiers-styled PDF, Word DOCX, and CSV laboratory reports.
- **11 Settings**: Global configuration overrides.
""")
