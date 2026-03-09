"""
Academic Research Test Suite
=============================
Comprehensive tests with statistical analysis for academic publication.
"""

import numpy as np
import sys
import os
import time
from typing import Dict, List

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from src.lo_shu_matrix import LoShuMatrix
from src.lo_shu_filter import LoShuBalanceFilter, lo_shu_denoise
from src.benchmark_filters import BenchmarkFilters
from src.metrics import ImageMetrics
from src.statistical_analysis import (
    StatisticalAnalyzer, 
    analyze_method_comparison,
    StatisticalResult
)


class AcademicTestSuite:
    """
    Academic-grade test suite with rigorous statistical analysis.
    """
    
    def __init__(self, n_iterations: int = 10):
        """
        Initialize academic test suite.
        
        Args:
            n_iterations: Number of iterations for statistical significance
        """
        self.lo_shu_filter = LoShuBalanceFilter()
        self.analyzer = StatisticalAnalyzer(alpha=0.05)
        self.n_iterations = n_iterations
        self.results = {}
        self.all_scores = {
            'Lo Shu': [],
            'Mean': [],
            'Gaussian': [],
            'Median': []
        }
    
    def _generate_test_image(self, image_type: str, size: int = 128) -> np.ndarray:
        """Generate various test image types."""
        if image_type == 'gradient':
            x = np.linspace(0, 255, size)
            y = np.linspace(0, 255, size)
            xx, yy = np.meshgrid(x, y)
            return np.clip((xx + yy) / 2, 0, 255).astype(np.uint8)
        
        elif image_type == 'checkerboard':
            square_size = 16
            x = np.arange(size) // square_size
            y = np.arange(size) // square_size
            xx, yy = np.meshgrid(x, y)
            return ((xx + yy) % 2) * 255
    
        elif image_type == 'sine_wave':
            x = np.linspace(0, 8 * np.pi, size)
            y = np.linspace(0, 8 * np.pi, size)
            xx, yy = np.meshgrid(x, y)
            pattern = np.sin(xx) * np.cos(yy)
            return np.clip((pattern + 1) * 127.5, 0, 255).astype(np.uint8)
        
        elif image_type == 'circles':
            center = size // 2
            x = np.arange(size) - center
            y = np.arange(size) - center
            xx, yy = np.meshgrid(x, y)
            circles = np.sqrt(xx ** 2 + yy ** 2)
            return np.clip((circles % 20) / 20 * 255, 0, 255).astype(np.uint8)
        
        elif image_type == 'random_pattern':
            np.random.seed(42)
            base = np.random.randint(50, 200, (size, size), dtype=np.uint8)
            # Add some structure
            x = np.linspace(0, 4 * np.pi, size)
            y = np.linspace(0, 4 * np.pi, size)
            xx, yy = np.meshgrid(x, y)
            modulation = (np.sin(xx) * np.cos(yy) + 1) * 50
            return np.clip(base.astype(float) + modulation, 0, 255).astype(np.uint8)
        
        else:
            raise ValueError(f"Unknown image type: {image_type}")
    
    def _add_noise(self, image: np.ndarray, noise_type: str, 
                   noise_level: float) -> np.ndarray:
        """Add various types of noise."""
        if noise_type == 'gaussian':
            noise = np.random.normal(0, noise_level, image.shape)
            return np.clip(image.astype(float) + noise, 0, 255).astype(np.uint8)
        
        elif noise_type == 'salt_pepper':
            noisy = image.copy()
            h, w = image.shape
            salt_mask = np.random.random((h, w)) < noise_level
            pepper_mask = np.random.random((h, w)) < noise_level
            noisy[salt_mask] = 255
            noisy[pepper_mask] = 0
            return noisy
        
        elif noise_type == 'poisson':
            normalized = image.astype(float) / 255.0
            noisy = np.random.poisson(normalized * 100) / 100.0
            return np.clip(noisy * 255, 0, 255).astype(np.uint8)
        
        else:
            raise ValueError(f"Unknown noise type: {noise_type}")
    
    def run_single_test(self, image_type: str, noise_type: str, 
                        noise_level: float, metric: str) -> Dict[str, list]:
        """
        Run single test configuration with multiple iterations.
        
        Returns:
            Dictionary of method scores for this test configuration
        """
        scores = {
            'Lo Shu': [],
            'Mean': [],
            'Gaussian': [],
            'Median': []
        }
        
        for iteration in range(self.n_iterations):
            # Generate image with different seed each iteration
            np.random.seed(iteration * 100 + int(time.time() * 1000) % 10000)
            original = self._generate_test_image(image_type)
            noisy = self._add_noise(original, noise_type, noise_level)
            
            # Apply all filters
            lo_shu_result = self.lo_shu_filter.apply(noisy)
            mean_result = BenchmarkFilters.mean_filter(noisy)
            gaussian_result = BenchmarkFilters.gaussian_filter(noisy)
            median_result = BenchmarkFilters.median_filter(noisy)
            
            # Calculate metrics
            if metric == 'psnr':
                scores['Lo Shu'].append(ImageMetrics.psnr(original, lo_shu_result))
                scores['Mean'].append(ImageMetrics.psnr(original, mean_result))
                scores['Gaussian'].append(ImageMetrics.psnr(original, gaussian_result))
                scores['Median'].append(ImageMetrics.psnr(original, median_result))
            
            elif metric == 'ssim':
                scores['Lo Shu'].append(ImageMetrics.ssim(original, lo_shu_result))
                scores['Mean'].append(ImageMetrics.ssim(original, mean_result))
                scores['Gaussian'].append(ImageMetrics.ssim(original, gaussian_result))
                scores['Median'].append(ImageMetrics.ssim(original, median_result))
            
            elif metric == 'edge_preservation':
                scores['Lo Shu'].append(ImageMetrics.edge_preservation(original, lo_shu_result))
                scores['Mean'].append(ImageMetrics.edge_preservation(original, mean_result))
                scores['Gaussian'].append(ImageMetrics.edge_preservation(original, gaussian_result))
                scores['Median'].append(ImageMetrics.edge_preservation(original, median_result))
        
        return scores
    
    def run_comprehensive_tests(self):
        """Run comprehensive academic test suite."""
        print("\n" + "=" * 70)
        print("ACADEMIC RESEARCH TEST SUITE")
        print("=" * 70)
        print(f"\nConfiguration:")
        print(f"  Iterations per test: {self.n_iterations}")
        print(f"  Significance level (alpha): 0.05")
        print("=" * 70)
        
        # Test configurations
        test_configs = [
            ('gradient', 'gaussian', 0.1, 'psnr'),
            ('gradient', 'gaussian', 0.2, 'psnr'),
            ('gradient', 'gaussian', 0.3, 'psnr'),
            ('checkerboard', 'gaussian', 0.15, 'psnr'),
            ('checkerboard', 'salt_pepper', 0.05, 'psnr'),
            ('checkerboard', 'salt_pepper', 0.1, 'psnr'),
            ('sine_wave', 'gaussian', 0.15, 'ssim'),
            ('circles', 'gaussian', 0.1, 'edge_preservation'),
            ('random_pattern', 'gaussian', 0.15, 'psnr'),
            ('random_pattern', 'poisson', 0.0, 'psnr'),
        ]
        
        all_results = {
            'psnr': {'Lo Shu': [], 'Mean': [], 'Gaussian': [], 'Median': []},
            'ssim': {'Lo Shu': [], 'Mean': [], 'Gaussian': [], 'Median': []},
            'edge_preservation': {'Lo Shu': [], 'Mean': [], 'Gaussian': [], 'Median': []}
        }
        
        print("\nRunning test configurations...")
        print("-" * 70)
        
        for i, (img_type, noise_type, noise_level, metric) in enumerate(test_configs):
            print(f"\nTest {i+1}/{len(test_configs)}: {img_type} + {noise_type} "
                  f"(level={noise_level}) -> {metric}")
            
            scores = self.run_single_test(img_type, noise_type, noise_level, metric)
            
            for method in scores:
                all_results[metric][method].extend(scores[metric] if metric in scores 
                                                    else scores[method])
            
            # Print iteration results
            mean_scores = {m: np.mean(s) for m, s in scores.items()}
            print(f"  Mean Scores: Lo Shu={mean_scores['Lo Shu']:.4f}, "
                  f"Mean={mean_scores['Mean']:.4f}, "
                  f"Gaussian={mean_scores['Gaussian']:.4f}, "
                  f"Median={mean_scores['Median']:.4f}")
        
        # Store results
        self.results = all_results
        
        print("\n" + "=" * 70)
        print("Test execution complete. Generating statistical analysis...")
        print("=" * 70)
        
        return all_results
    
    def generate_statistical_report(self, results: Dict) -> str:
        """Generate comprehensive statistical report."""
        report = []
        
        for metric, method_scores in results.items():
            # Convert to numpy arrays
            scores_dict = {k: np.array(v) for k, v in method_scores.items()}
            
            # Generate statistical analysis
            stat_report = analyze_method_comparison(scores_dict, metric.upper())
            report.append(stat_report)
            report.append("\n\n")
        
        return "\n".join(report)
    
    def compute_ranking(self, results: Dict) -> Dict[str, Dict[str, int]]:
        """
        Compute method rankings for each metric.
        
        Returns:
            Dictionary with rankings per metric
        """
        rankings = {}
        
        for metric, method_scores in results.items():
            mean_scores = {k: np.mean(v) for k, v in method_scores.items()}
            sorted_methods = sorted(mean_scores.keys(), key=lambda x: mean_scores[x], reverse=True)
            
            rankings[metric] = {method: rank+1 for rank, method in enumerate(sorted_methods)}
        
        return rankings
    
    def print_ranking_summary(self, rankings: Dict[str, Dict[str, int]]):
        """Print ranking summary table."""
        print("\n" + "=" * 70)
        print("METHOD RANKING SUMMARY")
        print("=" * 70)
        print(f"\n{'Metric':<25} {'1st':<15} {'2nd':<15} {'3rd':<15} {'4th':<15}")
        print("-" * 70)
        
        methods = ['Lo Shu', 'Mean', 'Gaussian', 'Median']
        
        for metric, ranks in rankings.items():
            sorted_by_rank = sorted(ranks.items(), key=lambda x: x[1])
            row = [f"{m[0]} (#{m[1]})" for m in sorted_by_rank]
            # Pad if needed
            while len(row) < 4:
                row.append("-")
            print(f"{metric:<25} {row[0]:<15} {row[1]:<15} {row[2]:<15} {row[3]:<15}")
        
        # Count first place finishes
        first_place_counts = {m: 0 for m in methods}
        for ranks in rankings.values():
            for method, rank in ranks.items():
                if rank == 1:
                    first_place_counts[method] += 1
        
        print("\n" + "-" * 70)
        print("TOTAL FIRST PLACE FINISHES:")
        for method, count in sorted(first_place_counts.items(), key=lambda x: x[1], reverse=True):
            print(f"  {method}: {count}")
        
        print("=" * 70)


def run_academic_research_tests(n_iterations: int = 10):
    """
    Main function to run complete academic research tests.
    
    Args:
        n_iterations: Number of iterations per test configuration
        
    Returns:
        Tuple of (results, statistical_report, rankings)
    """
    suite = AcademicTestSuite(n_iterations=n_iterations)
    
    # Run comprehensive tests
    results = suite.run_comprehensive_tests()
    
    # Generate statistical report
    stat_report = suite.generate_statistical_report(results)
    
    # Compute rankings
    rankings = suite.compute_ranking(results)
    suite.print_ranking_summary(rankings)
    
    # Save statistical report
    report_path = os.path.join(os.path.dirname(__file__), '..', 'results', 
                               'statistical_analysis.txt')
    os.makedirs(os.path.dirname(report_path), exist_ok=True)
    with open(report_path, 'w', encoding='utf-8') as f:
        f.write(stat_report)
    
    print(f"\nStatistical report saved to: {report_path}")
    
    return results, stat_report, rankings


if __name__ == "__main__":
    results, report, rankings = run_academic_research_tests(n_iterations=10)
