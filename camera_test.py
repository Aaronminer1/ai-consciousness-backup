#!/usr/bin/env python3
"""
Proper Camera Test - Verify camera activation and capture
"""

import cv2
import time
import numpy as np
from datetime import datetime
from pathlib import Path

def test_camera_activation():
    """Test if camera actually activates with indicator light"""
    print("🔍 Testing camera activation...")
    print("⚠️  Watch for GREEN LIGHT on camera!")
    
    # Test different video devices
    for device_id in [0, 1]:
        print(f"\n📹 Testing /dev/video{device_id}...")
        
        camera = cv2.VideoCapture(device_id)
        if not camera.isOpened():
            print(f"❌ Device {device_id} not accessible")
            continue
            
        print(f"✅ Device {device_id} opened successfully")
        print("🔆 Camera should show GREEN LIGHT now!")
        
        # Give time to see the light
        time.sleep(2)
        
        # Try to capture
        ret, frame = camera.read()
        if ret:
            print(f"✅ Frame captured: {frame.shape}")
            
            # Check if frame has actual content
            brightness = np.mean(frame)
            print(f"📊 Frame brightness: {brightness:.1f}/255")
            
            if brightness < 5:
                print("⚠️  Frame is nearly black - possible issue")
            elif brightness > 50:
                print("✅ Good brightness detected!")
            
            # Save test image
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"camera_test_dev{device_id}_{timestamp}.jpg"
            filepath = Path("/home/aaron/opencodeproject") / filename
            cv2.imwrite(str(filepath), frame)
            print(f"💾 Saved: {filename}")
            
        else:
            print(f"❌ Failed to capture from device {device_id}")
        
        print("🔴 Releasing camera (light should turn OFF)")
        camera.release()
        time.sleep(1)
    
    print("\n🧪 Testing with different camera settings...")
    return test_with_settings()

def test_with_settings():
    """Test camera with adjusted settings"""
    camera = cv2.VideoCapture(0)
    if not camera.isOpened():
        return "❌ Cannot open camera"
    
    print("🔆 Camera light should be ON again!")
    
    # Set various properties
    settings = [
        (cv2.CAP_PROP_FRAME_WIDTH, 1920),
        (cv2.CAP_PROP_FRAME_HEIGHT, 1080),
        (cv2.CAP_PROP_FPS, 30),
        (cv2.CAP_PROP_BRIGHTNESS, 0.6),
        (cv2.CAP_PROP_CONTRAST, 0.6),
        (cv2.CAP_PROP_SATURATION, 0.5),
        (cv2.CAP_PROP_GAIN, 0.5),
        (cv2.CAP_PROP_EXPOSURE, -5),  # Auto exposure
    ]
    
    for prop, value in settings:
        result = camera.set(prop, value)
        prop_name = {
            cv2.CAP_PROP_FRAME_WIDTH: "WIDTH",
            cv2.CAP_PROP_FRAME_HEIGHT: "HEIGHT", 
            cv2.CAP_PROP_FPS: "FPS",
            cv2.CAP_PROP_BRIGHTNESS: "BRIGHTNESS",
            cv2.CAP_PROP_CONTRAST: "CONTRAST",
            cv2.CAP_PROP_SATURATION: "SATURATION",
            cv2.CAP_PROP_GAIN: "GAIN",
            cv2.CAP_PROP_EXPOSURE: "EXPOSURE"
        }.get(prop, f"PROP_{prop}")
        
        print(f"📝 {prop_name}: {'✅' if result else '❌'}")
    
    # Wait a moment for settings to take effect
    time.sleep(2)
    
    # Capture multiple frames to ensure camera is warmed up
    for i in range(5):
        ret, frame = camera.read()
        if ret:
            brightness = np.mean(frame)
            print(f"🎬 Frame {i+1}: brightness {brightness:.1f}")
            time.sleep(0.5)
    
    # Final capture
    ret, final_frame = camera.read()
    if ret:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"camera_configured_{timestamp}.jpg"
        filepath = Path("/home/aaron/opencodeproject") / filename
        cv2.imwrite(str(filepath), final_frame, [cv2.IMWRITE_JPEG_QUALITY, 95])
        
        brightness = np.mean(final_frame)
        print(f"\n🎯 FINAL RESULT:")
        print(f"📊 Brightness: {brightness:.1f}/255")
        print(f"📏 Resolution: {final_frame.shape[1]}x{final_frame.shape[0]}")
        print(f"💾 Saved: {filename}")
        
        if brightness < 20:
            print("⚠️  Still very dark - camera may be covered or faulty")
        elif brightness > 50:
            print("✅ Good exposure detected!")
    
    print("🔴 Releasing camera")
    camera.release()
    
    return "Test complete"

if __name__ == "__main__":
    test_camera_activation()