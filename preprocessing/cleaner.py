"""
Signal Preprocessing Module for NeuroLearn Research Suite.
Provides zero-phase Bandpass, Notch filtering, Baseline detrending, DC offset removal,
ICA Artifact Rejection, Montage Referencing (CAR, Longitudinal Bipolar), Signal Standardization,
and complete pipeline logging.
"""

from typing import Dict, Any, Optional, Tuple, List
import numpy as np
from scipy import signal
from data.loader import EEGData
from utils.logger import get_logger

logger = get_logger("Preprocessor")


class EEGPreprocessor:
    """Configurable Biomedical Signal Processing cleaner pipeline."""

    def __init__(
        self,
        lowcut: float = 1.0,
        highcut: float = 40.0,
        filter_order: int = 4,
        notch_freq: float = 50.0,
        notch_q: float = 30.0,
        detrend: bool = True,
        dc_offset_removal: bool = True,
        normalization: str = "zscore",  # "zscore", "minmax", "robust", "none"
        montage_ref: str = "raw",       # "raw", "car" (common average reference), "bipolar"
        use_ica: bool = False
    ):
        self.lowcut = lowcut
        self.highcut = highcut
        self.filter_order = filter_order
        self.notch_freq = notch_freq
        self.notch_q = notch_q
        self.detrend = detrend
        self.dc_offset_removal = dc_offset_removal
        self.normalization = normalization
        self.montage_ref = montage_ref
        self.use_ica = use_ica

    def apply_bandpass(self, data: np.ndarray, fs: float) -> np.ndarray:
        """Apply zero-phase Butterworth Bandpass filter (lowcut - highcut Hz)."""
        nyquist = 0.5 * fs
        low = self.lowcut / nyquist
        high = self.highcut / nyquist

        low = max(1e-4, min(low, 0.99))
        high = max(low + 1e-4, min(high, 0.99))

        b, a = signal.butter(self.filter_order, [low, high], btype="band")
        filtered = signal.filtfilt(b, a, data, axis=-1)
        return filtered

    def apply_notch(self, data: np.ndarray, fs: float) -> np.ndarray:
        """Apply IIR Notch filter to eliminate powerline interference (50/60 Hz)."""
        nyquist = 0.5 * fs
        if self.notch_freq >= nyquist:
            logger.warning(f"Notch frequency {self.notch_freq}Hz >= Nyquist {nyquist}Hz. Skipping notch filter.")
            return data

        w0 = self.notch_freq / nyquist
        b, a = signal.iirnotch(w0, self.notch_q)
        filtered = signal.filtfilt(b, a, data, axis=-1)
        return filtered

    def apply_baseline_correction(self, data: np.ndarray) -> np.ndarray:
        """Remove mean offset and linear trends."""
        res = data.copy()
        if self.dc_offset_removal:
            res = res - np.mean(res, axis=-1, keepdims=True)
        if self.detrend:
            res = signal.detrend(res, axis=-1, type="linear")
        return res

    def apply_montage_reference(self, data: np.ndarray, channel_names: List[str]) -> Tuple[np.ndarray, List[str]]:
        """Apply Common Average Reference (CAR) or Longitudinal Bipolar Montage."""
        if self.montage_ref == "car":
            # Common Average Reference: subtract spatial mean
            car_ref = np.mean(data, axis=0, keepdims=True)
            return data - car_ref, list(channel_names)

        elif self.montage_ref == "bipolar":
            # Bipolar Double Banana Pairs
            pairs = [
                ("Fp1", "F3"), ("F3", "C3"), ("C3", "P3"), ("P3", "O1"),
                ("Fp2", "F4"), ("F4", "C4"), ("C4", "P4"), ("P4", "O2"),
                ("Fz", "Cz"), ("Cz", "Pz")
            ]
            new_signals = []
            new_labels = []

            ch_map = {ch.upper(): idx for idx, ch in enumerate(channel_names)}
            for ch1, ch2 in pairs:
                if ch1.upper() in ch_map and ch2.upper() in ch_map:
                    i1, i2 = ch_map[ch1.upper()], ch_map[ch2.upper()]
                    diff = data[i1] - data[i2]
                    new_signals.append(diff)
                    new_labels.append(f"{ch1}-{ch2}")

            if new_signals:
                return np.array(new_signals), new_labels

        return data, list(channel_names)

    def apply_ica_cleaning(self, data: np.ndarray) -> np.ndarray:
        """Isolate & remove high-variance ocular/EMG components via FastICA."""
        try:
            from sklearn.decomposition import FastICA
            n_ch, n_samples = data.shape
            if n_ch < 2:
                return data

            ica = FastICA(n_components=min(n_ch, 8), random_state=42, max_iter=200)
            sources = ica.fit_transform(data.T)  # Shape (n_samples, n_components)

            # Detect ocular/blink components (high variance or kurtosis)
            kurtosis = np.mean(((sources - np.mean(sources, axis=0)) / np.std(sources, axis=0)) ** 4, axis=0)
            clean_sources = sources.copy()

            # Zero out top artifact component if kurtosis > 5.0
            bad_comp_idx = np.where(kurtosis > 5.0)[0]
            for idx in bad_comp_idx:
                clean_sources[:, idx] = 0.0

            reconstructed = ica.inverse_transform(clean_sources).T
            return reconstructed
        except Exception as e:
            logger.warning(f"ICA cleaning fallback: {e}")
            return data

    def apply_normalization(self, data: np.ndarray) -> np.ndarray:
        """Apply standardization or normalization across time axis."""
        if self.normalization == "none":
            return data

        res = data.copy()
        if self.normalization == "zscore":
            std = np.std(res, axis=-1, keepdims=True)
            std[std == 0] = 1.0
            mean = np.mean(res, axis=-1, keepdims=True)
            res = (res - mean) / std

        elif self.normalization == "minmax":
            min_val = np.min(res, axis=-1, keepdims=True)
            max_val = np.max(res, axis=-1, keepdims=True)
            rng = max_val - min_val
            rng[rng == 0] = 1.0
            res = (res - min_val) / rng

        elif self.normalization == "robust":
            med = np.median(res, axis=-1, keepdims=True)
            q75, q25 = np.percentile(res, [75, 25], axis=-1, keepdims=True)
            iqr = q75 - q25
            iqr[iqr == 0] = 1.0
            res = (res - med) / iqr

        return res

    def process(self, eeg_data: EEGData) -> Tuple[EEGData, Dict[str, Any]]:
        """Run complete preprocessing pipeline on EEGData object."""
        logger.info(f"Preprocessing signal: {eeg_data.subject_id} (fs={eeg_data.sampling_rate}Hz)")
        raw_signals = eeg_data.signals.copy()
        fs = eeg_data.sampling_rate
        ch_names = list(eeg_data.channel_names)

        # Step 1: Baseline detrend & DC removal
        s1 = self.apply_baseline_correction(raw_signals)

        # Step 2: Montage Referencing (CAR / Bipolar)
        s2, ch_names = self.apply_montage_reference(s1, ch_names)

        # Step 3: Bandpass filter
        s3 = self.apply_bandpass(s2, fs)

        # Step 4: Notch filter
        s4 = self.apply_notch(s3, fs)

        # Step 5: Optional ICA Cleaning
        if self.use_ica:
            s4 = self.apply_ica_cleaning(s4)

        # Step 6: Normalization
        s_clean = self.apply_normalization(s4)

        pipeline_log = {
            "lowcut": self.lowcut,
            "highcut": self.highcut,
            "filter_order": self.filter_order,
            "notch_freq": self.notch_freq,
            "detrend": self.detrend,
            "montage_ref": self.montage_ref,
            "use_ica": self.use_ica,
            "normalization": self.normalization,
            "orig_std": float(np.std(raw_signals)),
            "clean_std": float(np.std(s_clean))
        }

        clean_eeg = EEGData(
            signals=s_clean,
            sampling_rate=fs,
            channel_names=ch_names,
            duration_sec=eeg_data.duration_sec,
            units=eeg_data.units if self.normalization == "none" else "norm",
            subject_id=eeg_data.subject_id,
            session_id=eeg_data.session_id,
            source_type=eeg_data.source_type,
            metadata={**eeg_data.metadata, "preprocessed": True, "pipeline_log": pipeline_log}
        )

        return clean_eeg, pipeline_log
