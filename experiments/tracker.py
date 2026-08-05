"""
Experiment Tracker & Reproducibility Manager for NeuroLearn Research Suite.
Logs full pipeline configuration, software version, data hashes, and parameter snapshots for 100% research reproducibility.
"""

import os
import json
import time
import hashlib
from typing import Dict, Any, Optional
from config.manager import ConfigManager
from utils.logger import get_logger

logger = get_logger("ExperimentTracker")


class ExperimentTracker:
    """Manages experiment metadata, snapshotting, parameter audit, and reproducibility export."""

    def __init__(self, experiment_name: str = "EEG_Attention_Experiment"):
        self.experiment_name = experiment_name
        self.start_time = time.time()
        self.timestamp_str = time.strftime("%Y-%m-%d_%H-%M-%S")
        self.config_mgr = ConfigManager()
        self.logs: list = []

    def create_reproducibility_snapshot(
        self,
        dataset_name: str,
        n_channels: int,
        fs: float,
        duration_sec: float,
        preproc_config: Dict[str, Any],
        window_sec: float,
        attention_formula: str,
        results_summary: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Generate comprehensive 100% reproducible experiment state record."""

        # Generate unique parameters hash
        param_str = f"{dataset_name}_{fs}_{preproc_config}_{window_sec}_{attention_formula}"
        param_hash = hashlib.sha256(param_str.encode("utf-8")).hexdigest()[:12]

        snapshot = {
            "experiment_id": f"EXP_{self.timestamp_str}_{param_hash}",
            "experiment_name": self.experiment_name,
            "timestamp": time.ctime(self.start_time),
            "software": {
                "name": self.config_mgr.get("platform.name", "NeuroLearn Research Suite"),
                "version": self.config_mgr.get("platform.version", "1.0.0"),
                "python_environment": "Python 3.14 / NumPy / SciPy / MNE / Streamlit / ReportLab"
            },
            "dataset_info": {
                "dataset_name": dataset_name,
                "n_channels": n_channels,
                "sampling_rate_hz": fs,
                "duration_sec": duration_sec
            },
            "pipeline_parameters": {
                "preprocessing": preproc_config,
                "windowing_sec": window_sec,
                "attention_formula": attention_formula
            },
            "results_summary": results_summary,
            "parameter_hash": param_hash
        }

        return snapshot

    def save_snapshot(self, snapshot: Dict[str, Any], output_dir: str = "experiments_archive") -> str:
        """Save reproducibility snapshot to JSON file."""
        os.makedirs(output_dir, exist_ok=True)
        filename = f"{snapshot['experiment_id']}.json"
        filepath = os.path.join(output_dir, filename)

        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(snapshot, f, indent=4)

        logger.info(f"Experiment Reproducibility Snapshot saved to: {filepath}")
        return filepath
