"""
Unit Tests for Dataset Loader & Biopac Import Manager.
"""

import pytest
import os
import numpy as np
from data.sample_generator import generate_synthetic_eeg, save_sample_datasets
from data.loader import EEGDataLoader
from data.biopac import BiopacImportManager


def test_synthetic_generator():
    eeg = generate_synthetic_eeg(duration_sec=10.0, state="focused")
    assert eeg.n_channels == 13
    assert eeg.sampling_rate == 256.0
    assert eeg.duration_sec == 10.0
    assert eeg.signals.shape == (13, 2560)


def test_sample_files_loader():
    sample_files = save_sample_datasets(output_dir="test_sample_data")
    assert len(sample_files) >= 3

    for f_path in sample_files:
        if f_path.endswith("biopac_export_eeg.mat"):
            eeg = BiopacImportManager.import_biopac_recording(f_path)
            assert eeg.source_type == "Biopac_AcqKnowledge"
        else:
            eeg = EEGDataLoader.load_file(f_path)
            assert eeg.n_channels > 0
            assert eeg.sampling_rate > 0
