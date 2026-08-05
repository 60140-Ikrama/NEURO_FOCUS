"""
Unit Tests for Formula Evaluator & Attention Calculator.
"""

import pytest
import numpy as np
from attention.formula_builder import FormulaEvaluator
from attention.calculator import AttentionCalculator
from data.sample_generator import generate_synthetic_eeg
from segmentation.windowing import EEGSegmenter
from features.extractor import FeatureExtractionEngine


def test_formula_evaluator():
    vars_dict = {"theta": 2.0, "alpha": 4.0, "beta": 6.0, "gamma": 8.0}
    val1 = FormulaEvaluator.evaluate("beta / theta", vars_dict)
    assert val1 == 3.0

    val2 = FormulaEvaluator.evaluate("(beta + gamma) / (theta + alpha)", vars_dict)
    assert val2 == (14.0 / 6.0)


def test_attention_calculator():
    eeg = generate_synthetic_eeg(duration_sec=10.0, state="focused")
    segmenter = EEGSegmenter(window_sec=5.0, overlap_ratio=0.5)
    epochs = segmenter.segment(eeg)

    fe = FeatureExtractionEngine(psd_method="welch")
    df_feat = fe.extract_features(epochs)

    calc = AttentionCalculator(formula_str="beta / theta")
    df_att, summary = calc.compute_attention(df_feat)

    assert "attention_score" in df_att.columns
    assert "attention_category" in df_att.columns
    assert 0.0 <= summary["average_attention"] <= 100.0
