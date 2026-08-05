# NeuroLearn Research Suite - User Manual

Welcome to the **NeuroLearn Research Suite** operational guide.

## Quick Start Guide

### 1. Installation
Clone the repository and install required dependencies:
```bash
pip install -r requirements.txt
```

### 2. Launching the Streamlit Application
Run the main Streamlit application:
```bash
streamlit run dashboard/app.py
```

---

## Workspace Navigation Guide

1. **Dataset Manager**: Import EDF, MAT, CSV, TXT files or Biopac AcqKnowledge export files.
2. **EEG Viewer**: Scroll, zoom, and pan across multi-channel raw vs. filtered signal waveforms.
3. **Signal Preprocessing**: Configure 1-40Hz Bandpass filter, 50Hz Notch filter, detrending, and SQI bad channel auto-exclusion.
4. **Frequency Analysis**: Inspect Welch & Multitaper Power Spectral Density (PSD) curves, relative band powers, and SEF95 metrics.
5. **Attention Analysis**: Compute mathematical attention index scores (0-100) and view epoch timeline.
6. **Statistical Analysis**: Perform parametric/non-parametric hypothesis testing, normality tests, and Bland-Altman agreement analysis.
7. **Ablation Study**: Systematically evaluate the impact of preprocessing filters, window sizes (2s–30s), and PSD methods on attention metrics.
8. **Research Validation**: Directly evaluate agreement between PhysioNet and Biopac EEG sessions.
9. **Experiment Explorer**: View, export, and restore 100% reproducible experiment state snapshots.
10. **Report Center**: Generate publication-ready PDF, Word DOCX, and CSV reports.
