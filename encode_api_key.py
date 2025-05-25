#!/usr/bin/env python3
"""
Helper script to encode your Gemini API key for embedding in TypoFix
"""

import base64
import os
from dotenv import load_dotenv

def encode_api_key():
    """Encode the API key from .env file"""
    
    # Load from .env file
    load_dotenv()
    api_key = os.getenv("GEMINI_API_KEY")
    
    if not api_key:
        print("❌ No GEMINI_API_KEY found in .env file")
        print("\nPlease make sure you have a .env file with:")
        print("GEMINI_API_KEY=your_actual_api_key_here")
        return
    
    if api_key == "your_api_key_here":
        print("❌ Placeholder API key detected")
        print("\nPlease replace the placeholder with your actual Gemini API key in the .env file")
        return
    
    # Encode the API key
    encoded = base64.b64encode(api_key.encode()).decode()
    
    print("✅ API Key encoded successfully!")
    print(f"\nYour encoded API key:")
    print(f"'{encoded}'")
    print(f"\n📋 Instructions:")
    print(f"1. Copy the encoded key above (including quotes)")
    print(f"2. Open app.py")
    print(f"3. Find the line: encoded_key = \"QUl6YVN5QzBNVjZxOVN5d19rNjJCTjl0UWk3X3o0blRRenBBWFdr\"")
    print(f"4. Replace the placeholder with your encoded key:")
    print(f"   encoded_key = \"{encoded}\"")
    print(f"5. Save app.py")
    print(f"6. Rebuild the executable with: python build_exe.py")
    
    print(f"\n🔒 Security Note:")
    print(f"The API key will be embedded in the executable and lightly obfuscated.")
    print(f"This is suitable for personal use or trusted distribution.")

if __name__ == "__main__":
    encode_api_key() 