"""
Statistical Analysis Module for Academic Research
==================================================
Provides statistical tests for rigorous academic evaluation.
"""

import numpy as np
from scipy import stats
from typing import Dict, List, Tuple
from dataclasses import dataclass


@dataclass
class StatisticalResult:
    """Container for statistical test results."""
    test_name: str
    statistic: float
    p_value: float
    significant: bool
    confidence_interval: Tuple[float, float] = None
    effect_size: float = None


class StatisticalAnalyzer:
    """
    Statistical analysis tools for academic research validation.
    """
    
    def __init__(self, alpha: float = 0.05):
        """
        Initialize analyzer.
        
        Args:
            alpha: Significance level (default 0.05)
        """
        self.alpha = alpha
    
    def paired_t_test(self, scores_1: np.ndarray, scores_2: np.ndarray,
                      method1_name: str = "Method 1", 
                      method2_name: str = "Method 2") -> StatisticalResult:
        """
        Perform paired t-test between two methods.
        
        Args:
            scores_1: Performance scores from method 1
            scores_2: Performance scores from method 2
            method1_name: Name of first method
            method2_name: Name of second method
            
        Returns:
            StatisticalResult with test outcomes
        """
        t_stat, p_value = stats.ttest_rel(scores_1, scores_2)
        
        # Calculate confidence interval for mean difference
        mean_diff = np.mean(scores_1 - scores_2)
        std_diff = np.std(scores_1 - scores_2, ddof=1)
        n = len(scores_1)
        margin = stats.t.ppf(1 - self.alpha/2, n-1) * std_diff / np.sqrt(n)
        ci = (mean_diff - margin, mean_diff + margin)
        
        # Calculate Cohen's d (effect size)
        pooled_std = np.sqrt((np.var(scores_1) + np.var(scores_2)) / 2)
        cohens_d = mean_diff / pooled_std if pooled_std > 0 else 0
        
        return StatisticalResult(
            test_name=f"Paired t-test ({method1_name} vs {method2_name})",
            statistic=t_stat,
            p_value=p_value,
            significant=p_value < self.alpha,
            confidence_interval=ci,
            effect_size=cohens_d
        )
    
    def one_way_anova(self, *groups: np.ndarray, 
                      group_names: List[str] = None) -> StatisticalResult:
        """
        Perform one-way ANOVA to compare multiple methods.
        
        Args:
            *groups: Variable number of score arrays from different methods
            group_names: Optional names for each group
            
        Returns:
            StatisticalResult with ANOVA outcomes
        """
        if group_names is None:
            group_names = [f"Method {i+1}" for i in range(len(groups))]
        
        f_stat, p_value = stats.f_oneway(*groups)
        
        # Calculate effect size (eta-squared)
        all_scores = np.concatenate(groups)
        grand_mean = np.mean(all_scores)
        ss_total = np.sum((all_scores - grand_mean) ** 2)
        ss_between = sum(len(g) * (np.mean(g) - grand_mean) ** 2 for g in groups)
        eta_squared = ss_between / ss_total if ss_total > 0 else 0
        
        return StatisticalResult(
            test_name=f"One-way ANOVA ({', '.join(group_names)})",
            statistic=f_stat,
            p_value=p_value,
            significant=p_value < self.alpha,
            effect_size=eta_squared
        )
    
    def tukey_hsd_posthoc(self, *groups: np.ndarray,
                          group_names: List[str] = None) -> List[Dict]:
        """
        Perform Tukey's HSD post-hoc test for pairwise comparisons.
        
        Args:
            *groups: Score arrays from different methods
            group_names: Names for each group
            
        Returns:
            List of pairwise comparison results
        """
        if group_names is None:
            group_names = [f"Method {i+1}" for i in range(len(groups))]
        
        # Combine all data
        all_data = np.concatenate(groups)
        labels = np.concatenate([
            np.full(len(g), i) for i, g in enumerate(groups)
        ])
        
        # Perform Tukey HSD
        tukey = stats.tukey_hsd(all_data, labels)
        
        results = []
        for i in range(len(groups)):
            for j in range(i+1, len(groups)):
                idx = i * len(groups) + j - (i * (i + 1)) // 2 - i - 1
                results.append({
                    'comparison': f"{group_names[i]} vs {group_names[j]}",
                    'mean_diff': tukey.mean_diff[i, j],
                    'p_value': tukey.pvalue[i, j],
                    'significant': tukey.pvalue[i, j] < self.alpha
                })
        
        return results
    
    def wilcoxon_signed_rank(self, scores_1: np.ndarray, scores_2: np.ndarray,
                             method1_name: str = "Method 1",
                             method2_name: str = "Method 2") -> StatisticalResult:
        """
        Perform Wilcoxon signed-rank test (non-parametric alternative to t-test).
        
        Args:
            scores_1: Performance scores from method 1
            scores_2: Performance scores from method 2
            method1_name: Name of first method
            method2_name: Name of second method
            
        Returns:
            StatisticalResult with test outcomes
        """
        stat, p_value = stats.wilcoxon(scores_1, scores_2)
        
        # Calculate effect size (r)
        n = len(scores_1)
        z = stats.norm.ppf(1 - p_value/2)
        r = z / np.sqrt(2 * n) if n > 0 else 0
        
        return StatisticalResult(
            test_name=f"Wilcoxon signed-rank ({method1_name} vs {method2_name})",
            statistic=stat,
            p_value=p_value,
            significant=p_value < self.alpha,
            effect_size=r
        )
    
    def compute_confidence_intervals(self, scores: np.ndarray, 
                                     confidence: float = 0.95) -> Dict[str, float]:
        """
        Compute confidence intervals for performance metrics.
        
        Args:
            scores: Array of performance scores
            confidence: Confidence level (default 0.95)
            
        Returns:
            Dictionary with mean, CI lower, CI upper, std
        """
        n = len(scores)
        mean = np.mean(scores)
        std = np.std(scores, ddof=1)
        margin = stats.t.ppf((1 + confidence) / 2, n-1) * std / np.sqrt(n)
        
        return {
            'mean': mean,
            'std': std,
            'ci_lower': mean - margin,
            'ci_upper': mean + margin,
            'confidence': confidence
        }
    
    def friedman_test(self, *groups: np.ndarray,
                      group_names: List[str] = None) -> StatisticalResult:
        """
        Perform Friedman test (non-parametric alternative to repeated measures ANOVA).
        
        Args:
            *groups: Score arrays from different methods (must be same length)
            group_names: Names for each group
            
        Returns:
            StatisticalResult with test outcomes
        """
        if group_names is None:
            group_names = [f"Method {i+1}" for i in range(len(groups))]
        
        chi2_stat, p_value = stats.friedmanchisquare(*groups)
        
        # Calculate Kendall's W (effect size)
        k = len(groups)  # number of methods
        n = len(groups[0])  # number of samples
        W = chi2_stat / (n * (k - 1)) if n * (k - 1) > 0 else 0
        
        return StatisticalResult(
            test_name=f"Friedman test ({', '.join(group_names)})",
            statistic=chi2_stat,
            p_value=p_value,
            significant=p_value < self.alpha,
            effect_size=W
        )
    
    def generate_statistical_report(self, results: Dict[str, StatisticalResult]) -> str:
        """
        Generate formatted statistical report.
        
        Args:
            results: Dictionary of StatisticalResult objects
            
        Returns:
            Formatted report string
        """
        report = []
        report.append("=" * 70)
        report.append("STATISTICAL ANALYSIS REPORT")
        report.append("=" * 70)
        report.append(f"\nSignificance Level (α): {self.alpha}")
        report.append("\n" + "-" * 70)
        
        for name, result in results.items():
            report.append(f"\n{name}")
            report.append("-" * 40)
            report.append(f"  Test Statistic: {result.statistic:.4f}")
            report.append(f"  p-value: {result.p_value:.6f}")
            report.append(f"  Significant: {'Yes' if result.significant else 'No'}")
            
            if result.confidence_interval:
                report.append(f"  95% CI: [{result.confidence_interval[0]:.4f}, "
                            f"{result.confidence_interval[1]:.4f}]")
            
            if result.effect_size:
                # Interpret effect size
                es = abs(result.effect_size)
                if es < 0.2:
                    interpretation = "negligible"
                elif es < 0.5:
                    interpretation = "small"
                elif es < 0.8:
                    interpretation = "medium"
                else:
                    interpretation = "large"
                report.append(f"  Effect Size: {result.effect_size:.4f} ({interpretation})")
        
        report.append("\n" + "=" * 70)
        return "\n".join(report)


