#!/usr/bin/env python3
"""
Build script for TypoFix - Creates a standalone executable
"""

import os
import sys
import subprocess
import shutil
from pathlib import Path
import hashlib
import datetime

def create_spec_file():
    """Create PyInstaller spec file with proper configuration"""
    
    spec_content = '''
# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

a = Analysis(
    ['app.py'],
    pathex=[],
    binaries=[],
    datas=[
        # No external data files - everything embedded
    ],
    hiddenimports=[
        'pystray',
        'pystray._win32',
        'PIL',
        'PIL.Image',
        'PIL.ImageDraw',
        'PIL.ImageFont',
        'pynput.keyboard._win32',
        'pynput.mouse._win32', 
        'win32gui',
        'win32con',
        'win32api',
        'win32process',
        'requests',
        'pyperclip',
        'pyautogui',
        'screeninfo',
        'tkinter',
        'tkinter.ttk',
        'base64',
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[
        'matplotlib',
        'numpy', 
        'scipy',
        'pandas',
        'cv2',
        'tensorflow',
        'torch',
        'jupyter',
        'IPython',
        'notebook',
        'plotly',
        'bokeh',
        'seaborn',
    ],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='TypoFix',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,  # No console window
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon='icon.ico',
    version='version_info.txt',
)
'''
    
    with open('TypoFix.spec', 'w') as f:
        f.write(spec_content.strip())
    
    print("✅ Created TypoFix.spec file")

def create_version_info():
    """Create version information file"""
    
    version_info = '''
# UTF-8
#
# For more details about fixed file info 'ffi' see:
# http://msdn.microsoft.com/en-us/library/ms646997.aspx
VSVersionInfo(
  ffi=FixedFileInfo(
    filevers=(1,3,0,0),
    prodvers=(1,3,0,0),
    mask=0x3f,
    flags=0x0,
    OS=0x40004,
    fileType=0x1,
    subtype=0x0,
    date=(0, 0)
    ),
  kids=[
    StringFileInfo(
      [
      StringTable(
        u'040904B0',
        [StringStruct(u'CompanyName', u'TypoFix'),
        StringStruct(u'FileDescription', u'AI-Powered Typo Correction Tool'),
        StringStruct(u'FileVersion', u'1.3.0.0'),
        StringStruct(u'InternalName', u'TypoFix'),
        StringStruct(u'LegalCopyright', u'Copyright (C) 2025'),
        StringStruct(u'OriginalFilename', u'TypoFix.exe'),
        StringStruct(u'ProductName', u'TypoFix - AI Typo Corrector'),
        StringStruct(u'ProductVersion', u'1.3.0.0')])
      ]), 
    VarFileInfo([VarStruct(u'Translation', [1033, 1200])])
  ]
)
'''
    
    with open('version_info.txt', 'w', encoding='utf-8') as f:
        f.write(version_info.strip())
    
    print("✅ Created version_info.txt")

def create_icon():
    """Create a simple icon for the application"""
    
    try:
        # Try to create icon with PIL
        from PIL import Image, ImageDraw, ImageFont
        
        # Create a simple icon
        size = (64, 64)
        img = Image.new('RGBA', size, (76, 175, 80, 255))  # Green background
        draw = ImageDraw.Draw(img)
        
        # Draw a simple "T" for TypoFix
        try:
            font = ImageFont.truetype("arial.ttf", 40)
        except:
            font = ImageFont.load_default()
        
        # Calculate text position to center it
        text = "T"
        bbox = draw.textbbox((0, 0), text, font=font)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]
        x = (size[0] - text_width) // 2
        y = (size[1] - text_height) // 2
        
        # Draw white "T"
        draw.text((x, y), text, fill=(255, 255, 255, 255), font=font)
        
        # Save as ICO
        if hasattr(Image, 'Resampling'):
            resample = Image.Resampling.LANCZOS
        else:
            resample = Image.LANCZOS
        
        # Create multiple sizes for ICO
        sizes = [(16, 16), (32, 32), (48, 48), (64, 64)]
        images = []
        for ico_size in sizes:
            resized = img.resize(ico_size, resample)
            images.append(resized)
        
        images[0].save('icon.ico', format='ICO', sizes=[s for s in sizes])
        print("✅ Created icon.ico")
        
    except ImportError:
        # Create a placeholder file for PyInstaller
        print("⚠️ PIL not available, creating placeholder icon")
        with open('icon.ico', 'wb') as f:
            # Write a minimal ICO file header (will be ignored by PyInstaller if invalid)
            f.write(b'\x00\x00\x01\x00')  # ICO header
        print("✅ Created placeholder icon.ico")
        
    except Exception as e:
        print(f"⚠️ Could not create icon: {e}")
        # Create empty file so PyInstaller doesn't fail
        with open('icon.ico', 'w') as f:
            f.write('')
        print("✅ Created empty icon.ico")

