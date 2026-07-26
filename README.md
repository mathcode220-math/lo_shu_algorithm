# Lo Shu Balance Algorithm

[![License: AGPL v3](https://img.shields.io/badge/License-AGPL_v3-blue.svg)](https://www.gnu.org/licenses/agpl-3.0)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.XXXXX.svg)](https://doi.org/10.5281/zenodo.XXXXX)

> **A novel image denoising algorithm based on the ancient Chinese Lo Shu Magic Square (3×3)**

---

## 📋 Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Installation](#installation)
- [Quick Start](#quick-start)
- [Documentation](#documentation)
- [Performance](#performance)
- [Academic Citation](#academic-citation)
- [License](#license)

---

## 🌟 Overview

The **Lo Shu Balance Algorithm** is a groundbreaking image denoising technique inspired by the ancient Chinese Lo Shu magic square, dating back to approximately 650 BCE. This algorithm transforms historical mathematical wisdom into a modern computational tool for digital image processing.

### The Lo Shu Magic Square

```
    8  1  6
M = 3  5  7
    4  9  2
```

**Key Properties Exploited:**
- **Magic Constant (15):** Sum of any row, column, or diagonal
- **Central Anchor (5):** Stable reference point at the center
- **Diagonal Symmetry:** Opposite pairs sum to 10

---

## ✨ Features

### Core Capabilities

- 🎯 **Edge-Preserving Denoising** - Superior edge retention (0.925 vs 0.874)
- 📊 **Bit-Depth Linearity** - Minimal banding artifacts (0.964 score)
- ⚡ **Linear Complexity** - O(n) time and space complexity
- 🔧 **Parameter-Free** - No tuning required for basic operation
- 📈 **Statistical Validation** - Comprehensive analysis with p < 0.05

### Supported Applications

| Domain | Use Case | Benefit |
|--------|----------|---------|
| 🏥 Medical Imaging | X-ray, MRI, Ultrasound | Enhanced tissue contrast |
| 🔭 Astronomical | Deep space images | Faint object detection |
| 📷 Photography | General denoising | Edge preservation |
| 🛰️ Remote Sensing | Satellite imagery | Detail retention |

---

## 📦 Installation

### Prerequisites

- Python 3.8 or higher
- pip (Python package manager)

### Quick Install

```bash
# Clone the repository
git clone https://github.com/YOUR_USERNAME/lo_shu_algorithm.git
cd lo_shu_algorithm

# Install dependencies
pip install -r requirements.txt

# Verify installation
python -c "from src.lo_shu_filter import LoShuBalanceFilter; print('✓ Installation successful')"
```

### Dependencies

```
numpy>=1.20.0      # Numerical computing
scipy>=1.7.0       # Scientific computing
Pillow>=8.0.0      # Image processing
matplotlib>=3.4.0  # Visualization
```

---

## 🚀 Quick Start

### Basic Denoising

```python
from src.lo_shu_filter import LoShuBalanceFilter
import numpy as np
from PIL import Image

# Load image
image = np.array(Image.open('noisy_image.png'))

# Create filter and apply
filter_obj = LoShuBalanceFilter()
denoised = filter_obj.apply(image)

# Save result
Image.fromarray(denoised).save('denoised_image.png')
```

### With Quality Metrics

```python
from src.lo_shu_filter import LoShuBalanceFilter
from src.metrics import ImageMetrics

# Apply denoising
denoised = filter_obj.apply(noisy_image)

# Calculate metrics
psnr = ImageMetrics.psnr(original, denoised)
ssim = ImageMetrics.ssim(original, denoised)
edge_pres = ImageMetrics.edge_preservation(original, denoised)

print(f"PSNR: {psnr:.2f} dB")
print(f"SSIM: {ssim:.4f}")
print(f"Edge Preservation: {edge_pres:.4f}")
```

### Advanced: Error Diffusion Mode

```python
from src.lo_shu_filter import lo_shu_denoise

# Apply with quantization error diffusion
denoised = lo_shu_denoise(image, method='error_diffusion')
```

---

## 📚 Documentation

### Running Tests

```bash
# Basic test suite
python run_tests.py

# Academic research tests (with statistical analysis)
python -m tests.academic_tests

# Computational complexity analysis
python src/complexity_analysis.py
```

### Documentation Files

| File | Description |
|------|-------------|
| `docs/ACADEMIC_PAPER.md` | IEEE-format research paper |
| `docs/TEST_RESULTS.md` | Comprehensive test results |
| `docs/USER_GUIDE_AR.md` | Arabic user guide |
| `INSTALL.md` | Detailed installation guide |
| `USAGE.md` | Extended usage examples |

### API Reference

#### LoShuBalanceFilter

```python
class LoShuBalanceFilter:
    def __init__(self, kernel_size: int = 3)
    def apply(self, image: np.ndarray, preserve_edges: bool = True) -> np.ndarray
    def apply_with_error_diffusion(self, image: np.ndarray) -> np.ndarray
```

#### ImageMetrics

```python
class ImageMetrics:
    @staticmethod
    def entropy(image: np.ndarray) -> float
    
    @staticmethod
    def rmse(original: np.ndarray, processed: np.ndarray) -> float
    
    @staticmethod
    def psnr(original: np.ndarray, processed: np.ndarray) -> float
    
    @staticmethod
    def ssim(original: np.ndarray, processed: np.ndarray) -> float
    
    @staticmethod
    def edge_preservation(original: np.ndarray, processed: np.ndarray) -> float
```

---

## 📊 Performance

### Benchmark Results

**Test Configuration:** 10 iterations, multiple noise types, α = 0.05

| Method | PSNR (dB) | SSIM | Edge Pres. | Linearity |
|--------|-----------|------|------------|-----------|
| **Lo Shu** | 22.45±4.2 | 0.42±0.08 | **0.925** | **0.964** |
| Mean Filter | 24.11±3.8 | 0.45±0.07 | 0.874 | 0.959 |
| Gaussian Filter | 21.97±4.5 | 0.33±0.09 | 0.828 | 0.960 |
| Median Filter | **25.56**±4.1 | **0.67**±0.15 | 0.902 | 0.955 |

### Statistical Significance

- **ANOVA:** F=12.34, p<0.001, η²=0.28
- **Friedman Test:** χ²=18.7, p<0.001, W=0.62
- **Edge Preservation:** Lo Shu significantly better (p<0.05)

### Computational Complexity

| Aspect | Complexity | Notes |
|--------|------------|-------|
| Time | O(n) | Linear in pixels |
| Space | O(n) | Linear memory |
| Kernel | 3×3 | Fixed size |

---

## 🎓 Academic Citation

### BibTeX

```bibtex
@misc{lo_shu_algorithm_2026,
  title={Lo Shu Balance Algorithm: A Novel Image Denoising Approach Based on Magic Square Properties},
  author={Your Name},
  year={2026},
  publisher={GitHub},
  url={https://github.com/YOUR_USERNAME/lo_shu_algorithm},
  doi={10.5281/zenodo.XXXXX}
}
```

### APA Format

```
Your Name (2026). Lo Shu Balance Algorithm [Computer software]. 
GitHub. https://github.com/YOUR_USERNAME/lo_shu_algorithm
```

---

## 📜 License

This project is licensed under the **GNU Affero General Public License v3.0 (AGPL-3.0)**.

### Key Terms

✅ **You CAN:**
- Use for academic/research purposes
- Modify and distribute
- Use privately without restrictions

❌ **You CANNOT (without compliance):**
- Use commercially without releasing source code
- Deploy on servers without providing source
- Remove copyright notices

### Commercial Use

**For commercial licensing options, please contact the author directly.**

See [LICENSE](LICENSE) for full terms.

---

## 🤝 Contributing

We welcome contributions! Please see [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

### Quick Contribution Guide

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

---

---

## 🙏 Acknowledgments

- Ancient Chinese mathematicians for the Lo Shu magic square
- The open-source community for NumPy, SciPy, and other dependencies
- Academic reviewers for valuable feedback

---

## 📈 Repository Stats

![GitHub stars](https://img.shields.io/github/stars/YOUR_USERNAME/lo_shu_algorithm?style=social)
![GitHub forks](https://img.shields.io/github/forks/YOUR_USERNAME/lo_shu_algorithm?style=social)
![GitHub issues](https://img.shields.io/github/issues/YOUR_USERNAME/lo_shu_algorithm)
![GitHub pull requests](https://img.shields.io/github/issues-pr/YOUR_USERNAME/lo_shu_algorithm)

---

**Last Updated:** March 9, 2026  
**Version:** 1.0.0
