import torch
import torch.nn as nn
import torchvision.models as models
import torch.nn.functional as F


class ConvNet(nn.Module):
    """EmbeddingNet using ResNet-101."""

    def __init__(self):
        """Initialize EmbeddingNet model."""
        super(ConvNet, self).__init__()

        # Use ResNet for ConvNet
        resnet = models.resnet101(pretrained=True)
        for param in resnet.parameters():
            param.requires_grad = False

        self.features = nn.Sequential(*list(resnet.children())[:-1])
        num_ftrs = resnet.fc.in_features
        self.fc1 = nn.Linear(num_ftrs, 4096)

    def forward(self, x):
        """Forward pass of EmbeddingNet."""
        out = self.features(x)
        out = out.view(out.size(0), -1)
        out = self.fc1(out)

        return out


class DeepRank(nn.Module):
    """ Deep Rank Network """

    def __init__(self):
        super(DeepRank, self).__init__()

        self.conv_model = ConvNet()  # ResNet101

        # 1st sub sampling
        self.conv1 = torch.nn.Conv2d(in_channels=3, out_channels=96, kernel_size=8, padding=1, stride=16)
        self.maxpool1 = torch.nn.MaxPool2d(kernel_size=3, stride=4, padding=1)

        # 2nd sub sampling
        self.conv2 = torch.nn.Conv2d(in_channels=3, out_channels=96, kernel_size=8, padding=4, stride=32)
        self.maxpool2 = torch.nn.MaxPool2d(kernel_size=7, stride=2, padding=3)

        self.dense_layer = torch.nn.Linear(in_features=(4096 + 3072), out_features=4096)

    def forward(self, X):
        conv_input = self.conv_model(X)
        conv_norm = conv_input.norm(p=2, dim=1, keepdim=True)
        conv_input = conv_input.div(conv_norm.expand_as(conv_input))

        first_input = self.conv1(X)
        first_input = self.maxpool1(first_input)
        first_input = first_input.view(first_input.size(0), -1)  # reshape tensor
        first_input = F.normalize(first_input, dim=1, p=2)  # dim=1 : vector norm

        second_input = self.conv2(X)
        second_input = self.maxpool2(second_input)
        second_input = second_input.view(second_input.size(0), -1)  # reshape tensor
        second_input = F.normalize(second_input, dim=1, p=2)  # dim=1 : vector norm

        merge_subsample = torch.cat([first_input, second_input], 1)  # batch x (3072)
        merge_conv = torch.cat([merge_subsample, conv_input], 1)  # batch x (4096 + 3072)

        final_input = self.dense_layer(merge_conv)
        final_input = F.normalize(final_input, dim=1, p=2)

        return final_input
