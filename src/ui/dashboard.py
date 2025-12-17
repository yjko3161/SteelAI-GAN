from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QGroupBox, 
                             QLabel, QSlider, QPushButton, QProgressBar, QGridLayout, QFileDialog, QCheckBox)
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QImage, QPixmap
import cv2
import numpy as np
import sys
import os
import time

# Ensure we can import from src
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

from src.gan.inference import DefectGenerator

class DashboardWidget(QWidget):
    def __init__(self):
        super().__init__()
        
        self.layout = QHBoxLayout(self)
        self.loaded_image_path = None # State for loaded image
        self.generated_dir = os.path.join(os.getcwd(), "data", "generated")
        os.makedirs(self.generated_dir, exist_ok=True)
        
        # Left Panel: Controls & Status
        self.left_panel = QVBoxLayout()
        self.setup_control_panel()
        self.setup_status_panel()
        self.layout.addLayout(self.left_panel, 1) # 1/3 width
        
        # Right Panel: Monitor
        self.right_panel = QVBoxLayout()
        self.setup_monitor_panel()
        self.layout.addLayout(self.right_panel, 2) # 2/3 width
        
        # Initialize GAN Generator (Mock/Random for now if model not found)
        self.gan = DefectGenerator(z_dim=100)
        
        # Timer for simulating real-time feed
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_monitor)
        # self.timer.start(2000) # Update every 2 seconds

    def setup_control_panel(self):
        group = QGroupBox("Equipment Control")
        layout = QGridLayout()
        
        # Motor Speed
        layout.addWidget(QLabel("Motor Speed (RPM)"), 0, 0)
        self.speed_slider = QSlider(Qt.Horizontal)
        self.speed_slider.setRange(0, 3000)
        self.speed_slider.setValue(1200)
        layout.addWidget(self.speed_slider, 0, 1)
        
        # Light Power
        layout.addWidget(QLabel("Light Power (%)"), 1, 0)
        self.light_slider = QSlider(Qt.Horizontal)
        self.light_slider.setRange(0, 100)
        self.light_slider.setValue(80)
        layout.addWidget(self.light_slider, 1, 1)
        
        # Reference Image Loader
        btn_load = QPushButton("Load Ref Image")
        btn_load.setStyleSheet("background-color: #555555; color: white;")
        btn_load.clicked.connect(self.load_reference_image)
        layout.addWidget(btn_load, 2, 0, 1, 2)
        
        # Auto-Save Checkbox
        self.chk_autosave = QCheckBox("Auto-Save Generated Images")
        self.chk_autosave.setStyleSheet("margin-top: 10px; font-weight: bold;")
        layout.addWidget(self.chk_autosave, 3, 0, 1, 2)
        
        # Start/Stop Buttons
        btn_layout = QHBoxLayout()
        self.btn_start = QPushButton("START")
        self.btn_start.setStyleSheet("background-color: #00cc66; color: white;")
        self.btn_start.clicked.connect(self.start_system)
        
        self.btn_stop = QPushButton("STOP")
        self.btn_stop.setStyleSheet("background-color: #ff4444; color: white;")
        self.btn_stop.clicked.connect(self.stop_system)
        
        btn_layout.addWidget(self.btn_start)
        btn_layout.addWidget(self.btn_stop)
        layout.addLayout(btn_layout, 4, 0, 1, 2)
        
        group.setLayout(layout)
        self.left_panel.addWidget(group)

    def setup_status_panel(self):
        group = QGroupBox("System Status")
        layout = QVBoxLayout()
        
        self.status_label = QLabel("STATUS: STANDBY")
        self.status_label.setProperty("class", "stat-label") # For future styling
        self.status_label.setStyleSheet("color: orange; font-weight: bold; font-size: 16px;")
        layout.addWidget(self.status_label)
        
        layout.addWidget(QLabel("Progress:"))
        self.pbar = QProgressBar()
        layout.addWidget(self.pbar)
        
        self.lbl_save_status = QLabel("Saved: None")
        self.lbl_save_status.setStyleSheet("color: #888888; font-size: 11px;")
        layout.addWidget(self.lbl_save_status)
        
        group.setLayout(layout)
        self.left_panel.addWidget(group)
        self.left_panel.addStretch()

    def setup_monitor_panel(self):
        group = QGroupBox("Real-time Inspection Monitor")
        layout = QVBoxLayout()
        
        screen_layout = QHBoxLayout()
        
        # Original (Camera Feed) Placeholder
        self.lbl_camera = QLabel("Camera Feed / Ref Image")
        self.lbl_camera.setFixedSize(300, 300)
        self.lbl_camera.setStyleSheet("background-color: black; border: 1px solid #333;")
        self.lbl_camera.setAlignment(Qt.AlignCenter)
        self.lbl_camera.setScaledContents(True)
        
        # GAN Result Placeholder
        self.lbl_gan = QLabel("GAN Augmentation")
        self.lbl_gan.setFixedSize(300, 300)
        self.lbl_gan.setStyleSheet("background-color: black; border: 1px solid #333;")
        self.lbl_gan.setAlignment(Qt.AlignCenter)
        self.lbl_gan.setScaledContents(True)
        
        screen_layout.addWidget(self.lbl_camera)
        screen_layout.addWidget(self.lbl_gan)
        
        layout.addLayout(screen_layout)
        
        # Info Overlay
        self.lbl_info = QLabel("Inspection Result: WAITING")
        self.lbl_info.setAlignment(Qt.AlignCenter)
        self.lbl_info.setStyleSheet("font-size: 18px; font-weight: bold; color: #aaaaaa;")
        layout.addWidget(self.lbl_info)
        
        group.setLayout(layout)
        self.right_panel.addWidget(group)

    def load_reference_image(self):
        print("[DEBUG] Opening File Dialog...")
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        file_path, _ = QFileDialog.getOpenFileName(self, "Load Reference Image", "", 
                                                 "Images (*.png *.jpg *.jpeg *.bmp);;All Files (*)", options=options)
        print(f"[DEBUG] File Selected: {file_path}")
        if file_path:
            self.loaded_image_path = file_path
            # Display immediately
            pixmap = QPixmap(file_path)
            self.lbl_camera.setPixmap(pixmap)

    def start_system(self):
        self.status_label.setText("STATUS: RUNNING")
        self.status_label.setStyleSheet("color: #00ff99; font-weight: bold; font-size: 16px;")
        self.pbar.setRange(0, 0) # Infinite loading
        self.timer.start(1500) # Start generating images
        
    def stop_system(self):
        self.status_label.setText("STATUS: STOPPED")
        self.status_label.setStyleSheet("color: #ff4444; font-weight: bold; font-size: 16px;")
        self.pbar.setRange(0, 100)
        self.pbar.setValue(0)
        self.timer.stop()

    def update_monitor(self):
        # Prepare Base Image for Mock Generation if available
        base_img_for_gan = None
        if self.loaded_image_path:
             # cv2 reads as BGR, but QT displays RGB. 
             # Let's read it for processing.
             bgr_img = cv2.imread(self.loaded_image_path)
             if bgr_img is not None:
                 base_img_for_gan = cv2.cvtColor(bgr_img, cv2.COLOR_BGR2RGB)

        # 1. Generate Fake Defect Image
        # Pass base image for "CycleGAN-like" demo effect in Mock Mode
        fake_img = self.gan.generate_image(base_image=base_img_for_gan) # HWC, RGB
        
        # 2. Display on Label
        h, w, ch = fake_img.shape
        bytes_per_line = ch * w
        # Convert RGB to QImage
        q_img = QImage(fake_img.data, w, h, bytes_per_line, QImage.Format_RGB888)
        pixmap = QPixmap.fromImage(q_img) #.scaled(300, 300, Qt.KeepAspectRatio) -> handled by setScaledContents
        
        self.lbl_gan.setPixmap(pixmap)
        
        # 3. Save if Checkbox is enabled
        if self.chk_autosave.isChecked():
            timestamp = int(time.time() * 1000)
            filename = f"gen_{timestamp}.png"
            filepath = os.path.join(self.generated_dir, filename)
            
            # Convert RGB to BGR for OpenCV
            fake_img_bgr = cv2.cvtColor(fake_img, cv2.COLOR_RGB2BGR)
            cv2.imwrite(filepath, fake_img_bgr)
            
            self.lbl_save_status.setText(f"Saved: {filename}")
        
        # 4. Simulate Camera Feed OR Use Loaded Image
        if self.loaded_image_path:
            # If loaded, keep showing it (or maybe jitter it to simulate video?)
            # For now, just keep the static image as "Reference"
            pass 
        else:
            # Generate random noise/feed simulation if nothing loaded
            noise = np.random.randint(0, 255, (256, 256, 3), dtype=np.uint8)
            q_img_cam = QImage(noise.data, 256, 256, 256*3, QImage.Format_RGB888)
            pixmap_cam = QPixmap.fromImage(q_img_cam)
            self.lbl_camera.setPixmap(pixmap_cam)
        
        # 5. Update Info
        self.lbl_info.setText("Inspection Result: DEFECT DETECTED (GAN Generated)")
        self.lbl_info.setStyleSheet("font-size: 18px; font-weight: bold; color: #ff5555;")
