"""
Signal Quality Assessment Module for NeuroLearn Research Suite.
Computes Signal Quality Index (SQI), SNR, artifact contamination, flat line channels,
and performs automatic bad channel exclusion.
"""

from typing import Dict, List, Tuple, Any
import numpy as np
from scipy import stats
from data.loader import EEGData
from utils.logger import get_logger

logger = get_logger("QualityAssessment")


class SignalQualityAssessment:
    """Evaluates channel quality and computes research Signal Quality Index (SQI)."""

    def __init__(
        self,
        flatline_threshold: float = 1e-6,
        amplitude_threshold_uv: float = 150.0,
        kurtosis_threshold: float = 6.0,
        min_sqi_threshold: float = 40.0
    ):
        self.flatline_threshold = flatline_threshold
        self.amplitude_threshold_uv = amplitude_threshold_uv
        self.kurtosis_threshold = kurtosis_threshold
        self.min_sqi_threshold = min_sqi_threshold

    def evaluate(self, eeg_data: EEGData) -> Dict[str, Any]:
        """Perform quality audit across all channels."""
        n_channels = eeg_data.n_channels
        signals = eeg_data.signals

        channel_sqi: Dict[str, float] = {}
        channel_status: Dict[str, str] = {}
        channel_snr_db: Dict[str, float] = {}
        bad_channels: List[str] = []

        for i, ch_name in enumerate(eeg_data.channel_names):
            sig = signals[i]
            std_val = np.std(sig)
            max_amp = np.max(np.abs(sig))
            kurt_val = stats.kurtosis(sig) if std_val > 0 else 0.0

            # 1. Check for flatline channel
            if std_val < self.flatline_threshold:
                sqi = 0.0
                status = "Flatline / Disconnected"
            else:
                # 2. Base SQI metric calculation
                # Sub-score A: Amplitude normality (penalize extreme voltage spikes)
                amp_score = max(0.0, 100.0 - max(0.0, max_amp - self.amplitude_threshold_uv) * 0.5)

                # Sub-score B: Kurtosis penalty (excess kurtosis indicates transient spikes)
                kurt_score = max(0.0, 100.0 - max(0.0, abs(kurt_val) - 3.0) * 10.0)

                # Sub-score C: Variance sanity check
                var_score = 100.0 if (1.0 <= std_val <= 100.0) else max(30.0, 100.0 - abs(std_val - 50.0))

                sqi = float(0.4 * amp_score + 0.4 * kurt_score + 0.2 * var_score)
                sqi = min(100.0, max(0.0, sqi))

                if sqi >= 80.0:
                    status = "Excellent"
                elif sqi >= 60.0:
                    status = "Good"
                elif sqi >= self.min_sqi_threshold:
                    status = "Acceptable"
                else:
                    status = "Poor / Artifact Contaminated"

            # Estimate SNR (Signal-to-Noise Ratio in dB)
            # Signal power (low-freq band) vs Noise power (high-freq band >30Hz)
            if std_val > 0:
                signal_power = np.var(sig)
                noise_est = np.var(np.diff(sig)) / 2.0
                snr_db = float(10.0 * np.log10(signal_power / noise_est)) if noise_est > 0 else 0.0
            else:
                snr_db = 0.0

            channel_sqi[ch_name] = round(sqi, 2)
            channel_status[ch_name] = status
            channel_snr_db[ch_name] = round(snr_db, 2)

            if sqi < self.min_sqi_threshold:
                bad_channels.append(ch_name)

        overall_sqi = round(float(np.mean(list(channel_sqi.values()))), 2)

        report = {
            "overall_sqi": overall_sqi,
            "channel_sqi": channel_sqi,
            "channel_status": channel_status,
            "channel_snr_db": channel_snr_db,
            "bad_channels": bad_channels,
            "good_channel_count": n_channels - len(bad_channels),
            "total_channel_count": n_channels
        }

        logger.info(f"Signal Quality Audit Complete: Overall SQI = {overall_sqi}%, Bad Channels = {bad_channels}")
        return report

    def exclude_bad_channels(self, eeg_data: EEGData, bad_channels: List[str]) -> EEGData:
        """Create new EEGData object with bad channels removed."""
        if not bad_channels:
            return eeg_data

        good_indices = [i for i, ch in enumerate(eeg_data.channel_names) if ch not in bad_channels]
        good_channels = [ch for ch in eeg_data.channel_names if ch not in bad_channels]

        if not good_indices:
            logger.warning("All channels flagged as bad! Retaining original signal matrix.")
            return eeg_data

        filtered_signals = eeg_data.signals[good_indices, :]

        return EEGData(
            signals=filtered_signals,
            sampling_rate=eeg_data.sampling_rate,
            channel_names=good_channels,
            duration_sec=eeg_data.duration_sec,
            units=eeg_data.units,
            subject_id=eeg_data.subject_id,
            session_id=eeg_data.session_id,
            source_type=eeg_data.source_type,
            metadata={**eeg_data.metadata, "excluded_channels": bad_channels}
        )
