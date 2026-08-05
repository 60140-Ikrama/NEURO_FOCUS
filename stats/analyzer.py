"""
Statistical Analysis Module for NeuroLearn Research Suite.
Provides hypothesis testing, Bland-Altman agreement, Cohen's d effect sizes,
normality checks, and automated scientific interpretation.
"""

from typing import Dict, Any, Tuple, Optional, List
import numpy as np
import pandas as pd
from scipy import stats
from utils.logger import get_logger

logger = get_logger("StatisticalAnalyzer")


class StatisticalAnalyzer:
    """Comprehensive Biomedical Statistical Engine for EEG Attention Research."""

    @staticmethod
    def descriptive_stats(data: np.ndarray, ci: float = 0.95) -> Dict[str, float]:
        """Compute mean, std, median, IQR, 95% CI bounds."""
        clean_data = data[~np.isnan(data)]
        if len(clean_data) == 0:
            return {}

        n = len(clean_data)
        mean_val = float(np.mean(clean_data))
        std_val = float(np.std(clean_data, ddof=1)) if n > 1 else 0.0
        med_val = float(np.median(clean_data))

        q75, q25 = np.percentile(clean_data, [75, 25])
        iqr_val = float(q75 - q25)

        # 95% Confidence Interval
        sem = std_val / np.sqrt(n) if n > 0 else 0.0
        h = sem * stats.t.ppf((1 + ci) / 2.0, n - 1) if n > 1 else 0.0

        return {
            "n": n,
            "mean": round(mean_val, 4),
            "std": round(std_val, 4),
            "median": round(med_val, 4),
            "iqr": round(iqr_val, 4),
            "ci_lower": round(mean_val - h, 4),
            "ci_upper": round(mean_val + h, 4),
            "skewness": round(float(stats.skew(clean_data)), 4) if std_val > 0 else 0.0,
            "kurtosis": round(float(stats.kurtosis(clean_data)), 4) if std_val > 0 else 0.0
        }

    @staticmethod
    def test_normality(data: np.ndarray) -> Dict[str, Any]:
        """Run Shapiro-Wilk test for normality."""
        clean = data[~np.isnan(data)]
        if len(clean) < 3:
            return {"is_normal": False, "p_value": 0.0, "stat": 0.0}

        # Subsample if n > 5000 (Shapiro limit)
        sample_data = clean if len(clean) <= 5000 else np.random.choice(clean, 5000, replace=False)
        stat_val, p_val = stats.shapiro(sample_data)

        return {
            "is_normal": bool(p_val > 0.05),
            "p_value": float(p_val),
            "statistic": float(stat_val),
            "interpretation": "Data is normally distributed (p > 0.05)" if p_val > 0.05 else "Data deviates significantly from normality (p <= 0.05)"
        }

    @staticmethod
    def compare_groups(
        group1: np.ndarray,
        group2: np.ndarray,
        paired: bool = False,
        group1_name: str = "Group 1",
        group2_name: str = "Group 2"
    ) -> Dict[str, Any]:
        """Run appropriate parametric (t-test) or non-parametric (Wilcoxon/Mann-Whitney) test."""
        g1 = group1[~np.isnan(group1)]
        g2 = group2[~np.isnan(group2)]

        # Check normality
        norm1 = StatisticalAnalyzer.test_normality(g1)["is_normal"]
        norm2 = StatisticalAnalyzer.test_normality(g2)["is_normal"]
        both_normal = norm1 and norm2

        # Compute Cohen's d effect size
        n1, n2 = len(g1), len(g2)
        s_pooled = np.sqrt(((n1 - 1)*np.var(g1, ddof=1) + (n2 - 1)*np.var(g2, ddof=1)) / (n1 + n2 - 2)) if (n1+n2)>2 else 1.0
        cohens_d = float((np.mean(g1) - np.mean(g2)) / (s_pooled + 1e-9))

        if paired:
            if both_normal:
                test_name = "Paired Student's t-Test"
                stat_val, p_val = stats.ttest_rel(g1, g2)
            else:
                test_name = "Wilcoxon Signed-Rank Test"
                stat_val, p_val = stats.wilcoxon(g1, g2)
        else:
            if both_normal:
                test_name = "Independent Two-Sample t-Test"
                stat_val, p_val = stats.ttest_ind(g1, g2)
            else:
                test_name = "Mann-Whitney U Test"
                stat_val, p_val = stats.mannwhitneyu(g1, g2)

        p_val = float(p_val)
        significant = p_val < 0.05

        # Text interpretation
        sig_str = "statistically significant" if significant else "not statistically significant"
        interp = (
            f"The difference between {group1_name} (Mean={np.mean(g1):.2f}) and {group2_name} "
            f"(Mean={np.mean(g2):.2f}) is {sig_str} using {test_name} (statistic={stat_val:.3f}, p={p_val:.4f}, Cohen's d={cohens_d:.2f})."
        )

        return {
            "test_name": test_name,
            "statistic": float(stat_val),
            "p_value": p_val,
            "cohens_d": round(cohens_d, 3),
            "is_significant": significant,
            "group1_mean": round(float(np.mean(g1)), 3),
            "group2_mean": round(float(np.mean(g2)), 3),
            "interpretation": interp
        }

    @staticmethod
    def bland_altman(data1: np.ndarray, data2: np.ndarray) -> Dict[str, Any]:
        """Compute Bland-Altman agreement metrics between two measurement series."""
        d1 = data1[~np.isnan(data1)]
        d2 = data2[~np.isnan(data2)]

        min_len = min(len(d1), len(d2))
        d1, d2 = d1[:min_len], d2[:min_len]

        means = (d1 + d2) / 2.0
        diffs = d1 - d2

        mean_diff = float(np.mean(diffs))
        sd_diff = float(np.std(diffs, ddof=1)) if min_len > 1 else 0.0

        loa_upper = mean_diff + 1.96 * sd_diff
        loa_lower = mean_diff - 1.96 * sd_diff

        # Pearson correlation
        r_val, p_val = stats.pearsonr(d1, d2)

        return {
            "mean_difference": round(mean_diff, 4),
            "sd_difference": round(sd_diff, 4),
            "loa_upper_95": round(loa_upper, 4),
            "loa_lower_95": round(loa_lower, 4),
            "pearson_r": round(float(r_val), 4),
            "p_value": round(float(p_val), 5),
            "sample_size": min_len,
            "interpretation": f"Bland-Altman mean bias is {mean_diff:.2f} with 95% limits of agreement [{loa_lower:.2f}, {loa_upper:.2f}]. Correlation r = {r_val:.3f}."
        }
