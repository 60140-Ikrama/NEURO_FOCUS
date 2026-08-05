"""
Unit Tests for Ablation Study Engine.
"""

import pytest
from data.sample_generator import generate_synthetic_eeg
from ablation.engine import AblationEngine


def test_ablation_engine():
    eeg = generate_synthetic_eeg(duration_sec=10.0, state="focused")
    engine = AblationEngine(eeg)

    df_pre = engine.run_preprocessing_ablation()
    assert not df_pre.empty
    assert "Configuration" in df_pre.columns

    df_win = engine.run_window_size_ablation(window_sizes=[2.0, 5.0])
    assert not df_win.empty
    assert "Window Size (s)" in df_win.columns
