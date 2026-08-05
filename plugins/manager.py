"""
Plugin Manager Architecture for NeuroLearn Research Suite.
Enables dynamic extension of signal filters, feature extractors, and custom attention formulations.
"""

from typing import Dict, Any, Callable, List
from utils.logger import get_logger

logger = get_logger("PluginManager")


class PluginManager:
    """Registry and executor for user-defined processing plugins."""

    _filters: Dict[str, Callable] = {}
    _feature_extractors: Dict[str, Callable] = {}
    _attention_formulas: Dict[str, str] = {}

    @classmethod
    def register_filter(cls, name: str, filter_func: Callable) -> None:
        """Register a custom filter plugin."""
        cls._filters[name] = filter_func
        logger.info(f"Registered custom filter plugin: '{name}'")

    @classmethod
    def register_feature_extractor(cls, name: str, extractor_func: Callable) -> None:
        """Register a custom feature extractor plugin."""
        cls._feature_extractors[name] = extractor_func
        logger.info(f"Registered custom feature extractor plugin: '{name}'")

    @classmethod
    def register_attention_formula(cls, name: str, formula_str: str) -> None:
        """Register a custom attention index formula plugin."""
        cls._attention_formulas[name] = formula_str
        logger.info(f"Registered custom attention formula plugin: '{name}' -> '{formula_str}'")

    @classmethod
    def list_plugins(cls) -> Dict[str, List[str]]:
        """List all currently active plugins."""
        return {
            "filters": list(cls._filters.keys()),
            "feature_extractors": list(cls._feature_extractors.keys()),
            "attention_formulas": list(cls._attention_formulas.keys())
        }
