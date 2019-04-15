from skimage.feature import hog
import os
import torch
from skimage import transform
from skimage import img_as_ubyte
from skimage import io
import matplotlib.pyplot as plt
import numpy as np


def get_hog_tensor():

    length=len(os.listdir(r"/Users/liyuhang/Documents/GitHub/hashing_yalefaces/yuhang/traindata"))

    hog_tensor=torch.empty(length,1,100,100)
    sim_mat=torch.empty(length,length)
    for i in range(length):
        print(i)
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
                sim_mat[i,l]=1
            else:
                sim_mat[i,l]=-1/14
        print(im_tensor)
        break
    return hog_tensor,sim_mat


get_hog_tensor()