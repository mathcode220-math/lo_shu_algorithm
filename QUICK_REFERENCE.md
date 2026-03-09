# Lo Shu Balance Algorithm - Quick Reference Guide

## Project Overview

A novel image denoising algorithm based on the Lo Shu Magic Square (3×3).

## Quick Start

```bash
# Install dependencies
pip install -r requirements.txt

# Run basic tests
python run_tests.py

# Run academic research tests
python -m tests.academic_tests

# Run complexity analysis
python src/complexity_analysis.py
```

## Project Structure

```
lo_shu_algorithm/
├── src/
│   ├── lo_shu_matrix.py       # Magic square implementation
│   ├── lo_shu_filter.py       # Main denoising algorithm
│   ├── benchmark_filters.py   # Comparison filters
│   ├── metrics.py             # Evaluation metrics
│   ├── statistical_analysis.py # Statistical tests
│   └── complexity_analysis.py  # Complexity analysis
├── tests/
│   ├── test_suite.py          # Basic tests
│   └── academic_tests.py      # Academic research tests
├── docs/
│   ├── ACADEMIC_PAPER.md      # IEEE-format paper
│   ├── FINAL_RESEARCH_REPORT_AR.md  # Arabic report
│   ├── TEST_RESULTS.md        # Test results
│   └── USER_GUIDE_AR.md       # Arabic user guide
├── results/                    # Generated results
├── run_tests.py               # Test runner
└── requirements.txt           # Dependencies
```

## Usage Examples

### Basic Denoising

```python
from src.lo_shu_filter import LoShuBalanceFilter

filter_obj = LoShuBalanceFilter()
denoised = filter_obj.apply(noisy_image)
```

### With Metrics

```python
from src.lo_shu_filter import LoShuBalanceFilter
from src.metrics import ImageMetrics

filter_obj = LoShuBalanceFilter()
denoised = filter_obj.apply(noisy)

psnr = ImageMetrics.psnr(original, denoised)
ssim = ImageMetrics.ssim(original, denoised)
edge_pres = ImageMetrics.edge_preservation(original, denoised)
```

### Statistical Analysis

```python
from src.statistical_analysis import analyze_method_comparison
import numpy as np

scores = {
    'Lo Shu': np.array([25.3, 26.1, 24.8]),
    'Mean': np.array([28.2, 27.9, 28.5]),
    'Gaussian': np.array([22.6, 23.1, 22.2]),
    'Median': np.array([26.3, 26.8, 25.9])
}

report = analyze_method_comparison(scores, 'PSNR')
print(report)
```

## Key Results

| Metric | Lo Shu | Best Method |
|--------|--------|-------------|
| Edge Preservation | **0.925** | Lo Shu (1st) |
| Bit Linearity | **0.964** | Lo Shu (1st) |
| PSNR | 22.45 | Median (25.56) |
| SSIM | 0.42 | Median (0.67) |

## Complexity

| Aspect | Complexity |
|--------|------------|
| Time | O(n) |
| Space | O(n) |
| Kernel | 3×3 fixed |

## Research Status

✅ **Academic Research Complete**

- [x] Mathematical foundation
- [x] Algorithm implementation
- [x] Comprehensive testing
- [x] Statistical analysis
- [x] Complexity analysis
- [x] Academic paper
- [x] Full documentation

## Publications

- **Academic Paper**: `docs/ACADEMIC_PAPER.md`
- **Arabic Report**: `docs/FINAL_RESEARCH_REPORT_AR.md`
- **Test Results**: `docs/TEST_RESULTS.md`

## Citation

```bibtex
@misc{lo_shu_algorithm_2026,
  title={Lo Shu Balance Algorithm: A Novel Image Denoising Approach Based on Magic Square Properties},
  author={Your Name},
  year={2026},
  note={Available at: GitHub repository}
}
```

## License

MIT License
