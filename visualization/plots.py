"""
Plotly Interactive Visualization Engine for NeuroLearn Research Suite.
Generates publication-quality interactive charts with dark medical theme styling.
"""

from typing import List, Dict, Any, Optional
import numpy as np
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
from visualization.styles import MEDICAL_DARK_THEME, BAND_COLORS, get_plotly_layout
from data.loader import EEGData


class VisualizationEngine:
    """Publication-Grade Plotly Chart Generator."""

    @staticmethod
    def plot_eeg_signals(
        eeg_data: EEGData,
        selected_channels: Optional[List[str]] = None,
        max_seconds: float = 10.0,
        title: str = "Multi-Channel EEG Recording"
    ) -> go.Figure:
        """Plot multi-channel EEG signals stacked vertically."""
        channels = selected_channels or eeg_data.channel_names[:8]
        fs = eeg_data.sampling_rate
        max_samples = int(max_seconds * fs)
        n_samples = min(max_samples, eeg_data.n_samples)
        t = np.linspace(0, n_samples / fs, n_samples)

        fig = go.Figure()
        offset = 0.0
        step = 50.0  # uV vertical shift between stacked channels

        for i, ch in enumerate(channels):
            if ch in eeg_data.channel_names:
                idx = eeg_data.channel_names.index(ch)
                sig = eeg_data.signals[idx, :n_samples]

                fig.add_trace(go.Scatter(
                    x=t,
                    y=sig + offset,
                    mode="lines",
                    name=ch,
                    line=dict(width=1.2)
                ))
                offset -= step

        layout = get_plotly_layout(title, height=500)
        layout["xaxis"]["title"] = "Time (seconds)"
        layout["yaxis"]["title"] = "Amplitude (uV) [Stacked]"
        fig.update_layout(layout)
        return fig

    @staticmethod
    def plot_signal_quality(sqi_report: Dict[str, Any]) -> go.Figure:
        """Plot Signal Quality Index (SQI) per channel as colored bar chart."""
        ch_sqi = sqi_report.get("channel_sqi", {})
        channels = list(ch_sqi.keys())
        scores = list(ch_sqi.values())

        colors = []
        for s in scores:
            if s >= 80:
                colors.append(MEDICAL_DARK_THEME["success_green"])
            elif s >= 60:
                colors.append(MEDICAL_DARK_THEME["accent_cyan"])
            elif s >= 40:
                colors.append(MEDICAL_DARK_THEME["warning_yellow"])
            else:
                colors.append(MEDICAL_DARK_THEME["danger_red"])

        fig = go.Figure(go.Bar(
            x=channels,
            y=scores,
            marker_color=colors,
            text=[f"{s}%" for s in scores],
            textposition="auto"
        ))

        layout = get_plotly_layout("Signal Quality Index (SQI) Audit", height=380)
        layout["xaxis"]["title"] = "EEG Channel"
        layout["yaxis"]["title"] = "SQI Score (%)"
        layout["yaxis"]["range"] = [0, 105]
        fig.update_layout(layout)
        return fig

    @staticmethod
    def plot_psd(
        freqs: np.ndarray,
        psd: np.ndarray,
        channel_name: str = "Cz",
        psd_method: str = "Welch"
    ) -> go.Figure:
        """Plot Power Spectral Density with frequency band color shading."""
        fig = go.Figure()

        # PSD Line
        fig.add_trace(go.Scatter(
            x=freqs,
            y=psd,
            mode="lines",
            name=f"{channel_name} PSD",
            line=dict(color=MEDICAL_DARK_THEME["accent_cyan"], width=2.0)
        ))

        # Band Shading overlay
        bands = [
            ("Delta (0.5-4Hz)", 0.5, 4.0, BAND_COLORS["delta"]),
            ("Theta (4-8Hz)", 4.0, 8.0, BAND_COLORS["theta"]),
            ("Alpha (8-13Hz)", 8.0, 13.0, BAND_COLORS["alpha"]),
            ("Beta (13-30Hz)", 13.0, 30.0, BAND_COLORS["beta"]),
            ("Gamma (30-40Hz)", 30.0, 40.0, BAND_COLORS["gamma"])
        ]

        max_psd = np.max(psd) if len(psd) > 0 else 1.0

        for b_name, l_f, h_f, color in bands:
            idx = np.where((freqs >= l_f) & (freqs <= h_f))[0]
            if len(idx) > 0:
                fig.add_trace(go.Scatter(
                    x=freqs[idx],
                    y=psd[idx],
                    mode="lines",
                    fill="tozeroy",
                    name=b_name,
                    line=dict(color=color, width=0),
                    opacity=0.3
                ))

        layout = get_plotly_layout(f"Power Spectral Density ({psd_method} Method) - Channel {channel_name}", height=450)
        layout["xaxis"]["title"] = "Frequency (Hz)"
        layout["yaxis"]["title"] = "Power (uV^2 / Hz)"
        layout["xaxis"]["range"] = [0, 45]
        fig.update_layout(layout)
        return fig

    @staticmethod
    def plot_attention_timeline(df_attention: pd.DataFrame) -> go.Figure:
        """Plot Attention Score timeline (0-100) with 5-level threshold zones."""
        fig = go.Figure()

        if "start_sec" not in df_attention.columns or "attention_score" not in df_attention.columns:
            return fig

        t = df_attention["start_sec"]
        scores = df_attention["attention_score"]

        # Background threshold zones
        fig.add_hrect(y0=0, y1=20, fillcolor=MEDICAL_DARK_THEME["danger_red"], opacity=0.12, line_width=0, annotation_text="Very Low")
        fig.add_hrect(y0=20, y1=40, fillcolor=MEDICAL_DARK_THEME["warning_yellow"], opacity=0.12, line_width=0, annotation_text="Low")
        fig.add_hrect(y0=40, y1=60, fillcolor="#3498db", opacity=0.12, line_width=0, annotation_text="Moderate")
        fig.add_hrect(y0=60, y1=80, fillcolor=MEDICAL_DARK_THEME["accent_cyan"], opacity=0.12, line_width=0, annotation_text="High")
        fig.add_hrect(y0=80, y1=100, fillcolor=MEDICAL_DARK_THEME["success_green"], opacity=0.12, line_width=0, annotation_text="Very High")

        # Timeline curve
        fig.add_trace(go.Scatter(
            x=t,
            y=scores,
            mode="lines+markers",
            name="Attention Score",
            line=dict(color=MEDICAL_DARK_THEME["accent_cyan"], width=2.5),
            marker=dict(size=6, color=MEDICAL_DARK_THEME["accent_blue"])
        ))

        layout = get_plotly_layout("Neurophysiological Attention Score Timeline", height=450)
        layout["xaxis"]["title"] = "Recording Time (seconds)"
        layout["yaxis"]["title"] = "Attention Index Score (0-100)"
        layout["yaxis"]["range"] = [-2, 102]
        fig.update_layout(layout)
        return fig

    @staticmethod
    def plot_bland_altman(ba_metrics: Dict[str, Any], title: str = "Bland-Altman Agreement Plot") -> go.Figure:
        """Plot Bland-Altman agreement chart with mean bias and 95% Limits of Agreement."""
        fig = go.Figure()

        bias = ba_metrics.get("mean_difference", 0.0)
        loa_u = ba_metrics.get("loa_upper_95", 0.0)
        loa_l = ba_metrics.get("loa_lower_95", 0.0)

        # Plot horizontal bias lines
        fig.add_hline(y=bias, line_dash="dash", line_color=MEDICAL_DARK_THEME["accent_cyan"], annotation_text=f"Mean Bias ({bias:.2f})")
        fig.add_hline(y=loa_u, line_dash="dot", line_color=MEDICAL_DARK_THEME["warning_yellow"], annotation_text=f"+1.96 SD ({loa_u:.2f})")
        fig.add_hline(y=loa_l, line_dash="dot", line_color=MEDICAL_DARK_THEME["warning_yellow"], annotation_text=f"-1.96 SD ({loa_l:.2f})")

        layout = get_plotly_layout(title, height=420)
        layout["xaxis"]["title"] = "Mean of Measurements"
        layout["yaxis"]["title"] = "Difference (Measurement 1 - Measurement 2)"
        fig.update_layout(layout)
        return fig

    @staticmethod
    def plot_ablation_matrix(df_ablation: pd.DataFrame, title: str = "Ablation Study Matrix") -> go.Figure:
        """Plot comparative bar chart for Ablation Study results."""
        if df_ablation.empty:
            return go.Figure()

        x_col = df_ablation.columns[0]
        y_col = "Mean Attention" if "Mean Attention" in df_ablation.columns else df_ablation.columns[1]

        fig = px.bar(
            df_ablation,
            x=x_col,
            y=y_col,
            color=y_col,
            color_continuous_scale="Viridis",
            text_auto=".1f"
        )
        layout = get_plotly_layout(title, height=420)
        fig.update_layout(layout)
        return fig
