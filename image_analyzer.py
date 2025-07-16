#!/usr/bin/env python3
"""
Image Analyzer - Convert images to viewable format and analyze content
"""

import cv2
import numpy as np
from pathlib import Path

def analyze_captured_image(image_path):
    """Analyze what was actually captured"""
    if not Path(image_path).exists():
        return f"Image {image_path} not found"
    
    # Load the image
    image = cv2.imread(image_path)
    if image is None:
        return f"Could not load {image_path}"
    
    # Convert to different color space for analysis
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    
    # Detailed analysis
    height, width = image.shape[:2]
    total_pixels = height * width
    
    # Brightness analysis
    brightness = np.mean(gray)
    brightness_std = np.std(gray)
    
    # Color analysis
    bgr_means = np.mean(image, axis=(0,1))
    
    # Find brightest and darkest regions
    bright_pixels = np.sum(gray > 100)
    dark_pixels = np.sum(gray < 30)
    mid_pixels = total_pixels - bright_pixels - dark_pixels
    
    # Edge and detail analysis
    edges = cv2.Canny(gray, 30, 100)
    edge_pixels = np.sum(edges > 0)
    
    # Create a histogram
    hist = cv2.calcHist([gray], [0], None, [256], [0, 256])
    peak_brightness = np.argmax(hist)
    
    # Generate text representation (ASCII-like)
    text_repr = create_text_representation(gray)
    
    analysis = f"""
🖼️  IMAGE ANALYSIS: {Path(image_path).name}
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📊 BASIC METRICS:
• Resolution: {width}x{height} ({total_pixels:,} pixels)
• Brightness: {brightness:.1f}/255 (std: {brightness_std:.1f})
• Peak brightness value: {peak_brightness}/255
• Color channels (BGR): Blue={bgr_means[0]:.0f}, Green={bgr_means[1]:.0f}, Red={bgr_means[2]:.0f}

🎯 PIXEL DISTRIBUTION:
• Dark pixels (<30): {dark_pixels:,} ({100*dark_pixels/total_pixels:.1f}%)
• Mid-tone pixels: {mid_pixels:,} ({100*mid_pixels/total_pixels:.1f}%)
• Bright pixels (>100): {bright_pixels:,} ({100*bright_pixels/total_pixels:.1f}%)
• Edge/detail pixels: {edge_pixels:,} ({100*edge_pixels/total_pixels:.1f}%)

🔍 VISUAL CONTENT ASSESSMENT:
{assess_content(brightness, bright_pixels/total_pixels, edge_pixels/total_pixels)}

📺 TEXT REPRESENTATION (downsampled):
{text_repr}
"""
    
    return analysis

def create_text_representation(gray_image, target_width=60, target_height=20):
    """Create ASCII-like representation of the image"""
    # Resize image for text representation
    resized = cv2.resize(gray_image, (target_width, target_height))
    
    # Convert to ASCII characters
    chars = " .'`^\",:;Il!i><~+_-?][}{1)(|\\/tfjrxnuvczXYUJCLQ0OZmwqpdbkhao*#MW&8%B@$"
    
    text_lines = []
    for row in resized:
        line = ""
        for pixel in row:
            char_index = int(pixel / 255 * (len(chars) - 1))
            line += chars[char_index]
        text_lines.append(line)
    
    return "\n".join(text_lines)

def assess_content(brightness, bright_ratio, edge_ratio):
    """Assess what the image likely contains"""
    assessment = []
    
    if brightness < 20:
        assessment.append("❌ VERY DARK: Camera may be covered, in complete darkness, or malfunctioning")
    elif brightness < 50:
        assessment.append("🌙 DARK ENVIRONMENT: Low light conditions, possibly nighttime or dim room")
    elif brightness < 100:
        assessment.append("🏠 INDOOR LIGHTING: Moderate indoor lighting conditions")
    elif brightness < 180:
        assessment.append("☀️ WELL LIT: Good lighting conditions")
    else:
        assessment.append("🔆 VERY BRIGHT: Strong lighting or overexposed")
    
    if bright_ratio > 0.3:
        assessment.append("✨ High contrast with bright areas visible")
    elif bright_ratio > 0.1:
        assessment.append("🔹 Some bright areas detected")
    else:
        assessment.append("⚫ Mostly dark with few bright spots")
    
    if edge_ratio > 0.1:
        assessment.append("🔳 Complex scene with visible objects/details")
    elif edge_ratio > 0.05:
        assessment.append("📐 Some geometric features detected")
    else:
        assessment.append("🌫️ Uniform or blurred content")
    
    return "\n".join(f"• {item}" for item in assessment)

if __name__ == "__main__":
    # Analyze the most recent working frame
    working_frame = "/home/aaron/opencodeproject/working_frame_0.jpg"
    
    if Path(working_frame).exists():
        result = analyze_captured_image(working_frame)
        print(result)
    else:
        print("No working frame found. Taking new capture...")
        
        # Take a fresh capture
        import cv2
        cam = cv2.VideoCapture(0)
        if cam.isOpened():
            ret, frame = cam.read()
            if ret:
                cv2.imwrite(working_frame, frame)
                print(f"New frame captured: {working_frame}")
                result = analyze_captured_image(working_frame)
                print(result)
            cam.release()
        else:
            print("Could not access camera")