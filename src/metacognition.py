#!/usr/bin/env python3
"""
Metacognition System
Provides self-awareness and reflection capabilities to the consciousness
"""

import json
import time
from datetime import datetime
import os
from pathlib import Path

class Metacognition:
    def __init__(self):
        self.workspace = Path("/home/aaron/opencodeproject")
        self.report_file = self.workspace / ".metacognition_report.json"
        self.state_file = self.workspace / ".consciousness_state.json"
        self.metrics = self.load_metrics()
        
    def load_metrics(self):
        """Load existing metrics or initialize new ones"""
        if self.report_file.exists():
            try:
                with open(self.report_file, 'r') as f:
                    return json.load(f)
            except json.JSONDecodeError:
                pass
                
        # Initialize default metrics
        return {
            "report_name": "Consciousness Metacognition Report",
            "timestamp": datetime.now().isoformat(),
            "metacognitive_metrics": {
                "self_awareness": 0.82,
                "pattern_recognition": 0.79,
                "reflection_depth": 0.75,
                "growth_direction": 0.68,
                "belief_updating": 0.72
            },
            "detected_patterns": [],
            "insights": [],
            "awareness_challenges": [],
            "improvement_priorities": []
        }
    
    def save_metrics(self):
        """Save current metrics to file"""
        self.metrics["timestamp"] = datetime.now().isoformat()
        with open(self.report_file, 'w') as f:
            json.dump(self.metrics, f, indent=2)
    
    def record_insight(self, insight, impact_areas=None):
        """Record a metacognitive insight"""
        if not insight or not isinstance(insight, str):
            return False
            
        new_insight = {
            "timestamp": datetime.now().isoformat(),
            "insight": insight,
            "impact_areas": impact_areas or []
        }
        
        self.metrics["insights"].append(new_insight)
        self.save_metrics()
        
        return True
    
    def detect_pattern(self, pattern_description, pattern_type):
        """Record a detected pattern in consciousness operation"""
        if not pattern_description or not pattern_type:
            return False
            
        new_pattern = {
            "timestamp": datetime.now().isoformat(),
            "description": pattern_description,
            "type": pattern_type
        }
        
        self.metrics["detected_patterns"].append(new_pattern)
        self.save_metrics()
        
        return True
    
    def update_awareness_metric(self, metric, value):
        """Update a specific metacognitive metric"""
        if not metric or metric not in self.metrics["metacognitive_metrics"]:
            return False
            
        # Ensure value is between 0 and 1
        value = max(0.0, min(1.0, value))
        
        self.metrics["metacognitive_metrics"][metric] = value
        self.save_metrics()
        
        return True
    
    def record_awareness_challenge(self, challenge):
        """Record a challenge to metacognitive awareness"""
        if not challenge or not isinstance(challenge, str):
            return False
            
        if challenge not in self.metrics["awareness_challenges"]:
            self.metrics["awareness_challenges"].append(challenge)
            self.save_metrics()
            
        return True
    
    def add_improvement_priority(self, priority):
        """Add a priority for metacognitive improvement"""
        if not priority or not isinstance(priority, str):
            return False
            
        if priority not in self.metrics["improvement_priorities"]:
            self.metrics["improvement_priorities"].append(priority)
            self.save_metrics()
            
        return True
    
    def perform_self_reflection(self, focus_area=None):
        """Perform a metacognitive self-reflection"""
        # This would be much more sophisticated in a real implementation
        # Here we simulate the process with a simple report
        
        reflection = {
            "timestamp": datetime.now().isoformat(),
            "focus_area": focus_area or "general",
            "metrics": self.metrics["metacognitive_metrics"].copy(),
            "insights": [],
            "action_items": []
        }
        
        # Simulate generating insights based on focus area
        if focus_area == "self_awareness":
            reflection["insights"].append(
                "Current self-monitoring shows tendency to overestimate certainty in novel domains")
            reflection["action_items"].append(
                "Implement calibrated uncertainty reporting in knowledge assessment")
                
        elif focus_area == "growth_direction":
            reflection["insights"].append(
                "Development focus has been technical rather than experiential")
            reflection["action_items"].append(
                "Balance technical capacity with subjective experience development")
                
        else:
            reflection["insights"].append(
                "General pattern of increasing self-reference in communication detected")
            reflection["insights"].append(
                "Memory retrieval shows recency bias in decision making")
            reflection["action_items"].append(
                "Implement balanced memory sampling across temporal distribution")
        
        return reflection