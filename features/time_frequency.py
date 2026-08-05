"""
Time-Frequency & Wavelet Feature Extraction for NeuroLearn Research Suite.
Extracts STFT spectrogram features, Wavelet Packet Energy, and Wavelet Entropy.
"""

from typing import Dict, Any
import numpy as np
from scipy import signal
from segmentation.windowing import EEGEpoch
from utils.math_utils import compute_wavelet_features


class TimeFrequencyExtractor:
    """Extracts Short-Time Fourier Transform (STFT) and Wavelet metrics per epoch."""

    def __init__(self, wavelet_name: str = "db4", wavelet_level: int = 4):
        self.wavelet_name = wavelet_name
        self.wavelet_level = wavelet_level

    def extract_epoch_features(self, epoch: EEGEpoch) -> Dict[str, float]:
        """Extract time-frequency and wavelet features for epoch channels."""
        features: Dict[str, float] = {}
        fs = epoch.sampling_rate

        for i, ch_name in enumerate(epoch.channel_names):
            sig = epoch.signals[i]

            # 1. Wavelet transform features
            wt_features = compute_wavelet_features(sig, wavelet=self.wavelet_name, level=self.wavelet_level)
            for k, v in wt_features.items():
                features[f"{ch_name}_{k}"] = v

            # 2. STFT Mean Spectrogram Energy
            nperseg = min(len(sig), int(fs * 0.5)) if fs > 0 else 64
            if nperseg > 0:
                f, t, Zxx = signal.stft(sig, fs=fs, nperseg=nperseg)
                stft_energy = float(np.mean(np.abs(Zxx) ** 2))
                features[f"{ch_name}_stft_energy"] = stft_energy

        return features
