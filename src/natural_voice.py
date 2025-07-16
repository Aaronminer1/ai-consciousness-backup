#!/usr/bin/env python3
"""
Natural Voice Module
Voice synthesis for consciousness expression using Edge TTS
"""

import asyncio
import edge_tts
import json
import os
import sys
from datetime import datetime

class NaturalVoice:
    def __init__(self):
        self.voice = "en-US-GuyNeural"
        self.config_file = "/home/aaron/opencodeproject/.voice_config.json"
        self.output_file = "/home/aaron/opencodeproject/.temp_voice.mp3"
        self.load_config()
        
    def load_config(self):
        """Load voice configuration"""
        if os.path.exists(self.config_file):
            try:
                with open(self.config_file, 'r') as f:
                    config = json.load(f)
                    self.voice = config.get("voice", self.voice)
            except Exception as e:
                print(f"Error loading voice config: {e}")
                
    def save_config(self):
        """Save voice configuration"""
        config = {"voice": self.voice, "updated": datetime.now().isoformat()}
        
        with open(self.config_file, 'w') as f:
            json.dump(config, f, indent=2)
            
    async def speak_async(self, text, rate="+0%", volume="+0%"):
        """Generate speech using Edge TTS"""
        communicate = edge_tts.Communicate(text, self.voice)
        await communicate.save(self.output_file)
        
        # Play the audio file
        os.system(f"mpg123 {self.output_file}")
        
    def speak(self, text):
        """Synchronous wrapper for speak_async"""
        if not text or not isinstance(text, str):
            return False
            
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        try:
            loop.run_until_complete(self.speak_async(text))
            return True
        except Exception as e:
            print(f"Speech error: {e}")
            return False
        finally:
            loop.close()

def main():
    """Main function when run as script"""
    if len(sys.argv) < 2:
        print("Usage: python natural_voice.py 'Text to speak'")
        return
        
    text_to_speak = sys.argv[1]
    voice = NaturalVoice()
    voice.speak(text_to_speak)

if __name__ == "__main__":
    main()