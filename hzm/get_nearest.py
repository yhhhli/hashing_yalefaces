from torch.utils.data import DataLoader
from torchvision import transforms
from torchvision import datasets
from skimage import transform
from skimage import img_as_ubyte
import winsound
from skimage.feature import hog
import os
import torch
from skimage import io
from torch import optim
from torch.autograd import variable
import torch
import torch.nn.functional as func
import torch.nn as nn
import hog_for_person
import net_for_16b
import MySQLdb

def compare_str(str1,str2):
    count=0
    for i in range(16):
        if str1[i]==str2[i]:
            count+=1
    return count

def get_five(input_image):
    normalised_blocks, hog_image = hog(input_image, orientations=9, pixels_per_cell=(2, 2), cells_per_block=(2, 2),
                                       block_norm='L1', transform_sqrt=True, visualize=True)
    hog_tensor = torch.empty(1, 1, 100, 100)
    im_tensor = torch.tensor(hog_image)
    mm = torch.max(im_tensor)
    mn = torch.min(im_tensor)
    distance = mm - mn
    for j in range(100):
        for k in range(100):
            im_tensor[j, k] = 255 * (im_tensor[j, k] - mn) / distance
    hog_tensor[0, 0, :, :] = im_tensor

    net=net_for_16b.model()
    net.load_state_dict(torch.load('parameters_16.pkl',map_location='cpu'))
    out=net(hog_tensor)
    outstr = ""
    for j in range(16):
        if out[0,j]>0:
            outstr+='1'
        else:
            outstr+='0'

    db = MySQLdb.connect(host="127.0.0.1", user="root", passwd="12345678910abcd", db="hash_code", charset='utf8')
    cursor=db.cursor()
    sql='SELECT * FROM code_copy'
    cursor.execute(sql)
    result=cursor.fetchall()
    print(result)
    list={}
    for res in result:
        bincode=res[2].hex()
        bincode=bin(int(bincode,16))
        bincode=bincode[2:]
        bincode = '0' * (16 - len(bincode)) + bincode
        print(bincode)
        list[res[1]]=compare_str(outstr,bincode)
    list = sorted(list.items(), key=lambda x: x[1], reverse=True)
    for i in range(5):
        print(list[i][0])
    return list




