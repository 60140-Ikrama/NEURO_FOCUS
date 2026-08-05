"""
Configuration Manager for NeuroLearn Research Suite.
Handles loading, validation, and updating of research configuration settings.
"""

import os
import yaml
from typing import Any, Dict, Optional


class ConfigManager:
    """Singleton Configuration Manager class for research parameters."""

    _instance = None

    def __new__(cls, config_path: Optional[str] = None):
        if cls._instance is None:
            cls._instance = super(ConfigManager, cls).__new__(cls)
            cls._instance._init_config(config_path)
        return cls._instance

    def _init_config(self, config_path: Optional[str] = None) -> None:
        if config_path is None:
            base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            config_path = os.path.join(base_dir, "config", "default_config.yaml")

        self.config_path = config_path
        self.config: Dict[str, Any] = self._load_file(config_path)

    def _load_file(self, path: str) -> Dict[str, Any]:
        if not os.path.exists(path):
            raise FileNotFoundError(f"Configuration file not found at: {path}")
        with open(path, "r", encoding="utf-8") as f:
            return yaml.safe_load(f) or {}

    def get(self, key_path: str, default: Any = None) -> Any:
        """Fetch nested config using dot notation (e.g., 'preprocessing.bandpass.lowcut')."""
        keys = key_path.split(".")
        val = self.config
        for k in keys:
            if isinstance(val, dict) and k in val:
                val = val[k]
            else:
                return default
        return val

    def set(self, key_path: str, value: Any) -> None:
        """Set nested config value using dot notation."""
        keys = key_path.split(".")
        d = self.config
        for k in keys[:-1]:
            if k not in d or not isinstance(d[k], dict):
                d[k] = {}
            d = d[k]
        d[keys[-1]] = value

    def save(self, output_path: Optional[str] = None) -> None:
        """Save current configuration to YAML file."""
        target = output_path or self.config_path
        os.makedirs(os.path.dirname(target), exist_ok=True)
        with open(target, "w", encoding="utf-8") as f:
            yaml.dump(self.config, f, default_flow_style=False)

    def to_dict(self) -> Dict[str, Any]:
        """Return a copy of the configuration dictionary."""
        return dict(self.config)
