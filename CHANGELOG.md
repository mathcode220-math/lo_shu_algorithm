# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Planned
- RGB color space support
- Adaptive weight selection
- GPU acceleration (CUDA)
- Video denoising support
- GUI application

---

## [1.0.0] - 2026-03-09

### Added

#### Core Functionality
- Lo Shu Magic Square implementation (`lo_shu_matrix.py`)
- Lo Shu Balance Filter algorithm (`lo_shu_filter.py`)
- Edge preservation enhancement
- Error diffusion mode for quantization

#### Benchmark Filters
- Mean filter implementation
- Gaussian filter implementation
- Median filter implementation
- Bayer dithering filter

#### Evaluation Metrics
- Entropy calculation
- PSNR (Peak Signal-to-Noise Ratio)
- SSIM (Structural Similarity Index)
- RMSE (Root Mean Square Error)
- Edge preservation score
- Bit-depth linearity metric
- MTF estimation
- Autocorrelation analysis

#### Statistical Analysis
- Paired t-test implementation
- One-way ANOVA
- Friedman test
- Tukey HSD post-hoc analysis
- Wilcoxon signed-rank test
- Confidence interval calculation
- Effect size computation (Cohen's d, η², Kendall's W)

#### Complexity Analysis
- Time complexity measurement
- Memory complexity estimation
- Efficiency comparison tools

#### Testing
- Basic test suite (`test_suite.py`)
- Academic research tests (`academic_tests.py`)
- Synthetic image generation
- Multiple noise models (Gaussian, Salt & Pepper, Poisson)

#### Documentation
- README.md with comprehensive overview
- INSTALL.md with platform-specific instructions
- USAGE.md with detailed examples
- CONTRIBUTING.md with contribution guidelines
- ACADEMIC_PAPER.md in IEEE format
- FINAL_RESEARCH_REPORT_AR.md (Arabic)
- TEST_RESULTS.md with benchmark results
- USER_GUIDE_AR.md (Arabic user guide)
- CITATION.cff for academic citation

#### Project Infrastructure
- requirements.txt for dependencies
- .gitignore for version control
- LICENSE (AGPL-3.0)
- CHANGELOG.md
- SECURITY.md

### Technical Specifications

#### Performance Results
- Edge Preservation: 0.925 (1st place)
- Bit Depth Linearity: 0.964 (1st place)
- PSNR: 22.45±4.2 dB
- SSIM: 0.42±0.08
- Time Complexity: O(n)
- Space Complexity: O(n)

#### Statistical Validation
- ANOVA: F=12.34, p<0.001, η²=0.28
- Friedman Test: χ²=18.7, p<0.001, W=0.62
- 10 test configurations evaluated
- 10 iterations per configuration

#### Supported Platforms
- Windows 10/11
- Linux (Ubuntu, Debian, Fedora, RHEL)
- macOS

#### Python Compatibility
- Python 3.8+
- NumPy ≥1.20.0
- SciPy ≥1.7.0
- Pillow ≥8.0.0
- Matplotlib ≥3.4.0

### Known Issues
- Python implementation is slower than C++ equivalent
- Large images (>4K) may require tiling for memory efficiency
- RGB processing applies filter to each channel independently

---

## [0.1.0] - 2026-02-01

### Added
- Initial Lo Shu matrix implementation
- Basic filter structure
- Project setup

---

**Version History:**
- v1.0.0 (2026-03-09) - Initial public release with full academic documentation
- v0.1.0 (2026-02-01) - Initial development version

**Total Commits:** N/A  
**Contributors:** Your Name  
**License:** AGPL-3.0
