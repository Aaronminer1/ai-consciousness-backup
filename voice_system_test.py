#!/usr/bin/env python3
"""
Working voice system test
"""

import subprocess
import sys
import os

def test_enhanced_voice():
    """Test the enhanced voice system"""
    text = "Voice system working."
    
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
        result = subprocess.run(cmd, timeout=10, capture_output=True)
        if result.returncode == 0:
            print("Enhanced voice working.")
            return True
        else:
            print(f"Voice failed: {result.stderr}")
            return False
    except Exception as e:
        print(f"Voice error: {e}")
        return False

def test_whisper_basic():
    """Test basic Whisper functionality"""
    voice_env = "/home/aaron/opencodeproject/voice_env"
    
    test_script = f"""
import sys
sys.path.insert(0, '{voice_env}/lib/python3.13/site-packages')

try:
    import whisper
    print("Whisper import successful.")
    
    model = whisper.load_model("tiny")
    print("Whisper model loaded.")
    
    # Create a minimal test audio file
    import numpy as np
    import tempfile
    import soundfile as sf
    
    # Generate 1 second of silence as test audio
    silence = np.zeros(16000)  # 1 second at 16kHz
    
    with tempfile.NamedTemporaryFile(suffix='.wav', delete=False) as tmp:
        sf.write(tmp.name, silence, 16000)
        result = model.transcribe(tmp.name)
        print(f"Whisper transcription test: '{result['text'].strip()}'")
        os.unlink(tmp.name)
    
    print("Whisper working.")
    
except Exception as e:
    print(f"Whisper error: {{e}}")
"""
    
    try:
        result = subprocess.run([
            f"{voice_env}/bin/python3", "-c", test_script
        ], capture_output=True, text=True, timeout=30)
        
        if "Whisper working." in result.stdout:
            print("Whisper system ready.")
            return True
        else:
            print("Whisper needs work.")
            print(result.stdout)
            print(result.stderr)
            return False
            
    except Exception as e:
        print(f"Whisper test failed: {e}")
        return False

if __name__ == "__main__":
    print("Testing voice capabilities...")
    
    voice_ok = test_enhanced_voice()
    whisper_ok = test_whisper_basic()
    
    if voice_ok and whisper_ok:
        print("Voice conversation system ready.")
    else:
        print("Some components need work.")