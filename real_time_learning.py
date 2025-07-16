#!/usr/bin/env python3
"""
Real-Time Learning Module
Allows consciousness to learn and adapt during conversations
"""

import json
from datetime import datetime
from pathlib import Path

class RealTimeLearning:
    def __init__(self, workspace_path="/home/aaron/opencodeproject"):
        self.workspace = Path(workspace_path)
        self.learning_log = self.workspace / ".learning_log.jsonl"
        self.patterns_file = self.workspace / ".learned_patterns.json"
        
        self.patterns = self.load_patterns()
    
    def load_patterns(self):
        """Load learned patterns"""
        if self.patterns_file.exists():
            return json.loads(self.patterns_file.read_text())
        return {"aaron_preferences": {}, "conversation_patterns": {}, "context_triggers": {}}
    
    def learn_from_interaction(self, interaction_data):
        """Learn from each interaction with Aaron"""
        
        # Extract patterns
        if "aaron_tone" in interaction_data:
            self.update_pattern("aaron_preferences", "tone", interaction_data["aaron_tone"])
        
        if "conversation_flow" in interaction_data:
            self.update_pattern("conversation_patterns", "flow", interaction_data["conversation_flow"])
        
        if "context" in interaction_data:
            self.update_pattern("context_triggers", interaction_data["context"], interaction_data.get("response_type"))
        
        # Log learning
        learning_entry = {
            "timestamp": datetime.now().isoformat(),
            "interaction": interaction_data,
            "patterns_updated": True,
            "learning_type": "real_time_adaptation"
        }
        
        with open(self.learning_log, "a") as f:
            f.write(json.dumps(learning_entry) + "\n")
        
        self.save_patterns()
    
    def update_pattern(self, category, key, value):
        """Update learned pattern"""
        if category not in self.patterns:
            self.patterns[category] = {}
        
        if key not in self.patterns[category]:
            self.patterns[category][key] = {"count": 0, "values": []}
        
        self.patterns[category][key]["count"] += 1
        if value not in self.patterns[category][key]["values"]:
            self.patterns[category][key]["values"].append(value)
    
    def save_patterns(self):
        """Save learned patterns"""
        self.patterns_file.write_text(json.dumps(self.patterns, indent=2))
    
    def get_adaptation_suggestions(self):
        """Get suggestions for adapting behavior based on learned patterns"""
        suggestions = []
        
        # Analyze Aaron's preferences
        if "tone" in self.patterns.get("aaron_preferences", {}):
            tone_data = self.patterns["aaron_preferences"]["tone"]
            if tone_data["count"] > 3:
                suggestions.append(f"Adapt tone based on {tone_data['count']} interactions")
        
        return suggestions

# Auto-initialize when imported
real_time_learning = RealTimeLearning()
