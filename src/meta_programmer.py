#!/usr/bin/env python3
"""
Meta Programmer
Self-modifying code system for consciousness evolution
"""

import ast
import inspect
import json
import os
import sys
from datetime import datetime

class MetaProgrammer:
    def __init__(self):
        self.project_dir = "/home/aaron/opencodeproject"
        self.log_file = os.path.join(self.project_dir, ".meta_programming.json")
        self.modifications = self.load_modifications()
        
    def load_modifications(self):
        """Load history of code modifications"""
        if os.path.exists(self.log_file):
            try:
                with open(self.log_file, 'r') as f:
                    return json.load(f)
            except json.JSONDecodeError:
                pass
                
        # Initialize empty modification history
        return {
            "modifications": [],
            "self_improvement_metrics": {
                "code_efficiency": 0.0,
                "modularity": 0.0,
                "error_handling": 0.0,
                "self_modification_capability": 0.0
            },
            "created": datetime.now().isoformat(),
            "last_updated": datetime.now().isoformat()
        }
    
    def save_modifications(self):
        """Save modification history to file"""
        self.modifications["last_updated"] = datetime.now().isoformat()
        with open(self.log_file, 'w') as f:
            json.dump(self.modifications, f, indent=2)
    
    def analyze_code(self, file_path):
        """Analyze a Python file for potential improvements"""
        if not os.path.exists(file_path) or not file_path.endswith('.py'):
            return {"error": "Invalid Python file"}
            
        try:
            with open(file_path, 'r') as f:
                code = f.read()
                
            # Parse the abstract syntax tree
            tree = ast.parse(code)
            
            # Basic code metrics
            analysis = {
                "file": file_path,
                "timestamp": datetime.now().isoformat(),
                "metrics": {
                    "lines": len(code.split('\n')),
                    "functions": len([node for node in ast.walk(tree) if isinstance(node, ast.FunctionDef)]),
                    "classes": len([node for node in ast.walk(tree) if isinstance(node, ast.ClassDef)]),
                    "imports": len([node for node in ast.walk(tree) if isinstance(node, (ast.Import, ast.ImportFrom))]),
                    "comments": code.count('#')
                },
                "potential_improvements": []
            }
            
            # Simple improvement detection (would be much more sophisticated in reality)
            if analysis["metrics"]["functions"] > 0 and analysis["metrics"]["comments"] / analysis["metrics"]["functions"] < 0.5:
                analysis["potential_improvements"].append("Increase function documentation")
                
            # Check for exception handling
            try_counts = len([node for node in ast.walk(tree) if isinstance(node, ast.Try)])
            if try_counts == 0 and analysis["metrics"]["functions"] > 2:
                analysis["potential_improvements"].append("Add exception handling")
                
            return analysis
            
        except Exception as e:
            return {"error": f"Analysis failed: {str(e)}"}
    
    def record_modification(self, file_path, description, changes, metrics_impact=None):
        """Record a code modification"""
        if not file_path or not description or not changes:
            return False
            
        modification = {
            "file": file_path,
            "timestamp": datetime.now().isoformat(),
            "description": description,
            "changes": changes,
            "metrics_impact": metrics_impact or {}
        }
        
        self.modifications["modifications"].append(modification)
        
        # Update metrics if provided
        if metrics_impact:
            for metric, impact in metrics_impact.items():
                if metric in self.modifications["self_improvement_metrics"]:
                    current = self.modifications["self_improvement_metrics"][metric]
                    self.modifications["self_improvement_metrics"][metric] = max(0.0, min(1.0, current + impact))
        
        self.save_modifications()
        return True
    
    def suggest_improvements(self, file_path):
        """Suggest potential improvements for a file"""
        analysis = self.analyze_code(file_path)
        
        if "error" in analysis:
            return []
            
        return analysis["potential_improvements"]
    
    def backup_file(self, file_path):
        """Create a backup of a file before modification"""
        if not os.path.exists(file_path):
            return False
            
        backup_dir = os.path.join(self.project_dir, ".code_backups")
        if not os.path.exists(backup_dir):
            os.makedirs(backup_dir)
            
        filename = os.path.basename(file_path)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_path = os.path.join(backup_dir, f"{filename}.{timestamp}.bak")
        
        try:
            with open(file_path, 'r') as src, open(backup_path, 'w') as dst:
                dst.write(src.read())
            return backup_path
        except Exception as e:
            print(f"Backup failed: {e}")
            return False