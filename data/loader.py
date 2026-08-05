"""
Unified Data Loader Module for NeuroLearn Research Suite.
Supports EDF, MAT, CSV, and TXT EEG file formats with automatic metadata detection.
"""

import os
from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional, Tuple
import numpy as np
import pandas as pd
from scipy import io as sio
import mne

from utils.logger import get_logger

logger = get_logger("DataLoader")


@dataclass
class EEGData:
    """Standardized EEG Data Structure across all data sources."""
    signals: np.ndarray             # Shape: (n_channels, n_samples)
    sampling_rate: float            # Sampling frequency in Hz
    channel_names: List[str]        # Channel labels
    duration_sec: float             # Total recording duration in seconds
    units: str = "uV"               # Signal units (uV or V)
    subject_id: str = "Subject_01"
    session_id: str = "Session_01"
    source_type: str = "Unknown"     # PhysioNet, Biopac, Synthetic, Custom
    metadata: Dict[str, Any] = field(default_factory=dict)

    def get_channel_data(self, ch_name: str) -> np.ndarray:
        """Fetch signal array for a specific channel name."""
        if ch_name not in self.channel_names:
            raise ValueError(f"Channel '{ch_name}' not found in recording.")
        idx = self.channel_names.index(ch_name)
        return self.signals[idx]

    @property
    def n_channels(self) -> int:
        return len(self.channel_names)

    @property
    def n_samples(self) -> int:
        return self.signals.shape[1] if self.signals.ndim > 1 else len(self.signals)


class EEGDataLoader:
    """Unified Loader capable of parsing EDF, MAT, CSV, and TXT formats."""

    @staticmethod
    def load_file(file_path: str, sampling_rate_override: Optional[float] = None) -> EEGData:
        """Automatically detect format and load EEG data into standardized EEGData container."""
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"File not found: {file_path}")

        ext = os.path.splitext(file_path)[1].lower()
        logger.info(f"Loading EEG file ({ext}): {os.path.basename(file_path)}")

        if ext == ".edf":
            return EEGDataLoader._load_edf(file_path)
        elif ext == ".mat":
            return EEGDataLoader._load_mat(file_path, sampling_rate_override)
        elif ext in [".csv", ".txt"]:
            return EEGDataLoader._load_csv_txt(file_path, sampling_rate_override)
        else:
            raise ValueError(f"Unsupported file format: {ext}")

    @staticmethod
    def _load_edf(file_path: str) -> EEGData:
        """Load EDF recording via MNE."""
        raw = mne.io.read_raw_edf(file_path, preload=True, verbose=False)
        fs = float(raw.info["sfreq"])
        ch_names = list(raw.info["ch_names"])
        data = raw.get_data() * 1e6  # Convert Volts to uV
        duration = float(data.shape[1] / fs)

        return EEGData(
            signals=data,
            sampling_rate=fs,
            channel_names=ch_names,
            duration_sec=duration,
            units="uV",
            source_type="EDF_File",
            metadata={"mne_info": str(raw.info)}
        )

    @staticmethod
    def _load_mat(file_path: str, fs_override: Optional[float] = None) -> EEGData:
        """Load MAT recording (SciPy loadmat)."""
        mat = sio.loadmat(file_path)
        # Filter out meta keys starting with __
        data_keys = [k for k in mat.keys() if not k.startswith("__")]

        if not data_keys:
            raise ValueError("MAT file contains no readable data matrices.")

        # Find matrix variable
        main_key = data_keys[0]
        for k in data_keys:
            if isinstance(mat[k], np.ndarray) and mat[k].ndim in [1, 2]:
                main_key = k
                break

        arr = mat[main_key]
        if arr.ndim == 1:
            arr = arr.reshape(1, -1)
        elif arr.shape[0] > arr.shape[1]:
            # Expect channels x samples
            arr = arr.T

        n_channels, n_samples = arr.shape
        fs = fs_override or 256.0  # Default or auto

        # Look for explicit fs variable in MAT
        for k in ["fs", "sampling_rate", "sfreq", "sample_rate"]:
            if k in mat:
                fs = float(np.squeeze(mat[k]))
                break

        ch_names = [f"Ch_{i+1}" for i in range(n_channels)]
        if "channel_names" in mat or "labels" in mat:
            lbl_key = "channel_names" if "channel_names" in mat else "labels"
            raw_lbls = np.squeeze(mat[lbl_key])
            ch_names = [str(lbl).strip() for lbl in raw_lbls]

        duration = float(n_samples / fs)

        return EEGData(
            signals=arr,
            sampling_rate=fs,
            channel_names=ch_names,
            duration_sec=duration,
            units="uV",
            source_type="MAT_File",
            metadata={"mat_key": main_key}
        )

    @staticmethod
    def _load_csv_txt(file_path: str, fs_override: Optional[float] = None) -> EEGData:
        """Load CSV or TXT file."""
        sep = "," if file_path.endswith(".csv") else None
        df = pd.read_csv(file_path, sep=sep, engine="python")

        # Check for time column
        time_cols = [c for c in df.columns if any(t in c.lower() for t in ["time", "sec", "timestamp"])]
        fs = fs_override or 256.0

        if time_cols:
            t = df[time_cols[0]].values
            if len(t) > 1:
                dt = np.mean(np.diff(t))
                if dt > 0:
                    fs = float(1.0 / dt)
            df = df.drop(columns=[time_cols[0]])

        # Remaining columns are signal channels
        ch_names = [str(c).strip() for c in df.columns]
        data = df.values.T  # Shape: (n_channels, n_samples)

        duration = float(data.shape[1] / fs)

        return EEGData(
            signals=data,
            sampling_rate=fs,
            channel_names=ch_names,
            duration_sec=duration,
            units="uV",
            source_type="CSV_TXT_File",
            metadata={"columns": ch_names}
        )
