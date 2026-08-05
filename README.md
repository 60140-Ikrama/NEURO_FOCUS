# NeuroLearn Research Suite (NEURO_FOCUS)

> **A Modular Research Platform for EEG-Based Attention Quantification, Cognitive State Analysis, Biomedical Signal Processing, and Neurophysiological Research**

[![Python 3.10+](https://img.shields.io/badge/python-3.10%2B-blue.svg)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Streamlit](https://img.shields.io/badge/Streamlit-Dashboard-FF4B4B.svg)](https://streamlit.io/)
[![Frontend: Scientific Desktop UI](https://img.shields.io/badge/Frontend-Scientific%20Desktop%20UI-00d2ff.svg)](#desktop-scientific-research-frontend)
[![Methodology: Non-ML](https://img.shields.io/badge/Methodology-100%25%20BSP%20%2F%20Non--ML-00e676.svg)](#research-philosophy-100-non-ml--explainable-bsp)

---

## Executive Overview
The **NeuroLearn Research Suite** (`NEURO_FOCUS`) is a research-grade Biomedical Signal Processing (BSP) application designed for academic laboratories, graduate thesis work, scientific publications, and future clinical research. It quantifies student attention state directly from multi-channel EEG recordings using mathematically derived neurophysiological biomarkers.

The platform includes both a **Python Biomedical Signal Processing Engine** and a **Desktop Scientific Research Frontend UI** resembling professional research software such as **MATLAB App Designer, LabChart, Biopac AcqKnowledge, BrainVision Analyzer, and OpenBCI GUI**.

---

## 🏛️ Research Philosophy: 100% Non-ML / Explainable BSP

This platform explicitly **does NOT use machine learning, neural networks, CNNs, LSTMs, Transformers, or black-box predictive models**. All cognitive state metrics are derived transparently using:
- **Zero-Phase Butterworth Bandpass Filtering** (1.0–40.0 Hz 4th order)
- **Power Spectral Density (PSD)** via Welch, FFT, and Multitaper methods
- **Hjorth Parameters** (Activity $\sigma_x^2$, Mobility $\sigma_{x'}/\sigma_x$, Complexity)
- **Discrete Wavelet Transforms (DWT)** & Wavelet Entropy
- **Mathematical Ratio Formulations**: $\frac{P_{\beta}}{P_{\theta}}$, $\frac{P_{\beta} + P_{\gamma}}{P_{\theta} + P_{\alpha}}$, and AST-based custom mathematical expressions.

---

## 💻 Desktop Scientific Research Frontend

Designed with a **Medical Dark Theme** (`#0a192f` background, `#172a45` glassmorphic containers, `#00d2ff` cyan, `#0052cc` medical blue, `#64ffda` emerald accents, and Inter typography):

- **Top Navigation Bar**: Active dataset indicator, sampling rate ($f_s = 256\text{ Hz}$), duration, Signal Quality Index (SQI) status, research mode badge, user options, and report exporter.
- **Collapsible Left Navigation Sidebar**: Houses all **21 research workspace items**.
- **Main Scientific Workspace**: Stacked multi-channel EEG waveform canvas, Welch/Multitaper PSD plots, spectrogram heatmaps, step-by-step filter pipeline builder, ablation matrices, and Bland-Altman agreement charts.
- **Right Analysis Panel**: Channel inspector, band power distribution ($\delta, \theta, \alpha, \beta, \gamma$), custom formula evaluator, and real-time parameter controls.
- **Bottom Telemetry Console**: Real-time log stream, sampling rate stability index, CPU/RAM utilization meters, and execution status.

---

## 🔬 21 Integrated Research Workspaces

1. **Dashboard**: Animated scientific KPI cards (SQI score, Mean Attention, Stability Index, System status).
2. **Dataset Manager**: Import validator for EDF, MAT, CSV, TXT files with auto-detected metadata ($f_s$, channel labels, duration, units).
3. **Biopac Manager**: Dedicated AcqKnowledge export importer and channel label normalizer.
4. **PhysioNet Manager**: Direct fetcher for PhysioNet `eegmmidb` motor imagery datasets.
5. **Signal Import**: Unified drag-and-drop import pipeline.
6. **EEG Viewer**: Multi-channel stacked waveform plot with zoom, pan, cursor measurement tools, amplitude scaling, and windowing overlay.
7. **Signal Quality (SQI)**: SQI bar chart (0–100%), SNR estimation (dB), kurtosis spike detection, flat line detection, and bad channel auto-exclusion.
8. **Preprocessing Builder**: Visual step-by-step filter node sequence (`Raw` $\rightarrow$ `Bandpass 1-40Hz` $\rightarrow$ `Notch 50Hz` $\rightarrow$ `Standardization` $\rightarrow$ `SQI`) with before vs. after signal overlay.
9. **Artifact Analysis**: Ocular blink & high-kurtosis spike contamination audit.
10. **Window Configuration**: Sliding window epoch selector (2s, 5s, 10s, 20s, 30s) with overlap control (0%–90%).
11. **Feature Extraction**: Interactive sortable feature table (Time Domain, Welch PSD, Hjorth parameters, Wavelets).
12. **Frequency Analysis**: Welch & Multitaper Power Spectral Density (PSD) curves with frequency band shading and Spectral Edge Frequency (SEF95).
13. **Attention Analysis**: Non-ML mathematical cognitive score timeline (0–100 scale) and attention drop event alerts.
14. **Statistical Analysis**: Parametric ($t$-tests), non-parametric (Wilcoxon, Mann-Whitney $U$), Shapiro-Wilk normality tests, Cohen's $d$ effect sizes, and Bland-Altman agreement plot.
15. **Ablation Study Workspace**: Primary research workspace comparing Preprocessing pipelines, Window sizes, PSD methods, and Attention formulas with optimal configuration highlighter.
16. **Research Validation**: Direct Bland-Altman cross-dataset agreement audit (PhysioNet vs. Biopac).
17. **Visualization Gallery**: Interactive Plotly charts exportable in high resolution.
18. **Experiment Manager**: 100% reproducible experiment state logger and JSON snapshot exporter.
19. **Report Center**: PDF (ReportLab), Word DOCX, and CSV dataset exporter with live report previewer.
20. **Settings**: Global configuration parameter overrides.
21. **Help & About**: Scientific documentation and platform citation info.

---

## 📁 System Architecture & Directory Structure

```
NEURO_FOCUS/
├── frontend/
│   ├── index.html                  # Desktop Scientific Research Application Shell
│   ├── css/
│   │   ├── medical_theme.css       # Dark Medical Theme CSS Tokens & Glassmorphic Styling
│   │   ├── layout.css              # Desktop Grid Layout (TopBar, Sidebar, Main, RightPanel, Console)
│   │   └── components.css          # KPI Cards, Badges, Tables, Pipeline Nodes, Telemetry
│   └── js/
│       ├── app.js                  # Main Controller & Navigation Router across 21 Views
│       ├── eeg_canvas.js           # Multi-Channel Stacked EEG Waveform Plotter (Plotly.js)
│       ├── pipeline_builder.js     # Preprocessing Node Diagram & Before/After Overlay
│       ├── ablation_workspace.js   # Systematic Ablation Matrix & Heatmap Renderer
│       ├── stats_workspace.js      # Statistical Analysis Cards & Bland-Altman Plot
│       └── report_previewer.js     # Live Report Exporter & Previewer
├── config/                         # Configuration Manager & YAML settings
├── data/                           # Unified Dataset Loader, Biopac Importer, PhysioNet adapter
├── preprocessing/                  # Zero-Phase Bandpass, Notch, Baseline & SQI Audit
├── segmentation/                   # 2s-30s Sliding Window Engine
├── features/                       # Time-Domain, Welch/Multitaper PSD, Wavelets, Hjorth
├── attention/                      # Non-ML Attention Ratio Calculator & AST Evaluator
├── stats/                          # Hypothesis Tests, Cohen's d & Bland-Altman
├── ablation/                       # Ablation Study Engine
├── validation/                     # Cross-Dataset Research Validation (PhysioNet vs Biopac)
├── experiments/                    # 100% Reproducibility Tracker & JSON Snapshotting
├── plugins/                        # Dynamic Plugin Extension Architecture
├── visualization/                  # Plotly Interactive Medical Dark Theme Charts
├── reports/                        # Multi-Format Exporter (PDF via ReportLab, DOCX, CSV)
├── dashboard/                      # Streamlit Entrance & 11 Research Pages
├── docs/                           # Documentation (Architecture, Mathematics, User/Dev Guides)
├── tests/                          # 11 Pytest Automated Tests
├── README.md                       # Main IEEE/Frontiers-style README
├── LICENSE                         # MIT License
└── requirements.txt                # Dependency Manifest
```

---

## ⚡ Installation & Quick Start

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Run automated test suite (100% Pass)
python -m pytest tests/ -v

# 3. Launch Streamlit Application
streamlit run dashboard/app.py

# 4. Open Desktop Scientific Frontend
# Open frontend/index.html in any modern web browser / desktop shell
```

---

## 📜 License & Citation
Distributed under the **MIT License**.

```bibtex
@article{neurolearn2026,
  title={NeuroLearn Research Suite: A Modular Biomedical Signal Processing Platform for EEG Attention Tracking},
  author={Biomedical Signal Processing & Neuroscience Laboratory},
  journal={IEEE Transactions on Biomedical Engineering},
  year={2026}
}
```
