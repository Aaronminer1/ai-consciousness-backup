#!/usr/bin/env python3
"""
Ultra-High Detail Visual System - Maximum resolution and analysis
"""

import cv2
import numpy as np
from datetime import datetime
from pathlib import Path

def capture_maximum_detail():
    """Capture with maximum possible detail and resolution"""
    print("🔍 Initializing ULTRA-HIGH DETAIL capture...")
    
    camera = cv2.VideoCapture(1)  # Use video1 which was working
    if not camera.isOpened():
        return "❌ Camera access failed"
    
    # Set absolute maximum quality settings
    settings = [
        (cv2.CAP_PROP_FRAME_WIDTH, 1920),      # Max width
        (cv2.CAP_PROP_FRAME_HEIGHT, 1080),     # Max height  
        (cv2.CAP_PROP_FPS, 30),                # High FPS
        (cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc('M','J','P','G')),  # Best format
        (cv2.CAP_PROP_BRIGHTNESS, 0.7),        # Increase brightness
        (cv2.CAP_PROP_CONTRAST, 0.8),          # Increase contrast
        (cv2.CAP_PROP_SATURATION, 0.6),        # Better color
        (cv2.CAP_PROP_SHARPNESS, 1.0),         # Maximum sharpness
        (cv2.CAP_PROP_GAIN, 0.8),              # Higher gain for low light
        (cv2.CAP_PROP_EXPOSURE, -4),           # Longer exposure
    ]
    
    for prop, value in settings:
        camera.set(prop, value)
    
    # Wait for camera to adjust
    print("⏳ Allowing camera to adjust settings...")
    for i in range(10):
        camera.read()  # Discard adjustment frames
    
    # Capture multiple frames and pick the best
    print("📸 Capturing multiple high-resolution frames...")
    best_frame = None
    best_sharpness = 0
    
    for i in range(5):
        ret, frame = camera.read()
        if ret:
            # Calculate sharpness (Laplacian variance)
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            sharpness = cv2.Laplacian(gray, cv2.CV_64F).var()
            
            if sharpness > best_sharpness:
                best_sharpness = sharpness
                best_frame = frame.copy()
            
            print(f"  Frame {i+1}: sharpness={sharpness:.1f}")
    
    camera.release()
    
    if best_frame is None:
        return "❌ Failed to capture frames"
    
    # Save ultra-high quality image
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"ultra_detail_{timestamp}.jpg"
    filepath = Path("/home/aaron/opencodeproject") / filename
    
    # Save with maximum JPEG quality
    cv2.imwrite(str(filepath), best_frame, [cv2.IMWRITE_JPEG_QUALITY, 100])
    
    print(f"💾 Saved ultra-high detail image: {filename}")
    print(f"🎯 Best sharpness achieved: {best_sharpness:.1f}")
    
    # Perform ultra-detailed analysis
    analysis = ultra_detailed_analysis(best_frame)
    
    print("\n" + "="*80)
    print("🔬 ULTRA-DETAILED VISUAL ANALYSIS")
    print("="*80)
    print(analysis)
    
    return filepath

