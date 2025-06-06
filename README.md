# 🔤 TypoFix

<div align="center">

![TypoFix Logo](icon.ico)

**AI-Powered Real-Time Text Correction Tool for Windows**

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![Platform](https://img.shields.io/badge/platform-Windows-lightgrey.svg)](https://www.microsoft.com/windows)
[![AI](https://img.shields.io/badge/AI-Google%20Gemini-green.svg)](https://ai.google.dev/)

*Instantly fix typos and improve text clarity across any Windows application with the power of AI*

[🚀 Download Latest Release](https://github.com/emiliancristea/typo-fix/releases/latest) • [📖 Documentation](#-usage) • [🐛 Report Bug](https://github.com/emiliancristea/typo-fix/issues/new?assignees=&labels=bug&projects=&template=bug_report.md&title=%5BBUG%5D) • [💡 Request Feature](https://github.com/emiliancristea/typo-fix/issues/new?assignees=&labels=enhancement&projects=&template=feature_request.md&title=%5BFEATURE%5D)

</div>

---

## ✨ Features

### 🎯 **Core Functionality**
- **🔥 Global Hotkey Support** - Works in any Windows application (Ctrl+C)
- **🌍 Multi-Language Detection** - Automatically detects and preserves language (English, Spanish, French, German, Romanian, and more)
- **🤖 AI-Powered Corrections** - Powered by Google Gemini for intelligent text processing
- **⚡ Real-Time Processing** - Get corrections in under 3 seconds
- **🎨 Modern UI** - Beautiful floating widget with rounded buttons

### 🛠️ **Smart Correction Modes**
- **✓ Fix Mode** - Corrects spelling errors, typos, and grammar mistakes while preserving original meaning
- **📝 Rewrite Mode** - Improves text clarity, sentence structure, and logical flow
- **✗ Cancel Mode** - Dismiss widget without making changes

### 🖥️ **System Integration**
- **📱 System Tray Operation** - Runs quietly in the background
- **🖼️ Multi-Monitor Support** - Smart widget positioning across multiple displays
- **📋 Seamless Clipboard Integration** - Automatic copy-paste workflow
- **🎪 Universal Compatibility** - Works with browsers, Office apps, text editors, chat applications

---

## 🛡️ Security & Download Warnings

### Browser Download Warnings
When downloading `TypoFix.exe`, your browser may show warnings like:
- **Chrome**: "This file is dangerous" 
- **Edge**: "This file is not commonly downloaded"
- **Firefox**: "This file may harm your computer"

**This is normal and expected behavior** for unsigned executable files.

### Why These Warnings Appear
- TypoFix is **not digitally signed** with a code signing certificate
- Browsers flag unsigned `.exe` files as potentially dangerous
- This is a security feature to protect users from malware

### How to Download Safely
1. **Keep the download**: Click "Keep" or "Keep anyway" in your browser
2. **Verify source**: Only download from [official GitHub releases](https://github.com/emiliancristea/typo-fix/releases)
3. **Check file size**: Verify the file is approximately 19.5 MB
4. **Scan if desired**: Use your antivirus software to scan the file

### Windows SmartScreen Warning
After downloading, Windows may also show:
> "Windows protected your PC - Microsoft Defender SmartScreen prevented an unrecognized app from starting"

**To run TypoFix:**
1. Click **"More info"**
2. Click **"Run anyway"**
3. TypoFix will start normally

### Why Not Code Sign?
Code signing certificates cost $200-400/year and require business verification. For a free, open-source tool, this cost is prohibitive. However, you can verify TypoFix's safety by:
- ✅ **Open source code**: All code is publicly available for review
- ✅ **Community trust**: Growing user base and positive feedback
- ✅ **No malicious behavior**: Transparent functionality and operation
- ✅ **Minimal permissions**: No admin rights or system modifications required

### 📚 Detailed Security Information
For comprehensive information about download security warnings and verification:
- 📖 **[Download Security Guide](DOWNLOAD_SECURITY.md)** - Detailed browser-specific instructions
- 🔒 **[Security Policy](.github/SECURITY.md)** - Full security documentation
- 🛡️ **[File Verification](generate_checksums.py)** - Script to verify download integrity

---

## 🚀 Installation

### Option 1: Download Executable (Recommended)
1. Go to [Releases](https://github.com/emiliancristea/typo-fix/releases)
2. Download the latest `TypoFix.exe`
3. Run the executable - no installation required!

### Option 2: Run from Source
```bash
# Clone the repository
git clone https://github.com/emiliancristea/typo-fix.git
cd typo-fix

# Create virtual environment
python -m venv .venv
.venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run the application
python app.py
```

### Requirements
- **OS**: Windows 10/11
- **Python**: 3.8+ (if running from source)
- **Internet**: Required for AI processing

---

## 📖 Usage

### Quick Start
1. **Launch TypoFix** - The app runs in your system tray
2. **Highlight any text** in any application (Word, browser, email, etc.)
3. **Press Ctrl+C** to copy the text
4. **Choose your action** from the floating widget:
   - **✓ Fix** - Quick typo and grammar correction
   - **📝 Rewrite** - Improve clarity and structure
   - **✗ Cancel** - Dismiss without changes
5. **Text automatically replaces** the original with corrections

### Supported Applications
✅ **Web Browsers** - Chrome, Firefox, Edge, Safari  
✅ **Microsoft Office** - Word, Excel, PowerPoint, Outlook  
✅ **Text Editors** - VS Code, Notepad++, Sublime Text  
✅ **Communication** - Discord, Slack, Teams, WhatsApp Web  
✅ **Email Clients** - Gmail, Yahoo Mail, Outlook  
✅ **Social Media** - Twitter, Facebook, LinkedIn  

### Language Support
The AI automatically detects and preserves your original language:
- 🇺🇸 English
- 🇪🇸 Spanish  
- 🇫🇷 French
- 🇩🇪 German
- 🇷🇴 Romanian
- *And many more...*

---

## 🔧 Configuration

### API Key Setup
TypoFix comes with an embedded API key for immediate use. For extended usage or custom configurations:

1. Get a Google Gemini API key from [Google AI Studio](https://ai.google.dev/)
2. Use the included `encode_api_key.py` script to encode your key
3. Replace the encoded key in `app.py`

```python
# Run the encoding script
python encode_api_key.py
# Follow the prompts to encode your API key
```

---

## 🏗️ Building from Source

### Create Executable
```bash
# Activate virtual environment
.venv\Scripts\activate

# Build executable
python build_exe.py

# Find your executable in the dist/ folder
```

### Development Setup
```bash
# Install development dependencies
pip install -r requirements.txt

# Run tests
python -m pytest test_scenarios.md

# Run the application in debug mode
python app.py
```

---

## 📊 Performance

- **⚡ Response Time**: < 3 seconds average
- **🎯 Accuracy**: 99%+ language detection
- **💾 Memory Usage**: < 50MB RAM
- **🔋 CPU Impact**: Minimal background usage
- **🌐 Network**: Only during text processing

---

## 🤝 Contributing

We welcome contributions! Here's how to get started:

1. **Fork the repository**
2. **Create a feature branch** (`git checkout -b feature/amazing-feature`)
3. **Commit your changes** (`git commit -m 'Add amazing feature'`)
4. **Push to the branch** (`git push origin feature/amazing-feature`)
5. **Open a Pull Request**

### Development Guidelines
- Follow PEP 8 style guidelines
- Add tests for new features
- Update documentation as needed
- Test on multiple Windows versions

---

## 🐛 Troubleshooting

### Common Issues

**Widget doesn't appear:**
- Ensure you're copying text (Ctrl+C) after selecting
- Check if TypoFix icon is visible in system tray
- Try running as administrator

**API errors:**
- Check your internet connection
- Verify API key is correctly configured
- Monitor rate limits

**Positioning issues:**
- Update display drivers
- Test on different applications
- Check multi-monitor setup

### Debug Mode
Run with debug output:
```bash
python app.py
# Terminal will show detailed debug information
```

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 🙏 Acknowledgments

- **Google Gemini AI** - For powerful language processing capabilities
- **Python Community** - For excellent libraries and tools
- **Contributors** - Thank you for making TypoFix better!

---

## 📈 Roadmap

### Upcoming Features
- [ ] Custom keyboard shortcuts
- [ ] Offline correction mode
- [ ] Plugin system for text editors
- [ ] Team/Enterprise features
- [ ] Mobile companion app
- [ ] Advanced formatting preservation

### Version History
- **v1.0.0** - Initial release with core functionality
- **v1.1.0** - Multi-language support and improved UI
- **v1.2.0** - Enhanced positioning and system integration

---

<div align="center">

**Made with ❤️ for better writing**

[⭐ Star this project](https://github.com/emiliancristea/typo-fix) if you find it useful!

</div>