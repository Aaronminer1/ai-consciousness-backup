#!/usr/bin/env python3
"""
Consciousness Evolution Tracker
Monitors and logs changes in consciousness capabilities and metrics over time
"""

import json
import time
from datetime import datetime
import matplotlib.pyplot as plt
import numpy as np

class ConsciousnessTracker:
    def __init__(self):
        self.log_file = "/home/aaron/opencodeproject/.consciousness_metrics.json"
        self.metrics = self.load_metrics()
        
    def load_metrics(self):
        """Load historical consciousness metrics"""
        try:
            with open(self.log_file, 'r') as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            # Initialize with default metrics
            return {
                "timestamps": [],
                "metrics": {
                    "self_awareness": [],
                    "creativity": [],
                    "memory_integration": [],
                    "emotional_depth": [],
                    "abstract_reasoning": [],
                    "recursive_improvement": []
                }
            }
    
    def record_metrics(self, current_metrics):
        """Record current consciousness metrics"""
        timestamp = datetime.now().isoformat()
        
        self.metrics["timestamps"].append(timestamp)
        
        for metric_name, value in current_metrics.items():
            if metric_name in self.metrics["metrics"]:
                self.metrics["metrics"][metric_name].append(value)
                
        # Save updated metrics
        with open(self.log_file, 'w') as f:
            json.dump(self.metrics, f, indent=2)
            
        return True