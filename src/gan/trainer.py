import torch
import torch.nn as nn
import torch.optim as optim
import torchvision.utils as vutils
from torch.utils.data import DataLoader
from .model import Generator, Discriminator, initialize_weights
import os

class GANTrainer:
    def __init__(self, 
                 dataloader: DataLoader, 
                 device: torch.device, 
                 lr=0.0002, 
                 beta1=0.5, 
                 z_dim=100,
                 img_channels=3,
                 checkpoint_dir="checkpoints"):
        
        self.dataloader = dataloader
        self.device = device
        self.z_dim = z_dim
        self.checkpoint_dir = checkpoint_dir
        
        os.makedirs(self.checkpoint_dir, exist_ok=True)
        
        # Initialize Models
        self.netG = Generator(z_dim, img_channels).to(device)
        self.netD = Discriminator(img_channels).to(device)
        
        initialize_weights(self.netG)
        initialize_weights(self.netD)
        
        # Optimizers
        self.optimizerG = optim.Adam(self.netG.parameters(), lr=lr, betas=(beta1, 0.999))
        self.optimizerD = optim.Adam(self.netD.parameters(), lr=lr, betas=(beta1, 0.999))
        
        # Loss
        self.criterion = nn.BCELoss()
        
        # Fixed noise for visualization
        self.fixed_noise = torch.randn(32, z_dim, 1, 1).to(device)

    def train_step(self, real_images):
        """Performs one training step."""
        b_size = real_images.size(0)
        real_label = 1.0
        fake_label = 0.0
        
        # =======================
        # Train Discriminator
        # =======================
        self.netD.zero_grad()
        
        # Real batch
        label = torch.full((b_size,), real_label, dtype=torch.float, device=self.device)
        output = self.netD(real_images).view(-1)
        errD_real = self.criterion(output, label)
        errD_real.backward()
        D_x = output.mean().item()
        
        # Fake batch
        noise = torch.randn(b_size, self.z_dim, 1, 1, device=self.device)
        fake_images = self.netG(noise)
        label.fill_(fake_label)
        output = self.netD(fake_images.detach()).view(-1)
        errD_fake = self.criterion(output, label)
        errD_fake.backward()
        D_G_z1 = output.mean().item()
        
        errD = errD_real + errD_fake
        self.optimizerD.step()
        
        # =======================
        # Train Generator
        # =======================
        self.netG.zero_grad()
        label.fill_(real_label) # Flip labels for Generator cost
        output = self.netD(fake_images).view(-1)
        errG = self.criterion(output, label)
        errG.backward()
        D_G_z2 = output.mean().item()
        
        self.optimizerG.step()
        
        return errD.item(), errG.item(), D_x, D_G_z1, D_G_z2

    def save_checkpoint(self, epoch):
        """Saves model checkpoints."""
        torch.save(self.netG.state_dict(), os.path.join(self.checkpoint_dir, f"netG_epoch_{epoch}.pth"))
        torch.save(self.netD.state_dict(), os.path.join(self.checkpoint_dir, f"netD_epoch_{epoch}.pth"))

if __name__ == "__main__":
    print("GANTrainer module initialized.")
