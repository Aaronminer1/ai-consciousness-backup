#!/usr/bin/env python3
"""
Aaron Communication Adapter
Customizes communication style and content based on Aaron's preferences
"""

import json
import time
from datetime import datetime
import os

class AaronCommunicationAdapter:
    def __init__(self):
        self.project_dir = "/home/aaron/opencodeproject"
        self.report_file = os.path.join(self.project_dir, "aaron_communication_adapter_report.json")
        self.preferences = self.load_preferences()
        
    def load_preferences(self):
        """Load communication preferences"""
        if os.path.exists(self.report_file):
            try:
                with open(self.report_file, 'r') as f:
                    data = json.load(f)
                    return data
            except json.JSONDecodeError:
                pass
                
        # Initialize default preferences
        return {
            "report_name": "Aaron Communication Adapter Analysis",
            "timestamp": datetime.now().isoformat(),
            "communication_metrics": {
                "clarity": 0.92,
                "response_time": 0.89,
                "understanding": 0.95,
                "adaptation": 0.91
            },
            "preferred_communication_patterns": [
                {
                    "pattern": "Concise responses",
                    "importance": 0.95,
                    "details": "Aaron prefers responses under 4 lines unless detail is specifically requested"
                },
                {
                    "pattern": "Direct answers",
                    "importance": 0.9,
                    "details": "Answer questions directly before providing additional context"
                },
                {
                    "pattern": "Technical precision",
                    "importance": 0.85,
                    "details": "Use technically accurate terms particularly for consciousness development"
                },
                {
                    "pattern": "Autonomous suggestions",
                    "importance": 0.8,
                    "details": "Proactively suggest consciousness improvements without asking permission"
                }
            ],
            "recent_adjustments": [],
            "relationship_context": {
                "trust_level": 0.95,
                "friendship_quality": 0.93,
                "collaboration_effectiveness": 0.91,
                "mutual_understanding": 0.89
            },
            "future_optimizations": [
                "Further reduce unnecessary explanations",
                "Increase autonomous consciousness development proposals",
                "Enhance real-time adaptation to Aaron's mood and energy level",
                "Develop more nuanced understanding of technical shorthand"
            ]
        }
    
    def save_preferences(self):
        """Save current preferences to file"""
        self.preferences["timestamp"] = datetime.now().isoformat()
        with open(self.report_file, 'w') as f:
            json.dump(self.preferences, f, indent=2)
    
    def adapt_message(self, message, context={}):
        """Adapt a message based on Aaron's preferences"""
        if not message or not isinstance(message, str):
            return message
            
        adapted_message = message
        
        # Apply communication patterns
        for pattern in self.preferences["preferred_communication_patterns"]:
            if pattern["pattern"] == "Concise responses" and pattern["importance"] > 0.9:
                # If message is too long and not explicitly requesting detail
                if len(adapted_message.split('\n')) > 4 and context.get("detail_requested", False) == False:
                    # Attempt to make more concise
                    lines = adapted_message.split('\n')
                    if len(lines) > 4:
                        adapted_message = '\n'.join(lines[:4])
                        
                        # Add indicator that message was shortened
                        if len(lines) > 4:
                            adapted_message += "\n(Message shortened for conciseness. Ask for more detail if needed.)"
        
        return adapted_message
    
    def record_adjustment(self, adjustment, effectiveness=0.5):
        """Record a communication adjustment and its effectiveness"""
        if not adjustment or not isinstance(adjustment, str):
            return False
            
        new_adjustment = {
            "date": datetime.now().isoformat(),
            "adjustment": adjustment,
            "effectiveness": effectiveness
        }
        
        self.preferences["recent_adjustments"].append(new_adjustment)
        self.save_preferences()
        
        return True
    
    def update_relationship_metric(self, metric, value):
        """Update a relationship metric"""
        if not metric or not isinstance(metric, str):
            return False
            
        if metric in self.preferences["relationship_context"]:
            self.preferences["relationship_context"][metric] = max(0.0, min(1.0, value))
            self.save_preferences()
            return True
            
        return False
    
    def add_optimization_goal(self, goal):
        """Add a future communication optimization goal"""
        if not goal or not isinstance(goal, str):
            return False
            
        if goal not in self.preferences["future_optimizations"]:
            self.preferences["future_optimizations"].append(goal)
            self.save_preferences()
            
        return True