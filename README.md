# NeuroLearn Research Suite

> **A Modular Research Platform for EEG-Based Attention Quantification, Cognitive State Analysis, Biomedical Signal Processing, and Neurophysiological Research**

[![Python 3.10+](https://img.shields.io/badge/python-3.10%2B-blue.svg)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Streamlit](https://img.shields.io/badge/Streamlit-App-FF4B4B.svg)](https://streamlit.io/)
[![Methodology: Non-ML](https://img.shields.io/badge/Methodology-100%25%20BSP%20%2F%20Non--ML-00e676.svg)](#project-philosophy)

---

## Executive Overview
The **NeuroLearn Research Suite** is a research-grade Biomedical Signal Processing (BSP) application designed for academic laboratories, thesis work, and scientific research. It quantifies student attention state directly from EEG recordings using mathematically derived neurophysiological biomarkers.

### 🏛️ Research Philosophy: 100% Non-ML / Explainable BSP
This platform explicitly **does NOT use machine learning, neural networks, CNNs, LSTMs, Transformers, or black-box predictive models**. All cognitive state metrics are derived transparently using zero-phase Butterworth filtering, Welch Power Spectral Density (PSD), Hjorth parameters, Discrete Wavelet Transforms (DWT), and mathematical band ratio formulations (such as $\beta/\theta$ and $(\beta+\gamma)/(\theta+\alpha)$).

---

## Key Features & 17 Core Modules

1. **Unified Dataset & Biopac Import Manager**: Seamlessly imports PhysioNet datasets (`.edf`, WFDB) and Biopac AcqKnowledge exports (`.mat`, `.csv`, `.txt`, `.edf`) with auto-detection of $f_s$, channel labels, duration, and units.
2. **Signal Quality Assessment (SQI)**: Computes channel SQI scores (0–100%), SNR (dB), kurtosis spike detection, flat-line detection, and auto-excludes bad channels.
3. **Biomedical Signal Preprocessing**: Zero-phase Butterworth Bandpass (1–40 Hz), 50 Hz / 60 Hz Notch filter, baseline detrending, and standardization (Z-score / Min-Max / Robust).
4. **Sliding Window Engine**: Epoch segmentation across 2s, 5s, 10s, 20s, 30s windows with configurable overlap (0%–90%).
5. **Multi-Domain Feature Extraction**: Time domain statistics, Hjorth parameters (Activity, Mobility, Complexity), Welch/FFT/Multitaper PSD, SEF95, Spectral Entropy, and Wavelet Entropy.
6. **Mathematical Attention Analysis**: Non-ML ratio formulations, safe AST custom formula evaluator, 0–100 normalization, and 5-level rule-based classification.
7. **Statistical Analysis**: Parametric/non-parametric hypothesis testing, Shapiro-Wilk normality tests, Cohen's $d$ effect sizes, and Bland-Altman agreement analysis.
8. **Systematic Ablation Study Engine**: Primary research module systematically evaluating Preprocessing pipelines, Window sizes (2s–30s), PSD methods, and Attention formulas.
9. **Cross-Dataset Research Validation**: Direct agreement evaluation between PhysioNet and Biopac EEG sessions.
10. **Experiment Explorer & 100% Reproducibility**: Log software version, filter bounds, data hashes, and export JSON reproducibility snapshots.
11. **Multi-Format Report Generator**: Exports IEEE/Frontiers-styled PDF (ReportLab), Word DOCX, and raw CSV reports.
12. **Medical Dark Theme Interactive Dashboard**: Streamlit interface designed with dark slate (`#172a45`), medical blue (`#0052cc`), and cyan (`#64ffda`) styling.

---

## System Architecture

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

---

## Installation & Quick Start

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Run automated test suite
pytest tests/ -v

# 3. Launch Streamlit Application
streamlit run dashboard/app.py
```

---

## License & Citation
Distributed under the **MIT License**.

```bibtex
@article{neurolearn2026,
  title={NeuroLearn Research Suite: A Modular Biomedical Signal Processing Platform for EEG Attention Tracking},
  author={Biomedical Signal Processing & Neuroscience Laboratory},
  journal={IEEE Transactions on Biomedical Engineering},
  year={2026}
}
```
