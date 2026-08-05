"""
Unit Tests for Statistical Analysis Module & Bland-Altman Agreement.
"""

import pytest
import numpy as np
from stats.analyzer import StatisticalAnalyzer


def test_statistical_analyzer():
    np.random.seed(42)
    g1 = np.random.normal(50.0, 10.0, 100)
    g2 = np.random.normal(60.0, 10.0, 100)

    desc = StatisticalAnalyzer.descriptive_stats(g1)
    assert "mean" in desc
    assert "std" in desc

    norm = StatisticalAnalyzer.test_normality(g1)
    assert "is_normal" in norm

    comp = StatisticalAnalyzer.compare_groups(g1, g2, group1_name="G1", group2_name="G2")
    assert comp["is_significant"] == True
    assert comp["cohens_d"] != 0.0

    ba = StatisticalAnalyzer.bland_altman(g1, g2)
    assert "mean_difference" in ba
    assert "loa_upper_95" in ba
