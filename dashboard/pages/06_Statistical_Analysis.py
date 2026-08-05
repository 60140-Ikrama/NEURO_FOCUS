"""
Page 06: Statistical Analysis Workspace for NeuroLearn Research Suite.
"""

import sys
import os
import streamlit as st
import numpy as np

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from stats.analyzer import StatisticalAnalyzer
from dashboard.components import render_header, render_kpi_card
from visualization.plots import VisualizationEngine

render_header("Statistical Analysis", "Hypothesis Testing, Normality Checks, Effect Sizes (Cohen's d), & Bland-Altman Agreement")

df_att = st.session_state.df_attention
scores = df_att["attention_score"].values if "attention_score" in df_att.columns else np.array([50.0])

# 1. Descriptive Stats & Normality
st.markdown("### 1. Descriptive Statistics & Normality Audit")

desc = StatisticalAnalyzer.descriptive_stats(scores)
norm = StatisticalAnalyzer.test_normality(scores)

c1, c2, c3, c4 = st.columns(4)
with c1:
    render_kpi_card("Mean ± SD", f"{desc.get('mean', 0):.2f} ± {desc.get('std', 0):.2f}", f"95% CI: [{desc.get('ci_lower', 0):.2f}, {desc.get('ci_upper', 0):.2f}]")
with c2:
    render_kpi_card("Median (IQR)", f"{desc.get('median', 0):.2f}", f"IQR: {desc.get('iqr', 0):.2f}")
with c3:
    render_kpi_card("Normality Test", "Normal" if norm["is_normal"] else "Non-Normal", f"Shapiro p = {norm['p_value']:.4f}")
with c4:
    render_kpi_card("Skewness & Kurtosis", f"{desc.get('skewness', 0):.2f}", f"Kurtosis: {desc.get('kurtosis', 0):.2f}")

st.info(f"**Automatic Statistical Interpretation:** {norm['interpretation']}")

st.markdown("---")
# 2. Hypothesis Testing & Group Comparison
st.markdown("### 2. Group Hypothesis Testing & Comparative Statistics")

col_test1, col_test2 = st.columns(2)
with col_test1:
    g1_split = st.slider("Split Epoch Dataset at Epoch Index:", 1, max(2, len(scores)-1), max(1, len(scores)//2))
    paired_flag = st.checkbox("Paired Samples Test", value=False)

g1 = scores[:g1_split]
g2 = scores[g1_split:]

if len(g1) > 0 and len(g2) > 0:
    comp = StatisticalAnalyzer.compare_groups(g1, g2, paired=paired_flag, group1_name="Phase 1 (Early)", group2_name="Phase 2 (Late)")

    st.markdown(f"**Selected Test:** `{comp['test_name']}`")
    c_res1, c_res2, c_res3 = st.columns(3)
    with c_res1:
        render_kpi_card("Test Statistic", f"{comp['statistic']:.3f}", f"p-value: {comp['p_value']:.4f}")
    with c_res2:
        render_kpi_card("Cohen's d Effect Size", f"{comp['cohens_d']:.2f}", "Standardized Mean Difference")
    with c_res3:
        render_kpi_card("Significance", "Significant (p < 0.05)" if comp['is_significant'] else "Not Significant", "alpha = 0.05")

    st.success(f"**Interpretation:** {comp['interpretation']}")

st.markdown("---")
# 3. Bland-Altman Agreement Analysis
st.markdown("### 3. Bland-Altman Agreement Analysis")
if len(g1) > 0 and len(g2) > 0:
    ba = StatisticalAnalyzer.bland_altman(g1, g2)
    fig_ba = VisualizationEngine.plot_bland_altman(ba, title="Bland-Altman Agreement: Phase 1 vs Phase 2 Attention")
    st.plotly_chart(fig_ba, use_container_width=True)
    st.caption(f"Bland-Altman Interpretation: {ba['interpretation']}")