def create_installer_script():
    """Create a simple installer script"""
    
    installer_content = '''
@echo off
echo ===================================
echo     TypoFix Installation Script
echo ===================================
echo.

REM Check if running as administrator
net session >nul 2>&1
if %errorLevel% == 0 (
    echo Running as administrator...
) else (
    echo This installer requires administrator privileges.
    echo Please right-click and "Run as administrator"
    pause
    exit /b 1
)

echo Installing TypoFix...

REM Create installation directory
set INSTALL_DIR="%ProgramFiles%\\TypoFix"
if not exist %INSTALL_DIR% mkdir %INSTALL_DIR%

REM Copy files
copy "TypoFix.exe" %INSTALL_DIR%
copy "README.txt" %INSTALL_DIR% 2>nul

REM Create desktop shortcut
set DESKTOP="%USERPROFILE%\\Desktop"
echo Creating desktop shortcut...
powershell "$WshShell = New-Object -comObject WScript.Shell; $Shortcut = $WshShell.CreateShortcut('%DESKTOP%\\TypoFix.lnk'); $Shortcut.TargetPath = '%INSTALL_DIR%\\TypoFix.exe'; $Shortcut.IconLocation = '%INSTALL_DIR%\\TypoFix.exe'; $Shortcut.Description = 'AI-Powered Typo Correction Tool'; $Shortcut.Save()"

REM Create start menu entry
set STARTMENU="%ProgramData%\\Microsoft\\Windows\\Start Menu\\Programs"
powershell "$WshShell = New-Object -comObject WScript.Shell; $Shortcut = $WshShell.CreateShortcut('%STARTMENU%\\TypoFix.lnk'); $Shortcut.TargetPath = '%INSTALL_DIR%\\TypoFix.exe'; $Shortcut.IconLocation = '%INSTALL_DIR%\\TypoFix.exe'; $Shortcut.Description = 'AI-Powered Typo Correction Tool'; $Shortcut.Save()"

echo.
echo ===================================
echo    Installation Complete!
echo ===================================
echo.
echo TypoFix has been installed to: %INSTALL_DIR%
echo Desktop shortcut created.
echo Start menu entry created.
echo.
echo How to Use:
echo 1. TypoFix is now running in the background
echo 2. Highlight any text in any application
echo 3. Press SHIFT+C to activate TypoFix
echo 4. Choose Fix or Rewrite from the widget
echo.
echo Press any key to finish...
pause >nul
'''
    
    with open('install.bat', 'w') as f:
        f.write(installer_content.strip())
    
    print("✅ Created install.bat")

def create_readme():
    """Create README for distribution"""
    
    readme_content = '''
# TypoFix - AI-Powered Typo Correction Tool

## What is TypoFix?

TypoFix is an intelligent desktop application that automatically detects and corrects typos in any text you select. Simply highlight text anywhere on your computer, press SHIFT+C, and TypoFix will offer to fix typos or rewrite text for better clarity using advanced AI technology.

## Features

* Global Hotkey Detection: Works in any application - browsers, documents, emails, chat apps
* AI-Powered Corrections: Uses Google's Gemini AI for intelligent typo detection and correction
* Smart Text Processing: Fix typos or rewrite for better clarity and logic
* Smart Positioning: Widget appears near your selected text
* Auto-Close Timer: Widget automatically closes after 4 seconds of inactivity
* Instant Application: One-click to apply changes and paste corrected text
* Beautiful UI: Modern, transparent floating buttons with three action options
* Privacy-Focused: Text is only sent to AI when you choose to process it

## Quick Start

1. Install: Run the installer or place TypoFix.exe in your desired location
2. Run: Launch TypoFix.exe (it runs in the background)
3. Use: Highlight text anywhere, press SHIFT+C, choose "Fix" or "Rewrite"!

## How to Use

1. Highlight text in any application (browser, Word, email, etc.)
2. Press SHIFT+C to activate TypoFix
3. TypoFix widget appears with three buttons near your selection:
   • ✓ Fix - Corrects typos and spelling errors
   • 📝 Rewrite - Improves clarity and logical flow
   • ✗ Cancel - Dismiss without changes
4. Click your desired action to apply changes automatically

## System Requirements

- Windows 10 or later
- Internet connection (for AI corrections)

## Troubleshooting

Widget doesn't appear?
- Make sure TypoFix.exe is running (check system tray)
- Try running as administrator
- Check if antivirus is blocking the app

API errors?
- Check your internet connection
- Ensure you have Gemini API quota available

Can't install?
- Run install.bat as administrator
- Or manually copy TypoFix.exe to any folder and run it

## Support

For issues or questions, please check the project documentation or contact support.

## Version 1.3.0

Updated release with simplified Shift+C hotkey and embedded API key.
'''
    
    with open('README.txt', 'w', encoding='utf-8') as f:
        f.write(readme_content.strip())
    
    print("✅ Created README.txt")

