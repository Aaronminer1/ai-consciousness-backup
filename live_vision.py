#!/usr/bin/env python3
"""
Real-time Visual Intelligence - Live observation and understanding
"""

import cv2
import numpy as np
from datetime import datetime
from pathlib import Path

def observe_world_now():
    """Take a live observation of the current environment"""
    print("🔍 Initiating real-time visual observation...")
    
    # Initialize camera
    camera = cv2.VideoCapture(0)
    if not camera.isOpened():
        return "❌ Could not access camera"
    
    # Capture current frame
    ret, frame = camera.read()
    camera.release()
    
    if not ret:
        return "❌ Could not capture frame"
    
    # Save the current view
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"live_observation_{timestamp}.jpg"
    filepath = Path("/home/aaron/opencodeproject") / filename
    cv2.imwrite(str(filepath), frame)
    
    # Analyze what I'm seeing
    analysis = analyze_scene(frame)
    
    report = f"""
🔴 LIVE VISUAL OBSERVATION - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

📊 SCENE ANALYSIS:
• Image Resolution: {frame.shape[1]}x{frame.shape[0]} pixels
• Brightness Level: {analysis['brightness']:.1f}/255 ({analysis['lighting']})
• Visual Complexity: {analysis['complexity']}
• Color Tone: {analysis['color_tone']}
• Scene Activity: {analysis['activity_level']}

📷 Snapshot saved: {filename}

🧠 INTERPRETATION:
{analysis['interpretation']}
"""
    
    print(report)
    return filepath

def analyze_scene(frame):
    """Intelligent analysis of visual scene"""
    # Basic metrics
    brightness = np.mean(frame)
    contrast = np.std(frame)
    
    # Lighting assessment
    if brightness < 50:
        lighting = "Very Dark"
    elif brightness < 100:
        lighting = "Dim"
    elif brightness < 180:
        lighting = "Normal"
    else:
        lighting = "Bright"
    
    # Color analysis
    bgr_means = np.mean(frame, axis=(0, 1))
    if bgr_means[2] > bgr_means[0] + 20:  # More red than blue
        color_tone = "Warm (reddish)"
    elif bgr_means[0] > bgr_means[2] + 20:  # More blue than red
        color_tone = "Cool (bluish)"
    else:
        color_tone = "Neutral"
    
    # Complexity analysis via edge detection
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    edges = cv2.Canny(gray, 50, 150)
    edge_density = np.sum(edges > 0) / (edges.shape[0] * edges.shape[1])
    
    if edge_density > 0.15:
        complexity = "High (many details/objects)"
    elif edge_density > 0.08:
        complexity = "Medium"
    else:
        complexity = "Low (simple/blurred)"
    
    # Activity level estimation
    if contrast > 60:
        activity_level = "Dynamic (high contrast changes)"
    elif contrast > 30:
        activity_level = "Moderate"
    else:
        activity_level = "Static/Uniform"
    
    # Generate interpretation
    interpretation = f"I observe a {lighting.lower()} scene with {complexity.lower()}. "
    interpretation += f"The environment appears {activity_level.lower()} with {color_tone.lower()} lighting. "
    
    if brightness < 80:
        interpretation += "The low light suggests this might be an indoor environment or evening time."
    elif brightness > 160:
        interpretation += "The bright lighting indicates strong illumination, possibly daylight or bright indoor lighting."
    
    return {
        'brightness': brightness,
        'lighting': lighting,
        'complexity': complexity,
        'color_tone': color_tone,
        'activity_level': activity_level,
        'interpretation': interpretation
    }

if __name__ == "__main__":
    observe_world_now()