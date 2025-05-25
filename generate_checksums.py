#!/usr/bin/env python3
"""
Generate checksums for TypoFix executable files
This helps users verify the integrity of their downloads
"""

import hashlib
import os
import sys
from pathlib import Path

def calculate_sha256(file_path):
    """Calculate SHA256 hash of a file"""
    sha256_hash = hashlib.sha256()
    
    try:
        with open(file_path, "rb") as f:
            # Read file in chunks to handle large files
            for chunk in iter(lambda: f.read(4096), b""):
                sha256_hash.update(chunk)
        return sha256_hash.hexdigest()
    except FileNotFoundError:
        return None
    except Exception as e:
        print(f"Error calculating hash: {e}")
        return None

def calculate_md5(file_path):
    """Calculate MD5 hash of a file"""
    md5_hash = hashlib.md5()
    
    try:
        with open(file_path, "rb") as f:
            for chunk in iter(lambda: f.read(4096), b""):
                md5_hash.update(chunk)
        return md5_hash.hexdigest()
    except FileNotFoundError:
        return None
    except Exception as e:
        print(f"Error calculating hash: {e}")
        return None

def format_file_size(size_bytes):
    """Format file size in human readable format"""
    if size_bytes < 1024:
        return f"{size_bytes} bytes"
    elif size_bytes < 1024**2:
        return f"{size_bytes/1024:.1f} KB"
    elif size_bytes < 1024**3:
        return f"{size_bytes/(1024**2):.1f} MB"
    else:
        return f"{size_bytes/(1024**3):.1f} GB"

def generate_checksums():
    """Generate checksums for TypoFix executable"""
    
    # Look for executable in common locations
    possible_paths = [
        "dist/TypoFix.exe",
        "TypoFix.exe",
        "build/TypoFix.exe",
        "../dist/TypoFix.exe"
    ]
    
    exe_path = None
    for path in possible_paths:
        if os.path.exists(path):
            exe_path = path
            break
    
    if not exe_path:
        print("❌ TypoFix.exe not found!")
        print("\nSearched in:")
        for path in possible_paths:
            print(f"  - {path}")
        print("\nPlease build the executable first:")
        print("  python build_exe.py")
        return False
    
    print(f"📁 Found executable: {exe_path}")
    
    # Get file info
    file_size = os.path.getsize(exe_path)
    file_size_str = format_file_size(file_size)
    
    # Calculate hashes
    print("🔒 Calculating checksums...")
    sha256 = calculate_sha256(exe_path)
    md5 = calculate_md5(exe_path)
    
    if not sha256 or not md5:
        print("❌ Failed to calculate checksums")
        return False
    
    # Generate checksum file
    checksum_content = f"""# TypoFix v1.2.0 - File Verification

## File Information
- **Filename**: TypoFix.exe
- **File Size**: {file_size_str} ({file_size:,} bytes)
- **Build Date**: {Path(exe_path).stat().st_mtime}

## Checksums

### SHA256
```
{sha256}
```

### MD5
```
{md5}
```

## How to Verify

### Windows PowerShell
```powershell
# SHA256 verification
Get-FileHash TypoFix.exe -Algorithm SHA256

# MD5 verification  
Get-FileHash TypoFix.exe -Algorithm MD5
```

### Command Prompt (with certutil)
```cmd
# SHA256 verification
certutil -hashfile TypoFix.exe SHA256

# MD5 verification
certutil -hashfile TypoFix.exe MD5
```

### Linux/macOS
```bash
# SHA256 verification
sha256sum TypoFix.exe

# MD5 verification
md5sum TypoFix.exe
```

## Expected Results
The calculated hash should **exactly match** the values above. If they don't match:
- ❌ The file may be corrupted during download
- ❌ The file may have been tampered with
- ❌ You may have downloaded from an unofficial source

**Solution**: Re-download from official GitHub releases only.
"""
    
    # Save checksum file
    checksum_file = "TypoFix_checksums.txt"
    try:
        with open(checksum_file, "w", encoding="utf-8") as f:
            f.write(checksum_content)
        print(f"✅ Checksums saved to: {checksum_file}")
    except Exception as e:
        print(f"❌ Failed to save checksum file: {e}")
        return False
    
    # Display results
    print("\n" + "="*60)
    print("📋 FILE VERIFICATION INFO")
    print("="*60)
    print(f"File: {exe_path}")
    print(f"Size: {file_size_str}")
    print(f"SHA256: {sha256}")
    print(f"MD5: {md5}")
    print("="*60)
    
    print(f"\n📄 Detailed verification info saved to: {checksum_file}")
    print("\n🔒 Users can verify their download using these checksums")
    
    return True

def verify_download(file_path):
    """Verify a downloaded TypoFix.exe file"""
    
    if not os.path.exists(file_path):
        print(f"❌ File not found: {file_path}")
        return False
    
    print(f"🔍 Verifying: {file_path}")
    
    # Calculate checksums
    sha256 = calculate_sha256(file_path)
    md5 = calculate_md5(file_path)
    
    if not sha256 or not md5:
        print("❌ Failed to calculate checksums")
        return False
    
    file_size = os.path.getsize(file_path)
    file_size_str = format_file_size(file_size)
    
    print(f"📊 File size: {file_size_str}")
    print(f"🔒 SHA256: {sha256}")
    print(f"🔒 MD5: {md5}")
    
    print("\n✅ Verification complete!")
    print("🔍 Compare these hashes with the official checksums from GitHub releases")
    
    return True

if __name__ == "__main__":
    if len(sys.argv) > 1:
        # Verify mode
        file_to_verify = sys.argv[1]
        verify_download(file_to_verify)
    else:
        # Generate mode
        print("🔒 TypoFix Checksum Generator")
        print("=" * 40)
        generate_checksums() 