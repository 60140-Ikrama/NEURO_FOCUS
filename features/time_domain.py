"""
Time Domain Feature Extraction for NeuroLearn Research Suite.
Extracts mean, median, variance, std, RMS, peak, peak-to-peak, skewness, kurtosis, ZCR,
and Hjorth parameters (Activity, Mobility, Complexity).
"""

from typing import Dict, Any, List
import numpy as np
from segmentation.windowing import EEGEpoch
from utils.math_utils import compute_hjorth_parameters, compute_time_domain_stats


class TimeDomainExtractor:
    """Extracts time-domain statistics and Hjorth parameters per epoch/channel."""

    @staticmethod
    def extract_epoch_features(epoch: EEGEpoch) -> Dict[str, float]:
        """Extract time-domain metrics for all channels in an epoch."""
        features: Dict[str, float] = {}

        for i, ch_name in enumerate(epoch.channel_names):
            sig = epoch.signals[i]

            # Standard statistical features
            stats_dict = compute_time_domain_stats(sig)
            for k, v in stats_dict.items():
                features[f"{ch_name}_{k}"] = v

            # Hjorth parameters
            act, mob, comp = compute_hjorth_parameters(sig)
            features[f"{ch_name}_hjorth_activity"] = act
            features[f"{ch_name}_hjorth_mobility"] = mob
            features[f"{ch_name}_hjorth_complexity"] = comp

        return features
