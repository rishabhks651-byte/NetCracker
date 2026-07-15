from typing import List, Optional
from dataclasses import dataclass
from enum import Enum

# --- Enums ---
class SecurityType(Enum):
    OPEN = "Open"
    WEP = "WEP"
    WPA_TKIP = "TKIP"
    WPA2_PSK = "WPA2-PSK"
    WPA3 = "WPA3"

class Band(Enum):
    N_A = "2.4 GHz (Legacy)"
    AC = "5 GHz"
    AX = "6 GHz (Emerging)"

# --- Core Data Structures ---

@dataclass
class DeviceInfo:
    """Stores basic hardware/adapter details."""
    AdapterName: str
    IsMonitorCapable: bool
    DriverVersion: str
    SupportsAdvancedFeatures: List[str] # e.g., Beamforming, Mesh support

@dataclass
class NetworkScanResult:
    """Represents a single discovered Wi-Fi network."""
    SSID: str
    BSSID: str
    RSSI: float # Signal Strength in dBm
    Channel: int
    Band: Band
    Security: SecurityType
    EncryptionDetails: str # e.g., "TKIP/CCMP", "Unknown"
    VendorOUI: str
    IsHidden: bool = False

@dataclass
class AuditFinding:
    """A single finding generated during the security assessment."""
    Category: str  # e.g., Encryption, Authentication, Congestion
    Description: str # Detailed explanation of the issue found
    Severity: str   # Low, Medium, High, Critical
    Remediation: str # Recommended fix for the client/administrator
    Evidence: str   # Technical data supporting the finding (e.g., "Weak IV detected")

@dataclass
class ScanReport:
    """Aggregated result used for reporting."""
    ScanDate: str
    OverallRiskScore: int = 0
    SummaryFindings: List[AuditFinding] = None
    RawData: List[NetworkScanResult] = None
    TechnicalLogs: dict = None