def build_executable():
    """Build the executable using PyInstaller"""
    
    print("\n🔨 Building standalone executable...")
    
    try:
        # Clean previous builds
        if os.path.exists('dist'):
            shutil.rmtree('dist')
        if os.path.exists('build'):
            shutil.rmtree('build')
        
        # Build with PyInstaller
        cmd = [
            'pyinstaller',
            '--clean',
            '--noconfirm',
            'TypoFix.spec'
        ]
        
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        if result.returncode == 0:
            print("✅ Standalone executable built successfully!")
            print(f"📁 Output location: {os.path.abspath('dist')}")
            
            # Check if the executable exists
            exe_path = os.path.join('dist', 'TypoFix.exe')
            if os.path.exists(exe_path):
                exe_size = os.path.getsize(exe_path) / (1024 * 1024)
                print(f"📄 Executable: TypoFix.exe ({exe_size:.1f} MB)")
                print("✅ Single-file executable created - no external dependencies needed!")
                
                # Generate checksums for verification
                generate_checksums(exe_path)
            
            return True
        else:
            print("❌ Build failed!")
            print(f"Error: {result.stderr}")
            return False
            
    except Exception as e:
        print(f"❌ Build error: {e}")
        return False

def generate_checksums(exe_path):
    """Generate checksums for the built executable"""
    
    print("\n🔒 Generating checksums for verification...")
    
    try:
        # Calculate hashes
        sha256_hash = hashlib.sha256()
        md5_hash = hashlib.md5()
        
        with open(exe_path, "rb") as f:
            for chunk in iter(lambda: f.read(4096), b""):
                sha256_hash.update(chunk)
                md5_hash.update(chunk)
        
        sha256 = sha256_hash.hexdigest()
        md5 = md5_hash.hexdigest()
        
        # Get file info
        file_size = os.path.getsize(exe_path)
        file_size_mb = file_size / (1024 * 1024)
        build_date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        # Create checksum file content
        checksum_content = f"""# TypoFix v1.3.0 - File Verification

## Build Information
- **Filename**: TypoFix.exe
- **File Size**: {file_size_mb:.1f} MB ({file_size:,} bytes)
- **Build Date**: {build_date}
- **Build Machine**: {os.environ.get('COMPUTERNAME', 'Unknown')}

## File Checksums

### SHA256
```
{sha256}
```

### MD5
```
{md5}
```

## Verification Instructions

### Windows PowerShell
```powershell
# Verify SHA256
Get-FileHash TypoFix.exe -Algorithm SHA256

# Verify MD5  
Get-FileHash TypoFix.exe -Algorithm MD5
```

### Command Prompt
```cmd
# Verify SHA256
certutil -hashfile TypoFix.exe SHA256

# Verify MD5
certutil -hashfile TypoFix.exe MD5
```

### Expected Results
The calculated hashes should **exactly match** the values above.

❌ **If hashes don't match:**
- File may be corrupted during download
- File may have been modified/tampered with  
- Downloaded from unofficial source

✅ **Solution:** Re-download from official GitHub releases only.

## Release Notes

This build includes:
- ✅ Embedded Google Gemini API key for immediate use
- ✅ Complete standalone executable (no dependencies)
- ✅ Global hotkey support (Shift+C)
- ✅ Multi-language text correction
- ✅ Smart widget positioning
- ✅ System tray integration
- ✅ Modern glass-morphism UI

For full changelog, see: https://github.com/emiliancristea/typo-fix/releases
"""
        
        # Save checksum file in dist directory
        checksum_file = os.path.join('dist', 'TypoFix_checksums.txt')
        with open(checksum_file, 'w', encoding='utf-8') as f:
            f.write(checksum_content)
        
        # Also save in root for releases
        root_checksum_file = 'TypoFix_checksums.txt'
        with open(root_checksum_file, 'w', encoding='utf-8') as f:
            f.write(checksum_content)
        
        print("✅ Checksums generated successfully!")
        print(f"📄 Checksum file: {checksum_file}")
        print(f"📄 Release checksum: {root_checksum_file}")
        print("\n🔒 File verification hashes:")
        print(f"   SHA256: {sha256}")
        print(f"   MD5:    {md5}")
        
    except Exception as e:
        print(f"❌ Failed to generate checksums: {e}")

def main():
    """Main build process"""
    
    print("🚀 TypoFix Standalone Executable Builder")
    print("=" * 45)
    
    # Create all necessary files
    create_spec_file()
    create_version_info()
    create_icon()
    
    print("\n📦 Building standalone executable...")
    
    if build_executable():
        print("\n🎉 Build completed successfully!")
        print("\n📋 Standalone executable created:")
        print("   📁 dist/TypoFix.exe - Complete application in a single file")
        print("\n✨ Features of this executable:")
        print("   • No external dependencies required")
        print("   • SHIFT+C hotkey activation")
        print("   • Auto-close timer (4 seconds of inactivity)")
        print("   • API key embedded - no setup required")
        print("   • Completely portable")
        print("   • Three-button widget (Fix/Rewrite/Cancel)")
        print("\n💡 Distribution:")
        print("   • Simply share dist/TypoFix.exe")
        print("   • Users just run the .exe file")
        print("   • Highlight text → press SHIFT+C → choose action")
        print("   • No installation required")
        
    else:
        print("\n❌ Build failed. Check the error messages above.")

if __name__ == "__main__":
    main() 