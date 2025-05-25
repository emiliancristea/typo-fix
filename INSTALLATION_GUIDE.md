# 📥 TypoFix Installation Guide

## 🚀 Quick Start (2 Minutes)

### Step 1: Download
1. Go to [GitHub Releases](https://github.com/emiliancristea/typo-fix/releases/latest)
2. Download `TypoFix.exe` (19.5 MB)
3. Save it anywhere on your computer

### Step 2: Run
1. **Double-click** `TypoFix.exe` to start
2. Windows may show a security warning - click **"More info"** → **"Run anyway"**
3. Look for the green **"T"** icon in your system tray (bottom-right corner)

### Step 3: Use
1. **Highlight any text** in any application (browser, Word, email, etc.)
2. **Press Ctrl+C** to copy the text
3. **Choose your action** from the popup widget:
   - **✓ Fix** - Correct typos and grammar
   - **📝 Rewrite** - Improve clarity and flow
   - **✗ Cancel** - No changes

**That's it! TypoFix is now improving your writing across all applications! 🎉**

---

## 🛠️ System Requirements

### ✅ **Compatible Systems**
- Windows 10 (any version)
- Windows 11 (any version)
- Both 32-bit and 64-bit systems

### 📋 **Requirements**
- **Internet connection** (for AI processing)
- **50 MB RAM** (minimal usage)
- **20 MB disk space** (for the executable)
- **No additional software** needed

### ❌ **Not Required**
- ❌ Administrator privileges
- ❌ Python installation
- ❌ Additional downloads
- ❌ Registration or account creation

---

## 🎯 Detailed Setup

### 🔽 **Download Options**

#### Option 1: Direct Download (Recommended)
1. Visit: https://github.com/emiliancristea/typo-fix/releases/latest
2. Click on `TypoFix.exe` under "Assets"
3. File will download to your Downloads folder

#### Option 2: Clone Repository
```bash
git clone https://github.com/emiliancristea/typo-fix.git
cd typo-fix
# Find executable in releases or build from source
```

### ⚠️ **Browser Download Warnings**

**Important**: Your browser will likely show security warnings when downloading `TypoFix.exe`.

#### Chrome Browser Warning
Chrome may show: **"This file is dangerous"** with options to delete or keep the file.

**Solution:**
1. Click the **"Keep"** button (may be hidden in a dropdown)
2. If you see "Delete from history", click the **"^"** arrow to see more options
3. Select **"Keep anyway"** or **"Keep download"**

#### Edge Browser Warning  
Edge may show: **"This file is not commonly downloaded and may be dangerous"**

**Solution:**
1. Click **"Keep"**
2. If prompted again, click **"Keep anyway"**

#### Firefox Browser Warning
Firefox may show: **"This file may harm your computer"**

**Solution:**
1. Click **"Keep"** or **"Save anyway"**
2. Allow the download to complete

#### Why These Warnings Occur
- TypoFix is **not digitally signed** (costs $200-400/year)
- Browsers protect users by flagging unsigned executables
- **This is completely normal** for open-source software
- The file is **safe** - all code is publicly available for review

### 🏃‍♂️ **First Run**

#### Windows Security Warning
When you first run TypoFix, Windows may show:
> "Windows protected your PC - Microsoft Defender SmartScreen prevented an unrecognized app from starting"

**This is normal for new applications.** To proceed:
1. Click **"More info"**
2. Click **"Run anyway"**
3. TypoFix will start normally

#### System Tray Icon
After starting, TypoFix runs in the background:
- Look for a **green "T" icon** in your system tray
- If you don't see it, click the **"^"** arrow to show hidden icons
- Right-click the icon for options

### 🧪 **Testing TypoFix**

Try these quick tests to ensure everything works:

#### Test 1: Basic Correction
1. Open any text app (Notepad, Word, browser)
2. Type: `Ths is a tets with erors`
3. Select the text and press **Ctrl+C**
4. Click **✓ Fix** in the popup
5. Should paste: `This is a test with errors`

#### Test 2: Text Improvement
1. Type: `me want go store buy thing`
2. Select and press **Ctrl+C**
3. Click **📝 Rewrite**
4. Should improve to: `I want to go to the store to buy something`

#### Test 3: Different Applications
Test in multiple apps:
- Web browser (Chrome, Firefox, Edge)
- Microsoft Word or Google Docs
- Email client (Outlook, Gmail)
- Text editor (Notepad, VS Code)
- Chat app (Discord, Slack)

---

## ⚙️ Configuration (Optional)

TypoFix works immediately with no configuration needed. However, you can customize:

### 🔑 **API Key (For Heavy Usage)**
The app includes an embedded API key, but for unlimited usage:
1. Get a free Google Gemini API key at https://ai.google.dev/
2. Use the `encode_api_key.py` script to encode your key
3. Edit `app.py` to replace the embedded key

### 📍 **Portable Installation**
TypoFix is completely portable:
- **USB Drive**: Copy `TypoFix.exe` to a USB drive
- **Network Share**: Run from shared folders
- **Multiple Computers**: Same executable works everywhere
- **No Registry**: All settings stored with the executable

---

## 🔧 Troubleshooting

### ❓ **Common Issues**

#### Widget Doesn't Appear
- ✅ Ensure TypoFix is running (check system tray)
- ✅ Try selecting text again and pressing Ctrl+C
- ✅ Check if your internet connection is active
- ✅ Try running as administrator

#### Text Doesn't Get Corrected
- ✅ Make sure you selected text before pressing Ctrl+C
- ✅ Check that the widget appeared and you clicked a button
- ✅ Verify the original app allows text replacement
- ✅ Try in a different application (like Notepad)

#### Performance Issues
- ✅ Close unnecessary applications to free memory
- ✅ Check your internet connection speed
- ✅ Try with shorter text snippets first

#### Antivirus Warnings
- ✅ Add TypoFix.exe to your antivirus exclusions
- ✅ Download only from official GitHub releases
- ✅ Verify file integrity if provided

### 📧 **Getting Help**
If you encounter issues:
1. **Check Documentation**: [README.md](https://github.com/emiliancristea/typo-fix#readme)
2. **Search Issues**: [GitHub Issues](https://github.com/emiliancristea/typo-fix/issues)
3. **Report Bug**: [Bug Report Template](https://github.com/emiliancristea/typo-fix/issues/new?template=bug_report.md)
4. **Ask Questions**: [Discussions](https://github.com/emiliancristea/typo-fix/discussions)

---

## 🎉 **You're All Set!**

TypoFix is now ready to improve your writing across all applications:

### **What TypoFix Does:**
- ✅ Corrects typos and spelling errors
- ✅ Fixes grammar mistakes
- ✅ Improves sentence structure
- ✅ Preserves your original language
- ✅ Works in any Windows application

### **What TypoFix Doesn't Do:**
- ❌ Translate between languages
- ❌ Store or log your text
- ❌ Require internet for basic functionality
- ❌ Interfere with other applications

**Enjoy better writing with TypoFix! 🚀✨**

---

*Having trouble? Check our [FAQ](https://github.com/emiliancristea/typo-fix#-troubleshooting) or [report an issue](https://github.com/emiliancristea/typo-fix/issues/new).* 