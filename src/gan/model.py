import torch
import torch.nn as nn

class Generator(nn.Module):
    def __init__(self, latent_dim=100, img_channels=3, feature_g=64):
        super(Generator, self).__init__()
        self.net = nn.Sequential(
            # Input: N x latent_dim x 1 x 1
            self._block(latent_dim, feature_g * 32, 4, 1, 0),  # 4x4
            self._block(feature_g * 32, feature_g * 16, 4, 2, 1),  # 8x8
            self._block(feature_g * 16, feature_g * 8, 4, 2, 1),  # 16x16
            self._block(feature_g * 8, feature_g * 4, 4, 2, 1),  # 32x32
            self._block(feature_g * 4, feature_g * 2, 4, 2, 1),  # 64x64
            self._block(feature_g * 2, feature_g, 4, 2, 1),  # 128x128
            # Final Layer for 256x256
            nn.ConvTranspose2d(feature_g, img_channels, 4, 2, 1), # 256x256
            nn.Tanh()
        )
        
    def _block(self, in_channels, out_channels, kernel_size, stride, padding):
        return nn.Sequential(
            nn.ConvTranspose2d(
                in_channels, out_channels, kernel_size, stride, padding, bias=False
            ),
            nn.BatchNorm2d(out_channels),
            nn.ReLU(),
        )

    def forward(self, x):
        return self.net(x)

class Discriminator(nn.Module):
    def __init__(self, img_channels=3, feature_d=64):
        super(Discriminator, self).__init__()
        self.net = nn.Sequential(
            # Input: N x channels x 256 x 256
            nn.Conv2d(img_channels, feature_d, 4, 2, 1), # 128x128
            nn.LeakyReLU(0.2),
            self._block(feature_d, feature_d * 2, 4, 2, 1), # 64x64
            self._block(feature_d * 2, feature_d * 4, 4, 2, 1), # 32x32
            self._block(feature_d * 4, feature_d * 8, 4, 2, 1), # 16x16
            self._block(feature_d * 8, feature_d * 16, 4, 2, 1), # 8x8
            self._block(feature_d * 16, feature_d * 32, 4, 2, 1), # 4x4
            nn.Conv2d(feature_d * 32, 1, 4, 2, 0), # 1x1
            nn.Sigmoid(),
        )

    def _block(self, in_channels, out_channels, kernel_size, stride, padding):
        return nn.Sequential(
            nn.Conv2d(
                in_channels, out_channels, kernel_size, stride, padding, bias=False
            ),
            nn.InstanceNorm2d(out_channels, affine=True),
            nn.LeakyReLU(0.2),
        )

    def forward(self, x):
        return self.net(x)

def initialize_weights(model):
    # Initializes weights according to the DCGAN paper
    for m in model.modules():
        if isinstance(m, (nn.Conv2d, nn.ConvTranspose2d, nn.BatchNorm2d)):
            nn.init.normal_(m.weight.data, 0.0, 0.02)

if __name__ == "__main__":
    # Correcting for 256x256 support dynamically if needed, 
    # but for now let's stick to 128x128 as it's lighter for local testing 
    # and then upsample for 256x256 if required by requirements.
    # Requirement say: "High resolution". 256 is decent.
    # Let's add one layer to Generator and Discriminator for 256x256 support.
    pass 
