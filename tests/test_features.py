"""
Unit Tests for Feature Extraction Engine & Hjorth Parameters.
"""

import pytest
import numpy as np
from data.sample_generator import generate_synthetic_eeg
from segmentation.windowing import EEGSegmenter
from features.extractor import FeatureExtractionEngine
from utils.math_utils import compute_hjorth_parameters


def test_hjorth_parameters():
    x = np.sin(np.linspace(0, 10, 256))
    act, mob, comp = compute_hjorth_parameters(x)
    assert act > 0
    assert mob > 0
    assert comp >= 0


def test_feature_extraction_engine():
    eeg = generate_synthetic_eeg(duration_sec=10.0, state="focused")
    segmenter = EEGSegmenter(window_sec=5.0, overlap_ratio=0.5)
    epochs = segmenter.segment(eeg)

    fe = FeatureExtractionEngine(psd_method="welch")
    df_feat = fe.extract_features(epochs)

    assert not df_feat.empty
    assert "epoch_id" in df_feat.columns
    assert len(df_feat) == len(epochs)
