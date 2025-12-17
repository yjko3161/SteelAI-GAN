import sys
import traceback
from PyQt5.QtWidgets import QApplication

def main():
    print("[DEBUG] Starting application...")
    try:
        app = QApplication(sys.argv)
        print("[DEBUG] QApplication created.")
        
        from src.ui.main_window import MainWindow
        print("[DEBUG] Imported MainWindow.")
        
        window = MainWindow()
        print("[DEBUG] MainWindow initialized.")
        
        window.show()
        print("[DEBUG] Window shown. Entering event loop.")
        
        sys.exit(app.exec_())
    except Exception:
        print("[ERROR] Critical failure in main:")
        traceback.print_exc()
        input("Press Enter to close window...") # Keep terminal open if it crashes

if __name__ == "__main__":
    main()
