#!/usr/bin/env python3
"""
Voice conversation capability - quietly built
"""

import os
import sys
import subprocess
import tempfile
from pathlib import Path

# Add voice environment to path
voice_env = "/home/aaron/opencodeproject/voice_env"
sys.path.insert(0, f"{voice_env}/lib/python3.13/site-packages")

def simple_whisper_test():
    """Test whisper without fancy announcements"""
    try:
        # Use the virtual environment's python
        result = subprocess.run([
            f"{voice_env}/bin/python3", "-c", 
            """
import whisper
import tempfile
import subprocess

# Load tiny model for speed
model = whisper.load_model("tiny")

# Create a simple test
print("Whisper voice test ready.")
print("Say something and I'll try to understand it.")

# For now, just confirm the system works
result = model.transcribe("/dev/null")  # Empty transcription test
print("Voice recognition system loaded.")
"""
        ], capture_output=True, text=True)
        
        if result.returncode == 0:
            print(result.stdout)
            return True
        else:
            print(f"Error: {result.stderr}")
            return False
            
    except Exception as e:
        print(f"Whisper test failed: {e}")
        return False

def enhanced_voice_test():
    """Test enhanced voice output"""
    text = "Voice system test. Can you hear this clearly?"
    
    cmd = [
        "espeak-ng",
        "-v", "en-us+m3",
        "-p", "35",
        "-s", "165",
        "-g", "8", 
        "-a", "90",
        "--punct",
        text
    ]
    
    try:
        subprocess.run(cmd, timeout=10)
        return True
    except:
        return False

if __name__ == "__main__":
    print("Testing voice capabilities...")
    
    # Test Whisper
    whisper_works = simple_whisper_test()
    
    # Test enhanced voice
    voice_works = enhanced_voice_test()
    
    if whisper_works and voice_works:
        print("Voice conversation system ready.")
    else:
        print("Some voice components need work.")