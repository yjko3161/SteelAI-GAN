import os
import shutil
import cv2
import numpy as np
from pathlib import Path

class ImageLoader:
    def __init__(self, raw_data_path="data/raw", processed_path="data/processed"):
        self.raw_data_path = Path(raw_data_path)
        self.processed_path = Path(processed_path)
        
        # Create directories if they don't exist
        self.raw_data_path.mkdir(parents=True, exist_ok=True)
        self.processed_path.mkdir(parents=True, exist_ok=True)

    def load_image(self, filepath):
        """Loads an image from a path."""
        if not os.path.exists(filepath):
            raise FileNotFoundError(f"File not found: {filepath}")
        
        # Read image using OpenCV
        img = cv2.imread(str(filepath))
        if img is None:
            raise ValueError(f"Failed to read image: {filepath}")
        
        # Convert BGR to RGB
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        return img

    def save_image(self, img, filename, subfolder=""):
        """Saves an image to the processed directory."""
        save_dir = self.processed_path / subfolder
        save_dir.mkdir(parents=True, exist_ok=True)
        
        full_path = save_dir / filename
        
        # OpenCV expects BGR
        img_bgr = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
        cv2.imwrite(str(full_path), img_bgr)
        return str(full_path)

class DataOrganizer:
    def __init__(self, base_path="data/processed"):
        self.base_path = Path(base_path)
        self.categories = ["normal", "defect_nut", "defect_crack", "defect_hole"]
        
        for cat in self.categories:
            (self.base_path / cat).mkdir(parents=True, exist_ok=True)

    def organize_file(self, source_path, category, filename=None):
        """Moves or copies a file to the appropriate category folder."""
        if category not in self.categories:
            raise ValueError(f"Unknown category: {category}. Valid categories: {self.categories}")
        
        if filename is None:
            filename = os.path.basename(source_path)
            
        dest_path = self.base_path / category / filename
        shutil.copy2(source_path, dest_path)
        return str(dest_path)

class ImageProcessor:
    @staticmethod
    def crop_roi(img, x, y, w, h):
        """Crops a region of interest from the image."""
        if img is None:
            raise ValueError("Image is None")
        
        height, width, _ = img.shape
        # Boundary checks
        x = max(0, x)
        y = max(0, y)
        w = min(w, width - x)
        h = min(h, height - y)
        
        return img[y:y+h, x:x+w]

    @staticmethod
    def resize_image(img, size=(256, 256)):
        """Resizes image to target size."""
        return cv2.resize(img, size)

if __name__ == "__main__":
    # Test script
    loader = ImageLoader()
    organizer = DataOrganizer()
    processor = ImageProcessor()
    print("DataLoader, Organizer, and Processor initialized.")
