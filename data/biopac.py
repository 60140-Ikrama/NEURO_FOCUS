"""
Biopac Import Manager for NeuroLearn Research Suite.
Normalizes exported Biopac AcqKnowledge EEG recordings (MAT, CSV, TXT) into unified EEGData containers.
"""

import os
from typing import Optional, Dict, Any
import numpy as np
from data.loader import EEGData, EEGDataLoader
from utils.logger import get_logger

logger = get_logger("BiopacImporter")


class BiopacImportManager:
    """Extension module to import and normalize exported Biopac EEG signals."""

    @staticmethod
    def import_biopac_recording(
        file_path: str,
        sampling_rate: Optional[float] = None,
        subject_id: str = "Biopac_Subject_01",
        session_id: str = "Biopac_Session_01"
    ) -> EEGData:
        """Import exported Biopac file and standardise channel naming and metadata."""
        logger.info(f"Importing Biopac recording from: {file_path}")
        raw_data = EEGDataLoader.load_file(file_path, sampling_rate_override=sampling_rate)

        # Standardize Biopac channel labels (e.g. 'EEG100C - Cz' -> 'Cz')
        cleaned_channels = []
        for ch in raw_data.channel_names:
            ch_clean = ch.replace("EEG100C", "").replace("AcqKnowledge", "").strip("- ").strip()
            cleaned_channels.append(ch_clean if ch_clean else ch)

        raw_data.channel_names = cleaned_channels
        raw_data.subject_id = subject_id
        raw_data.session_id = session_id
        raw_data.source_type = "Biopac_AcqKnowledge"
        raw_data.metadata["biopac_imported"] = True

        logger.info(f"Biopac recording normalized successfully ({raw_data.n_channels} channels, {raw_data.sampling_rate} Hz, {raw_data.duration_sec:.1f}s)")
        return raw_data
