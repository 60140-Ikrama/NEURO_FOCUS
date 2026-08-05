"""
Systematic Ablation Study Engine for NeuroLearn Research Suite.
Evaluates the quantitative impact of preprocessing choices, window sizes, PSD estimation methods,
attention formulas, and feature sets on final attention metrics.
"""

from typing import Dict, Any, List, Optional
import pandas as pd
import numpy as np
from data.loader import EEGData
from preprocessing.cleaner import EEGPreprocessor
from segmentation.windowing import EEGSegmenter
from features.extractor import FeatureExtractionEngine
from attention.calculator import AttentionCalculator
from utils.logger import get_logger

logger = get_logger("AblationEngine")


class AblationEngine:
    """Systematic Research Ablation Workspace."""

    def __init__(self, raw_eeg: EEGData):
        self.raw_eeg = raw_eeg

    def run_preprocessing_ablation(self) -> pd.DataFrame:
        """Systematically evaluate Preprocessing Pipeline configurations."""
        logger.info("Running Preprocessing Pipeline Ablation Study...")
        configs = [
            ("Raw Signal", EEGPreprocessor(normalization="none", detrend=False)),
            ("Bandpass Only", EEGPreprocessor(lowcut=1.0, highcut=40.0, detrend=False, normalization="none")),
            ("Bandpass + Notch", EEGPreprocessor(lowcut=1.0, highcut=40.0, notch_freq=50.0, detrend=False, normalization="none")),
            ("Full Preprocessing", EEGPreprocessor(lowcut=1.0, highcut=40.0, notch_freq=50.0, detrend=True, normalization="zscore"))
        ]

        results = []
        segmenter = EEGSegmenter(window_sec=5.0, overlap_ratio=0.5)

        for name, cleaner in configs:
            clean_eeg, _ = cleaner.process(self.raw_eeg)
            epochs = segmenter.segment(clean_eeg)

            fe = FeatureExtractionEngine(psd_method="welch")
            df_feat = fe.extract_features(epochs)

            calc = AttentionCalculator(formula_str="beta / theta")
            df_att, summary = calc.compute_attention(df_feat)

            results.append({
                "Configuration": name,
                "Mean Attention": summary["average_attention"],
                "Peak Attention": summary["peak_attention"],
                "Min Attention": summary["minimum_attention"],
                "Stability Index": summary["stability_index"],
                "Drop Count": summary["attention_drop_count"],
                "Dominant Category": summary["dominant_category"]
            })

        return pd.DataFrame(results)

    def run_window_size_ablation(self, window_sizes: List[float] = [2.0, 5.0, 10.0, 20.0, 30.0]) -> pd.DataFrame:
        """Systematically evaluate impact of Sliding Window sizes (2s - 30s)."""
        logger.info("Running Window Size Ablation Study...")
        cleaner = EEGPreprocessor(lowcut=1.0, highcut=40.0, notch_freq=50.0, detrend=True, normalization="zscore")
        clean_eeg, _ = cleaner.process(self.raw_eeg)

        results = []
        fe = FeatureExtractionEngine(psd_method="welch")
        calc = AttentionCalculator(formula_str="beta / theta")

        for w_sec in window_sizes:
            segmenter = EEGSegmenter(window_sec=w_sec, overlap_ratio=0.5)
            epochs = segmenter.segment(clean_eeg)

            df_feat = fe.extract_features(epochs)
            df_att, summary = calc.compute_attention(df_feat)

            results.append({
                "Window Size (s)": w_sec,
                "Epoch Count": len(epochs),
                "Mean Attention": summary["average_attention"],
                "Peak Attention": summary["peak_attention"],
                "Min Attention": summary["minimum_attention"],
                "Stability Index": summary["stability_index"],
                "Drop Count": summary["attention_drop_count"]
            })

        return pd.DataFrame(results)

    def run_psd_method_ablation(self) -> pd.DataFrame:
        """Systematically compare Welch vs FFT vs Multitaper PSD methods."""
        logger.info("Running PSD Method Ablation Study...")
        cleaner = EEGPreprocessor(lowcut=1.0, highcut=40.0, notch_freq=50.0, detrend=True)
        clean_eeg, _ = cleaner.process(self.raw_eeg)
        segmenter = EEGSegmenter(window_sec=5.0, overlap_ratio=0.5)
        epochs = segmenter.segment(clean_eeg)

        methods = ["welch", "fft", "multitaper"]
        results = []
        calc = AttentionCalculator(formula_str="beta / theta")

        for method in methods:
            fe = FeatureExtractionEngine(psd_method=method)
            df_feat = fe.extract_features(epochs)
            df_att, summary = calc.compute_attention(df_feat)

            results.append({
                "PSD Method": method.upper(),
                "Mean Attention": summary["average_attention"],
                "Peak Attention": summary["peak_attention"],
                "Min Attention": summary["minimum_attention"],
                "Stability Index": summary["stability_index"]
            })

        return pd.DataFrame(results)

    def run_formula_ablation(self) -> pd.DataFrame:
        """Systematically evaluate different Attention Index formulas."""
        logger.info("Running Attention Formula Ablation Study...")
        cleaner = EEGPreprocessor(lowcut=1.0, highcut=40.0, notch_freq=50.0)
        clean_eeg, _ = cleaner.process(self.raw_eeg)
        segmenter = EEGSegmenter(window_sec=5.0, overlap_ratio=0.5)
        epochs = segmenter.segment(clean_eeg)

        fe = FeatureExtractionEngine(psd_method="welch")
        df_feat = fe.extract_features(epochs)

        formulas = {
            "Classic Beta/Theta": "beta / theta",
            "Extended (Beta+Gamma)/(Theta+Alpha)": "(beta + gamma) / (theta + alpha)",
            "Beta/Alpha": "beta / alpha",
            "Alpha/Theta": "alpha / theta",
            "Composite Index": "(0.6 * beta + 0.4 * gamma) / (0.6 * theta + 0.4 * alpha)"
        }

        results = []
        for name, form in formulas.items():
            calc = AttentionCalculator(formula_str=form)
            df_att, summary = calc.compute_attention(df_feat)

            results.append({
                "Formula Name": name,
                "Formula Expression": form,
                "Mean Attention": summary["average_attention"],
                "Peak Attention": summary["peak_attention"],
                "Min Attention": summary["minimum_attention"],
                "Stability Index": summary["stability_index"],
                "Dominant Category": summary["dominant_category"]
            })

        return pd.DataFrame(results)
