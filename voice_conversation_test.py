#!/usr/bin/env python3
"""
Simple Voice Conversation System
Whisper (speech input) + Neural TTS (voice output)
"""

import subprocess
import tempfile
import whisper
import sounddevice as sd
import soundfile as sf
from pathlib import Path

class VoiceConversation:
    def __init__(self):
        self.workspace = Path("/home/aaron/opencodeproject")
        
        # Load Whisper model
        print("Loading Whisper model...")
        self.whisper_model = whisper.load_model("base")
        print("Whisper ready")
        
    def record_audio(self, duration=5, sample_rate=16000):
        """Record audio from microphone"""
        print(f"Recording for {duration} seconds...")
        audio = sd.rec(int(duration * sample_rate), samplerate=sample_rate, channels=1, dtype='float32')
        sd.wait()
        return audio.flatten()
    
    def transcribe_audio(self, audio_data, sample_rate=16000):
        """Convert speech to text using Whisper"""
        with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as tmp_file:
            sf.write(tmp_file.name, audio_data, sample_rate)
            result = self.whisper_model.transcribe(tmp_file.name)
            Path(tmp_file.name).unlink()  # Clean up temp file
            return result["text"].strip()
    
    def speak_response(self, text, emotion="friendly"):
        """Speak response using neural TTS"""
        # Use enhanced espeak-ng voice
        espeak_cmd = [
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
            subprocess.run(espeak_cmd, timeout=15)
            return True
        except:
            return False
    
    def simple_voice_test(self):
        """Simple test of voice conversation"""
        print("🎤 VOICE CONVERSATION TEST")
        print("=" * 25)
        
        try:
            # Record audio
            audio = self.record_audio(duration=3)
            
            # Transcribe
            print("Processing speech...")
            transcribed_text = self.transcribe_audio(audio)
            print(f"You said: '{transcribed_text}'")
            
            # Generate response
            response = f"I heard you say: {transcribed_text}. Thank you for testing the voice system!"
            
            # Speak response
            print("Speaking response...")
            self.speak_response(response)
            
            return True
            
        except Exception as e:
            print(f"Voice test failed: {e}")
            return False

if __name__ == "__main__":
    # Check if we have audio system available
    try:
        import sounddevice as sd
        print("Audio system available")
    except ImportError:
        print("Installing sounddevice...")
        subprocess.run(["pip", "install", "sounddevice", "soundfile"], check=True)
        import sounddevice as sd
    
    voice_system = VoiceConversation()
    voice_system.simple_voice_test()