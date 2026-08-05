"""
Cross-Dataset Research Validation Engine for NeuroLearn Research Suite.
Compares PhysioNet EEG recordings against Biopac EEG recordings across Signal Quality,
Feature Consistency, Band Power Stability, and Attention Score Agreement.
"""

from typing import Dict, Any, Tuple
import pandas as pd
import numpy as np
from data.loader import EEGData
from preprocessing.cleaner import EEGPreprocessor
from preprocessing.quality import SignalQualityAssessment
from segmentation.windowing import EEGSegmenter
from features.extractor import FeatureExtractionEngine
from attention.calculator import AttentionCalculator
from stats.analyzer import StatisticalAnalyzer
from utils.logger import get_logger

logger = get_logger("ValidationEngine")


class CrossDatasetValidationEngine:
    """Evaluates cross-dataset agreement between PhysioNet and Biopac EEG recordings."""

    def __init__(self, physionet_data: EEGData, biopac_data: EEGData):
        self.physionet_data = physionet_data
        self.biopac_data = biopac_data

    def validate(self) -> Dict[str, Any]:
        """Perform comprehensive cross-dataset comparative audit."""
        logger.info("Executing Cross-Dataset Validation (PhysioNet vs. Biopac)...")

        # 1. Quality Audit Comparison
        sqa = SignalQualityAssessment()
        pn_sqi = sqa.evaluate(self.physionet_data)
        bp_sqi = sqa.evaluate(self.biopac_data)

        # 2. Pipeline processing
        cleaner = EEGPreprocessor(lowcut=1.0, highcut=40.0, notch_freq=50.0, normalization="zscore")
        pn_clean, _ = cleaner.process(self.physionet_data)
        bp_clean, _ = cleaner.process(self.biopac_data)

        # 3. Epoch segmentation
        segmenter = EEGSegmenter(window_sec=5.0, overlap_ratio=0.5)
        pn_epochs = segmenter.segment(pn_clean)
        bp_epochs = segmenter.segment(bp_clean)

        # 4. Feature Extraction & Attention Calculation
        fe = FeatureExtractionEngine(psd_method="welch")
        pn_feat = fe.extract_features(pn_epochs)
        bp_feat = fe.extract_features(bp_epochs)

        calc = AttentionCalculator(formula_str="beta / theta")
        pn_att, pn_summary = calc.compute_attention(pn_feat)
        bp_att, bp_summary = calc.compute_attention(bp_feat)

        # 5. Statistical & Bland-Altman Agreement Analysis
        pn_scores = pn_att["attention_score"].values
        bp_scores = bp_att["attention_score"].values

        # Alignment for comparative statistical tests
        min_len = min(len(pn_scores), len(bp_scores))
        pn_aligned = pn_scores[:min_len]
        bp_aligned = bp_scores[:min_len]

        ba_result = StatisticalAnalyzer.bland_altman(pn_aligned, bp_aligned)
        stat_comp = StatisticalAnalyzer.compare_groups(
            pn_aligned, bp_aligned,
            group1_name="PhysioNet", group2_name="Biopac"
        )

        comparison_summary = {
            "physionet": {
                "subject_id": self.physionet_data.subject_id,
                "overall_sqi": pn_sqi["overall_sqi"],
                "mean_attention": pn_summary["average_attention"],
                "peak_attention": pn_summary["peak_attention"],
                "stability_index": pn_summary["stability_index"],
                "dominant_category": pn_summary["dominant_category"]
            },
            "biopac": {
                "subject_id": self.biopac_data.subject_id,
                "overall_sqi": bp_sqi["overall_sqi"],
                "mean_attention": bp_summary["average_attention"],
                "peak_attention": bp_summary["peak_attention"],
                "stability_index": bp_summary["stability_index"],
                "dominant_category": bp_summary["dominant_category"]
            },
            "bland_altman": ba_result,
            "statistical_comparison": stat_comp,
            "cross_dataset_correlation": ba_result["pearson_r"],
            "agreement_status": "High Agreement" if ba_result["pearson_r"] > 0.7 else "Moderate/Low Agreement"
        }

        logger.info(f"Cross-Dataset Validation Complete (Correlation r = {ba_result['pearson_r']:.3f})")
        return comparison_summary
