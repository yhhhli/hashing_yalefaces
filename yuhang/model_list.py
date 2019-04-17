import torch
import torch.nn as nn


def hashing(x, inference, beta):
    if inference:
        x = x.sign()
    else:
        x = (beta * x).tanh()
    return x


def loss(x):
    pass


class LeNet(nn.Module):

    def __init__(self, bit_num):
        super(LeNet, self).__init__()
        self.bit_num = bit_num
        self.beta = 1.0
        self.inference = False
        self.conv = nn.Sequential(
            nn.Conv2d(1, 6, kernel_size=5, stride=1),
            nn.ReLU(True),
            nn.MaxPool2d(kernel_size=2, stride=2),
            nn.Conv2d(6, 16, kernel_size=5, stride=1),
            nn.ReLU(True),
            nn.MaxPool2d(kernel_size=2, stride=2),
            nn.Conv2d(16, 120, kernel_size=5, stride=1)
        )
        self.linear = nn.Sequential(
            nn.Linear(18*18*120, 1000),
            nn.Linear(1000, self.bit_num)
        )

    def forward(self, x):
        x = self.conv(x)
        x = self.linear(x)
        x = hashing(x, self.inference, self.beta)
        return x

    def beta_schedule(self):
        self.beta = self.beta + 0.2