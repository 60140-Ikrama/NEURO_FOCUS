"""
Unit Tests for Multi-Format Report Generator.
"""

import pytest
import os
import tempfile
import pandas as pd
from reports.generator import ResearchReportGenerator


def test_report_generator():
    tmp_dir = tempfile.gettempdir()
    pdf_path = os.path.join(tmp_dir, "test_report.pdf")
    docx_path = os.path.join(tmp_dir, "test_report.docx")
    csv_path = os.path.join(tmp_dir, "test_report.csv")

    sqi_report = {"overall_sqi": 95.0, "bad_channels": []}
    preproc_log = {"lowcut": 1.0, "highcut": 40.0, "notch_freq": 50.0}
    att_summary = {"average_attention": 75.2, "peak_attention": 92.1, "minimum_attention": 45.0, "stability_index": 88.5, "dominant_category": "High Attention"}
    df_att = pd.DataFrame([{"epoch_id": 0, "start_sec": 0.0, "end_sec": 5.0, "attention_score": 75.2, "attention_category": "High Attention"}])

    res_pdf = ResearchReportGenerator.generate_pdf(pdf_path, "TestSubj", "Synthetic", sqi_report, preproc_log, att_summary, df_att)
    assert os.path.exists(res_pdf)

    res_docx = ResearchReportGenerator.generate_docx(docx_path, "TestSubj", att_summary)
    assert os.path.exists(res_docx)

    res_csv = ResearchReportGenerator.generate_csv(csv_path, df_att)
    assert os.path.exists(res_csv)
