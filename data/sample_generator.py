"""
Synthetic EEG Sample Generator for NeuroLearn Research Suite.
Generates realistic multi-channel EEG signals simulating resting state, high attention (focused), and noisy states.
Allows saving sample MAT, CSV, and EDF files for immediate offline research testing.
"""

import os
import numpy as np
import pandas as pd
from scipy import io as sio
from typing import Tuple, List, Optional
from data.loader import EEGData
from utils.logger import get_logger

logger = get_logger("SampleGenerator")

STANDARD_1020_CHANNELS = ["Fp1", "Fp2", "F3", "F4", "C3", "C4", "P3", "P4", "O1", "O2", "Fz", "Cz", "Pz"]


def generate_synthetic_eeg(
    duration_sec: float = 60.0,
    sampling_rate: float = 256.0,
    state: str = "focused",  # "focused", "resting", "drowsy", "artifact_heavy"
    channels: Optional[List[str]] = None,
    subject_id: str = "Subject_Synth_01",
    seed: int = 42
) -> EEGData:
    """
    Generate synthetic multi-channel EEG data with realistic frequency composition.
    - Focused state: High Beta (13-30 Hz) & Gamma (30-40 Hz), suppressed Theta (4-8 Hz) & Alpha (8-13 Hz).
    - Resting state: High Alpha (8-13 Hz) & Theta (4-8 Hz), low Beta.
    - Drowsy state: Dominant Theta (4-8 Hz) & Delta (1-4 Hz).
    - Artifact heavy: Baseline drift + 50Hz notch line noise + ocular spikes.
    """
    np.random.seed(seed)
    ch_names = channels or STANDARD_1020_CHANNELS
    n_channels = len(ch_names)
    n_samples = int(duration_sec * sampling_rate)
    t = np.linspace(0, duration_sec, n_samples, endpoint=False)

    signals = np.zeros((n_channels, n_samples))

    # Base band power weights per state
    if state == "focused":
        w_delta, w_theta, w_alpha, w_beta, w_gamma = 0.5, 0.8, 1.2, 4.5, 2.5
    elif state == "resting":
        w_delta, w_theta, w_alpha, w_beta, w_gamma = 1.0, 3.5, 6.0, 1.2, 0.5
    elif state == "drowsy":
        w_delta, w_theta, w_alpha, w_beta, w_gamma = 4.0, 6.5, 1.5, 0.5, 0.2
    else:  # artifact_heavy
        w_delta, w_theta, w_alpha, w_beta, w_gamma = 2.0, 2.0, 2.0, 2.0, 1.0

    for i in range(n_channels):
        # 1. Sinusoidal frequency band components
        delta = w_delta * np.sin(2 * np.pi * 2.5 * t + np.random.uniform(0, 2*np.pi))
        theta = w_theta * np.sin(2 * np.pi * 6.0 * t + np.random.uniform(0, 2*np.pi))
        alpha = w_alpha * np.sin(2 * np.pi * 10.5 * t + np.random.uniform(0, 2*np.pi))
        beta = w_beta * np.sin(2 * np.pi * 21.0 * t + np.random.uniform(0, 2*np.pi))
        gamma = w_gamma * np.sin(2 * np.pi * 35.0 * t + np.random.uniform(0, 2*np.pi))

        # 2. Pink noise background (1/f)
        noise = np.random.normal(0, 1.5, n_samples)
        # Apply simple cumulative sum filter for 1/f response
        pink_noise = np.convolve(noise, np.exp(-np.linspace(0, 2, 50)), mode="same")

        sig = delta + theta + alpha + beta + gamma + pink_noise

        # 3. Add powerline noise (50 Hz)
        sig += 0.8 * np.sin(2 * np.pi * 50.0 * t)

        # 4. Add channel specific spatial variance & ocular blinks for frontal channels (Fp1, Fp2)
        if ch_names[i] in ["Fp1", "Fp2"]:
            # Insert periodic blink artifacts every 6 seconds
            blink_times = np.arange(3.0, duration_sec, 6.0)
            for bt in blink_times:
                b_idx = int(bt * sampling_rate)
                w_len = int(0.3 * sampling_rate)
                if b_idx + w_len < n_samples:
                    sig[b_idx:b_idx+w_len] += 40.0 * np.hanning(w_len)

        signals[i, :] = sig * 5.0  # Scale amplitude in uV

    return EEGData(
        signals=signals,
        sampling_rate=sampling_rate,
        channel_names=ch_names,
        duration_sec=duration_sec,
        units="uV",
        subject_id=subject_id,
        session_id=f"Session_{state.capitalize()}",
        source_type=f"Synthetic_{state.capitalize()}",
        metadata={"state": state, "seed": seed}
    )


def save_sample_datasets(output_dir: str = "sample_data") -> List[str]:
    """Generate and save sample MAT, CSV, and PhysioNet/Biopac mock files."""
    os.makedirs(output_dir, exist_ok=True)
    created_files = []

    # 1. Focused State CSV
    eeg_focused = generate_synthetic_eeg(duration_sec=30.0, state="focused", subject_id="Subj_Focused")
    df_focused = pd.DataFrame(eeg_focused.signals.T, columns=eeg_focused.channel_names)
    df_focused.insert(0, "Time_sec", np.linspace(0, 30.0, eeg_focused.n_samples, endpoint=False))
    csv_path = os.path.join(output_dir, "sample_focused_eeg.csv")
    df_focused.to_csv(csv_path, index=False)
    created_files.append(csv_path)

    # 2. Resting State MAT
    eeg_resting = generate_synthetic_eeg(duration_sec=30.0, state="resting", subject_id="Subj_Resting")
    mat_path = os.path.join(output_dir, "sample_resting_eeg.mat")
    sio.savemat(mat_path, {
        "eeg_data": eeg_resting.signals,
        "fs": eeg_resting.sampling_rate,
        "labels": eeg_resting.channel_names
    })
    created_files.append(mat_path)

    # 3. Biopac Export MAT
    eeg_biopac = generate_synthetic_eeg(duration_sec=30.0, state="drowsy", subject_id="Biopac_Subject")
    biopac_labels = [f"EEG100C - {ch}" for ch in eeg_biopac.channel_names]
    biopac_path = os.path.join(output_dir, "biopac_export_eeg.mat")
    sio.savemat(biopac_path, {
        "val": eeg_biopac.signals,
        "sampling_rate": eeg_biopac.sampling_rate,
        "labels": biopac_labels
    })
    created_files.append(biopac_path)

    logger.info(f"Sample datasets generated in: {output_dir}")
    return created_files
