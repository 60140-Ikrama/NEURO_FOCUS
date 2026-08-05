"""
PhysioNet Dataset Loader & Adapter for NeuroLearn Research Suite.
Provides access to PhysioNet EEG Motor Movement/Imagery Dataset (eegmmidb) and local PhysioNet EDF files.
"""

from typing import Optional, List
import mne
from data.loader import EEGData
from utils.logger import get_logger

logger = get_logger("PhysioNetLoader")


class PhysioNetManager:
    """Fetcher and adapter for PhysioNet EEG datasets."""

    @staticmethod
    def load_physionet_subject(
        subject_id: int = 1,
        runs: List[int] = [1],
        read_raw_kwargs: Optional[dict] = None
    ) -> EEGData:
        """
        Fetch sample PhysioNet eegmmidb subject recording via MNE.
        - Run 1: Baseline, eyes open.
        - Run 2: Baseline, eyes closed.
        - Run 3: Task (motor movement/imagery).
        """
        logger.info(f"Fetching PhysioNet EEG dataset (Subject {subject_id}, Runs {runs})...")
        try:
            edf_paths = mne.datasets.eegmmidb.load_data(subject_id, runs, verbose=False)
            raw = mne.io.read_raw_edf(edf_paths[0], preload=True, verbose=False)

            fs = float(raw.info["sfreq"])
            ch_names = list(raw.info["ch_names"])
            # Clean channel labels (remove dots e.g. 'Fc5.' -> 'Fc5')
            ch_names = [ch.rstrip(".").upper() for ch in ch_names]
            signals = raw.get_data() * 1e6  # Volts to uV

            duration = float(signals.shape[1] / fs)

            return EEGData(
                signals=signals,
                sampling_rate=fs,
                channel_names=ch_names,
                duration_sec=duration,
                units="uV",
                subject_id=f"PhysioNet_S{subject_id:03d}",
                session_id=f"Run_{runs[0]:02d}",
                source_type="PhysioNet_eegmmidb",
                metadata={"file_path": edf_paths[0], "mne_info": str(raw.info)}
            )
        except Exception as e:
            logger.error(f"Failed to fetch PhysioNet dataset: {e}")
            raise e
