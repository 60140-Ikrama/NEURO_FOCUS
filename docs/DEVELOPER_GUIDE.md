# NeuroLearn Research Suite - Developer & Plugin API Guide

## Architecture Design Principles
The **NeuroLearn Research Suite** strictly adheres to:
- **SOLID Principles**: Single responsibility modules (`cleaner.py`, `quality.py`, `windowing.py`, `calculator.py`).
- **Clean Decoupled Architecture**: Independent data, preprocessing, feature extraction, attention, and presentation layers.
- **Strict Non-ML Policy**: Transparent mathematical signal processing without black-box models.

---

## Plugin Architecture

You can dynamically extend the system using the `PluginManager`:

```python
from plugins.manager import PluginManager

# Register a custom attention ratio formula
PluginManager.register_attention_formula(
    name="Frontal_Beta_Alpha",
    formula_str="(beta + gamma) / alpha"
)
```

---

## Folder Architecture

```
BSP_Project/
├── config/             # Configuration Manager & YAML settings
├── data/               # Unified Loader, Biopac Importer, PhysioNet adapter
├── preprocessing/      # Bandpass, Notch, Baseline, SQI quality audit
├── segmentation/       # 2s-30s sliding window epoching
├── features/           # Time domain, Welch/Multitaper PSD, Wavelets, Hjorth
├── attention/          # Mathematical attention index calculator & AST evaluator
├── stats/              # Hypothesis testing, Cohen's d, Bland-Altman
├── ablation/           # Systematic Ablation Study workspace
├── validation/         # Cross-dataset research validation (PhysioNet vs Biopac)
├── experiments/        # Reproducibility tracker & JSON snapshotting
├── plugins/            # Dynamic plugin extension architecture
├── visualization/      # Plotly interactive medical dark theme charts
├── reports/            # Multi-format report generator (PDF, DOCX, CSV)
├── dashboard/          # Streamlit entrance & 11 research pages
├── docs/               # System documentation & mathematical derivations
└── tests/              # Pytest automated testing suite
```
