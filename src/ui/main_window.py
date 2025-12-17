from PyQt5.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QTabWidget, QLabel
from .styles import DARK_THEME
from .dashboard import DashboardWidget
from .dataview import DataViewWidget

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("SteelAI-GAN: Data Augmentation System")
        self.setGeometry(100, 100, 1280, 800)
        self.setStyleSheet(DARK_THEME)
        
        # Central Widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        
        # Header
        header = QLabel("  SteelAI-GAN System v1.0")
        header.setStyleSheet("background-color: #000000; color: #00ccff; font-size: 18px; font-weight: bold; padding: 10px;")
        main_layout.addWidget(header)
        
        # Tabs
        self.tabs = QTabWidget()
        main_layout.addWidget(self.tabs)
        
        # Actual Widgets
        self.dashboard_tab = DashboardWidget()
        self.data_tab = DataViewWidget()
        
        self.tabs.addTab(self.dashboard_tab, "Dashboard & Monitor")
        self.tabs.addTab(self.data_tab, "Data Management")

if __name__ == "__main__":
    import sys
    from PyQt5.QtWidgets import QApplication
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
