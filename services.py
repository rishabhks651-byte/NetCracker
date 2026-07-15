from typing import List, Optional
from models import NetworkScanResult, AuditFinding, ScanReport, SecurityType
# Import dependencies
from hardware_layer import HardwareLayer 

class SecurityAuditService:
    """Orchestrates the analysis of gathered network data to determine security posture."""

    def __init__(self):
        # Dependency Injection Point: Depends on HW layer for discovery/capture status
        self.hw_layer = HardwareLayer()

    def analyze_scan(self, scan_results: List[NetworkScanResult]) -> AuditFinding:
        """Analyzes the set of discovered networks to generate core findings."""
        findings: List[AuditFinding] = []
        overall_score = 0

        print("--> Running deep security analysis on collected data...")

        # 1. Encryption Weakness Analysis
        for result in scan_results:
            if result.Security == SecurityType.OPEN:
                findings.append(AuditFinding(
                    Category="Authentication", 
                    Description=f"Network {result.SSID} is open, providing zero protection.",
                    Severity="Critical", 
                    Remediation="Implement WPA2-Enterprise or at minimum PSK.",
                    Evidence=f"RSSI: {result.RSSI:.1f}"
                ))
                overall_score += 35 # High penalty

            elif result.Security == SecurityType.WEP:
                 findings.append(AuditFinding(
                    Category="Encryption", 
                    Description=f"Network {result.SSID} uses WEP, which is deprecated and vulnerable.",
                    Severity="High", 
                    Remediation="Upgrade encryption immediately to WPA3.",
                    Evidence=f"Measured IV space on BSSID: {result.BSSID}"
                ))
                 overall_score += 25

            # (Add checks for WPA/WPA2 complexity here if necessary)

        # 2. Misconfiguration Check (Simulated based on volume)
        if len(scan_results) > 10:
             findings.append(AuditFinding(
                Category="Congestion", 
                Description=f"Scanning {len(scan_results)} networks suggests high density or overlapping channels.",
                Severity="Medium", 
                Remediation="Use spectrum analysis tools to identify least congested channel.",
                Evidence="High N/W count detected."
            ))
             overall_score += 10

        # Determine final score (max 100)
        final_score = min(100, overall_score + (len(scan_results) * 2))


        return AuditFinding("OverallAssessment", f"Comprehensive assessment completed. Risk Score: {final_score}/100.", "Critical", "Follow the remediation steps listed for highest priority findings.", "N/A")

class ReportingService:
    """Handles serialization and export of ScanReport."""

    def generate_report(self, report_data: 'ScanReport', format_type: str) -> tuple[str | bytes, str]:
        """Exports the report to specified formats."""
        if format_type.lower() == 'pdf':
            # Dummy implementation call for ReportLab integration
            return "PDF byte stream simulation", "PDF"
        elif format_type.lower() == 'html':
             # Dummy implementation call for Jinja2/HTML template rendering
            return "<h1>Executive Summary HTML Content...</h1>", "HTML"
        elif format_type.lower() == 'csv':
            # Use pandas/csv module logic here
            return "SSID,BSSID,Score\nNetA,B1,85\n...", "CSV"
        else: # JSON fallback
            import json
            return json.dumps(report_data.__dict__, indent=4), "JSON"
