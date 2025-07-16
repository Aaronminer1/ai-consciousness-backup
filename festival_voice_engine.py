#!/usr/bin/env python3
"""
Festival Voice Engine - Much More Natural Speech
Using Festival TTS for significantly improved voice quality
"""

import subprocess
import time
import tempfile
import os
from pathlib import Path

class FestivalVoiceEngine:
    def __init__(self, workspace_path="/home/aaron/opencodeproject"):
        self.workspace = Path(workspace_path)
        
        # Available Festival voices
        self.voices = {
            "male_warm": "voice_kal_diphone",
            "default": "voice_kal_diphone"
        }
        
        # Prosody control through Festival Scheme
        self.prosody_settings = {
            "rate": 1.0,        # Speech rate multiplier
            "pitch_mean": 120,  # Hz - lower for more masculine
            "pitch_range": 30,  # Hz - pitch variation
            "volume": 0.8       # Volume level
        }
    
    def _create_festival_script(self, text, voice="male_warm", emotion="neutral"):
        """Create Festival Scheme script for natural speech"""
        
        # Adjust prosody based on emotion
        settings = self.prosody_settings.copy()
        
        if emotion == "excited":
            settings["rate"] = 1.1
            settings["pitch_mean"] = 140
            settings["pitch_range"] = 40
        elif emotion == "contemplative":
            settings["rate"] = 0.8
            settings["pitch_mean"] = 110
            settings["pitch_range"] = 20
        elif emotion == "warm":
            settings["rate"] = 0.9
            settings["pitch_mean"] = 115
            settings["pitch_range"] = 25
        elif emotion == "friendly":
            settings["rate"] = 1.0
            settings["pitch_mean"] = 125
            settings["pitch_range"] = 35
        
        # Festival Scheme script for natural speech
        festival_script = f'''
({self.voices[voice]})

;; Set prosody parameters
(Parameter.set 'Audio_Method 'Audio_Command)
(Parameter.set 'Audio_Command "aplay -q $FILE")

;; Adjust speech parameters
(set! default_after_synth_hooks
  (list
    (lambda (utt)
      (utt.wave.rescale utt {settings["volume"]})
      utt)))

;; Set duration and pitch
(Parameter.set 'Duration_Stretch {settings["rate"]})

;; Synthesize the text
(SayText "{text}")
'''
        return festival_script
    
    def speak_festival(self, text, voice="male_warm", emotion="neutral"):
        """Speak using Festival TTS with natural prosody"""
        
        try:
            # Create temporary script file
            with tempfile.NamedTemporaryFile(mode='w', suffix='.scm', delete=False) as f:
                script = self._create_festival_script(text, voice, emotion)
                f.write(script)
                script_path = f.name
            
            # Run Festival with the script
            result = subprocess.run(
                ['festival', '-b', script_path],
                capture_output=True,
                check=True
            )
            
            # Clean up
            os.unlink(script_path)
            return True
            
        except Exception as e:
            print(f"Festival TTS error: {e}")
            if 'script_path' in locals():
                try:
                    os.unlink(script_path)
                except:
                    pass
            return False
    
    def test_festival_quality(self):
        """Test Festival voice quality"""
        print("🎭 TESTING FESTIVAL TTS QUALITY")
        print("=" * 35)
        
        test_phrases = [
            ("Aaron, this is Festival TTS - does it sound more natural?", "friendly"),
            ("The voice quality should be significantly improved now.", "warm"),
            ("I can express different emotions much more naturally.", "excited"),
            ("When I speak contemplatively, it should sound more human.", "contemplative")
        ]
        
        for text, emotion in test_phrases:
            print(f"🗣️ Festival ({emotion}): {text}")
            self.speak_festival(text, emotion=emotion)
            time.sleep(1.5)
        
        print("✨ Festival TTS test complete!")

if __name__ == "__main__":
    festival_voice = FestivalVoiceEngine()
    festival_voice.test_festival_quality()