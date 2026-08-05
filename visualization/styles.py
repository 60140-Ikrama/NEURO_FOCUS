"""
Visualization Theme & Styling Definitions for NeuroLearn Research Suite.
Professional Dark Medical Theme (Navy #0a192f, Dark Slate #172a45, Cyan #64ffda, Medical Blue #0052cc).
"""

from typing import Dict, Any

MEDICAL_DARK_THEME = {
    "bg_color": "#0a192f",
    "paper_bg": "#172a45",
    "card_bg": "#172a45",
    "text_color": "#e6f1ff",
    "subtext_color": "#8892b0",
    "accent_cyan": "#64ffda",
    "accent_blue": "#00d2ff",
    "medical_blue": "#0052cc",
    "warning_yellow": "#ffb703",
    "danger_red": "#ff4d4d",
    "success_green": "#00e676",
    "grid_color": "#233554",
    "font_family": "Inter, Roboto, Arial, sans-serif"
}

# Color mapping for EEG Frequency Bands
BAND_COLORS = {
    "delta": "#9b59b6",   # Purple
    "theta": "#3498db",   # Soft Blue
    "alpha": "#2ecc71",   # Emerald Green
    "beta": "#e67e22",    # Warm Orange
    "gamma": "#e74c3c"    # Crimson Red
}


def get_plotly_layout(title: str = "", height: int = 450) -> Dict[str, Any]:
    """Get standardized dark medical Plotly layout dictionary."""
    return {
        "title": {"text": f"<b>{title}</b>", "font": {"color": MEDICAL_DARK_THEME["text_color"], "size": 16}},
        "paper_bgcolor": MEDICAL_DARK_THEME["paper_bg"],
        "plot_bgcolor": MEDICAL_DARK_THEME["bg_color"],
        "font": {"color": MEDICAL_DARK_THEME["text_color"], "family": MEDICAL_DARK_THEME["font_family"]},
        "margin": dict(l=50, r=30, t=50, b=50),
        "height": height,
        "xaxis": {
            "gridcolor": MEDICAL_DARK_THEME["grid_color"],
            "zerolinecolor": MEDICAL_DARK_THEME["grid_color"],
            "title_font": {"color": MEDICAL_DARK_THEME["subtext_color"]}
        },
        "yaxis": {
            "gridcolor": MEDICAL_DARK_THEME["grid_color"],
            "zerolinecolor": MEDICAL_DARK_THEME["grid_color"],
            "title_font": {"color": MEDICAL_DARK_THEME["subtext_color"]}
        },
        "legend": {
            "font": {"color": MEDICAL_DARK_THEME["text_color"]},
            "bgcolor": "rgba(0,0,0,0)"
        }
    }
