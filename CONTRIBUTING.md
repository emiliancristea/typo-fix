# Contributing to TypoFix

Thank you for your interest in contributing to TypoFix! This document provides guidelines and information for contributors.

## 🤝 How to Contribute

### Reporting Bugs

Before creating bug reports, please check the [existing issues](https://github.com/emiliancristea/typo-fix/issues) to avoid duplicates.

**When submitting a bug report, please include:**
- Detailed description of the issue
- Steps to reproduce the behavior
- Expected vs. actual behavior
- Screenshots or screen recordings if applicable
- System information:
  - Windows version
  - Python version (if running from source)
  - Application where the issue occurred

### Suggesting Features

We welcome feature suggestions! Please:
- Check existing feature requests first
- Provide clear description of the proposed feature
- Explain the use case and benefits
- Consider implementation complexity

### Pull Requests

1. **Fork the repository**
2. **Create a feature branch**: `git checkout -b feature/your-feature-name`
3. **Make your changes** following our coding standards
4. **Test thoroughly** across different applications
5. **Update documentation** if needed
6. **Commit with clear messages**: `git commit -m "Add feature: description"`
7. **Push to your fork**: `git push origin feature/your-feature-name`
8. **Create a Pull Request**

## 🛠️ Development Setup

### Prerequisites
- Python 3.8+
- Windows 10/11 (for testing Windows-specific features)
- Git

### Setup Instructions
```bash
# Clone your fork
git clone https://github.com/emiliancristea/typo-fix.git
cd typo-fix

# Create virtual environment
python -m venv .venv
.venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Install development dependencies
pip install pytest black flake8 mypy

# Run the application
python app.py
```

### Testing
```bash
# Run basic functionality tests
python -m pytest test_scenarios.md

# Test across different applications manually
# See test_scenarios.md for comprehensive test cases

# Build and test executable
python build_exe.py
```

## 📝 Coding Standards

### Python Style
- Follow [PEP 8](https://pep8.org/) style guidelines
- Use [Black](https://black.readthedocs.io/) for code formatting
- Maximum line length: 88 characters
- Use type hints where appropriate

### Code Formatting
```bash
# Format code with Black
black app.py

# Check with flake8
flake8 app.py

# Type checking with mypy
mypy app.py
```

### Documentation
- Add docstrings for all public functions and classes
- Update README.md for user-facing changes
- Update CHANGELOG.md for all changes
- Include inline comments for complex logic

### Example Code Style
```python
def fix_text_with_ai(text: str, language: str) -> Optional[str]:
    """
    Fix typos and grammar errors in the provided text.
    
    Args:
        text: The text to be corrected
        language: The detected language of the text
        
    Returns:
        Corrected text or None if processing fails
    """
    if not text or not text.strip():
        return None
        
    # Process with AI API
    corrected = call_gemini_api(text, language)
    return corrected
```

## 🧪 Testing Guidelines

### Manual Testing
- Test in multiple applications (browsers, Office, text editors)
- Test with different languages
- Verify widget positioning on different screen configurations
- Test both Fix and Rewrite modes

### Test Cases
When adding features, include test cases for:
- Normal usage scenarios
- Edge cases (very short/long text, special characters)
- Error conditions (network issues, API failures)
- Different Windows versions and configurations

### Performance Testing
- Monitor memory usage during extended use
- Test API response times
- Verify system resource impact

## 🔍 Code Review Process

### What We Look For
- **Functionality**: Does the code work as intended?
- **Quality**: Is the code well-written and maintainable?
- **Testing**: Are there appropriate tests?
- **Documentation**: Is the code properly documented?
- **Performance**: Does it maintain good performance?
- **Compatibility**: Does it work across different Windows versions?

### Review Checklist
- [ ] Code follows style guidelines
- [ ] Changes are tested manually
- [ ] Documentation is updated
- [ ] No breaking changes (or properly documented)
- [ ] Performance impact is minimal
- [ ] Error handling is appropriate

## 📚 Project Structure

```
typo-fix/
├── app.py                  # Main application code
├── build_exe.py           # Executable building script
├── encode_api_key.py      # API key encoding utility
├── requirements.txt       # Python dependencies
├── test_scenarios.md      # Testing documentation
├── README.md             # Project documentation
├── CHANGELOG.md          # Version history
├── CONTRIBUTING.md       # This file
├── LICENSE               # MIT license
├── .gitignore           # Git ignore rules
└── icon.ico             # Application icon
```

## 🎯 Areas for Contribution

### High Priority
- [ ] Custom keyboard shortcuts
- [ ] Offline correction mode
- [ ] Performance optimizations
- [ ] Additional language support
- [ ] UI/UX improvements

### Medium Priority
- [ ] Plugin system for text editors
- [ ] Advanced formatting preservation
- [ ] Configuration options
- [ ] Accessibility improvements

### Low Priority
- [ ] Team/Enterprise features
- [ ] Mobile companion app
- [ ] Integration with cloud services

## 📧 Getting Help

- **Questions**: Open a [discussion](https://github.com/emiliancristea/typo-fix/discussions)
- **Bugs**: Create an [issue](https://github.com/emiliancristea/typo-fix/issues)
- **Features**: Open a feature request issue

## 📄 License

By contributing to TypoFix, you agree that your contributions will be licensed under the MIT License.

## 🙏 Recognition

Contributors will be:
- Listed in the README.md acknowledgments
- Mentioned in release notes for significant contributions
- Added to the repository contributors list

Thank you for helping make TypoFix better! 🎉 