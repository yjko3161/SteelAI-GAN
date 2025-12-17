import sys
import os

# Add src to path
sys.path.append(os.path.abspath("src"))

from data.ingestion import ImageLoader, DataOrganizer, ImageProcessor
import cv2
import shutil

def test_ingestion_pipeline():
    print("Starting Ingestion Pipeline Test...")
    
    # Setup
    if os.path.exists("data/processed/test_run"):
        shutil.rmtree("data/processed/test_run")
    
    loader = ImageLoader()
    organizer = DataOrganizer()
    processor = ImageProcessor()
    
    # 1. Load Image
    # Ensure raw test image exists
    raw_path = os.path.abspath("data/raw/test_sample.png")
    if not os.path.exists(raw_path):
        print(f"Error: Test image not found at {raw_path}")
        return

    print(f"Loading image from: {raw_path}")
    
    try:
        img = loader.load_image(raw_path)
        print(f"Image loaded successfully. Shape: {img.shape}")
    except Exception as e:
        print(f"Failed to load image: {e}")
        return

    # 2. Crop ROI (Center crop for simple testing)
    h, w, _ = img.shape
    crop_size = 256
    x = (w - crop_size) // 2
    y = (h - crop_size) // 2
    
    try:
        cropped_img = processor.crop_roi(img, x, y, crop_size, crop_size)
        print(f"ROI Cropped. New Shape: {cropped_img.shape}")
    except Exception as e:
        print(f"Failed to crop ROI: {e}")
        return

    # 3. Save Processed Image
    try:
        saved_path = loader.save_image(cropped_img, "processed_sample.png", subfolder="test_run")
        print(f"Processed image saved to: {saved_path}")
    except Exception as e:
        print(f"Failed to save processed image: {e}")
        return

    # 4. Organize File
    try:
        # Organize into 'normal' category
        org_path = organizer.organize_file(saved_path, "normal", filename="organized_sample.png")
        print(f"File organized to: {org_path}")
    except Exception as e:
        print(f"Failed to organize file: {e}")
        return

    print("Test Pipeline Completed Successfully.")

if __name__ == "__main__":
    test_ingestion_pipeline()
