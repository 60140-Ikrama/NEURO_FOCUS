"""
Frequency Domain & Spectral Feature Extraction for NeuroLearn Research Suite.
Supports Welch PSD, FFT, Multitaper PSD, Absolute/Relative Band Powers, SEF95, Spectral Entropy, and Band Ratios.
"""

from typing import Dict, Any, List, Tuple
import numpy as np
from scipy import signal, integrate
from segmentation.windowing import EEGEpoch
from utils.math_utils import compute_spectral_edge_frequency, compute_spectral_entropy


def _trapz(y: np.ndarray, x: np.ndarray) -> float:
    """Trapezoidal integration compatible with both NumPy 1.x and NumPy 2.x."""
    if hasattr(np, "trapezoid"):
        return float(np.trapezoid(y, x))
    elif hasattr(integrate, "trapezoid"):
        return float(integrate.trapezoid(y, x))
    else:
        return float(np.trapz(y, x))


DEFAULT_BANDS = {
    "delta": (0.5, 4.0),
    "theta": (4.0, 8.0),
    "alpha": (8.0, 13.0),
    "beta": (13.0, 30.0),
    "gamma": (30.0, 40.0)
}


class FrequencyDomainExtractor:
    """Frequency-domain feature extractor across PSD methods and band formulations."""

    def __init__(self, psd_method: str = "welch", bands: Dict[str, Tuple[float, float]] = None):
        self.psd_method = psd_method.lower()
        self.bands = bands or DEFAULT_BANDS

    def compute_psd(self, x: np.ndarray, fs: float) -> Tuple[np.ndarray, np.ndarray]:
        """Compute Power Spectral Density using specified method (Welch, FFT, Multitaper)."""
        n = len(x)
        if n == 0:
            return np.array([0.0]), np.array([0.0])

        if self.psd_method == "welch":
            nperseg = min(n, int(fs * 2.0)) if fs > 0 else min(n, 256)
            freqs, psd = signal.welch(x, fs=fs, window="hann", nperseg=nperseg)

        elif self.psd_method == "fft":
            fft_vals = np.fft.rfft(x)
            freqs = np.fft.rfftfreq(n, d=1.0/fs)
            psd = (np.abs(fft_vals) ** 2) / (n * fs)

        elif self.psd_method == "multitaper":
            dpss_win = signal.windows.dpss(n, NW=2.5, Kmax=3)
            psd_list = []
            for win in dpss_win:
                freqs, p = signal.periodogram(x * win, fs=fs)
                psd_list.append(p)
            psd = np.mean(psd_list, axis=0)

        else:
            freqs, psd = signal.welch(x, fs=fs)

        return freqs, psd

    def extract_epoch_features(self, epoch: EEGEpoch) -> Dict[str, float]:
        """Extract frequency-domain metrics and band ratios per epoch."""
        features: Dict[str, float] = {}
        fs = epoch.sampling_rate

        for i, ch_name in enumerate(epoch.channel_names):
            sig = epoch.signals[i]
            freqs, psd = self.compute_psd(sig, fs)

            if len(psd) == 0 or np.sum(psd) == 0:
                continue

            total_power = _trapz(psd, freqs)
            total_power = total_power if total_power > 0 else 1e-9

            # 1. Absolute & Relative Band Powers
            band_powers = {}
            for b_name, (l_freq, h_freq) in self.bands.items():
                idx = np.where((freqs >= l_freq) & (freqs <= h_freq))[0]
                if len(idx) > 0:
                    b_power = _trapz(psd[idx], freqs[idx])
                else:
                    b_power = 0.0

                band_powers[b_name] = b_power
                rel_power = b_power / total_power

                features[f"{ch_name}_{b_name}_abs_power"] = b_power
                features[f"{ch_name}_{b_name}_rel_power"] = rel_power

            # 2. Spectral Metrics
            peak_freq = float(freqs[np.argmax(psd)])
            sef95 = compute_spectral_edge_frequency(freqs, psd, edge_ratio=0.95)
            spec_ent = compute_spectral_entropy(psd)

            # Median frequency
            cum_power = np.cumsum(psd)
            med_idx = np.where(cum_power >= total_power / 2.0)[0]
            med_freq = float(freqs[med_idx[0]]) if len(med_idx) > 0 else 0.0

            features[f"{ch_name}_peak_frequency"] = peak_freq
            features[f"{ch_name}_median_frequency"] = med_freq
            features[f"{ch_name}_sef95"] = sef95
            features[f"{ch_name}_spectral_entropy"] = spec_ent

            # 3. Key Neurophysiological Band Ratios
            theta = band_powers.get("theta", 1e-6)
            alpha = band_powers.get("alpha", 1e-6)
            beta = band_powers.get("beta", 1e-6)
            gamma = band_powers.get("gamma", 1e-6)

            theta = theta if theta > 0 else 1e-6
            alpha = alpha if alpha > 0 else 1e-6

            features[f"{ch_name}_ratio_beta_theta"] = float(beta / theta)
            features[f"{ch_name}_ratio_theta_beta"] = float(theta / beta) if beta > 0 else 0.0
            features[f"{ch_name}_ratio_alpha_theta"] = float(alpha / theta)
            features[f"{ch_name}_ratio_beta_alpha"] = float(beta / alpha)
            features[f"{ch_name}_ratio_gamma_beta"] = float(gamma / beta) if beta > 0 else 0.0

        return features
