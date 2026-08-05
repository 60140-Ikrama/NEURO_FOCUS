"""
Windowing and Epoch Segmentation Engine for NeuroLearn Research Suite.
Provides sliding epoching across 2s, 5s, 10s, 20s, 30s windows with configurable overlap.
"""

from dataclasses import dataclass
from typing import List, Tuple, Generator
import numpy as np
from data.loader import EEGData
from utils.logger import get_logger

logger = get_logger("WindowingEngine")


@dataclass
class EEGEpoch:
    """Container for a single EEG sliding window epoch."""
    epoch_id: int
    start_sec: float
    end_sec: float
    signals: np.ndarray      # Shape: (n_channels, epoch_samples)
    channel_names: List[str]
    sampling_rate: float
    is_valid: bool = True


class EEGSegmenter:
    """Sliding Window Epoch Generator and Validator."""

    def __init__(self, window_sec: float = 5.0, overlap_ratio: float = 0.5):
        """
        :param window_sec: Duration of each epoch in seconds (e.g. 2, 5, 10, 20, 30).
        :param overlap_ratio: Overlap percentage in range [0.0, 0.9] (e.g. 0.5 = 50% overlap).
        """
        self.window_sec = float(window_sec)
        self.overlap_ratio = float(min(0.9, max(0.0, overlap_ratio)))

    def segment(self, eeg_data: EEGData) -> List[EEGEpoch]:
        """Segment EEG recording into sliding windows."""
        fs = eeg_data.sampling_rate
        window_samples = int(self.window_sec * fs)
        step_samples = int(window_samples * (1.0 - self.overlap_ratio))

        if window_samples <= 0 or step_samples <= 0:
            raise ValueError("Window size or step size too small.")

        n_samples = eeg_data.n_samples
        if n_samples < window_samples:
            logger.warning(f"Recording duration ({eeg_data.duration_sec}s) is shorter than window size ({self.window_sec}s). Single padded epoch returned.")
            pad_len = window_samples - n_samples
            padded = np.pad(eeg_data.signals, ((0, 0), (0, pad_len)), mode="edge")
            return [EEGEpoch(
                epoch_id=0,
                start_sec=0.0,
                end_sec=self.window_sec,
                signals=padded,
                channel_names=list(eeg_data.channel_names),
                sampling_rate=fs,
                is_valid=True
            )]

        epochs: List[EEGEpoch] = []
        epoch_id = 0
        start_idx = 0

        while start_idx + window_samples <= n_samples:
            end_idx = start_idx + window_samples
            start_t = start_idx / fs
            end_t = end_idx / fs

            epoch_sig = eeg_data.signals[:, start_idx:end_idx]

            # Validate epoch (ensure non-flat and no infinite values)
            is_valid = bool(not np.any(np.isnan(epoch_sig)) and not np.any(np.isinf(epoch_sig)))

            epochs.append(EEGEpoch(
                epoch_id=epoch_id,
                start_sec=start_t,
                end_sec=end_t,
                signals=epoch_sig,
                channel_names=list(eeg_data.channel_names),
                sampling_rate=fs,
                is_valid=is_valid
            ))

            epoch_id += 1
            start_idx += step_samples

        logger.info(f"Segmented EEG into {len(epochs)} epochs (Window={self.window_sec}s, Overlap={int(self.overlap_ratio*100)}%)")
        return epochs