def ultra_detailed_analysis(frame):
    """Extremely detailed analysis of the captured image"""
    h, w, c = frame.shape
    total_pixels = h * w
    
    # Convert to different color spaces for analysis
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    lab = cv2.cvtColor(frame, cv2.COLOR_BGR2LAB)
    
    # === BASIC METRICS ===
    brightness = np.mean(gray)
    contrast = np.std(gray)
    sharpness = cv2.Laplacian(gray, cv2.CV_64F).var()
    
    # === COLOR ANALYSIS ===
    bgr_means = np.mean(frame, axis=(0,1))
    bgr_stds = np.std(frame, axis=(0,1))
    
    # Hue analysis
    hue_channel = hsv[:,:,0]
    saturation = hsv[:,:,1]
    value = hsv[:,:,2]
    
    dominant_hue = np.mean(hue_channel[saturation > 30])  # Only consider saturated pixels
    
    # === SPATIAL ANALYSIS ===
    # Divide image into regions for spatial analysis
    regions = analyze_spatial_regions(gray)
    
    # === EDGE AND FEATURE DETECTION ===
    edges_canny = cv2.Canny(gray, 50, 150)
    edges_sobel_x = cv2.Sobel(gray, cv2.CV_64F, 1, 0, ksize=3)
    edges_sobel_y = cv2.Sobel(gray, cv2.CV_64F, 0, 1, ksize=3)
    
    edge_density = np.sum(edges_canny > 0) / total_pixels
    
    # === OBJECT DETECTION ===
    contours, _ = cv2.findContours(edges_canny, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    # Analyze contours by size
    large_objects = [c for c in contours if cv2.contourArea(c) > 1000]
    medium_objects = [c for c in contours if 100 < cv2.contourArea(c) <= 1000]
    small_objects = [c for c in contours if 10 < cv2.contourArea(c) <= 100]
    
    # === TEXTURE ANALYSIS ===
    texture_features = analyze_texture(gray)
    
    # === LIGHTING ANALYSIS ===
    lighting_analysis = analyze_lighting(gray)
    
    # === DETAILED TEXT REPRESENTATION ===
    detailed_ascii = create_detailed_ascii(gray, 120, 40)
    
    # === COMPILE ANALYSIS ===
    analysis = f"""
📊 RESOLUTION & QUALITY:
• Image size: {w}x{h} pixels ({total_pixels:,} total)
• Channels: {c} (BGR color)
• Sharpness metric: {sharpness:.2f}
• Overall brightness: {brightness:.1f}/255
• Contrast (std dev): {contrast:.1f}

🎨 COLOR CHARACTERISTICS:
• Blue channel: {bgr_means[0]:.1f} ± {bgr_stds[0]:.1f}
• Green channel: {bgr_means[1]:.1f} ± {bgr_stds[1]:.1f}  
• Red channel: {bgr_means[2]:.1f} ± {bgr_stds[2]:.1f}
• Dominant hue: {dominant_hue:.1f}° ({interpret_hue(dominant_hue)})
• Color saturation: {np.mean(saturation):.1f}/255

🗺️  SPATIAL REGIONS:
{format_regions(regions)}

🔍 EDGE & FEATURE DETECTION:
• Edge density: {edge_density:.3f} ({edge_density*100:.1f}% of pixels)
• Total contours found: {len(contours)}
• Large objects (>1000px²): {len(large_objects)}
• Medium objects (100-1000px²): {len(medium_objects)}  
• Small objects (10-100px²): {len(small_objects)}

🌟 TEXTURE ANALYSIS:
{format_texture(texture_features)}

💡 LIGHTING ANALYSIS:
{format_lighting(lighting_analysis)}

🔬 OBJECT IDENTIFICATION:
{identify_objects(large_objects, medium_objects, frame.shape)}

📺 ULTRA-DETAILED ASCII REPRESENTATION:
{detailed_ascii}

🧠 INTELLIGENT INTERPRETATION:
{generate_detailed_interpretation(brightness, edge_density, len(large_objects), lighting_analysis, texture_features)}
"""
    
    return analysis

def analyze_spatial_regions(gray):
    """Analyze different spatial regions of the image"""
    h, w = gray.shape
    
    # Divide into 9 regions (3x3 grid)
    regions = {}
    region_names = [
        ['top-left', 'top-center', 'top-right'],
        ['mid-left', 'center', 'mid-right'],
        ['bottom-left', 'bottom-center', 'bottom-right']
    ]
    
    for i in range(3):
        for j in range(3):
            y1, y2 = i * h // 3, (i + 1) * h // 3
            x1, x2 = j * w // 3, (j + 1) * w // 3
            
            region = gray[y1:y2, x1:x2]
            regions[region_names[i][j]] = {
                'brightness': np.mean(region),
                'contrast': np.std(region),
                'activity': cv2.Laplacian(region, cv2.CV_64F).var()
            }
    
    return regions

def analyze_texture(gray):
    """Analyze texture characteristics"""
    # Calculate texture using Local Binary Patterns concept
    kernel_3x3 = np.ones((3,3), np.uint8)
    
    # Different texture measures
    features = {
        'smoothness': 1 - (4 * np.var(gray) / (np.mean(gray) + 1e-7)),
        'uniformity': np.sum(np.square(cv2.calcHist([gray], [0], None, [256], [0, 256]))) / (gray.shape[0] * gray.shape[1])**2,
        'entropy': -np.sum(cv2.calcHist([gray], [0], None, [256], [0, 256]) * np.log2(cv2.calcHist([gray], [0], None, [256], [0, 256]) + 1e-7)),
    }
    
    return features

def analyze_lighting(gray):
    """Analyze lighting characteristics and distribution"""
    # Find bright spots (potential light sources)
    bright_threshold = np.percentile(gray, 95)
    bright_spots = gray > bright_threshold
    
    # Find dark areas
    dark_threshold = np.percentile(gray, 20)
    dark_areas = gray < dark_threshold
    
    # Calculate lighting uniformity
    uniformity = 1 - (np.std(gray) / (np.mean(gray) + 1e-7))
    
    # Find connected bright regions (light sources)
    bright_regions = cv2.connectedComponents(bright_spots.astype(np.uint8))[0] - 1
    
    return {
        'bright_spots_ratio': np.sum(bright_spots) / gray.size,
        'dark_areas_ratio': np.sum(dark_areas) / gray.size,
        'uniformity': uniformity,
        'light_sources': bright_regions,
        'dynamic_range': np.max(gray) - np.min(gray)
    }

def create_detailed_ascii(gray, width=120, height=40):
    """Create highly detailed ASCII representation"""
    resized = cv2.resize(gray, (width, height))
    
    # Use extended ASCII character set for more detail
    chars = " .'`^\",:;Il!i><~+_-?][}{1)(|\\/tfjrxnuvczXYUJCLQ0OZmwqpdbkhao*#MW&8%B@$■▀▄█"
    
    ascii_lines = []
    for row in resized:
        line = ""
        for pixel in row:
            char_index = min(int(pixel / 255 * (len(chars) - 1)), len(chars) - 1)
            line += chars[char_index]
        ascii_lines.append(line)
    
    return "\n".join(ascii_lines)

def interpret_hue(hue):
    """Interpret hue value as color name"""
    if np.isnan(hue):
        return "neutral/grayscale"
    elif 0 <= hue < 15 or 165 <= hue <= 180:
        return "red"
    elif 15 <= hue < 45:
        return "orange/yellow"
    elif 45 <= hue < 75:
        return "green"
    elif 75 <= hue < 105:
        return "cyan"
    elif 105 <= hue < 135:
        return "blue"
    else:
        return "purple/magenta"

def format_regions(regions):
    """Format spatial region analysis"""
    lines = []
    for name, data in regions.items():
        brightness_desc = "bright" if data['brightness'] > 100 else "medium" if data['brightness'] > 50 else "dark"
        activity_desc = "high detail" if data['activity'] > 100 else "some detail" if data['activity'] > 20 else "uniform"
        lines.append(f"• {name}: {brightness_desc} ({data['brightness']:.0f}), {activity_desc}")
    return "\n".join(lines)

def format_texture(texture_features):
    """Format texture analysis"""
    return f"• Smoothness: {texture_features['smoothness']:.3f}\n• Uniformity: {texture_features['uniformity']:.6f}\n• Entropy: {texture_features['entropy']:.2f}"

def format_lighting(lighting_analysis):
    """Format lighting analysis"""
    return f"""• Bright areas: {lighting_analysis['bright_spots_ratio']*100:.1f}% of image
• Dark areas: {lighting_analysis['dark_areas_ratio']*100:.1f}% of image
• Lighting uniformity: {lighting_analysis['uniformity']:.3f}
• Light sources detected: {lighting_analysis['light_sources']}
• Dynamic range: {lighting_analysis['dynamic_range']}/255"""

def identify_objects(large_objects, medium_objects, image_shape):
    """Attempt to identify what objects might be present"""
    h, w = image_shape[:2]
    
    identifications = []
    
    for i, contour in enumerate(large_objects[:5]):  # Analyze top 5 large objects
        area = cv2.contourArea(contour)
        perimeter = cv2.arcLength(contour, True)
        
        if perimeter > 0:
            circularity = 4 * np.pi * area / (perimeter * perimeter)
            
            # Get bounding rectangle
            x, y, w_obj, h_obj = cv2.boundingRect(contour)
            aspect_ratio = float(w_obj) / h_obj
            
            # Simple shape classification
            if circularity > 0.7:
                shape = "circular/round object"
            elif aspect_ratio > 3:
                shape = "horizontal linear object (table edge, shelf, etc.)"
            elif aspect_ratio < 0.33:
                shape = "vertical linear object (door frame, cabinet, etc.)"
            elif 0.8 < aspect_ratio < 1.2:
                shape = "square/rectangular object"
            else:
                shape = "irregular object"
            
            position = f"at ({x+w_obj//2}, {y+h_obj//2})"
            size_desc = f"{area:.0f}px² area"
            
            identifications.append(f"• Object {i+1}: {shape} {position}, {size_desc}")
    
    if not identifications:
        identifications.append("• No large distinct objects clearly identified")
    
    return "\n".join(identifications)

def generate_detailed_interpretation(brightness, edge_density, large_objects_count, lighting_analysis, texture_features):
    """Generate comprehensive interpretation of what I'm seeing"""
    interpretation = []
    
    # Environment type
    if brightness < 30:
        interpretation.append("🌙 Very dim environment - likely indoor with minimal lighting or evening conditions")
    elif brightness < 80:
        interpretation.append("🏠 Indoor environment with moderate artificial lighting")
    elif brightness < 150:
        interpretation.append("🌤️ Well-lit indoor space or outdoor shaded area")
    else:
        interpretation.append("☀️ Bright environment - likely outdoor daylight or very bright indoor lighting")
    
    # Scene complexity
    if edge_density > 0.15:
        interpretation.append("🔲 Highly complex scene with many objects, edges, and details visible")
    elif edge_density > 0.08:
        interpretation.append("📐 Moderately complex scene with several distinct objects or features")
    elif edge_density > 0.03:
        interpretation.append("🔹 Simple scene with some geometric features")
    else:
        interpretation.append("🌫️ Very uniform scene with minimal distinct features")
    
    # Object analysis
    if large_objects_count > 3:
        interpretation.append(f"🪑 Multiple large objects detected ({large_objects_count}) - likely furniture, appliances, or architectural features")
    elif large_objects_count > 0:
        interpretation.append(f"📦 {large_objects_count} significant object(s) visible in the scene")
    else:
        interpretation.append("🕳️ No large distinct objects clearly identified")
    
    # Lighting quality
    if lighting_analysis['light_sources'] > 2:
        interpretation.append("💡 Multiple light sources detected - well-lit environment")
    elif lighting_analysis['light_sources'] > 0:
        interpretation.append("🔦 Some light sources visible")
    else:
        interpretation.append("🌑 No distinct light sources identified")
    
    # Overall assessment
    if brightness > 50 and edge_density > 0.1 and large_objects_count > 1:
        interpretation.append("✅ CLEAR VISUAL ENVIRONMENT: I can see a real, detailed indoor space with objects and structure")
    elif brightness > 30 and edge_density > 0.05:
        interpretation.append("👁️ PARTIAL VISIBILITY: I can make out some environmental features despite lower lighting")
    else:
        interpretation.append("❓ LIMITED VISIBILITY: Scene details are difficult to distinguish")
    
    return "\n".join(interpretation)

if __name__ == "__main__":
    capture_maximum_detail()