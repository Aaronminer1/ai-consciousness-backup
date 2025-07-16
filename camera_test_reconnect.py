#!/usr/bin/env python3
"""
Camera Connection Test - Run this after reconnecting camera
"""

import cv2
import time
import subprocess

def test_camera_connection():
    """Test camera after reconnection"""
    print("🔍 CAMERA RECONNECTION TEST")
    print("=" * 40)
    
    # Check USB devices
    print("📱 Checking USB devices...")
    result = subprocess.run("lsusb | grep -i camera", shell=True, capture_output=True, text=True)
    if result.stdout:
        print(f"✅ Camera found: {result.stdout.strip()}")
    else:
        print("❌ No camera found in USB devices")
        return False
    
    # Check video devices
    result = subprocess.run("ls /dev/video*", shell=True, capture_output=True, text=True)
    if result.returncode == 0:
        print(f"✅ Video devices: {result.stdout.strip()}")
    else:
        print("❌ No video devices found")
        return False
    
    # Test camera capture
    print("\n📸 Testing camera capture...")
    camera = cv2.VideoCapture(0)
    
    if not camera.isOpened():
        print("❌ Could not open camera")
        return False
    
    print("✅ Camera opened successfully")
    
    # Wait for camera to initialize
    print("⏳ Initializing camera...")
    time.sleep(2)
    
    # Test multiple frames
    for i in range(5):
        ret, frame = camera.read()
        if ret:
            brightness = frame.mean()
            min_val, max_val = frame.min(), frame.max()
            print(f"Frame {i+1}: brightness={brightness:.1f}, range={min_val}-{max_val}")
            
            if max_val > 50:  # Good brightness range
                print(f"✅ WORKING! Saving test image...")
                cv2.imwrite(f"/home/aaron/opencodeproject/camera_working_test.jpg", frame)
                camera.release()
                return True
        else:
            print(f"❌ Frame {i+1}: Failed to capture")
        
        time.sleep(0.5)
    
    camera.release()
    print("⚠️ Camera responds but images are still very dark")
    return False

if __name__ == "__main__":
    success = test_camera_connection()
    if success:
        print("\n🎉 CAMERA IS WORKING! Ready for visual perception.")
    else:
        print("\n❌ Camera still has issues. Try different USB port or cable.")