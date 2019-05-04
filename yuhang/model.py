import torch
import torch.nn as nn


def hashing(x, inference, beta):
    if inference:
        x = x.sign()
    else:
        x = (beta * x).tanh()
    return x


def hash_loss(output, sim_mat, wgt_mat):
    inner_product = torch.mm(output, output.t())
    return wgt_mat.mul(inner_product.exp().add(1.).log() - sim_mat.mul(inner_product)).mean()


def beta_schedule(model):
    model.beta += (model.end_beta - 1.0) / model.iters


class LeNet(nn.Module):

    def __init__(self, bit_num=32, end_beta=2.0, iters=3000):
        super(LeNet, self).__init__()
        self.bit_num = bit_num
        self.beta = 1.0
        self.inference = False
        self.end_beta = end_beta
        self.iters = iters
        self.conv = nn.Sequential(
            nn.Conv2d(1, 32, kernel_size=5, stride=1),
            nn.ReLU(True),
            nn.MaxPool2d(kernel_size=2, stride=2),
            nn.Conv2d(32, 64, kernel_size=5, stride=1),
            nn.ReLU(True),
            nn.MaxPool2d(kernel_size=2, stride=2),
            nn.Conv2d(64, 128, kernel_size=5, stride=1)
        )
        self.linear = nn.Sequential(
            nn.Linear(18 * 18 * 128, 1000),
            nn.Linear(1000, self.bit_num)
        )

        for m in self.modules():
            if isinstance(m, nn.Conv2d):
                nn.init.kaiming_normal_(m.weight, mode='fan_out', nonlinearity='relu')

    def forward(self, x):
        x = self.conv(x)
        x = x.view(x.shape[0], -1)
        x = self.linear(x)
        x = hashing(x, self.inference, self.beta)
        # The output shape should be [batch_size, bit_num]
        return x


class AlexNet(nn.Module):
    def __init__(self, bit_num=32, end_beta=2.0, iters=3000):
        super(AlexNet, self).__init__()
        self.bit_num = bit_num
        self.beta = 1.0
        self.inference = False
        self.end_beta = end_beta
        self.iters = iters
        self.features =nn.Sequential(
            nn.Conv2d(1, 64, kernel_size=8, stride=4),
            nn.BatchNorm2d(64),
            nn.ReLU(True),
            nn.MaxPool2d(2,2),
            nn.Conv2d(64, 128, kernel_size=4, stride=2, padding=2),
            nn.BatchNorm2d(128),
            nn.ReLU(True),
            nn.Conv2d(128, 256, kernel_size=3, stride=1, padding=1),
            nn.BatchNorm2d(256),
            nn.ReLU(True),
            nn.Conv2d(256, 512, kernel_size=3, stride=1, padding=1),
            nn.BatchNorm2d(512),
            nn.ReLU(True),
            nn.MaxPool2d(kernel_size=3, stride=2),
        )
        self.linear = nn.Sequential(
            nn.Linear(512*3*3, 1024),
            nn.Linear(1000, self.bit_num)
        )
        for m in self.modules():
            if isinstance(m, nn.Conv2d):
                nn.init.kaiming_normal_(m.weight, mode='fan_out', nonlinearity='relu')


    def forward(self, x):
        x = self.features(x)
        x = x.view(x.shape[0], -1)
        x = self.linear(x)
        x = hashing(x, self.inference, self.beta)
        # The output shape should be [batch_size, bit_num]
        return x
