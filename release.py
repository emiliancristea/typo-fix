#!/usr/bin/env python3
"""
Release script for TypoFix - Creates new release with proper versioning
"""

import subprocess
import re
import datetime
import sys

def get_current_version():
    """Get current version from version_info.txt"""
    try:
        with open('version_info.txt', 'r') as f:
            content = f.read()
            match = re.search(r'filevers=\((\d+),(\d+),(\d+),(\d+)\)', content)
            if match:
                return f"{match.group(1)}.{match.group(2)}.{match.group(3)}"
    except FileNotFoundError:
        pass
    return "1.3.0"  # Default version

def update_version_files(version):
    """Update version in all relevant files"""
    
    major, minor, patch = version.split('.')
    
    # Update version_info.txt
    version_info = f'''
# UTF-8
#
# For more details about fixed file info 'ffi' see:
# http://msdn.microsoft.com/en-us/library/ms646997.aspx
VSVersionInfo(
  ffi=FixedFileInfo(
    filevers=({major},{minor},{patch},0),
    prodvers=({major},{minor},{patch},0),
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
        StringStruct(u'FileVersion', u'{version}.0'),
        StringStruct(u'InternalName', u'TypoFix'),
        StringStruct(u'LegalCopyright', u'Copyright (C) 2025'),
        StringStruct(u'OriginalFilename', u'TypoFix.exe'),
        StringStruct(u'ProductName', u'TypoFix - AI Typo Corrector'),
        StringStruct(u'ProductVersion', u'{version}.0')])
      ]), 
    VarFileInfo([VarStruct(u'Translation', [1033, 1200])])
  ]
)
'''
    
    with open('version_info.txt', 'w', encoding='utf-8') as f:
        f.write(version_info.strip())
    
    print(f"✅ Updated version_info.txt to v{version}")

def update_changelog(version):
    """Update CHANGELOG.md with new release"""
    
    today = datetime.datetime.now().strftime("%Y-%m-%d")
    
    new_entry = f"""
## [v{version}] - {today}

### 🎯 Major Changes
- **Simplified Hotkey**: Now uses **Shift+C** instead of Ctrl+Alt+T
- **Embedded API Key**: No setup required - works out of the box
- **Improved User Experience**: More intuitive activation

### ✨ Features
- Global hotkey detection (Shift+C)
- AI-powered typo correction and text rewriting
- Smart widget positioning near selected text
- Auto-close timer (4 seconds of inactivity)
- System tray integration
- Modern transparent UI

### 🔧 Technical Improvements
- Standalone executable (no dependencies)
- Optimized build process
- Better error handling
- Enhanced key detection
- Cross-application compatibility

### 📦 Distribution
- Single file executable
- Optional installer script
- Verification checksums
- Complete documentation

---

"""
    
    try:
        with open('CHANGELOG.md', 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Insert new entry after the first heading
        lines = content.split('\n')
        insert_index = 1  # After the main heading
        for i, line in enumerate(lines):
            if line.startswith('## '):
                insert_index = i
                break
        
        lines.insert(insert_index, new_entry.strip())
        
        with open('CHANGELOG.md', 'w', encoding='utf-8') as f:
            f.write('\n'.join(lines))
            
        print(f"✅ Updated CHANGELOG.md with v{version}")
        
    except FileNotFoundError:
        # Create new changelog if it doesn't exist
        changelog_content = f"""# TypoFix Changelog

All notable changes to TypoFix will be documented in this file.

{new_entry.strip()}
"""
        with open('CHANGELOG.md', 'w', encoding='utf-8') as f:
            f.write(changelog_content)
        print(f"✅ Created CHANGELOG.md with v{version}")

def create_git_tag(version):
    """Create and push git tag for release"""
    
    try:
        # Add all changed files
        subprocess.run(['git', 'add', '.'], check=True)
        
        # Commit changes
        commit_msg = f"Release v{version}: Simplified Shift+C hotkey and embedded API"
        subprocess.run(['git', 'commit', '-m', commit_msg], check=True)
        
        # Create tag
        tag_name = f"v{version}"
        tag_msg = f"TypoFix v{version} - Shift+C hotkey and embedded API key"
        subprocess.run(['git', 'tag', '-a', tag_name, '-m', tag_msg], check=True)
        
        print(f"✅ Created git tag {tag_name}")
        
        # Ask if user wants to push
        response = input(f"\nPush tag {tag_name} to trigger GitHub Actions release? (y/N): ")
        if response.lower() in ['y', 'yes']:
            subprocess.run(['git', 'push', 'origin', 'main'], check=True)
            subprocess.run(['git', 'push', 'origin', tag_name], check=True)
            print(f"🚀 Pushed tag {tag_name} - GitHub Actions will build and create release!")
            print(f"📦 Release will be available at: https://github.com/emiliancristea/typo-fix/releases/tag/{tag_name}")
        else:
            print(f"📝 Tag {tag_name} created locally. Push manually when ready:")
            print(f"   git push origin main")
            print(f"   git push origin {tag_name}")
            
    except subprocess.CalledProcessError as e:
        print(f"❌ Git error: {e}")
        return False
    
    return True

def main():
    """Main release process"""
    
    print("🚀 TypoFix Release Creator")
    print("=" * 30)
    
    current_version = get_current_version()
    print(f"Current version: {current_version}")
    
    # Get new version from user
    new_version = input(f"Enter new version (current: {current_version}): ").strip()
    
    if not new_version:
        print("❌ No version specified. Exiting.")
        return
    
    # Validate version format
    if not re.match(r'^\d+\.\d+\.\d+$', new_version):
        print("❌ Invalid version format. Use X.Y.Z (e.g., 1.3.0)")
        return
    
    print(f"\n📝 Creating release v{new_version}...")
    
    # Update version files
    update_version_files(new_version)
    
    # Update changelog
    update_changelog(new_version)
    
    # Create git tag and push
    if create_git_tag(new_version):
        print(f"\n🎉 Release v{new_version} created successfully!")
        print("\n📋 What happens next:")
        print("1. GitHub Actions will build the executable")
        print("2. Release will be created with all artifacts")
        print("3. Users can download TypoFix.exe directly")
        print("4. No setup required - just run and use Shift+C!")
    else:
        print(f"\n⚠️ Release v{new_version} prepared but not pushed.")

if __name__ == "__main__":
    main()