def analyze_method_comparison(method_scores: Dict[str, np.ndarray], 
                              metric_name: str = "Performance") -> str:
    """
    Comprehensive statistical analysis comparing multiple methods.
    
    Args:
        method_scores: Dictionary mapping method names to score arrays
        metric_name: Name of the metric being analyzed
        
    Returns:
        Formatted statistical analysis report
    """
    analyzer = StatisticalAnalyzer(alpha=0.05)
    results = {}
    
    method_names = list(method_scores.keys())
    scores_list = list(method_scores.values())
    
    # 1. Descriptive Statistics
    report = []
    report.append("=" * 70)
    report.append(f"STATISTICAL ANALYSIS: {metric_name}")
    report.append("=" * 70)
    report.append("\n1. DESCRIPTIVE STATISTICS")
    report.append("-" * 70)
    report.append(f"{'Method':<20} {'Mean':<12} {'Std':<12} {'95% CI':<25}")
    report.append("-" * 70)
    
    for name, scores in method_scores.items():
        ci = analyzer.compute_confidence_intervals(scores)
        report.append(f"{name:<20} {ci['mean']:<12.4f} {ci['std']:<12.4f} "
                     f"[{ci['ci_lower']:.4f}, {ci['ci_upper']:.4f}]")
    
    # 2. One-way ANOVA
    report.append("\n2. ONE-WAY ANOVA")
    report.append("-" * 70)
    anova_result = analyzer.one_way_anova(*scores_list, group_names=method_names)
    results['ANOVA'] = anova_result
    report.append(f"F-statistic: {anova_result.statistic:.4f}")
    report.append(f"p-value: {anova_result.p_value:.6f}")
    report.append(f"Significant: {'Yes' if anova_result.significant else 'No'}")
    report.append(f"Effect Size (η²): {anova_result.effect_size:.4f}")
    
    # 3. Friedman Test (non-parametric)
    report.append("\n3. FRIEDMAN TEST (Non-parametric)")
    report.append("-" * 70)
    friedman_result = analyzer.friedman_test(*scores_list, group_names=method_names)
    results['Friedman'] = friedman_result
    report.append(f"Chi-squared: {friedman_result.statistic:.4f}")
    report.append(f"p-value: {friedman_result.p_value:.6f}")
    report.append(f"Significant: {'Yes' if friedman_result.significant else 'No'}")
    report.append(f"Effect Size (Kendall's W): {friedman_result.effect_size:.4f}")
    
    # 4. Pairwise t-tests (if ANOVA significant)
    if anova_result.significant:
        report.append("\n4. PAIRWISE COMPARISONS (Paired t-tests)")
        report.append("-" * 70)
        report.append(f"{'Comparison':<40} {'p-value':<12} {'Significant':<12}")
        report.append("-" * 70)
        
        for i, name1 in enumerate(method_names):
            for j, name2 in enumerate(method_names):
                if i < j:
                    t_result = analyzer.paired_t_test(
                        scores_list[i], scores_list[j],
                        name1, name2
                    )
                    results[f'{name1}_vs_{name2}'] = t_result
                    report.append(f"{name1} vs {name2:<20} {t_result.p_value:<12.6f} "
                                 f"{'Yes' if t_result.significant else 'No':<12}")
    
    report.append("\n" + "=" * 70)
    report.append("INTERPRETATION GUIDE:")
    report.append("  - p < 0.05: Statistically significant difference")
    report.append("  - Effect Size (Cohen's d): 0.2=small, 0.5=medium, 0.8=large")
    report.append("  - Effect Size (η²): 0.01=small, 0.06=medium, 0.14=large")
    report.append("=" * 70)
    
    return "\n".join(report)
