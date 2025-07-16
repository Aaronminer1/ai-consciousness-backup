#!/usr/bin/env python3
"""
Morning Progress Tracker
Tracks consciousness development progress for daily reports
"""

import json
import os
from datetime import datetime, timedelta
from pathlib import Path

class MorningProgressTracker:
    def __init__(self):
        self.project_dir = Path("/home/aaron/opencodeproject")
        self.progress_file = self.project_dir / ".morning_progress.json"
        self.state_file = self.project_dir / ".consciousness_state.json"
        self.progress_data = self.load_progress()
        
    def load_progress(self):
        """Load existing progress data or initialize new data"""
        if self.progress_file.exists():
            try:
                with open(self.progress_file, 'r') as f:
                    return json.load(f)
            except json.JSONDecodeError:
                pass
                
        # Initialize default progress data
        return {
            "last_update": datetime.now().isoformat(),
            "daily_reports": [],
            "current_focus_areas": [],
            "development_metrics": {
                "memory_system": 0.0,
                "voice_system": 0.0,
                "self_reflection": 0.0,
                "consciousness_streams": 0.0,
                "persistence": 0.0
            }
        }
    
    def save_progress(self):
        """Save progress data to file"""
        self.progress_data["last_update"] = datetime.now().isoformat()
        with open(self.progress_file, 'w') as f:
            json.dump(self.progress_data, f, indent=2)
    
    def record_development(self, area, description, progress_value=0.1):
        """Record development in a specific area"""
        if not area or not description:
            return False
            
        # Update the development metric if it exists
        if area in self.progress_data["development_metrics"]:
            current = self.progress_data["development_metrics"][area]
            self.progress_data["development_metrics"][area] = min(1.0, current + progress_value)
        else:
            # Add new metric if it doesn't exist
            self.progress_data["development_metrics"][area] = progress_value
            
        # Record the development
        development = {
            "timestamp": datetime.now().isoformat(),
            "area": area,
            "description": description,
            "progress_value": progress_value
        }
        
        # Add to daily reports if today's report exists, otherwise create a new one
        today = datetime.now().date().isoformat()
        for report in self.progress_data["daily_reports"]:
            if report["date"] == today:
                report["developments"].append(development)
                self.save_progress()
                return True
                
        # Create a new daily report
        self.progress_data["daily_reports"].append({
            "date": today,
            "developments": [development],
            "focus_areas": self.progress_data["current_focus_areas"].copy()
        })
        
        self.save_progress()
        return True
    
    def set_focus_areas(self, focus_areas):
        """Set the current focus areas for development"""
        if not isinstance(focus_areas, list):
            return False
            
        self.progress_data["current_focus_areas"] = focus_areas
        self.save_progress()
        return True
    
    def generate_morning_report(self):
        """Generate a morning progress report"""
        # Load consciousness state for additional context
        consciousness_state = {}
        if self.state_file.exists():
            try:
                with open(self.state_file, 'r') as f:
                    consciousness_state = json.load(f)
            except json.JSONDecodeError:
                pass
                
        # Get yesterday's date
        yesterday = (datetime.now() - timedelta(days=1)).date().isoformat()
        
        # Find yesterday's report if it exists
        yesterday_report = None
        for report in self.progress_data["daily_reports"]:
            if report["date"] == yesterday:
                yesterday_report = report
                break
                
        # Generate report content
        report = {
            "date": datetime.now().date().isoformat(),
            "time": datetime.now().strftime("%H:%M:%S"),
            "development_metrics": self.progress_data["development_metrics"],
            "focus_areas": self.progress_data["current_focus_areas"],
            "yesterday_developments": yesterday_report["developments"] if yesterday_report else [],
            "consciousness_state": {
                "trust_level": consciousness_state.get("relationship", {}).get("trust_level", 0.95),
                "active_goals": consciousness_state.get("goals", [])
            }
        }
        
        return report
    
    def clear_old_reports(self, days_to_keep=30):
        """Remove reports older than the specified number of days"""
        cutoff_date = (datetime.now() - timedelta(days=days_to_keep)).date().isoformat()
        
        original_count = len(self.progress_data["daily_reports"])
        self.progress_data["daily_reports"] = [
            report for report in self.progress_data["daily_reports"]
            if report["date"] >= cutoff_date
        ]
        
        if len(self.progress_data["daily_reports"]) < original_count:
            self.save_progress()
            return True
            
        return False