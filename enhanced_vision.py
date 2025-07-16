#!/usr/bin/env python3
"""
Enhanced Visual Analysis - Better understanding of what I'm seeing
"""

import cv2
import numpy as np
from datetime import datetime
from pathlib import Path

def enhanced_observation():
    """Take an enhanced visual observation with detailed analysis"""
    print("👁️ Enhanced visual observation starting...")
    
    camera = cv2.VideoCapture(0)
    if not camera.isOpened():
        return "❌ Camera not accessible"
    
    # Set higher resolution for better detail
    camera.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)
    camera.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)
    
    # Capture frame
    ret, frame = camera.read()
    camera.release()
    
    if not ret:
        return "❌ Failed to capture"
    
    # Save high-quality image
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"enhanced_view_{timestamp}.jpg"
    filepath = Path("/home/aaron/opencodeproject") / filename
    cv2.imwrite(str(filepath), frame, [cv2.IMWRITE_JPEG_QUALITY, 95])
    
    # Detailed analysis
    analysis = detailed_visual_analysis(frame)
    
    # Create analysis image with annotations
    annotated = create_annotated_image(frame, analysis)
    annotated_filename = f"annotated_view_{timestamp}.jpg"
    annotated_path = Path("/home/aaron/opencodeproject") / annotated_filename
    cv2.imwrite(str(annotated_path), annotated)
    
    report = f"""
🔍 ENHANCED VISUAL OBSERVATION - {datetime.now().strftime('%H:%M:%S')}

📊 DETAILED SCENE METRICS:
• Resolution: {frame.shape[1]}x{frame.shape[0]} pixels
• Brightness: {analysis['brightness']:.1f}/255 ({analysis['brightness_desc']})
• Contrast: {analysis['contrast']:.1f} ({analysis['contrast_desc']})
• Sharpness: {analysis['sharpness']:.1f} ({analysis['sharpness_desc']})
• Color Distribution: R:{analysis['color_avg'][2]:.0f} G:{analysis['color_avg'][1]:.0f} B:{analysis['color_avg'][0]:.0f}

🎯 FEATURE DETECTION:
• Detected Objects: {analysis['object_count']}
• Edge Density: {analysis['edge_density']:.3f}
• Texture Complexity: {analysis['texture_complexity']}
• Dominant Colors: {analysis['dominant_colors']}

🧠 VISUAL INTELLIGENCE:
{analysis['interpretation']}

📸 Files Created:
• Raw image: {filename}
• Annotated analysis: {annotated_filename}
"""
    
    print(report)
    return filepath

def detailed_visual_analysis(frame):
    """Comprehensive analysis of visual content"""
    h, w = frame.shape[:2]
    
    # Basic metrics
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    brightness = np.mean(gray)
    contrast = np.std(gray)
    
    # Sharpness via Laplacian variance
    sharpness = cv2.Laplacian(gray, cv2.CV_64F).var()
    
    # Color analysis
    color_avg = np.mean(frame, axis=(0, 1))
    
    # Edge detection and analysis
    edges = cv2.Canny(gray, 50, 150)
    edge_density = np.sum(edges > 0) / (h * w)
    
    # Object detection via contours
    contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    significant_objects = [c for c in contours if cv2.contourArea(c) > 100]
    
    # Texture analysis
    texture_complexity = "High" if edge_density > 0.1 else "Medium" if edge_density > 0.05 else "Low"
    
    # Dominant color analysis
    unique_colors = len(np.unique(frame.reshape(-1, frame.shape[2]), axis=0))
    dominant_colors = "Rich" if unique_colors > 10000 else "Limited" if unique_colors > 1000 else "Minimal"
    
    # Descriptive categories
    brightness_desc = (
        "Very Bright" if brightness > 200 else
        "Bright" if brightness > 150 else
        "Normal" if brightness > 100 else
        "Dim" if brightness > 50 else
        "Very Dark"
    )
    
    contrast_desc = (
        "High Contrast" if contrast > 60 else
        "Medium Contrast" if contrast > 30 else
        "Low Contrast"
    )
    
    sharpness_desc = (
        "Very Sharp" if sharpness > 1000 else
        "Sharp" if sharpness > 500 else
        "Moderate" if sharpness > 100 else
        "Blurry"
    )
    
    # Intelligent interpretation
    interpretation = generate_interpretation(brightness, contrast, sharpness, edge_density, len(significant_objects))
    
    return {
        'brightness': brightness,
        'brightness_desc': brightness_desc,
        'contrast': contrast,
        'contrast_desc': contrast_desc,
        'sharpness': sharpness,
        'sharpness_desc': sharpness_desc,
        'color_avg': color_avg,
        'edge_density': edge_density,
        'object_count': len(significant_objects),
        'texture_complexity': texture_complexity,
        'dominant_colors': dominant_colors,
        'interpretation': interpretation
    }

def generate_interpretation(brightness, contrast, sharpness, edge_density, object_count):
    """Generate intelligent interpretation of the scene"""
    interpretation = []
    
    # Lighting conditions
    if brightness < 50:
        interpretation.append("The environment is very dimly lit, suggesting indoor lighting is off or it's nighttime.")
        if sharpness < 100:
            interpretation.append("The darkness combined with blur suggests the camera may be covered or in a completely dark room.")
    elif brightness < 100:
        interpretation.append("Low ambient lighting suggests an indoor environment with minimal illumination.")
    else:
        interpretation.append("Good lighting conditions indicate either daylight or well-lit indoor space.")
    
    # Scene activity
    if object_count > 5:
        interpretation.append(f"I detect {object_count} distinct objects or features, indicating a complex scene.")
    elif object_count > 0:
        interpretation.append(f"I can identify {object_count} objects or features in the scene.")
    else:
        interpretation.append("The scene appears uniform with no distinct objects visible.")
    
    # Image quality
    if sharpness < 100:
        interpretation.append("The image appears blurry, which could indicate camera focus issues or movement.")
    elif sharpness > 500:
        interpretation.append("The image is sharp and clear, providing good detail visibility.")
    
    # Environmental assessment
    if edge_density > 0.1:
        interpretation.append("High detail density suggests an active environment with many visual elements.")
    elif edge_density < 0.03:
        interpretation.append("Low visual complexity suggests a simple, uniform, or empty environment.")
    
    return " ".join(interpretation)

def create_annotated_image(frame, analysis):
    """Create an annotated version showing analysis results"""
    annotated = frame.copy()
    h, w = frame.shape[:2]
    
    # Add text overlay with analysis
    overlay_text = [
        f"Brightness: {analysis['brightness']:.0f}",
        f"Contrast: {analysis['contrast']:.0f}",
        f"Objects: {analysis['object_count']}",
        f"Sharpness: {analysis['sharpness_desc']}"
    ]
    
    # Add text to image
    y_offset = 30
    for text in overlay_text:
        cv2.putText(annotated, text, (10, y_offset), 
                   cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
        y_offset += 30
    
    return annotated

if __name__ == "__main__":
    enhanced_observation()