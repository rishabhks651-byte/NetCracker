### 🛡️ NetCracker: Wi-Fi Security Assessment Suite

**The Professional Tool for Comprehensive Wireless Penetration Testing.**

***License   MIT License   
Python Version  3.10+***

NetCracker is an enterprise-grade desktop application designed to provide authorized security professionals with a unified, high-performance platform for conducting deep Wi-Fi security assessments. It moves beyond simple scanners by integrating real-time monitoring, advanced analytical engines, and professional reporting capabilities into one cohesive dashboard.
## ✨ Features Overview

    💎 Glassmorphism Dashboard: Modern, dark theme UI adhering to Material Design principles for excellent usability.
    📶 Real-Time Monitoring: Live status of adapter health, signal strength (RSSI), channel utilization, and connection metrics.
    🌐 Network Discovery Engine: Actively scans the environment for nearby SSIDs, capturing critical details like BSSID, RSSI, Band, and vendor OUI.
    <0xF0><0x9F><0x97><0x82>️ Adapter Manager: Tools to detect capabilities, manage monitor mode activation, and configure underlying interfaces.
    📡 Packet Capture &amp; Stream Metrics: Supports live sniffing, tracking frame counts for management, beacon, probe, and association frames in real time.
    🚨 Security Audit Core: The intelligence layer that automatically analyzes discovered networks against known vulnerabilities (WEP weakness, open authentication, etc.), generating a weighted Risk Score.
    📝 Comprehensive Reporting: Exports findings, evidence, remediation steps, and the overall risk posture into professional PDF, HTML, CSV, and JSON formats.

## 🏗️ Architecture & Technology Stack

NetCracker is built using Clean Architecture, ensuring every component—from UI widgets to OS interaction—is independently testable:

    UI Layer: PyQt6 (For rich, customizable desktop experience).
    Hardware Layer: Direct integration wrappers for scapy and platform-specific CLI tools (iwlist, netsh) for maximum compatibility.
    Business Logic: Orchestrated via services that calculate risk scores based on aggregated data from the hardware layer.
    Data Persistence: Local SQLite3 database (for scan history and metrics).

## 🚀 Tech Stack Used:

Category 	Technology 	Purpose
Framework 	Python 3.10+, PyQt6 	Core application GUI and logic binding.
Networking 	Scapy 	Packet crafting, sniffing, and analysis.
Reporting 	ReportLab, pandas 	Generating structured PDF/CSV reports from complex findings models.
Styling 	QSS (Qt Style Sheets) 	Implementing Glassmorphism and professional visual styling.

# ⚙️ Installation & Setup

    Prerequisites: Ensure you have the required system utilities installed on your OS (e.g., airmon-ng package on Linux for full functionality).
    Cloning: Clone this repository:
```bash
    git clone https://github.com/rishabhks651-byte/NetCracker.git
    cd netcracker
```
    Virtual Environment (Recommended):
```bash
    python -m venv venv
    source venv/bin/activate   # Linux/macOS
    venv\Scripts\activate      # Windows
```
    Install Dependencies:
```bash
    pip install -r requirements.txt
```
## 💻 Usage Guide

# 1. Running the Application

Execute the main entry point:
```bash
python main_app.py
```
# 2. Workflow Walkthrough

    System Initialization: The Dashboard loads, displaying live connection metrics (SSID, RSSI, Driver Info). If hardware is unavailable, descriptive error messages are shown instead of failing.
    Discovery Scan: Click 🔍 Start Network Discovery. The system runs the multi-threaded scan, populating the network list and updating the UI summary with immediate findings.
    Packet Capture: Click 📡 Start Packet Capture. A dedicated monitoring window (or status bar area) updates in real-time with frame counts (Management/Beacon/Probe).
    Security Audit: Click 🛡️ Run Security Audit. The Business Logic layer processes all gathered data, calculating the overall risk score and flagging specific weak points.
    Review & Report: Review the detailed findings on the dashboard. Select 📄 Generate Report to export structured deliverables (PDF/HTML are primary targets).

# ⚠️ Development Notes & Limitations

    Authorization Notice: The application enforces a mandatory, visible legal authorization modal upon startup for all testing functions.
    Platform Dependency: Hardware interaction (HardwareLayer) contains OS-specific code paths (Linux/Windows/macOS) that must be maintained and updated with platform changes.
    Glassmorphism Blending: Achieving true system-wide blur requires deep integration hooks, but the current implementation uses enhanced QSS to simulate the effect using strong gradients and transparency.

# 📚 Documentation & Contributions

We are actively developing modules for advanced attack vectors (e.g., dictionary brute-force cracking). All improvements should follow the Clean Architecture guidelines to maintain separation of concerns.

Contributing:

    Fork the repository and create a feature branch (git checkout -b feature/AmazingFeature).
    Implement changes, ensuring unit tests are updated (pytest).
    Commit your changes (git commit -m 'feat: Added X functionality').
    Push to the develop branch (git push origin develop).

Contact: Rishabh Kumar Singh | rishabhks651@gmail.com 
