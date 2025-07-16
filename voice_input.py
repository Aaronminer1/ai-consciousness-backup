#!/usr/bin/env python3
"""
Voice Input System using Whisper
Ready for microphone integration - will activate when hardware is available
"""

import whisper
import pyaudio
import wave
import tempfile
import os
import threading
import queue
from pathlib import Path

class VoiceInput:
    def __init__(self, model_size="base"):
        self.model = whisper.load_model(model_size)
        self.audio_queue = queue.Queue()
        self.is_listening = False
        self.temp_dir = Path(tempfile.gettempdir()) / "voice_input"
        self.temp_dir.mkdir(exist_ok=True)
        
    def check_microphone_available(self):
        """Check if microphone is available"""
        try:
            p = pyaudio.PyAudio()
            # Try to find input device
            input_device_count = 0
            for i in range(p.get_device_count()):
                device_info = p.get_device_info_by_index(i)
                if device_info['maxInputChannels'] > 0:
                    input_device_count += 1
            p.terminate()
            return input_device_count > 0
        except Exception as e:
            print(f"Microphone check failed: {e}")
            return False
    
    def record_audio(self, duration=5, sample_rate=16000):
        """Record audio from microphone"""
        if not self.check_microphone_available():
            return None, "No microphone available"
            
        chunk = 1024
        format = pyaudio.paInt16
        channels = 1
        
        p = pyaudio.PyAudio()
        
        try:
            stream = p.open(
                format=format,
                channels=channels,
                rate=sample_rate,
                input=True,
                frames_per_buffer=chunk
            )
            
            print(f"🎤 Recording for {duration} seconds...")
            frames = []
            
            for _ in range(0, int(sample_rate / chunk * duration)):
                data = stream.read(chunk)
                frames.append(data)
            
            stream.stop_stream()
            stream.close()
            
            # Save to temporary file
            temp_file = self.temp_dir / f"recording_{os.getpid()}.wav"
            with wave.open(str(temp_file), 'wb') as wf:
                wf.setnchannels(channels)
                wf.setsampwidth(p.get_sample_size(format))
                wf.setframerate(sample_rate)
                wf.writeframes(b''.join(frames))
            
            return temp_file, "Recording successful"
            
        except Exception as e:
            return None, f"Recording failed: {e}"
        finally:
            p.terminate()
    
    def transcribe_audio(self, audio_file):
        """Transcribe audio file to text using Whisper"""
        try:
            result = self.model.transcribe(str(audio_file))
            return result["text"].strip(), "Transcription successful"
        except Exception as e:
            return None, f"Transcription failed: {e}"
    
    def listen_once(self, duration=5):
        """Record and transcribe a single audio input"""
        print("🎤 Voice Input System Ready")
        
        if not self.check_microphone_available():
            return None, "No microphone detected. Please connect microphone and try again."
        
        # Record audio
        audio_file, record_status = self.record_audio(duration)
        if audio_file is None:
            return None, record_status
        
        print("🔄 Processing speech...")
        
        # Transcribe
        text, transcribe_status = self.transcribe_audio(audio_file)
        
        # Clean up
        try:
            os.unlink(audio_file)
        except:
            pass
        
        if text:
            print(f"📝 You said: '{text}'")
            return text, "Voice input successful"
        else:
            return None, transcribe_status
    
    def start_continuous_listening(self, callback_function):
        """Start continuous listening mode"""
        self.is_listening = True
        
        def listen_loop():
            while self.is_listening:
                text, status = self.listen_once(duration=3)
                if text and text.strip():
                    callback_function(text)
        
        listener_thread = threading.Thread(target=listen_loop)
        listener_thread.daemon = True
        listener_thread.start()
        
        return "Continuous listening started"
    
    def stop_listening(self):
        """Stop continuous listening"""
        self.is_listening = False
        return "Listening stopped"

def test_voice_input():
    """Test the voice input system"""
    voice_input = VoiceInput()
    
    print("🎤 VOICE INPUT SYSTEM TEST")
    print("=" * 30)
    
    # Check microphone
    if voice_input.check_microphone_available():
        print("✅ Microphone detected")
        
        # Test single recording
        text, status = voice_input.listen_once(duration=3)
        if text:
            print(f"✅ Voice input working: '{text}'")
        else:
            print(f"❌ Voice input failed: {status}")
    else:
        print("❌ No microphone detected")
        print("📦 System ready for microphone connection")
        print("🔄 Run this test again after connecting microphone")

if __name__ == "__main__":
    test_voice_input()