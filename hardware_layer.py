import subprocess
import platform
from typing import List, Optional, Dict
from models import DeviceInfo, NetworkScanResult, SecurityType, Band

class HardwareLayer:
    """Handles all raw interactions with the operating system and physical interfaces."""

    def __init__(self):
        print("HardwareLayer Initialized: Ready to interface with OS.")
        # --- Initialize internal state for simulation fallback ---
        self.last_scan_data = []

    # ========================================================
    # 1. Adapter Status & Info (Dashboard Data)
    # ========================================================
    def get_adapter_status(self) -> Dict:
        """Simulates/calls OS tools to get connectivity metrics."""
        if platform.system() == "Windows":
            # Placeholder for calling netsh/WLAN APIs
            return {
                "Status": "Active", 
                "SignalStrength": "-65 dBm",
                "Channel": "6",
                "Frequency": "2.4 GHz",
                "InterfaceInfo": "Wi-Fi Adapter XYZ (Intel)",
                "DriverVersion": "19.22.1.203",
            }
        elif platform.system() == "Linux":
            # Placeholder for calling iwlist/nmcli
            return {
                "Status": "Active", 
                "SignalStrength": "-78 dBm (Via iw)",
                "Channel": "1",
                "Frequency": "5.2 GHz",
                "InterfaceInfo": "/dev/wlan0",
                "DriverVersion": "mac80216-core (Kernel)",
            }
        else: # macOS fallback
            return {
                "Status": "Active", 
                "SignalStrength": "-55 dBm",
                "Channel": "11",
                "Frequency": "2.4 GHz",
                "InterfaceInfo": "AirportLink Adapter (Built-in)",
                "DriverVersion": "Apple CoreWifi",
            }

    def check_monitor_mode(self) -> str:
        """Checks if monitor mode is feasible."""
        # Real implementation: try to run 'sudo airmon-ng zpanel' and check exit code/output.
        if platform.system() == "Linux":
            return "Feasible (Requires root access)"
        return "Estimated Feasible via API abstraction"

    def get_interface_info(self) -> Dict:
        """Returns adapter capabilities."""
        # Real implementation: subprocess call to iw list or similar.
        if platform.system() == "Linux":
            return {"AvailableAdapters": ["wlan0", "wlp2s0"], "MonitorSupport": True}
        return {"AvailableAdapters": ["Wi-Fi Controller"], "MonitorSupport": True}


    # ========================================================
    # 2. Network Discovery (Scanners)
    # ========================================================
    def discover_networks(self, num_scans: int = 10) -> List[NetworkScanResult]:
        """Performs active scanning using scapy or specialized libraries."""
        print("--> Executing simulated deep packet scan for networks...")

        # --- SIMULATED REAL DATA FOR DEMONSTRATION ---
        results = []

        # Simulate the successful discovery of several nodes with varying metrics
        nodes_data = [
            ("Enterprise_HQ", "AA:BB:CC:11:22:33", -45, 6, Band.AC, SecurityType.WPA2_PSK, "VendorA", False),
            ("CoffeeShop_Guest", "11:22:33:FF:EE:DD", -70, 1, Band.N_A, SecurityType.OPEN, "VendorB", True),
            ("IoT_Mesh_Net", "00:A1:B2:C3:D4:E5", -60, 9, Band.AX, SecurityType.WPA3, "VendorC", False),
            # Simulate a hidden network
            ("SecretPass", "AA:BB:CC:11:22:33", -50, 1, Band.AC, SecurityType.WEP, "VendorA", True)
        ]

        for ssid, bssid, rssi, ch, band, sec, oui, hidden in nodes_data:
            results.append(NetworkScanResult(
                SSID=ssid, 
                BSSID=bssid, 
                RSSI=rssi, 
                Channel=ch, 
                Band=band, 
                Security=sec, 
                EncryptionDetails="CCMP", # Assume WPA2 for simulation simplicity
                VendorOUI=oui, 
                IsHidden=hidden
            ))

        print(f"--> Discovery complete. Found {len(results)} potential nodes.")
        return results


    # ========================================================
    # 3. Packet Capture Metrics (Streaming)
    # ========================================================
    def get_capture_metrics(self, duration_seconds: int = 10) -> Dict:
        """Simulates real-time packet statistics collection."""
        # In a true implementation, this would poll the packet capture thread's internal counters.
        print("--> Fetching Packet Capture Metrics...")
        return {
            "LivePacketCount": 12456,
            "ManagementFrames": 3890, # Beacon/Probe count
            "BeaconFrames": 1200,
            "ProbeRequests": 750,
            "AuthFrames": 50,
            "AssociationFrames": 150,
            "ChannelUtilizationPct": "45%",
        }

    # ... (Methods for WPS Brute Force and Key Cracking would follow here)
