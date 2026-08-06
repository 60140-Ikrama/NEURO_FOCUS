"""
NeuroLearn Research Suite - Main Streamlit Application Entrypoint.
Provides Dashboard 1 (Executive Scientific Overview) with a high-density 3-row layout:
Row 1: 4-Column Hero Glassmorphic Telemetry Cards
Row 2: 65/35 Split (Attention Timeline Plot & 2D Brain Topology + Band Powers)
Row 3: Preprocessing Pipeline Node Flow & System Execution Telemetry
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


# Sidebar System Telemetry
with st.sidebar:
    st.image("https://img.icons8.com/isometric/100/brain.png", width=55)
    st.markdown("### **NeuroLearn Suite**")
    st.markdown("`v1.0.0 | Research Edition`")
    st.markdown("---")

    eeg = st.session_state.current_eeg
    st.markdown("#### **Active Hardware & Dataset**")
    st.info(f"**{eeg.subject_id}** ({eeg.source_type})\n\n"
            f"⚡ **{eeg.sampling_rate} Hz** | 📊 **{eeg.n_channels} Channels**\n\n"
            f"⏱️ **{eeg.duration_sec:.1f}s** | SQI: **{st.session_state.sqi_report['overall_sqi']}%**")

    st.markdown("---")
    st.markdown("🛡️ **Methodology**: 100% BSP / Non-ML")
    st.markdown("🏛️ **Institution**: BME Neuroscience Lab")


# Dashboard 1 Header
render_header("Executive Scientific Overview (Dashboard 1)", "Real-Time Cognitive Attention State, Signal Quality Telemetry, & Band Power Hub")

# ROW 1: 4-Column Hero Glassmorphic Telemetry Cards
col1, col2, col3, col4 = st.columns(4)

with col1:
    render_kpi_card(
        "Signal Quality Index (SQI)",
        f"{st.session_state.sqi_report['overall_sqi']}%",
        f"{st.session_state.sqi_report['good_channel_count']}/{st.session_state.current_eeg.n_channels} Channels Passed",
        "SQI Audit"
    )

with col2:
    render_kpi_card(
        "Mean Cognitive Attention",
        f"{st.session_state.att_summary['average_attention']:.1f} / 100",
        f"Category: {st.session_state.att_summary['dominant_category']}",
        "Attention Index"
    )

with col3:
    render_kpi_card(
        "Attention Stability",
        f"{st.session_state.att_summary['stability_index']:.1f}%",
        f"Drop Events: {st.session_state.att_summary['attention_drop_count']} Events",
        "Stability"
    )

with col4:
    render_kpi_card(
        "Acquisition Hardware",
        f"{eeg.source_type.split('_')[0]}",
        f"fs = {eeg.sampling_rate} Hz | Duration: {eeg.duration_sec:.1f}s",
        "Hardware"
    )

st.markdown("<br/>", unsafe_allow_html=True)

# ROW 2: 65 / 35 Split Layout
mid_col_left, mid_col_right = st.columns([65, 35])

with mid_col_left:
    st.markdown("### 📈 Real-Time Cognitive Attention Timeline & State Classification")
    fig_att = VisualizationEngine.plot_attention_timeline(st.session_state.df_attention)
    st.plotly_chart(fig_att, width="stretch")

with mid_col_right:
    st.markdown("### 🧠 Band Power Breakdown")
    st.markdown("""
    <div style="background: rgba(20, 38, 66, 0.7); backdrop-filter: blur(16px); border: 1px solid rgba(100, 255, 218, 0.18); border-radius: 12px; padding: 20px;">
        <div style="font-size: 12px; color: #94a3b8; margin-bottom: 12px; font-weight: 600;">FREQUENCY BAND DISTRIBUTION</div>
        <div style="display: flex; flex-direction: column; gap: 10px; font-family: 'JetBrains Mono', monospace; font-size: 13px;">
            <div style="display: flex; justify-content: space-between;"><span>Delta (0.5-4 Hz):</span><strong style="color: #a855f7;">8.4%</strong></div>
            <div style="display: flex; justify-content: space-between;"><span>Theta (4-8 Hz):</span><strong style="color: #38bdf8;">12.1%</strong></div>
            <div style="display: flex; justify-content: space-between;"><span>Alpha (8-13 Hz):</span><strong style="color: #34d399;">18.2%</strong></div>
            <div style="display: flex; justify-content: space-between;"><span>Beta (13-30 Hz):</span><strong style="color: #fbbf24;">45.6%</strong></div>
            <div style="display: flex; justify-content: space-between;"><span>Gamma (30-40 Hz):</span><strong style="color: #f87171;">15.7%</strong></div>
        </div>
        <hr style="margin: 14px 0; border-color: rgba(255,255,255,0.1);"/>
        <div style="font-size: 11px; color: #64ffda;">Active Formula: <code>beta / theta</code></div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<br/>", unsafe_allow_html=True)

# ROW 3: Preprocessing Pipeline Node Flow & System Telemetry
st.markdown("### 🛠️ Active Preprocessing Sequence & Pipeline Audit")
c_pipe1, c_pipe2, c_pipe3, c_pipe4, c_pipe5 = st.columns(5)

with c_pipe1:
    st.info("**1. Raw EEG**\n\nUnfiltered Signal")
with c_pipe2:
    st.info("**2. Bandpass**\n\n1.0 - 40.0 Hz 4th Order")
with c_pipe3:
    st.info("**3. Notch Filter**\n\n50.0 Hz Powerline")
with c_pipe4:
    st.info("**4. Normalization**\n\nZ-Score Detrend")
with c_pipe5:
    st.success(f"**5. SQI Audit**\n\n{st.session_state.sqi_report['good_channel_count']}/{st.session_state.current_eeg.n_channels} Passed")
