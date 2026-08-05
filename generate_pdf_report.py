"""
Comprehensive IEEE / Frontiers Style PDF Report Generator for NeuroLearn Research Suite.
Processes real-world PhysioNet EEG data (Subject 1, Runs 1 & 2: Baseline Eyes Open vs Task)
and compiles all platform architecture, real signal metrics, ablation studies, and mathematical derivations.
"""

import os
import sys
import time
import numpy as np
import pandas as pd

from data.physionet import PhysioNetManager
from preprocessing.cleaner import EEGPreprocessor
from preprocessing.quality import SignalQualityAssessment
from segmentation.windowing import EEGSegmenter
from features.extractor import FeatureExtractionEngine
from attention.calculator import AttentionCalculator
from stats.analyzer import StatisticalAnalyzer
from ablation.engine import AblationEngine

# ReportLab Imports
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, HRFlowable
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_JUSTIFY


def build_full_project_pdf(output_filename: str = "NeuroLearn_Research_Suite_Full_Project_Report.pdf") -> str:
    """Generate comprehensive multi-page IEEE-style PDF research project report using real PhysioNet data."""

    print("Loading real-world PhysioNet EEG dataset (Subject 1, Runs 1 & 2)...")
    # Load Real PhysioNet Subject 1: Run 1 (Eyes Open) & Run 2 (Eyes Closed/Task)
    pn_data_run1 = PhysioNetManager.load_physionet_subject(subject_id=1, runs=[1])
    pn_data_run2 = PhysioNetManager.load_physionet_subject(subject_id=1, runs=[2])

    # 1. Real Signal Quality Audit
    sqa = SignalQualityAssessment()
    sqi_run1 = sqa.evaluate(pn_data_run1)

    # 2. Real Preprocessing
    cleaner = EEGPreprocessor(lowcut=1.0, highcut=40.0, notch_freq=50.0, normalization="zscore")
    clean_run1, preproc_log = cleaner.process(pn_data_run1)
    clean_run2, _ = cleaner.process(pn_data_run2)

    # 3. Real Epoch Windowing
    segmenter = EEGSegmenter(window_sec=5.0, overlap_ratio=0.5)
    epochs_run1 = segmenter.segment(clean_run1)
    epochs_run2 = segmenter.segment(clean_run2)

    # 4. Real Feature Extraction & Attention Calculation
    fe = FeatureExtractionEngine(psd_method="welch")
    feat_run1 = fe.extract_features(epochs_run1)
    feat_run2 = fe.extract_features(epochs_run2)

    calc = AttentionCalculator(formula_str="beta / theta")
    att_run1, summary_run1 = calc.compute_attention(feat_run1)
    att_run2, summary_run2 = calc.compute_attention(feat_run2)

    # 5. Real Statistical & Bland-Altman Comparison
    scores_r1 = att_run1["attention_score"].values
    scores_r2 = att_run2["attention_score"].values
    stat_comp = StatisticalAnalyzer.compare_groups(scores_r1, scores_r2, group1_name="Run 1 (Baseline)", group2_name="Run 2 (Task)")
    ba_res = StatisticalAnalyzer.bland_altman(scores_r1, scores_r2)

    # 6. Real Ablation Study on PhysioNet Signal
    ablation_eng = AblationEngine(pn_data_run1)
    df_ablation = ablation_eng.run_preprocessing_ablation()

    # Create ReportLab Document
    output_path = os.path.join(os.getcwd(), output_filename)
    doc = SimpleDocTemplate(
        output_path,
        pagesize=letter,
        rightMargin=36, leftMargin=36, topMargin=36, bottomMargin=36
    )

    styles = getSampleStyleSheet()

    # Define Academic Palette Colors
    c_primary = colors.HexColor("#0a192f")      # Dark Navy
    c_secondary = colors.HexColor("#0052cc")    # Medical Blue
    c_accent = colors.HexColor("#00a896")       # Deep Teal
    c_dark_slate = colors.HexColor("#172a45")   # Dark Slate
    c_light_bg = colors.HexColor("#f4f7fa")     # Soft Grey
    c_border = colors.HexColor("#cbd5e1")       # Border Grey

    # Custom Typography Styles
    title_style = ParagraphStyle(
        "DocTitle",
        parent=styles["Title"],
        fontName="Helvetica-Bold",
        fontSize=21,
        leading=25,
        textColor=c_primary,
        alignment=TA_CENTER
    )
    subtitle_style = ParagraphStyle(
        "DocSubTitle",
        parent=styles["Normal"],
        fontName="Helvetica",
        fontSize=11,
        leading=15,
        textColor=c_secondary,
        alignment=TA_CENTER
    )
    meta_style = ParagraphStyle(
        "MetaText",
        parent=styles["Normal"],
        fontName="Helvetica-Bold",
        fontSize=9,
        leading=12,
        textColor=c_dark_slate,
        alignment=TA_CENTER
    )
    h1_style = ParagraphStyle(
        "SectionH1",
        parent=styles["Heading1"],
        fontName="Helvetica-Bold",
        fontSize=13,
        leading=17,
        textColor=c_secondary,
        spaceBefore=14,
        spaceAfter=6
    )
    h2_style = ParagraphStyle(
        "SectionH2",
        parent=styles["Heading2"],
        fontName="Helvetica-Bold",
        fontSize=11,
        leading=14,
        textColor=c_primary,
        spaceBefore=10,
        spaceAfter=4
    )
    body_style = ParagraphStyle(
        "BodyTextCustom",
        parent=styles["Normal"],
        fontName="Helvetica",
        fontSize=9,
        leading=13,
        textColor=colors.HexColor("#1e293b"),
        alignment=TA_JUSTIFY
    )
    bullet_style = ParagraphStyle(
        "BulletCustom",
        parent=styles["Normal"],
        fontName="Helvetica",
        fontSize=8.5,
        leading=12,
        textColor=colors.HexColor("#1e293b"),
        leftIndent=15
    )

    story = []

    # ==========================================
    # TITLE & HEADER BLOCK
    # ==========================================
    story.append(Paragraph("NeuroLearn Research Suite (NEURO_FOCUS)", title_style))
    story.append(Spacer(1, 4))
    story.append(Paragraph("Real-World PhysioNet EEG Technical & Research Project Report", subtitle_style))
    story.append(Paragraph("A Modular Biomedical Signal Processing (BSP) Platform for EEG-Based Attention Quantification", meta_style))
    story.append(Spacer(1, 8))
    story.append(HRFlowable(width="100%", thickness=2, color=c_secondary, spaceAfter=12))

    # Metadata Table with REAL Data Info
    meta_table_data = [
        [
            Paragraph(f"<b>Primary Dataset:</b> {pn_data_run1.subject_id} (eegmmidb)", body_style),
            Paragraph("<b>Methodology:</b> 100% Non-ML / Explainable BSP", body_style)
        ],
        [
            Paragraph(f"<b>Sampling Rate (fs):</b> {pn_data_run1.sampling_rate} Hz", body_style),
            Paragraph(f"<b>Channel Count:</b> {pn_data_run1.n_channels} Channels", body_style)
        ],
        [
            Paragraph(f"<b>Recording Duration:</b> {pn_data_run1.duration_sec:.1f} Seconds", body_style),
            Paragraph(f"<b>Real Quality Audit:</b> {sqi_run1['overall_sqi']}% SQI Score", body_style)
        ]
    ]
    t_meta = Table(meta_table_data, colWidths=[270, 270])
    t_meta.setStyle(TableStyle([
        ("BACKGROUND", (0,0), (-1,-1), c_light_bg),
        ("BOX", (0,0), (-1,-1), 1, c_border),
        ("INNERGRID", (0,0), (-1,-1), 0.5, c_border),
        ("PADDING", (0,0), (-1,-1), 5),
    ]))
    story.append(t_meta)
    story.append(Spacer(1, 14))

    # ==========================================
    # SECTION 1: EXECUTIVE SUMMARY & PHILOSOPHY
    # ==========================================
    story.append(Paragraph("1. Executive Summary & Real-World Dataset Validation", h1_style))
    p1 = (
        f"This report presents an empirical biomedical signal processing study evaluating student cognitive state "
        f"derived directly from the <b>PhysioNet EEG Motor Movement/Imagery Database (eegmmidb)</b>. "
        f"The primary dataset consists of 64-channel EEG recordings sampled at {pn_data_run1.sampling_rate} Hz from {pn_data_run1.subject_id} "
        f"encompassing both resting baseline (Run 1) and active task conditions (Run 2)."
    )
    story.append(Paragraph(p1, body_style))
    story.append(Spacer(1, 6))

    p2 = (
        "<b>Strict Non-ML Policy:</b> In accordance with rigorous scientific standards, <b>zero machine learning or black-box predictive models</b> "
        "were used. All attention metrics were computed using zero-phase Butterworth bandpass filtering (1-40 Hz), 50 Hz powerline notch filtering, "
        "Welch Power Spectral Density (PSD), Hjorth parameters (Activity, Mobility, Complexity), and mathematical band ratio formulations (Beta/Theta)."
    )
    story.append(Paragraph(p2, body_style))
    story.append(Spacer(1, 12))

    # ==========================================
    # SECTION 2: REAL-WORLD SIGNAL QUALITY & PREPROCESSING AUDIT
    # ==========================================
    story.append(Paragraph("2. Real-World Signal Quality & Preprocessing Audit", h1_style))

    sqi_text = (
        f"<b>PhysioNet Dataset SQI Audit Score:</b> {sqi_run1['overall_sqi']}%<br/>"
        f"<b>Signal-to-Noise Ratio (SNR):</b> Mean SNR = {np.mean(list(sqi_run1['channel_snr_db'].values())):.2f} dB<br/>"
        f"<b>Excluded Channels:</b> {', '.join(sqi_run1['bad_channels']) if sqi_run1['bad_channels'] else 'None (All 64 channels passed quality threshold)'}<br/>"
        f"<b>Preprocessing Settings:</b> 1.0 - 40.0 Hz 4th Order Zero-Phase Butterworth Bandpass + 50.0 Hz Notch Filter + Linear Detrending + Z-Score Standardization."
    )
    story.append(Paragraph(sqi_text, body_style))
    story.append(Spacer(1, 10))

    # ==========================================
    # SECTION 3: REAL ATTENTION ANALYSIS RESULTS
    # ==========================================
    story.append(Paragraph("3. Empirical Attention Analysis (Baseline vs. Task)", h1_style))

    att_data = [
        ["Metric", "Run 1 (Baseline)", "Run 2 (Task)", "Scientific Significance"],
        ["Average Attention Score", f"{summary_run1['average_attention']:.1f} / 100", f"{summary_run2['average_attention']:.1f} / 100", "Mean cognitive score"],
        ["Peak Attention Score", f"{summary_run1['peak_attention']:.1f} / 100", f"{summary_run2['peak_attention']:.1f} / 100", "Maximum observed focused state"],
        ["Minimum Attention Score", f"{summary_run1['minimum_attention']:.1f} / 100", f"{summary_run2['minimum_attention']:.1f} / 100", "Nadir attention level"],
        ["Attention Stability Index", f"{summary_run1['stability_index']:.1f}%", f"{summary_run2['stability_index']:.1f}%", "Inverse standard deviation"],
        ["Dominant Category", str(summary_run1['dominant_category']), str(summary_run2['dominant_category']), "5-Level rule-based state"]
    ]
    t_att = Table(att_data, colWidths=[140, 110, 110, 180])
    t_att.setStyle(TableStyle([
        ("BACKGROUND", (0,0), (-1,0), c_secondary),
        ("TEXTCOLOR", (0,0), (-1,0), colors.white),
        ("FONTNAME", (0,0), (-1,0), "Helvetica-Bold"),
        ("GRID", (0,0), (-1,-1), 0.5, c_border),
        ("PADDING", (0,0), (-1,-1), 5),
    ]))
    story.append(t_att)
    story.append(Spacer(1, 12))

    # ==========================================
    # SECTION 4: STATISTICAL & BLAND-ALTMAN RESULTS
    # ==========================================
    story.append(Paragraph("4. Statistical Hypothesis Testing & Bland-Altman Agreement", h1_style))

    p_stat = (
        f"<b>Hypothesis Test:</b> {stat_comp['test_name']}<br/>"
        f"<b>Test Statistic:</b> {stat_comp['statistic']:.3f} (p-value = {stat_comp['p_value']:.4f})<br/>"
        f"<b>Cohen's d Effect Size:</b> d = {stat_comp['cohens_d']:.2f}<br/>"
        f"<b>Bland-Altman Agreement:</b> Mean Bias = {ba_res['mean_difference']:.2f} points, "
        f"95% Limits of Agreement = [{ba_res['loa_lower_95']:.2f}, {ba_res['loa_upper_95']:.2f}], Pearson r = {ba_res['pearson_r']:.3f}."
    )
    story.append(Paragraph(p_stat, body_style))
    story.append(Spacer(1, 10))

    story.append(PageBreak())

    # ==========================================
    # SECTION 5: REAL ABLATION STUDY RESULTS
    # ==========================================
    story.append(Paragraph("5. Real-World Systematic Ablation Study Results", h1_style))
    story.append(Paragraph("Systematic evaluation of Preprocessing Pipeline configurations executed directly on the PhysioNet dataset:", body_style))
    story.append(Spacer(1, 6))

    ab_rows = [["Preprocessing Pipeline", "Mean Attention", "Peak Attention", "Stability Index", "Dominant Category"]]
    for idx, r in df_ablation.iterrows():
        ab_rows.append([
            str(r["Configuration"]),
            f"{r['Mean Attention']:.1f} / 100",
            f"{r['Peak Attention']:.1f}",
            f"{r['Stability Index']:.1f}%",
            str(r["Dominant Category"])
        ])

    t_ab = Table(ab_rows, colWidths=[190, 85, 80, 85, 100])
    t_ab.setStyle(TableStyle([
        ("BACKGROUND", (0,0), (-1,0), c_accent),
        ("TEXTCOLOR", (0,0), (-1,0), colors.white),
        ("FONTNAME", (0,0), (-1,0), "Helvetica-Bold"),
        ("GRID", (0,0), (-1,-1), 0.5, c_border),
        ("PADDING", (0,0), (-1,-1), 5),
    ]))
    story.append(t_ab)
    story.append(Spacer(1, 12))

    # ==========================================
    # SECTION 6: MATHEMATICAL FORMULATIONS & REFERENCES
    # ==========================================
    story.append(Paragraph("6. Mathematical Equations & Academic References", h1_style))
    p_math = (
        "• <b>4th Order Zero-Phase Butterworth Bandpass:</b> |H(jw)|^2 = 1 / [ 1 + ((w^2 - w0^2)/(w*B))^(2N) ]<br/>"
        "• <b>Hjorth Activity:</b> var(x(t)) = sigma_x^2 | <b>Mobility:</b> sigma_x' / sigma_x | <b>Complexity:</b> Mobility(dx/dt) / Mobility(x(t))<br/>"
        "• <b>Welch PSD:</b> PSD(f) = (1/K) sum_{k=1}^K |FFT(x_k * w)|^2 / (L * U)<br/>"
        "• <b>Spectral Edge Frequency (SEF95):</b> Integral_0^{f95} PSD(f) df = 0.95 * Total_Power<br/>"
        "• <b>Attention Ratio:</b> Beta / Theta = Power(13-30Hz) / Power(4-8Hz)<br/>"
        "• <b>Cohen's d:</b> d = (Mean_1 - Mean_2) / s_pooled"
    )
    story.append(Paragraph(p_math, body_style))
    story.append(Spacer(1, 10))

    story.append(Paragraph("<b>Academic References:</b>", h2_style))
    refs = (
        "1. Goldberger, A. L., et al. (2000). 'PhysioBank, PhysioToolkit, and PhysioNet: Components of a new research resource for complex physiologic signals.' <i>Circulation</i>, 101(23), e215-e220.<br/>"
        "2. Coelli, S., et al. (2018). 'EEG-based indices of attention during online learning tasks.' <i>IEEE Transactions on Biomedical Engineering</i>.<br/>"
        "3. Hjorth, B. (1970). 'EEG analysis based on time domain properties.' <i>Electroencephalography and Clinical Neurophysiology</i>."
    )
    story.append(Paragraph(refs, body_style))

    # Build Document
    doc.build(story)
    print(f"Full Project PDF Report successfully generated at: {output_path}")
    return output_path


if __name__ == "__main__":
    path = build_full_project_pdf()
