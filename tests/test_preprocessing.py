"""
Unit Tests for Preprocessing & Signal Quality Assessment.
"""

import pytest
import numpy as np
from data.sample_generator import generate_synthetic_eeg
from preprocessing.cleaner import EEGPreprocessor
from preprocessing.quality import SignalQualityAssessment


def test_preprocessor_pipeline():
    eeg = generate_synthetic_eeg(duration_sec=5.0, state="focused")
    cleaner = EEGPreprocessor(lowcut=1.0, highcut=40.0, notch_freq=50.0, normalization="zscore")
    clean_eeg, log = cleaner.process(eeg)

    assert clean_eeg.n_channels == eeg.n_channels
    assert clean_eeg.signals.shape == eeg.signals.shape
    assert log["lowcut"] == 1.0
    assert log["highcut"] == 40.0


def test_signal_quality_assessment():
    eeg = generate_synthetic_eeg(duration_sec=5.0, state="focused")
    sqa = SignalQualityAssessment()
    sqi_report = sqa.evaluate(eeg)

    assert "overall_sqi" in sqi_report
    assert 0.0 <= sqi_report["overall_sqi"] <= 100.0
    assert sqi_report["good_channel_count"] <= eeg.n_channels
