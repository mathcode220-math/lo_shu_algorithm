# Installation Guide

This guide provides detailed instructions for installing the Lo Shu Balance Algorithm.

## 📋 Prerequisites

### Required Software

| Software | Version | Purpose |
|----------|---------|---------|
| Python | 3.8+ | Runtime environment |
| pip | 20.0+ | Package manager |
| git | 2.0+ | Version control |

### Optional Software

| Software | Version | Purpose |
|----------|---------|---------|
| virtualenv | 20.0+ | Virtual environment |
| conda | 4.0+ | Environment management |

---

## 🔧 Installation Methods

### Method 1: Standard Installation (Recommended)

#### Step 1: Clone the Repository

```bash
git clone https://github.com/YOUR_USERNAME/lo_shu_algorithm.git
cd lo_shu_algorithm
```

#### Step 2: Create Virtual Environment (Optional but Recommended)

**Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

**Linux/Mac:**
```bash
python3 -m venv venv
source venv/bin/activate
```

#### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

#### Step 4: Verify Installation

```bash
python -c "from src.lo_shu_filter import LoShuBalanceFilter; print('✓ Installation successful')"
```

---

### Method 2: pip Installation

```bash
# Install directly from GitHub (when published)
pip install git+https://github.com/YOUR_USERNAME/lo_shu_algorithm.git
```

---

### Method 3: Conda Environment

```bash
# Create conda environment
conda create -n lo_shu python=3.10
conda activate lo_shu

# Install dependencies
conda install numpy scipy matplotlib pillow
pip install -r requirements.txt
```

---

## 🖥️ Platform-Specific Instructions

### Windows

#### Install Python

1. Download from [python.org](https://www.python.org/downloads/)
2. Run installer
3. ✅ Check "Add Python to PATH"
4. Click "Install Now"

#### Verify Installation

```cmd
py --version
pip --version
```

#### Install Visual C++ Redistributable (if needed)

Some dependencies may require:
- Download: [Microsoft Visual C++ Redistributable](https://aka.ms/vs/17/release/vc_redist.x64.exe)

---

### Linux (Ubuntu/Debian)

```bash
# Update package list
sudo apt update

# Install Python and pip
sudo apt install python3 python3-pip python3-venv

# Install system dependencies
sudo apt install python3-dev python3-numpy python3-scipy

# Install project dependencies
pip3 install -r requirements.txt
```

---

### Linux (Fedora/RHEL)

```bash
# Install Python and pip
sudo dnf install python3 python3-pip

# Install dependencies
sudo dnf install python3-numpy python3-scipy python3-matplotlib

# Install project dependencies
pip3 install -r requirements.txt
```

---

### macOS

```bash
# Install Homebrew (if not installed)
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# Install Python
brew install python

# Install dependencies
pip3 install -r requirements.txt
```

---

## 🧪 Testing Installation

### Run Basic Tests

```bash
# Test suite
python run_tests.py

# Expected output:
# ============================================================
# LO SHU BALANCE ALGORITHM - COMPREHENSIVE TEST SUITE
# ============================================================
# ...
# [OK] All tests completed successfully!
```

### Test Individual Components

```bash
# Test Lo Shu matrix
python -c "from src.lo_shu_matrix import LoShuMatrix; m = LoShuMatrix(); print(m)"

# Test filter
python -c "from src.lo_shu_filter import LoShuBalanceFilter; f = LoShuBalanceFilter(); print('Filter created:', f)"

# Test metrics
python -c "from src.metrics import ImageMetrics; import numpy as np; img = np.random.randint(0, 255, (100, 100)); print('Entropy:', ImageMetrics.entropy(img))"
```

---

## ⚠️ Troubleshooting

### Common Issues

#### Issue 1: "ModuleNotFoundError: No module named 'numpy'"

**Solution:**
```bash
pip install numpy
# or
pip install -r requirements.txt
```

#### Issue 2: "Permission denied" when installing

**Solution:**
```bash
# Use --user flag
pip install --user -r requirements.txt

# Or use virtual environment
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows
pip install -r requirements.txt
```

#### Issue 3: "No module named 'src'"

**Solution:**
```bash
# Run from project root directory
cd lo_shu_algorithm
python run_tests.py

# Or add to PYTHONPATH
export PYTHONPATH="${PYTHONPATH}:/path/to/lo_shu_algorithm"
```

#### Issue 4: Slow performance

**Solution:**
```bash
# Install optimized numpy
pip uninstall numpy
pip install numpy --no-binary :all:

# Or use Intel distribution
pip install intelpython
```

#### Issue 5: Import errors on Windows

**Solution:**
```bash
# Reinstall with --force-reinstall
pip install --force-reinstall numpy scipy
```

---

## 📦 Dependencies Explained

| Package | Version | Purpose |
|---------|---------|---------|
| numpy | ≥1.20.0 | Array operations, mathematical functions |
| scipy | ≥1.7.0 | Scientific computing, statistics |
| Pillow | ≥8.0.0 | Image loading and saving |
| matplotlib | ≥3.4.0 | Visualization, plotting |

---

## 🔍 Verification Checklist

After installation, verify:

- [ ] Python 3.8+ is installed
- [ ] All dependencies are installed
- [ ] Basic tests pass
- [ ] Can import all modules
- [ ] Can run example code

---

## 📞 Getting Help

If you encounter issues:

1. Check this guide thoroughly
2. Search existing issues on GitHub
3. Create a new issue with:
   - Python version
   - Operating system
   - Error message
   - Steps to reproduce

**GitHub Issues:** https://github.com/YOUR_USERNAME/lo_shu_algorithm/issues

---

## 🔄 Updating

```bash
# Pull latest changes
git pull origin main

# Update dependencies
pip install -r requirements.txt --upgrade

# Run tests to verify
python run_tests.py
```

---

**Installation complete!** Proceed to [USAGE.md](USAGE.md) for usage examples.
