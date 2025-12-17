import sys
import os
import numpy as np
import cv2

# Global flag to track if Torch is available
TORCH_AVAILABLE = False
Generator = None

try:
    import torch
    # Ensure proper import whether run as script or module
    try:
        from src.gan.model import Generator
    except ImportError:
        from .model import Generator
    TORCH_AVAILABLE = True
except (ImportError, OSError) as e:
    print(f"Warning: Failed to load PyTorch or Model ({e}). Running in Mock Mode.")
    TORCH_AVAILABLE = False

class DefectGenerator:
    def __init__(self, model_path=None, z_dim=100, device=None):
        self.z_dim = z_dim
        self.device = None
        self.netG = None
        
        if TORCH_AVAILABLE:
            try:
                # Auto-detect device if not specified
                if device is None:
                    device = 'cuda' if torch.cuda.is_available() else 'cpu'
                
                print(f"[INFO] GAN Inference running on: {device}")
                self.device = torch.device(device)
                self.netG = Generator(z_dim).to(self.device)
                if model_path:
                    self.load_model(model_path)
                else:
                    print("Warning: No model path provided. Generating random noise images.")
                self.netG.eval()
            except Exception as e:
                print(f"Error initializing GAN: {e}. Switching to Mock Mode.")
                self.netG = None
        
    def load_model(self, path):
        if not self.netG: return
        try:
            state_dict = torch.load(path, map_location=self.device)
            self.netG.load_state_dict(state_dict)
            print(f"Model loaded from {path}")
        except Exception as e:
            print(f"Failed to load model: {e}")

    def generate_image(self, base_image=None):
        """Generates a single image."""
        if self.netG and TORCH_AVAILABLE:
            with torch.no_grad():
                noise = torch.randn(1, self.z_dim, 1, 1).to(self.device)
                fake_img = self.netG(noise)
                
                # Post-processing: Normalize to 0-255 and change to HWC
                img_t = fake_img[0].detach().cpu()
                img_np = (img_t.numpy() + 1) / 2.0 * 255.0 # Tanh -1..1 to 0..255
                img_np = img_np.astype(np.uint8)
                img_np = np.transpose(img_np, (1, 2, 0)) # CHW -> HWC
                return img_np
        else:
            # Mock Mode / Demo Mode
            if base_image is not None:
                # Demo Effect: Apply a stylistic change to the reference image
                # e.g., Convert to grayscale and add red tint to simulate 'defect analysis' style
                # Resize to 256x256 first
                img_resized = cv2.resize(base_image, (256, 256))
                
                # Create a "Defect Map" look (Blue/Purple tint)
                # Just for show: Invert colors or shift channels
                # BGR -> RGB already handled in UI, this assumes input is RGB or just modifies array
                # Let's add some random "Defect" boxes
                demo_img = img_resized.copy()
                
                # Add a simulated defect overlay (Red box)
                h, w, _ = demo_img.shape
                x = np.random.randint(50, 200)
                y = np.random.randint(50, 200)
                cv2.rectangle(demo_img, (x, y), (x+30, y+30), (255, 0, 0), 2) # Red box
                
                # Add some noise to look "generated"
                noise = np.random.randint(0, 50, (h, w, 3), dtype=np.uint8)
                demo_img = cv2.addWeighted(demo_img, 0.8, noise, 0.2, 0)
                
                return demo_img
            else:
                # Fallback to random noise if no ref image
                return np.random.randint(0, 255, (256, 256, 3), dtype=np.uint8)

    def generate_batch(self, batch_size=4):
        images = []
        for _ in range(batch_size):
            images.append(self.generate_image())
        return images

if __name__ == "__main__":
    gen = DefectGenerator()
    img = gen.generate_image()
    print(f"Generated image shape: {img.shape}")
