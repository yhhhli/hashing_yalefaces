from skimage.feature import hog
import os
import torch
from skimage import transform
from skimage import img_as_ubyte
from skimage import io
import matplotlib.pyplot as plt
import numpy as np


def get_hog_tensor(datapath=''):

    length =135
    hog_tensor = torch.empty(length,1,100,100)
    sim_mat = torch.empty(length,length)
    wgt_mat = torch.empty(length,length)
    for i in range(135):
        im = io.imread("/Users/liyuhang/Documents/GitHub/hashing_yalefaces/yuhang/traindata/s"+str(i+1)+".bmp",as_gray=True)
        normalised_blocks, hog_image = hog(im, orientations=9, pixels_per_cell=(2, 2), cells_per_block=(2, 2),
                                          block_norm = 'L1',transform_sqrt = True,visualize=True)
        #io.imshow(hog_image)
        #plt.show()
        im_tensor = torch.tensor(hog_image)
        mm=torch.max(im_tensor)
        mn=torch.min(im_tensor)
        distance=mm-mn
        for j in range(100):
            for k in range(100):
                im_tensor[j,k]=255*(im_tensor[j,k]-mn)/distance
        hog_tensor[i,0,:,:]=im_tensor

        for l in range(length):
            if i//9==l//9:
                sim_mat[i,l] = 1.
                wgt_mat[i,l] = 1.
            else:
                sim_mat[i,l] = 0.
                wgt_mat[i,l] = 1/14


    return hog_tensor.numpy(), sim_mat.numpy(), wgt_mat.numpy()

def get_test_tensor(datapath=''):
    length = 30
    hog_tensor = torch.empty(length, 1, 100, 100)
    for i in range(30):
        print(i)
        im = io.imread("/Users/liyuhang/Documents/GitHub/hashing_yalefaces/yuhang/testdata/t"+str(i+1)+".bmp",as_gray=True)
        normalised_blocks, hog_image = hog(im, orientations=9, pixels_per_cell=(2, 2), cells_per_block=(2, 2),
                                          block_norm = 'L1',transform_sqrt = True,visualize=True)

        im_tensor = torch.tensor(hog_image)
        mm=torch.max(im_tensor)
        mn=torch.min(im_tensor)
        distance=mm-mn
        for j in range(100):
            for k in range(100):
                im_tensor[j,k]=255*(im_tensor[j,k]-mn)/distance
        hog_tensor[i,0,:,:]=im_tensor

    return hog_tensor.numpy()

a, b, c=get_hog_tensor()
np.savez('/Users/liyuhang/Documents/GitHub/hashing_yalefaces/yuhang/traindata/traindata.npz', hog_tensor=a, sim_mat=b, wgt_mat=c)

hog_tensor=get_test_tensor()
np.savez('/Users/liyuhang/Documents/GitHub/hashing_yalefaces/yuhang/testdata/testdata.npz', test_tensor=hog_tensor)