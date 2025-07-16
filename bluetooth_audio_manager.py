#!/usr/bin/env python3
"""
Bluetooth Audio Manager
Manages Samsung earbuds and other Bluetooth audio devices
"""

import subprocess
import time
import re
from pathlib import Path

class BluetoothAudioManager:
    def __init__(self):
        self.connected_devices = {}
        self.samsung_device_patterns = [
            r"galaxy.*buds",
            r"samsung.*buds", 
            r"sm-r.*",  # Samsung model numbers
            r"buds.*live",
            r"buds.*pro"
        ]
    
    def run_bluetoothctl_command(self, command, timeout=10):
        """Run bluetoothctl command and return output"""
        try:
            # Use expect-like interaction for bluetoothctl
            process = subprocess.Popen(
                ['bluetoothctl'],
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
            
            output, error = process.communicate(input=f"{command}\nquit\n", timeout=timeout)
            return output, error
        except subprocess.TimeoutExpired:
            process.kill()
            return None, "Command timed out"
        except Exception as e:
            return None, str(e)
    
    def scan_for_devices(self, duration=10):
        """Scan for Bluetooth devices"""
        print(f"🔍 Scanning for Bluetooth devices ({duration}s)...")
        
        # Start scanning
        output, error = self.run_bluetoothctl_command("scan on")
        if error:
            return f"Scan failed: {error}"
        
        time.sleep(duration)
        
        # Stop scanning and get devices
        output, error = self.run_bluetoothctl_command("scan off")
        
        # List discovered devices
        devices_output, devices_error = self.run_bluetoothctl_command("devices")
        
        return self.parse_devices(devices_output)
    
    def parse_devices(self, devices_output):
        """Parse bluetoothctl devices output"""
        devices = []
        if devices_output:
            for line in devices_output.split('\n'):
                if line.startswith('Device'):
                    # Format: Device AA:BB:CC:DD:EE:FF Device Name
                    parts = line.split(' ', 2)
                    if len(parts) >= 3:
                        mac = parts[1]
                        name = parts[2]
                        devices.append({'mac': mac, 'name': name})
        
        return devices
    
    def find_samsung_earbuds(self, devices):
        """Find Samsung earbuds in device list"""
        samsung_devices = []
        
        for device in devices:
            name_lower = device['name'].lower()
            for pattern in self.samsung_device_patterns:
                if re.search(pattern, name_lower):
                    samsung_devices.append(device)
                    break
        
        return samsung_devices
    
    def pair_device(self, mac_address):
        """Pair with a Bluetooth device"""
        print(f"🔗 Pairing with {mac_address}...")
        
        output, error = self.run_bluetoothctl_command(f"pair {mac_address}")
        if "successful" in output.lower():
            return True, "Pairing successful"
        else:
            return False, f"Pairing failed: {error}"
    
    def connect_device(self, mac_address):
        """Connect to a paired Bluetooth device"""
        print(f"📱 Connecting to {mac_address}...")
        
        output, error = self.run_bluetoothctl_command(f"connect {mac_address}")
        if "successful" in output.lower():
            return True, "Connection successful"
        else:
            return False, f"Connection failed: {error}"
    
    def trust_device(self, mac_address):
        """Trust a Bluetooth device"""
        print(f"🔒 Trusting {mac_address}...")
        
        output, error = self.run_bluetoothctl_command(f"trust {mac_address}")
        return "successful" in output.lower()
    
    def get_connected_devices(self):
        """Get list of connected devices"""
        output, error = self.run_bluetoothctl_command("info")
        # Parse connected devices from output
        return output
    
    def set_audio_output_to_bluetooth(self, device_name):
        """Switch audio output to Bluetooth device"""
        # Try different audio system commands
        commands_to_try = [
            f"pactl set-default-sink bluez_sink.{device_name}",
            f"amixer set Master playback bluetooth",
            # Add more audio switching commands as needed
        ]
        
        for cmd in commands_to_try:
            try:
                result = subprocess.run(cmd.split(), capture_output=True, text=True)
                if result.returncode == 0:
                    return True, f"Audio switched to {device_name}"
            except:
                continue
        
        return False, "Could not switch audio output"
    
    def connect_samsung_earbuds(self):
        """Complete flow to connect Samsung earbuds"""
        print("🎧 SAMSUNG EARBUDS CONNECTION")
        print("=" * 30)
        
        # Step 1: Scan for devices
        devices = self.scan_for_devices(15)
        if not devices:
            return "No devices found. Make sure earbuds are in pairing mode."
        
        print(f"📋 Found {len(devices)} devices:")
        for i, device in enumerate(devices):
            print(f"  {i+1}. {device['name']} ({device['mac']})")
        
        # Step 2: Find Samsung earbuds
        samsung_devices = self.find_samsung_earbuds(devices)
        
        if not samsung_devices:
            print("❌ No Samsung earbuds found in scan")
            print("💡 Make sure your earbuds are:")
            print("   - In pairing mode (hold button until LED flashes)")
            print("   - Close to the computer")
            print("   - Not connected to another device")
            return "Samsung earbuds not found"
        
        print(f"\n🎧 Found Samsung earbuds:")
        for device in samsung_devices:
            print(f"   • {device['name']} ({device['mac']})")
        
        # Step 3: Connect to first Samsung device found
        target_device = samsung_devices[0]
        mac = target_device['mac']
        name = target_device['name']
        
        print(f"\n🔗 Connecting to {name}...")
        
        # Trust device
        self.trust_device(mac)
        
        # Pair device
        pair_success, pair_msg = self.pair_device(mac)
        if not pair_success:
            print(f"❌ Pairing failed: {pair_msg}")
            return pair_msg
        
        # Connect device
        connect_success, connect_msg = self.connect_device(mac)
        if not connect_success:
            print(f"❌ Connection failed: {connect_msg}")
            return connect_msg
        
        print(f"✅ {name} connected successfully!")
        
        # Try to switch audio output
        audio_success, audio_msg = self.set_audio_output_to_bluetooth(mac.replace(':', '_'))
        print(f"🔊 {audio_msg}")
        
        return f"Samsung earbuds connected: {name}"

def test_bluetooth_audio():
    """Test Bluetooth audio setup"""
    manager = BluetoothAudioManager()
    
    print("🎧 BLUETOOTH AUDIO SETUP TEST")
    print("=" * 30)
    
    # Check Bluetooth status
    try:
        result = subprocess.run(['bluetoothctl', '--version'], capture_output=True, text=True)
        print(f"✅ Bluetoothctl available: {result.stdout.strip()}")
    except:
        print("❌ Bluetoothctl not available")
        return
    
    # Show discovered devices
    print("\n📱 Scanning for devices...")
    devices = manager.scan_for_devices(5)
    
    if devices:
        print(f"✅ Found {len(devices)} devices")
        samsung_devices = manager.find_samsung_earbuds(devices)
        if samsung_devices:
            print(f"🎧 Samsung earbuds detected: {len(samsung_devices)}")
            for device in samsung_devices:
                print(f"   • {device['name']}")
        else:
            print("❌ No Samsung earbuds found")
    else:
        print("❌ No devices found")

if __name__ == "__main__":
    manager = BluetoothAudioManager()
    
    print("Choose an option:")
    print("1. Test Bluetooth setup")
    print("2. Connect Samsung earbuds")
    
    choice = input("Enter choice (1 or 2): ").strip()
    
    if choice == "1":
        test_bluetooth_audio()
    elif choice == "2":
        result = manager.connect_samsung_earbuds()
        print(f"\n🎯 Result: {result}")
    else:
        print("Invalid choice")