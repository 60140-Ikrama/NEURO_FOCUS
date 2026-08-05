"""
Mathematical & Signal Processing Utility Functions for NeuroLearn Research Suite.
Includes Hjorth parameters, Spectral Edge Frequency (SEF95), Spectral Entropy, Wavelet Entropy, and time-domain metrics.
"""

import numpy as np
from scipy import stats, signal
import pywt
from typing import Tuple, Dict, Any


def compute_hjorth_parameters(x: np.ndarray) -> Tuple[float, float, float]:
    """
    Compute Hjorth parameters: Activity, Mobility, Complexity.
    - Activity: variance of signal x(t)
    - Mobility: sqrt(var(dx/dt) / var(x(t)))
    - Complexity: Mobility(dx/dt) / Mobility(x(t))
    """
    if len(x) < 3 or np.all(x == 0):
        return 0.0, 0.0, 0.0

    dx = np.diff(x)
    ddx = np.diff(dx)

    var_x = float(np.var(x))
    var_dx = float(np.var(dx))
    var_ddx = float(np.var(ddx))

    if var_x == 0.0 or var_dx == 0.0:
        return var_x, 0.0, 0.0

    activity = var_x
    mobility = np.sqrt(var_dx / var_x)
    mobility_dx = np.sqrt(var_ddx / var_dx)

    complexity = mobility_dx / mobility if mobility > 0 else 0.0

    return float(activity), float(mobility), float(complexity)


def compute_spectral_edge_frequency(freqs: np.ndarray, psd: np.ndarray, edge_ratio: float = 0.95) -> float:
    """Compute Spectral Edge Frequency (e.g. SEF95)."""
    if len(psd) == 0 or np.sum(psd) == 0:
        return 0.0

    cum_psd = np.cumsum(psd)
    total_power = cum_psd[-1]
    target_power = total_power * edge_ratio

    idx = np.where(cum_psd >= target_power)[0]
    if len(idx) > 0:
        return float(freqs[idx[0]])
    return float(freqs[-1])


def compute_spectral_entropy(psd: np.ndarray) -> float:
    """Compute normalized Spectral Entropy in [0, 1]."""
    if len(psd) == 0 or np.sum(psd) == 0:
        return 0.0

    psd_norm = psd / np.sum(psd)
    psd_norm = psd_norm[psd_norm > 0]

    entropy = -np.sum(psd_norm * np.log2(psd_norm))
    max_entropy = np.log2(len(psd))

    return float(entropy / max_entropy) if max_entropy > 0 else 0.0


def compute_wavelet_features(x: np.ndarray, wavelet: str = "db4", level: int = 4) -> Dict[str, float]:
    """Compute Discrete Wavelet Transform (DWT) energy distribution & Wavelet Entropy."""
    if len(x) < (2 ** level):
        return {"wavelet_entropy": 0.0, "total_wavelet_energy": 0.0}

    coeffs = pywt.wavedec(x, wavelet=wavelet, level=level)
    energies = [float(np.sum(np.square(c))) for c in coeffs]
    total_energy = sum(energies)

    if total_energy == 0:
        return {"wavelet_entropy": 0.0, "total_wavelet_energy": 0.0}

    probs = [e / total_energy for e in energies if e > 0]
    wavelet_entropy = float(-sum(p * np.log2(p) for p in probs))

    res = {
        "total_wavelet_energy": float(total_energy),
        "wavelet_entropy": wavelet_entropy,
        "ca_energy": energies[0]
    }
    for i, e in enumerate(energies[1:], 1):
        res[f"cd{level - i + 1}_energy"] = e

    return res


def compute_time_domain_stats(x: np.ndarray) -> Dict[str, float]:
    """Compute comprehensive time-domain statistics for an EEG segment."""
    if len(x) == 0:
        return {
            "mean": 0.0, "median": 0.0, "variance": 0.0, "std": 0.0,
            "rms": 0.0, "peak": 0.0, "peak_to_peak": 0.0,
            "skewness": 0.0, "kurtosis": 0.0, "zcr": 0.0
        }

    mean_val = float(np.mean(x))
    median_val = float(np.median(x))
    var_val = float(np.var(x))
    std_val = float(np.std(x))
    rms_val = float(np.sqrt(np.mean(np.square(x))))
    peak_val = float(np.max(np.abs(x)))
    pk_to_pk = float(np.ptp(x))

    skew_val = float(stats.skew(x)) if std_val > 0 else 0.0
    kurt_val = float(stats.kurtosis(x)) if std_val > 0 else 0.0

    # Zero crossing rate
    zero_crossings = np.where(np.diff(np.signbit(x)))[0]
    zcr = float(len(zero_crossings) / len(x))

    return {
        "mean": mean_val,
        "median": median_val,
        "variance": var_val,
        "std": std_val,
        "rms": rms_val,
        "peak": peak_val,
        "peak_to_peak": pk_to_pk,
        "skewness": skew_val,
        "kurtosis": kurt_val,
        "zcr": zcr
    }
