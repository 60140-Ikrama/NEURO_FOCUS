"""
UI Components & Custom CSS Styling for NeuroLearn Research Suite Streamlit Dashboard.
Implements modern Dark Medical Theme (Navy #0a192f, Dark Slate #172a45, Cyan #64ffda, Medical Blue #0052cc).
"""

import streamlit as st
from visualization.styles import MEDICAL_DARK_THEME


def apply_custom_css():
    """Inject custom CSS for modern medical dark mode theme."""
    st.markdown(f"""
    <style>
    /* Main Background */
    .stApp {{
        background-color: {MEDICAL_DARK_THEME["bg_color"]};
        color: {MEDICAL_DARK_THEME["text_color"]};
        font-family: 'Inter', sans-serif;
    }}
    
    /* Sidebar styling */
    section[data-testid="stSidebar"] {{
        background-color: {MEDICAL_DARK_THEME["paper_bg"]};
        border-right: 1px solid {MEDICAL_DARK_THEME["grid_color"]};
    }}
    
    /* Card Container */
    .med-card {{
        background-color: {MEDICAL_DARK_THEME["card_bg"]};
        border: 1px solid {MEDICAL_DARK_THEME["grid_color"]};
        border-radius: 8px;
        padding: 18px;
        margin-bottom: 15px;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.3);
    }}
    
    /* KPI Card styling */
    .kpi-title {{
        font-size: 0.85rem;
        color: {MEDICAL_DARK_THEME["subtext_color"]};
        text-transform: uppercase;
        letter-spacing: 0.05em;
        margin-bottom: 4px;
    }}
    .kpi-value {{
        font-size: 1.8rem;
        font-weight: 700;
        color: {MEDICAL_DARK_THEME["accent_cyan"]};
    }}
    .kpi-subtext {{
        font-size: 0.8rem;
        color: {MEDICAL_DARK_THEME["accent_blue"]};
        margin-top: 2px;
    }}
    
    /* Badge tags */
    .badge-medical {{
        background-color: {MEDICAL_DARK_THEME["medical_blue"]};
        color: #ffffff;
        padding: 4px 10px;
        border-radius: 12px;
        font-size: 0.8rem;
        font-weight: 600;
    }}
    .badge-cyan {{
        background-color: {MEDICAL_DARK_THEME["accent_cyan"]};
        color: #0a192f;
        padding: 4px 10px;
        border-radius: 12px;
        font-size: 0.8rem;
        font-weight: 700;
    }}
    </style>
    """, unsafe_allow_html=True)


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
    """Render standardized page header."""
    st.markdown(f"""
    <div style="margin-bottom: 20px;">
        <h1 style="color: {MEDICAL_DARK_THEME['text_color']}; font-size: 2.2rem; margin-bottom: 0px;">
            {title}
        </h1>
        <p style="color: {MEDICAL_DARK_THEME['subtext_color']}; font-size: 1.0rem; margin-top: 4px;">
            {subtitle}
        </p>
    </div>
    """, unsafe_allow_html=True)
