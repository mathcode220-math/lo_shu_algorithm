# Contributing to Lo Shu Balance Algorithm

Thank you for your interest in contributing to this project! This document provides guidelines for contributing.

## 📋 Table of Contents

- [Code of Conduct](#code-of-conduct)
- [Getting Started](#getting-started)
- [Development Setup](#development-setup)
- [Pull Request Guidelines](#pull-request-guidelines)
- [Coding Standards](#coding-standards)
- [Testing](#testing)

---

## 🎯 Code of Conduct

- Be respectful and inclusive
- Provide constructive feedback
- Accept constructive criticism
- Focus on what's best for the community

---

## 🚀 Getting Started

### 1. Fork the Repository

```bash
# Click "Fork" on GitHub, then clone your fork
git clone https://github.com/YOUR_USERNAME/lo_shu_algorithm.git
cd lo_shu_algorithm
```

### 2. Create a Branch

```bash
# Create a feature branch
git checkout -b feature/your-feature-name

# Or for bug fixes
git checkout -b fix/issue-123
```

---

## 💻 Development Setup

### Install Development Dependencies

```bash
# Install base requirements
pip install -r requirements.txt

# Install development tools (optional)
pip install pytest pytest-cov black flake8 mypy
```

### Set Up Pre-commit Hooks (Optional)

```bash
# Install pre-commit
pip install pre-commit

# Set up hooks
pre-commit install
```

---

## 📝 Pull Request Guidelines

### Before Submitting

- [ ] Code follows the style guide
- [ ] Tests pass locally
- [ ] Documentation is updated
- [ ] Changes are well-tested

### PR Title Format

```
type: brief description

Examples:
- feat: add RGB image support
- fix: correct edge preservation calculation
- docs: update installation instructions
- test: add unit tests for metrics
```

### PR Description Template

```markdown
## Description
Brief description of changes

## Related Issue
Fixes #123

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Documentation update
- [ ] Performance improvement

## Testing
Describe tests performed

## Checklist
- [ ] Code follows style guidelines
- [ ] Tests pass
- [ ] Documentation updated
```

---

## 📐 Coding Standards

### Python Style

Follow [PEP 8](https://pep8.org/) guidelines:

```python
# Use descriptive variable names
pixel_value = 255  # Good
pv = 255  # Bad

# Use type hints
def process_image(image: np.ndarray) -> np.ndarray:
    """Process image and return result."""
    pass

# Use docstrings
class LoShuFilter:
    """Lo Shu Balance Algorithm implementation."""
    
    def apply(self, image: np.ndarray) -> np.ndarray:
        """
        Apply Lo Shu filter to image.
        
        Args:
            image: Input image array
            
        Returns:
            Filtered image array
        """
        pass
```

### Code Organization

```
src/
├── module.py          # Implementation
├── test_module.py     # Tests
└── docs/             # Documentation
```

---

## 🧪 Testing

### Running Tests

```bash
# Run all tests
python run_tests.py

# Run academic tests
python -m tests.academic_tests

# Run specific test
python -m pytest tests/test_suite.py -v
```

### Writing Tests

```python
def test_lo_shu_matrix_properties():
    """Test Lo Shu matrix mathematical properties."""
    lo_shu = LoShuMatrix()
    
    # Test magic constant
    assert lo_shu.verify_magic_constant()
    
    # Test center value
    assert lo_shu.center_value == 5
    
    # Test diagonal pairs
    for i in range(3):
        for j in range(3):
            if (i, j) != (1, 1):
                val = lo_shu.get_weight(i, j)
                opp_val = lo_shu.get_weight(2-i, 2-j)
                assert val + opp_val == 10
```

### Code Coverage

```bash
# Check coverage
pytest --cov=src --cov-report=html

# View HTML report
open htmlcov/index.html
```

---

## 📚 Documentation

### Updating Documentation

- Update README.md for user-facing changes
- Update docstrings for API changes
- Add examples for new features
- Update CHANGELOG.md

### Documentation Standards

```python
def function(param1: int, param2: str) -> bool:
    """
    One-line description.
    
    Extended description if needed.
    
    Args:
        param1: Description of param1
        param2: Description of param2
        
    Returns:
        Description of return value
        
    Raises:
        ValueError: When parameter is invalid
        
    Example:
        >>> function(1, "test")
        True
    """
    pass
```

---

## 🔍 Code Review

### Reviewers Will Check

- Code quality and style
- Test coverage
- Documentation completeness
- Performance implications
- Security considerations

### Responding to Reviews

- Be responsive and timely
- Address all comments
- Ask for clarification if needed
- Make requested changes promptly

---

## 📧 Questions?

Open an issue or contact the maintainers:
- Email: your.email@example.com
- GitHub Issues: https://github.com/YOUR_USERNAME/lo_shu_algorithm/issues

---

**Thank you for contributing!** 🎉
