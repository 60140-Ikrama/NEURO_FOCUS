# NeuroLearn Research Suite - Testing Guide

## Automated Unit & Integration Testing
The **NeuroLearn Research Suite** includes unit and integration tests covering data loaders, signal preprocessing, Hjorth & spectral feature extractors, mathematical attention calculators, statistical hypothesis testing, ablation study execution, and report generation.

### Running Pytest
Run the test suite from the project root:
```bash
pytest tests/ -v
```

### Test Coverage Summary:
- `tests/test_data.py`: Validates EDF, MAT, CSV loaders, Biopac importer, and synthetic EEG generator.
- `tests/test_preprocessing.py`: Validates Bandpass/Notch filters, detrending, and SQI bad channel detection.
- `tests/test_features.py`: Tests Welch PSD, Multitaper PSD, band powers, Hjorth parameters, and Wavelet entropy.
- `tests/test_attention.py`: Tests mathematical ratio formulas, AST formula parser, and 0-100 normalization.
- `tests/test_stats.py`: Tests t-tests, Mann-Whitney U, Cohen's d effect sizes, and Bland-Altman agreement.
- `tests/test_ablation.py`: Validates ablation pipeline execution across preprocessing steps, window sizes, and PSD methods.
- `tests/test_reports.py`: Tests PDF (ReportLab), Word DOCX, and CSV report export.
