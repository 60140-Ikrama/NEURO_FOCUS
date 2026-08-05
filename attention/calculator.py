"""
Mathematical Attention Calculator for NeuroLearn Research Suite.
Pure Biomedical Signal Processing attention quantification without machine learning models.
"""

from typing import Dict, Any, List, Optional, Tuple
import numpy as np
import pandas as pd
from attention.formula_builder import FormulaEvaluator
from utils.logger import get_logger

logger = get_logger("AttentionCalculator")


class AttentionCalculator:
    """Computes mathematical attention index, normalizes to 0-100, and classifies state."""

    def __init__(
        self,
        formula_str: str = "beta / theta",
        target_channels: Optional[List[str]] = None,
        very_low_thresh: float = 20.0,
        low_thresh: float = 40.0,
        mod_thresh: float = 60.0,
        high_thresh: float = 80.0
    ):
        self.formula_str = formula_str
        self.target_channels = target_channels
        self.thresholds = {
            "very_low": very_low_thresh,
            "low": low_thresh,
            "moderate": mod_thresh,
            "high": high_thresh
        }

    def compute_attention(self, df_features: pd.DataFrame) -> Tuple[pd.DataFrame, Dict[str, Any]]:
        """
        Calculate Attention Score (0-100) and Category per epoch.
        :param df_features: DataFrame output from FeatureExtractionEngine
        """
        if df_features.empty:
            return pd.DataFrame(), {}

        df_out = df_features.copy()
        raw_scores = []

        # Identify channels present in feature columns
        abs_power_cols = [c for c in df_features.columns if "_abs_power" in c]
        available_channels = list(set([c.split("_")[0] for c in abs_power_cols]))

        eval_channels = self.target_channels or available_channels

        for idx, row in df_features.iterrows():
            # Aggregate band powers across selected channels for epoch
            band_vals = {"delta": 0.0, "theta": 0.0, "alpha": 0.0, "beta": 0.0, "gamma": 0.0}
            ch_count = 0

            for ch in eval_channels:
                for b in band_vals.keys():
                    col_name = f"{ch}_{b}_abs_power"
                    if col_name in row:
                        band_vals[b] += float(row[col_name])
                ch_count += 1

            if ch_count > 0:
                for b in band_vals.keys():
                    band_vals[b] /= ch_count

            # Prevent zero division in denominator bands
            for b in band_vals.keys():
                if band_vals[b] <= 0:
                    band_vals[b] = 1e-6

            # Evaluate formula
            try:
                raw_idx = FormulaEvaluator.evaluate(self.formula_str, band_vals)
            except Exception as e:
                logger.warning(f"Formula evaluation error at epoch {idx}: {e}")
                raw_idx = 0.0

            raw_scores.append(raw_idx)

        df_out["attention_raw"] = raw_scores

        # Normalize to 0 - 100 scale using Sigmoid or Min-Max clipping
        raw_arr = np.array(raw_scores)
        if len(raw_arr) > 1 and np.std(raw_arr) > 0:
            # Sigmoidal mapping centered around median for smooth [0, 100] distribution
            med = np.median(raw_arr)
            scale = np.std(raw_arr) if np.std(raw_arr) > 0 else 1.0
            norm_scores = 100.0 / (1.0 + np.exp(-(raw_arr - med) / (scale + 1e-6)))
        else:
            norm_scores = np.clip(raw_arr * 20.0, 0.0, 100.0)

        df_out["attention_score"] = np.round(norm_scores, 2)

        # 5-Level Rule-Based Classification
        categories = []
        for score in norm_scores:
            if score < self.thresholds["very_low"]:
                cat = "Very Low Attention"
            elif score < self.thresholds["low"]:
                cat = "Low Attention"
            elif score < self.thresholds["moderate"]:
                cat = "Moderate Attention"
            elif score < self.thresholds["high"]:
                cat = "High Attention"
            else:
                cat = "Very High Attention"
            categories.append(cat)

        df_out["attention_category"] = categories

        # Aggregate Summary Statistics
        avg_score = float(np.mean(norm_scores))
        peak_score = float(np.max(norm_scores))
        min_score = float(np.min(norm_scores))
        stability_idx = float(100.0 - np.std(norm_scores))  # Higher stability = lower variance

        # Detect attention drops (drop > 25 points between consecutive epochs)
        drops = np.where(np.diff(norm_scores) < -25.0)[0]
        drop_sec = [float(df_out.iloc[d]["start_sec"]) for d in drops]

        summary = {
            "average_attention": round(avg_score, 2),
            "peak_attention": round(peak_score, 2),
            "minimum_attention": round(min_score, 2),
            "stability_index": round(max(0.0, stability_idx), 2),
            "attention_drop_count": len(drops),
            "attention_drop_timestamps_sec": drop_sec,
            "dominant_category": max(set(categories), key=categories.count) if categories else "N/A"
        }

        logger.info(f"Attention Analysis Completed: Avg Score = {avg_score:.1f}/100 ({summary['dominant_category']})")
        return df_out, summary
