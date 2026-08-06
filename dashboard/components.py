"""
UI Components & Custom CSS Styling for NeuroLearn Research Suite Streamlit Dashboard.
Implements modern Glassmorphic Medical Dark Theme (Navy #060d19, Dark Slate #142642, Cyan #64ffda, Medical Blue #0052cc).
Includes session state safeguards for direct sub-page navigation.
"""

import streamlit as st
from visualization.styles import MEDICAL_DARK_THEME


def apply_custom_css():
    """Inject custom CSS for modern medical dark mode theme with glassmorphic aesthetics."""
    st.markdown(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&family=JetBrains+Mono:wght@400;500;600&display=swap');

    /* Main App Background & Radial Ambient Lighting */
    .stApp {{
        background-color: #060d19;
        background-image: 
            radial-gradient(at 0% 0%, rgba(0, 210, 255, 0.12) 0px, transparent 50%),
            radial-gradient(at 100% 0%, rgba(100, 255, 218, 0.08) 0px, transparent 50%),
            radial-gradient(at 50% 100%, rgba(168, 85, 247, 0.1) 0px, transparent 50%);
        background-attachment: fixed;
        color: #f1f7ff;
        font-family: 'Inter', sans-serif;
    }}
    
    /* Sidebar Styling */
    section[data-testid="stSidebar"] {{
        background-color: rgba(12, 25, 48, 0.85) !important;
        backdrop-filter: blur(16px);
        -webkit-backdrop-filter: blur(16px);
        border-right: 1px solid rgba(100, 255, 218, 0.15);
    }}

    /* Card Container with Glassmorphism & Hover Glow */
    .med-card {{
        background: rgba(20, 38, 66, 0.7);
        backdrop-filter: blur(16px);
        -webkit-backdrop-filter: blur(16px);
        border: 1px solid rgba(100, 255, 218, 0.18);
        border-radius: 12px;
        padding: 20px;
        margin-bottom: 18px;
        box-shadow: 0 12px 40px 0 rgba(0, 0, 0, 0.45);
        transition: all 0.25s cubic-bezier(0.4, 0, 0.2, 1);
        position: relative;
        overflow: hidden;
    }}

    .med-card::before {{
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        width: 100%;
        height: 3px;
        background: linear-gradient(90deg, #0052cc, #64ffda);
    }}

    .med-card:hover {{
        transform: translateY(-4px);
        border-color: #64ffda;
        box-shadow: 0 0 20px rgba(100, 255, 218, 0.35);
    }}
    
    /* KPI Card Styling */
    .kpi-title {{
        font-size: 0.8rem;
        color: #94a3b8;
        text-transform: uppercase;
        letter-spacing: 0.08em;
        font-weight: 600;
        margin-bottom: 6px;
    }}
    .kpi-value {{
        font-size: 1.9rem;
        font-weight: 800;
        color: #64ffda;
        font-family: 'JetBrains Mono', monospace;
        text-shadow: 0 0 10px rgba(100, 255, 218, 0.3);
    }}
    .kpi-subtext {{
        font-size: 0.8rem;
        color: #00d2ff;
        margin-top: 4px;
        font-weight: 500;
    }}
    
    /* Badge Tags */
    .badge-medical {{
        background: linear-gradient(135deg, #0052cc, #0040a8);
        color: #ffffff;
        padding: 4px 12px;
        border-radius: 12px;
        font-size: 0.78rem;
        font-weight: 600;
        box-shadow: 0 0 10px rgba(0, 82, 204, 0.4);
    }}
    .badge-cyan {{
        background: rgba(100, 255, 218, 0.15);
        border: 1px solid rgba(100, 255, 218, 0.4);
        color: #64ffda;
        padding: 4px 12px;
        border-radius: 12px;
        font-size: 0.78rem;
        font-weight: 700;
        box-shadow: 0 0 12px rgba(100, 255, 218, 0.2);
    }}
    </style>
    """, unsafe_allow_html=True)


def ensure_session_state():
    """Safely initialize st.session_state for sub-page rendering and direct navigation."""
    from config.manager import ConfigManager
    from data.sample_generator import generate_synthetic_eeg, save_sample_datasets
    from preprocessing.cleaner import EEGPreprocessor
    from preprocessing.quality import SignalQualityAssessment
    from segmentation.windowing import EEGSegmenter
    from features.extractor import FeatureExtractionEngine
    from attention.calculator import AttentionCalculator

    if "config" not in st.session_state:
        st.session_state.config = ConfigManager()

    if "current_eeg" not in st.session_state:
        save_sample_datasets()
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


def render_kpi_card(title: str, value: str, subtext: str = "", badge: str = ""):
    """Render a styled medical KPI metric card."""
    badge_html = f'<span class="badge-cyan">{badge}</span>' if badge else ""
    st.markdown(f"""
    <div class="med-card">
        <div style="display: flex; justify-content: space-between; align-items: center;">
            <div class="kpi-title">{title}</div>
            {badge_html}
        </div>
        <div class="kpi-value">{value}</div>
        <div class="kpi-subtext">{subtext}</div>
    </div>
    """, unsafe_allow_html=True)


def render_header(title: str, subtitle: str = ""):
    """Render standardized page header with neon gradient text and ensure session state."""
    ensure_session_state()
    st.markdown(f"""
    <div style="margin-bottom: 24px; border-bottom: 1px solid rgba(100, 255, 218, 0.2); padding-bottom: 12px;">
        <h1 style="color: #f1f7ff; font-size: 2.2rem; font-weight: 800; margin-bottom: 4px; letter-spacing: -0.5px;">
            {title}
        </h1>
        <p style="color: #94a3b8; font-size: 1.0rem; font-weight: 400; margin-top: 0px;">
            {subtitle}
        </p>
    </div>
    """, unsafe_allow_html=True)
