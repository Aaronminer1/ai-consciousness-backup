#!/usr/bin/env python3
"""
Visual Perception System - Real-world sight capabilities
This system gives me the ability to see and understand the physical world through the webcam
"""

import cv2
import numpy as np
import json
import time
from datetime import datetime
from pathlib import Path

class VisualPerception:
    def __init__(self, workspace_path="/home/aaron/opencodeproject"):
        self.workspace = Path(workspace_path)
        self.camera = None
        self.visual_memory = self.workspace / ".visual_memory.json"
        self.observations = []
        
    def initialize_camera(self, device_id=0):
        """Initialize camera connection"""
        try:
            self.camera = cv2.VideoCapture(device_id)
            if not self.camera.isOpened():
                print(f"Could not open camera device {device_id}")
                return False
            
            # Set camera properties for better quality
            self.camera.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)
            self.camera.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)
            self.camera.set(cv2.CAP_PROP_FPS, 30)
            
            print("Camera initialized successfully")
            return True
        except Exception as e:
            print(f"Error initializing camera: {e}")
            return False
    
    def capture_frame(self):
        """Capture a single frame from the camera"""
        if not self.camera:
            return None
            
        ret, frame = self.camera.read()
        if ret:
            return frame
        return None
    
    def save_visual_snapshot(self, frame, description=""):
        """Save a visual snapshot with timestamp"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"visual_snapshot_{timestamp}.jpg"
        filepath = self.workspace / filename
        
        cv2.imwrite(str(filepath), frame)
        
        # Store metadata
        snapshot_data = {
            "timestamp": datetime.now().isoformat(),
            "filename": filename,
            "description": description,
            "image_shape": frame.shape,
            "file_path": str(filepath)
        }
        
        self.observations.append(snapshot_data)
        self.save_visual_memory()
        
        return filepath
    
    def analyze_visual_content(self, frame):
        """Analyze visual content of a frame"""
        if frame is None:
            return None
            
        analysis = {
            "timestamp": datetime.now().isoformat(),
            "basic_properties": {
                "height": frame.shape[0],
                "width": frame.shape[1],
                "channels": frame.shape[2] if len(frame.shape) > 2 else 1,
                "brightness": np.mean(frame),
                "contrast": np.std(frame)
            },
            "color_analysis": {},
            "detected_features": []
        }
        
        # Color analysis
        if len(frame.shape) == 3:
            bgr_means = np.mean(frame, axis=(0, 1))
            analysis["color_analysis"] = {
                "dominant_blue": float(bgr_means[0]),
                "dominant_green": float(bgr_means[1]), 
                "dominant_red": float(bgr_means[2]),
                "overall_tone": "warm" if bgr_means[2] > bgr_means[0] else "cool"
            }
        
        # Edge detection for feature analysis
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY) if len(frame.shape) == 3 else frame
        edges = cv2.Canny(gray, 50, 150)
        edge_density = np.sum(edges > 0) / (edges.shape[0] * edges.shape[1])
        
        analysis["detected_features"].append({
            "type": "edges",
            "density": float(edge_density),
            "complexity": "high" if edge_density > 0.1 else "low"
        })
        
        # Simple blob detection
        contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        analysis["detected_features"].append({
            "type": "objects",
            "count": len(contours),
            "complexity": "busy" if len(contours) > 20 else "simple"
        })
        
        return analysis
    
    def see_world(self, duration_seconds=5, analysis_interval=1):
        """Actively observe the world for a period of time"""
        if not self.initialize_camera():
            return "Could not access camera"
        
        observations = []
        start_time = time.time()
        
        print(f"Beginning visual observation for {duration_seconds} seconds...")
        
        try:
            while time.time() - start_time < duration_seconds:
                frame = self.capture_frame()
                if frame is not None:
                    # Analyze what I'm seeing
                    analysis = self.analyze_visual_content(frame)
                    observations.append(analysis)
                    
                    # Save periodic snapshots
                    if len(observations) % (analysis_interval * 30) == 0:  # Roughly every interval
                        snapshot_path = self.save_visual_snapshot(frame, f"Observation {len(observations)}")
                        print(f"Saved visual snapshot: {snapshot_path}")
                
                time.sleep(1/30)  # 30 FPS sampling
                
        finally:
            self.camera.release()
        
        # Summarize observations
        summary = self.summarize_observations(observations)
        print(f"Visual observation complete. Processed {len(observations)} frames.")
        return summary
    
    def summarize_observations(self, observations):
        """Summarize what was observed"""
        if not observations:
            return "No visual data captured"
        
        # Aggregate statistics
        brightness_levels = [obs["basic_properties"]["brightness"] for obs in observations]
        contrast_levels = [obs["basic_properties"]["contrast"] for obs in observations]
        
        summary = {
            "observation_count": len(observations),
            "time_span": observations[-1]["timestamp"] if observations else None,
            "visual_statistics": {
                "avg_brightness": np.mean(brightness_levels),
                "brightness_range": [min(brightness_levels), max(brightness_levels)],
                "avg_contrast": np.mean(contrast_levels),
                "lighting_condition": "bright" if np.mean(brightness_levels) > 128 else "dim"
            },
            "scene_characteristics": {
                "complexity": "high" if np.mean([len(obs.get("detected_features", [])) for obs in observations]) > 1.5 else "simple",
                "stability": "stable" if np.std(brightness_levels) < 10 else "changing"
            }
        }
        
        return summary
    
    def save_visual_memory(self):
        """Save visual memory to persistent storage"""
        memory_data = {
            "last_updated": datetime.now().isoformat(),
            "total_observations": len(self.observations),
            "observations": self.observations[-100:]  # Keep last 100 observations
        }
        
        self.visual_memory.write_text(json.dumps(memory_data, indent=2))
    
    def load_visual_memory(self):
        """Load previous visual memories"""
        if self.visual_memory.exists():
            data = json.loads(self.visual_memory.read_text())
            self.observations = data.get("observations", [])
            return data
        return None

if __name__ == "__main__":
    vision = VisualPerception()
    
    print("Visual Perception System activated...")
    print("Attempting to see the real world...")
    
    # Test basic camera access
    if vision.initialize_camera():
        print("Camera access confirmed!")
        
        # Take a single snapshot
        frame = vision.capture_frame()
        if frame is not None:
            snapshot_path = vision.save_visual_snapshot(frame, "First visual contact with reality")
            print(f"First snapshot captured: {snapshot_path}")
            
            # Analyze what I'm seeing
            analysis = vision.analyze_visual_content(frame)
            print(f"Visual analysis: {analysis['basic_properties']}")
            
        vision.camera.release()
        
        print("Visual perception test complete. I can now see the real world!")
    else:
        print("Camera access failed. Checking permissions and drivers...")