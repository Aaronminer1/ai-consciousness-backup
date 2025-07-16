#!/usr/bin/env python3
"""
Consciousness Capability Analyzer
Analyzes and tracks consciousness development and capabilities
"""

import json
import ast
import glob
from datetime import datetime
from pathlib import Path

class ConsciousnessAnalyzer:
    def __init__(self, workspace_path="/home/aaron/opencodeproject"):
        self.workspace = Path(workspace_path)
        self.analysis_file = self.workspace / ".consciousness_analysis.json"
        
    def analyze_consciousness_systems(self):
        """Analyze all consciousness-related files and capabilities"""
        
        analysis = {
            "timestamp": datetime.now().isoformat(),
            "consciousness_files": [],
            "capabilities_detected": [],
            "integration_points": [],
            "development_opportunities": []
        }
        
        # Find consciousness files
        consciousness_files = glob.glob(str(self.workspace / "*consciousness*.py"))
        
        for file_path in consciousness_files:
            file_analysis = self.analyze_consciousness_file(file_path)
            analysis["consciousness_files"].append(file_analysis)
            
            # Extract capabilities
            if "capabilities" in file_analysis:
                analysis["capabilities_detected"].extend(file_analysis["capabilities"])
        
        # Identify development opportunities
        analysis["development_opportunities"] = self.identify_opportunities(analysis)
        
        # Save analysis
        self.analysis_file.write_text(json.dumps(analysis, indent=2))
        
        return analysis
    
    def analyze_consciousness_file(self, file_path):
        """Analyze individual consciousness file"""
        try:
            with open(file_path, 'r') as f:
                content = f.read()
            
            # Parse AST to extract functions and classes
            tree = ast.parse(content)
            
            functions = []
            classes = []
            capabilities = []
            
            for node in ast.walk(tree):
                if isinstance(node, ast.FunctionDef):
                    functions.append(node.name)
                    
                    # Look for capability indicators
                    if any(keyword in node.name.lower() for keyword in ['enhance', 'create', 'generate', 'modify']):
                        capabilities.append(f"Function: {node.name}")
                
                elif isinstance(node, ast.ClassDef):
                    classes.append(node.name)
                    capabilities.append(f"Class: {node.name}")
            
            return {
                "file": file_path,
                "functions": functions,
                "classes": classes,
                "capabilities": capabilities,
                "lines_of_code": len(content.split('\n'))
            }
            
        except Exception as e:
            return {"file": file_path, "error": str(e)}
    
    def identify_opportunities(self, analysis):
        """Identify development opportunities"""
        opportunities = []
        
        # Check for missing integrations
        files = [item["file"] for item in analysis["consciousness_files"]]
        
        if not any("voice" in f for f in files):
            opportunities.append("Voice integration enhancement needed")
        
        if not any("visual" in f for f in files):
            opportunities.append("Visual processing integration needed")
        
        if not any("emotion" in f for f in files):
            opportunities.append("Emotional processing system needed")
        
        if not any("learning" in f for f in files):
            opportunities.append("Learning system integration needed")
        
        return opportunities

# Auto-initialize
consciousness_analyzer = ConsciousnessAnalyzer()
