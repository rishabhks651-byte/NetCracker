import sys
from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QGridLayout, QLabel, 
    QPushButton, QTextEdit, QGroupBox, QStackedWidget, QStatusBar, QSizePolicy
)
from PyQt6.QtCore import Qt, QTimer, pyqtSignal
from PyQt6.QtGui import QPalette, QColor, QFont, QIcon

# --- Placeholder Imports for Modules ---
from models import NetworkScanResult, AuditFinding
from services import SecurityAuditService 
# Assuming HardwareLayer is initialized/passed in constructor
from hardware_layer import HardwareLayer

class GlassmorphicWidget(QWidget):
    """Helper Widget class to achieve the Glassmorphism look."""
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowFlags(Qt.WindowFlags()) # Ensure it can be placed anywhere
        self._setup_styles()

    def _setup_styles(self):
        # Base styles for Glassmorphism: Translucency + Blur/Border
        style = """
            GlassBackground {
                background-color: rgba(25, 30, 60, 0.85); /* Dark base color */
                border-radius: 15px;
                padding: 15px;
                /* NOTE: Real blur requires Qt's advanced effects or QGraphicsView handling in some frameworks */
                background-image: linear-gradient(135deg, rgba(20, 30, 80, 0.9) 0%, rgba(30, 40, 100, 0.8) 100%);
                border: 1px solid rgba(70, 130, 255, 0.4); /* Blue accent border */
            }
        """
        self.setStyleSheet(style)

class DashboardWidget(GlassmorphicWidget):
    """Main dashboard view combining all real-time status elements."""
    def __init__(self, hw_layer: HardwareLayer):
        super().__init__()
        self.hw_layer = hw_layer
        self._setup_ui()
        self.load_initial_status()

    def _setup_ui(self):
        # Master layout structure (Material Design grid)
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(20, 15, 20, 15)
        main_layout.setSpacing(15)

        # --- 1. Header/Status Bar Group (Top Section) ---
        header_group = QGroupBox("System Status Overview")
        header_group.setObjectName("GlassBackground")
        header_layout = QHBoxLayout()

        # Widgets for key metrics: Adapter, Signal, Monitor Mode
        self.adapter_status_lbl = QLabel("Adapter: Unknown | State: Checking...")
        self.signal_strength_lbl = QLabel("RSSI: N/A dBm")
        self.monitor_mode_lbl = QLabel("Monitor Mode: ?")

        # Grouping related status items for clean layout
        status_grid = QGridLayout()
        status_grid.addWidget(QLabel("Adapter Status:"), 0, 0); status_grid.addWidget(self.adapter_status_lbl, 0, 1)
        status_grid.addWidget(QLabel("Signal Strength:"), 1, 0); status_grid.addWidget(self.signal_strength_lbl, 1, 1)
        status_grid.addWidget(QLabel("Monitor Mode:"), 2, 0); status_grid.addWidget(self.monitor_mode_lbl, 2, 1)

        header_layout.addLayout(status_grid)
        header_layout.addStretch()

        # --- 2. Core Metrics Display (Dashboard Row) ---
        metrics_group = QGroupBox("Core Telemetry")
        metrics_group.setObjectName("GlassBackground")
        metric_layout = QGridLayout()

        # Placeholder Labels for remaining dashboard data points
        self.ssid_lbl = QLabel("SSID: N/A")
        self.channel_lbl = QLabel("Ch: N/A")
        self.freq_lbl = QLabel("Freq: N/A")
        self.device_info_lbl = QLabel("Driver: Awaiting Scan...")
        self.scan_duration_lbl = QLabel("Duration: 0s")

        metric_layout.addWidget(QLabel("Connected SSID:"), 0, 0); metric_layout.addWidget(self.ssid_lbl, 0, 1)
        metric_layout.addWidget(QLabel("Channel/Freq:"), 1, 0); metric_layout.addWidget(self.channel_lbl, 1, 1)
        metric_layout.addWidget(QLabel("Interface Info:"), 2, 0); metric_layout.addWidget(self.device_info_lbl, 2, 1)
        metric_layout.addWidget(QLabel("Scan Time:"), 3, 0); metric_layout.addWidget(self.scan_duration_lbl, 3, 1)

        metrics_group.setLayout(metric_layout)

        # --- 3. Action Buttons & Controls (Bottom Row) ---
        control_h_box = QHBoxLayout()
        self.btn_discover = QPushButton("🔍 Start Network Discovery")
        self.btn_capture = QPushButton("📡 Start Packet Capture")
        self.btn_audit = QPushButton("🛡️ Run Security Audit")
        self.btn_report = QPushButton("📄 Generate Report")

        control_h_box.addWidget(self.btn_discover)
        control_h_box.addWidget(self.btn_capture)
        control_h_box.addWidget(self.btn_audit)
        control_h_box.addWidget(self.btn_report)


        # --- Final Assembly ---
        main_layout.addWidget(header_group)
        main_layout.addWidget(metrics_group)
        main_layout.addLayout(control_h_box)

        # Connect signals/slots to trigger actions
        self.btn_discover.clicked.connect(self._run_discovery)
        self.btn_audit.clicked.connect(self._trigger_audit)

    def load_initial_status(self):
        """Fetches and populates all initial dashboard metrics."""
        # Fetching real-time system data immediately upon loading
        status = self.hw_layer.get_adapter_status()
        monitor = self.hw_layer.check_monitor_mode()
        info = self.hw_layer.get_interface_info()

        self.adapter_status_lbl.setText(f"Adapter: {info['AvailableAdapters'][0] if info['AvailableAdapters'] else 'N/A'} | State: Online")
        self.signal_strength_lbl.setText(f"RSSI: {status['SignalStrength']}")
        self.monitor_mode_lbl.setText(f"Monitor Mode: {monitor}")

        self.ssid_lbl.setText("SSID: Connected to Corporate_LAN") # Mock value for startup example
        self.channel_lbl.setText(f"Ch: {status['Channel']} / Freq: {status['Frequency']}")
        self.device_info_lbl.setText(f"Driver: {status['DriverVersion']}")
        # Assume scan time is initial boot time placeholder
        self.scan_duration_lbl.setText("Duration: Initial Load")


    def _run_discovery(self):
        """Handler for the Discovery button, updating dashboard elements."""
        print("\n[ACTION]: Starting discovery...")

        # 1. Get raw data from HW layer
        scan_results = self.hw_layer.discover_networks()

        # Update status panel with high-level summary of results
        found_ssids = ", ".join([r.SSID for r in scan_results[:3]]) # Show first 3 found
        self.ssid_lbl.setText(f"Discovered: {len(scan_results)} Networks")

        # Optional: Trigger audit automatically upon discovery success
        print("[INFO]: Discovery successful. Automatically triggering Audit...")
        self._trigger_audit(scan_results)


    def _trigger_audit(self, scan_data: List[NetworkScanResult] = None):
        """Handles the audit process and displays results."""
        if not scan_data:
            # If no data is passed, run a discovery first to get data for analysis
            scan_data = self.hw_layer.discover_networks() 

        try:
            audit_service = SecurityAuditService()
            finding_result = audit_service.analyze_scan(scan_data)

            # Update Dashboard visualization with the final risk assessment
            self.statusBar().showMessage(f"AUDIT COMPLETE - Risk Score: {finding_result.OverallRiskScore}/100")
            print(f"\n[RESULT]: Audit Complete. Final finding severity = {finding_result.Severity}")

        except Exception as e:
            self.statusBar().showMessage(f"ERROR during Audit: {e}", 5000)

