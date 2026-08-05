"""
Page 10: Multi-Format Report Center Workspace for NeuroLearn Research Suite.
"""

import sys
import os
import streamlit as st
import tempfile

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from reports.generator import ResearchReportGenerator
from dashboard.components import render_header

render_header("Report Center", "Export Publication-Ready PDF (ReportLab), Word DOCX, & Raw Metrics CSV Reports")

eeg = st.session_state.current_eeg
sqi = st.session_state.sqi_report
log = st.session_state.preproc_log
att_sum = st.session_state.att_summary
df_att = st.session_state.df_attention

col_rep1, col_rep2, col_rep3 = st.columns(3)

with col_rep1:
    st.markdown("### 📄 IEEE PDF Report")
    st.markdown("Generates comprehensive PDF containing Methods, SQI Audit, Attention Metrics, Discussion & References.")
    if st.button("Export PDF Report", type="primary"):
        pdf_path = os.path.join(tempfile.gettempdir(), f"NeuroLearn_Report_{eeg.subject_id}.pdf")
        ResearchReportGenerator.generate_pdf(
            pdf_path, eeg.subject_id, eeg.source_type, sqi, log, att_sum, df_att
        )
        with open(pdf_path, "rb") as f:
            st.download_button("Download IEEE PDF Report", f, file_name=f"NeuroLearn_Report_{eeg.subject_id}.pdf", mime="application/pdf")

with col_rep2:
    st.markdown("### 📝 Word DOCX Report")
    st.markdown("Generates editable Microsoft Word (.docx) document formatted for academic thesis integration.")
    if st.button("Export Word DOCX"):
        docx_path = os.path.join(tempfile.gettempdir(), f"NeuroLearn_Report_{eeg.subject_id}.docx")
        ResearchReportGenerator.generate_docx(docx_path, eeg.subject_id, att_sum)
        with open(docx_path, "rb") as f:
            st.download_button("Download Word DOCX Report", f, file_name=f"NeuroLearn_Report_{eeg.subject_id}.docx", mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document")

with col_rep3:
    st.markdown("### 📊 Raw Metrics CSV")
    st.markdown("Export epoch-level feature vectors, band powers, and attention scores for external statistical analysis.")
    csv_data = df_att.to_csv(index=False)
    st.download_button("Download CSV Dataset", csv_data, file_name=f"NeuroLearn_Metrics_{eeg.subject_id}.csv", mime="text/csv")
