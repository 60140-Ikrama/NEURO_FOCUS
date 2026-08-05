"""
Unified Feature Extraction Engine for NeuroLearn Research Suite.
Combines Time Domain, Frequency Domain (Welch/FFT/Multitaper), and Time-Frequency Wavelet extractors.
"""

from typing import List, Dict, Any, Optional
import pandas as pd
import numpy as np
from segmentation.windowing import EEGEpoch
from features.time_domain import TimeDomainExtractor
from features.frequency_domain import FrequencyDomainExtractor
from features.time_frequency import TimeFrequencyExtractor
from utils.logger import get_logger

logger = get_logger("FeatureExtractionEngine")


class FeatureExtractionEngine:
    """Unified Feature Extraction Engine across all epochs."""

    def __init__(
        self,
        psd_method: str = "welch",
        include_time: bool = True,
        include_freq: bool = True,
        include_wavelet: bool = True
    ):
        self.psd_method = psd_method
        self.include_time = include_time
        self.include_freq = include_freq
        self.include_wavelet = include_wavelet

        self.time_extractor = TimeDomainExtractor()
        self.freq_extractor = FrequencyDomainExtractor(psd_method=psd_method)
        self.tf_extractor = TimeFrequencyExtractor()

    def extract_features(self, epochs: List[EEGEpoch]) -> pd.DataFrame:
        """Extract complete feature vector dataframe across all segmented epochs."""
        if not epochs:
            logger.warning("No epochs provided to FeatureExtractionEngine.")
            return pd.DataFrame()

        rows = []
        for epoch in epochs:
            row_dict: Dict[str, Any] = {
                "epoch_id": epoch.epoch_id,
                "start_sec": epoch.start_sec,
                "end_sec": epoch.end_sec,
                "is_valid": epoch.is_valid
            }

            # Extract active feature groups
            if self.include_time:
                row_dict.update(self.time_extractor.extract_epoch_features(epoch))

            if self.include_freq:
                row_dict.update(self.freq_extractor.extract_epoch_features(epoch))

            if self.include_wavelet:
                row_dict.update(self.tf_extractor.extract_epoch_features(epoch))

            rows.append(row_dict)

        df_features = pd.DataFrame(rows)
        logger.info(f"Extracted {df_features.shape[1] - 4} features across {len(df_features)} epochs.")
        return df_features