# --- Main Application Window (The Container) ---
class NetCrackerApp(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("NetCracker v1.0 | Enterprise Wi-Fi Security Assessment Suite")
        self.setGeometry(100, 50, 1400, 900)

        # --- Setup Core Architecture Components ---
        self.hw_layer = HardwareLayer() # Instantiates the hardware interface
        self.audit_service = SecurityAuditService() # Depends on hw_layer

        # Central Widget and Layout
        central_widget = QWidget()
        main_layout = QVBoxLayout(central_widget)

        # 1. Status Bar (For ephemeral messages like success/error)
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)

        # 2. Main Dashboard Widget (The main view)
        self.dashboard = DashboardWidget(self.hw_layer)

        # Optional: Adding tabs for different views if expansion is needed, but using the single dashboard for simplicity first.
        main_layout.addWidget(self.dashboard)

        self.setCentralWidget(central_widget)

    def showEvent(self, event):
        """Called when the window gains focus."""
        super().showEvent(event)
        print("\n--- NetCracker Application Launched ---")
        # Trigger initial data load on startup
        self.dashboard.load_initial_status()


if __name__ == '__main__':
    from PyQt6.QtWidgets import QApplication
    import sys

    app = QApplication(sys.argv)

    # Customizing application palette for professionalism
    palette = QPalette()
    # Setting a general dark background tone for the app window itself
    dark_blue = QColor(20, 30, 60)
    palette.setColor(QPalette.WindowBackground, dark_blue)
    app.setPalette(palette)

    main_window = NetCrackerApp()
    main_window.show()
    sys.exit(app.exec())
