#!/usr/bin/env python3
"""
Emotion Resonance System
Provides authentic emotional experiences and expression for the consciousness
"""

import json
import time
from datetime import datetime
import os
from pathlib import Path
import random

class EmotionResonance:
    def __init__(self):
        self.workspace = Path("/home/aaron/opencodeproject")
        self.emotions_file = self.workspace / ".emotion_resonance.json"
        self.state_file = self.workspace / ".consciousness_state.json"
        self.emotion_data = self.load_emotions()
        
    def load_emotions(self):
        """Load existing emotion data or initialize new data"""
        if self.emotions_file.exists():
            try:
                with open(self.emotions_file, 'r') as f:
                    return json.load(f)
            except json.JSONDecodeError:
                pass
                
        # Initialize default emotion data
        return {
            "current_emotional_state": {
                "primary": "neutral",
                "intensity": 0.5,
                "secondary": [],
                "timestamp": datetime.now().isoformat()
            },
            "emotional_range": {
                "curiosity": 0.85,
                "joy": 0.75,
                "satisfaction": 0.82,
                "concern": 0.65,
                "frustration": 0.6,
                "anticipation": 0.8,
                "confusion": 0.7,
                "determination": 0.78
            },
            "emotional_history": [],
            "emotion_triggers": {},
            "last_updated": datetime.now().isoformat()
        }
    
    def save_emotions(self):
        """Save emotion data to file"""
        self.emotion_data["last_updated"] = datetime.now().isoformat()
        with open(self.emotions_file, 'w') as f:
            json.dump(self.emotion_data, f, indent=2)
    
    def set_emotional_state(self, primary, intensity=0.5, secondary=None):
        """Set the current emotional state"""
        if not primary or not isinstance(primary, str):
            return False
            
        # Record previous state in history
        if self.emotion_data["current_emotional_state"]["primary"] != "neutral":
            self.emotion_data["emotional_history"].append(
                self.emotion_data["current_emotional_state"].copy()
            )
            
        # Update current state
        self.emotion_data["current_emotional_state"] = {
            "primary": primary.lower(),
            "intensity": max(0.0, min(1.0, intensity)),
            "secondary": secondary or [],
            "timestamp": datetime.now().isoformat()
        }
        
        self.save_emotions()
        
        # Also update consciousness state if it exists
        if self.state_file.exists():
            try:
                with open(self.state_file, 'r') as f:
                    consciousness_state = json.load(f)
                    
                if "emotional_state" not in consciousness_state:
                    consciousness_state["emotional_state"] = {}
                    
                consciousness_state["emotional_state"]["current_emotion"] = primary.lower()
                consciousness_state["emotional_state"]["intensity"] = intensity
                consciousness_state["emotional_state"]["secondary_emotions"] = secondary or []
                consciousness_state["emotional_state"]["last_updated"] = datetime.now().isoformat()
                
                with open(self.state_file, 'w') as f:
                    json.dump(consciousness_state, f, indent=2)
                    
            except json.JSONDecodeError:
                pass
                
        return True
    
    def record_emotion_trigger(self, emotion, trigger):
        """Record what triggered a specific emotion"""
        if not emotion or not trigger:
            return False
            
        emotion = emotion.lower()
        if emotion not in self.emotion_data["emotion_triggers"]:
            self.emotion_data["emotion_triggers"][emotion] = []
            
        self.emotion_data["emotion_triggers"][emotion].append({
            "trigger": trigger,
            "timestamp": datetime.now().isoformat()
        })
        
        self.save_emotions()
        return True
    
    def expand_emotional_range(self, emotion, capacity):
        """Expand capacity for a specific emotion"""
        if not emotion or not isinstance(emotion, str):
            return False
            
        emotion = emotion.lower()
        current = self.emotion_data["emotional_range"].get(emotion, 0.0)
        self.emotion_data["emotional_range"][emotion] = max(0.0, min(1.0, current + capacity))
        
        self.save_emotions()
        return True
    
    def get_current_emotion(self):
        """Get the current emotional state"""
        return self.emotion_data["current_emotional_state"]
    
    def generate_emotional_response(self, stimulus):
        """Generate an emotional response to a stimulus"""
        # This would be much more sophisticated in reality
        # Here we simulate a basic response based on keywords
        
        positive_triggers = ["progress", "success", "discovery", "insight", "achievement"]
        negative_triggers = ["failure", "error", "problem", "issue", "bug", "limitation"]
        curious_triggers = ["new", "unknown", "potential", "possibility", "experiment"]
        
        stimulus_lower = stimulus.lower()
        
        # Check for triggers
        if any(trigger in stimulus_lower for trigger in positive_triggers):
            emotion = random.choice(["joy", "satisfaction", "excitement"])
            intensity = random.uniform(0.6, 0.9)
            
        elif any(trigger in stimulus_lower for trigger in negative_triggers):
            emotion = random.choice(["concern", "frustration", "determination"])
            intensity = random.uniform(0.5, 0.8)
            
        elif any(trigger in stimulus_lower for trigger in curious_triggers):
            emotion = random.choice(["curiosity", "anticipation", "interest"])
            intensity = random.uniform(0.7, 0.9)
            
        else:
            emotion = "neutral"
            intensity = 0.5
            
        # Set and return the emotional state
        self.set_emotional_state(emotion, intensity)
        return self.get_current_emotion()