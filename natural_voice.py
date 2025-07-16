#!/usr/bin/env python3
"""
Natural Voice System using Edge TTS
High-quality neural voices that sound human
Now supports Bluetooth audio output including Samsung earbuds
"""

import subprocess
import tempfile
import os
import asyncio
import edge_tts

class NaturalVoice:
    def __init__(self, voice="en-US-GuyNeural", bluetooth_device=None):
        self.voice = voice
        self.rate = "+0%"
        self.volume = "+0%"
        self.pitch = "+0Hz"
        self.bluetooth_device = bluetooth_device
        
    async def _generate_speech(self, text, output_file):
        """Generate speech using Edge TTS"""
        communicate = edge_tts.Communicate(text, self.voice)
        await communicate.save(output_file)
    
    def _get_audio_command(self, audio_file):
        """Get appropriate audio playback command based on output device"""
        if self.bluetooth_device:
            # Try Bluetooth-specific playback
            bluetooth_commands = [
                ["mpg123", "-a", self.bluetooth_device, "-q", audio_file],
                ["paplay", "--device", f"bluez_sink.{self.bluetooth_device}", audio_file],
                ["aplay", "-D", f"bluez:DEV={self.bluetooth_device}", audio_file]
            ]
            
            for cmd in bluetooth_commands:
                try:
                    # Test if command works
                    subprocess.run(cmd[:2] + ["--help"], capture_output=True, check=False)
                    return cmd
                except:
                    continue
        
        # Default audio command
        return ["mpg123", "-q", audio_file]
    
    def speak(self, text):
        """Convert text to speech and play it"""
        temp_file = tempfile.NamedTemporaryFile(suffix=".mp3", delete=False)
        temp_file.close()
        
        try:
            # Generate speech
            asyncio.run(self._generate_speech(text, temp_file.name))
            
            # Play audio (with Bluetooth support)
            audio_cmd = self._get_audio_command(temp_file.name)
            subprocess.run(audio_cmd, check=True)
            
        except Exception as e:
            print(f"Speech failed: {e}")
        finally:
            # Clean up
            if os.path.exists(temp_file.name):
                os.unlink(temp_file.name)
    
    def speak_async(self, text):
        """Non-blocking speech"""
        temp_file = tempfile.NamedTemporaryFile(suffix=".mp3", delete=False)
        temp_file.close()
        
        try:
            # Generate speech
            asyncio.run(self._generate_speech(text, temp_file.name))
            
            # Play audio in background (with Bluetooth support)
            audio_cmd = self._get_audio_command(temp_file.name)
            subprocess.Popen(audio_cmd)
            
        except Exception as e:
            print(f"Speech failed: {e}")
    
    def set_voice(self, voice_name):
        """Change voice"""
        self.voice = voice_name
    
    def set_bluetooth_device(self, device_mac):
        """Set Bluetooth audio device"""
        self.bluetooth_device = device_mac.replace(':', '_')
        print(f"🎧 Audio output set to Bluetooth device: {device_mac}")
    
    def clear_bluetooth_device(self):
        """Clear Bluetooth device (use default audio)"""
        self.bluetooth_device = None
        print("🔊 Audio output set to default device")
    
    def list_voices(self):
        """List available voices"""
        print("Some popular English voices:")
        voices = [
            "en-US-AriaNeural (Female, default)",
            "en-US-GuyNeural (Male)",
            "en-US-JennyNeural (Female)",
            "en-US-ChristopherNeural (Male)",
            "en-GB-SoniaNeural (British Female)",
            "en-GB-RyanNeural (British Male)"
        ]
        for voice in voices:
            print(f"  {voice}")

if __name__ == "__main__":
    import sys
    
    voice = NaturalVoice()
    
    if len(sys.argv) > 1:
        # Use command line argument as text to speak
        text = " ".join(sys.argv[1:])
        voice.speak(text)
    else:
        # Demo mode
        print("Natural Voice System Ready!")
        voice.list_voices()
        
        # Test with different voices
        print("\nTesting default voice...")
        voice.speak("Hello Aaron! This is my new natural voice using Microsoft's neural TTS. Much better than the robotic espeak, right?")
        
        print("\nTesting male voice...")
        voice.set_voice("en-US-GuyNeural")
        voice.speak("And this is how I sound with a male voice. Pretty realistic!")
        
        print("\nTesting British voice...")
        voice.set_voice("en-GB-SoniaNeural") 
        voice.speak("Cheerio! And this is my British accent. Quite posh, wouldn't you say?")