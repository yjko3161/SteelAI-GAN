import sys
import os
import torch
import unittest

# Add src to path
sys.path.append(os.path.abspath("src"))

from gan.model import Generator, Discriminator
from gan.trainer import GANTrainer
from torch.utils.data import DataLoader, TensorDataset

class TestGANArchitecture(unittest.TestCase):
    def setUp(self):
        self.z_dim = 100
        self.img_channels = 3
        # Use CPU for testing to ensure it runs everywhere
        self.device = torch.device("cpu") 
        self.batch_size = 4
        
    def test_generator_output_shape(self):
        """Test if Generator outputs correct shape 256x256"""
        netG = Generator(self.z_dim, self.img_channels).to(self.device)
        noise = torch.randn(self.batch_size, self.z_dim, 1, 1).to(self.device)
        output = netG(noise)
        
        # Expected: Batch x Channels x 256 x 256
        self.assertEqual(output.shape, (self.batch_size, self.img_channels, 256, 256))
        
    def test_discriminator_output_shape(self):
        """Test if Discriminator accepts 256x256 and outputs probability"""
        netD = Discriminator(self.img_channels).to(self.device)
        # Random image batch: Batch x Channels x 256 x 256
        img = torch.randn(self.batch_size, self.img_channels, 256, 256).to(self.device)
        output = netD(img)
        
        # Expected: Batch x 1 x 1 x 1 (before view(-1)) or just Batch if squeezed.
        # Our model outputs Batch x 1 x 1 x 1
        self.assertEqual(output.shape, (self.batch_size, 1, 1, 1))

    def test_trainer_step(self):
        """Test one training step to ensure no runtime errors"""
        # Create dummy data
        dummy_data = torch.randn(10, 3, 256, 256) # 10 images
        dataset = TensorDataset(dummy_data)
        dataloader = DataLoader(dataset, batch_size=2)
        
        trainer = GANTrainer(dataloader, self.device, z_dim=self.z_dim)
        
        real_batch = next(iter(dataloader))[0].to(self.device)
        
        errD, errG, D_x, D_G_z1, D_G_z2 = trainer.train_step(real_batch)
        
        print(f"Train Step Result - Loss D: {errD}, Loss G: {errG}")
        
        self.assertIsInstance(errD, float)
        self.assertIsInstance(errG, float)

if __name__ == "__main__":
    unittest.main()
