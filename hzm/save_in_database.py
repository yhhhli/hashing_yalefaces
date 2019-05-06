from skimage.feature import hog
import os
from skimage import io
import torch
import net_for_16b
import MySQLdb

net=net_for_16b.model()
net.load_state_dict(torch.load('parameters_16.pkl'))
length = len(os.listdir(r"C:\\Users\\hzm\\Desktop\\hashface\\hashing_yalefaces\\yuhang\\traindata\\"))
hog_tensor = torch.empty(length, 1, 100, 100)
sim_mat = torch.empty(length, length)
for i in range(length):
    print(i)
    im = io.imread("C:\\Users\\hzm\\Desktop\\hashface\\hashing_yalefaces\\yuhang\\traindata\\s" + str(i + 1) + ".bmp", as_gray=True)
    normalised_blocks, hog_image = hog(im, orientations=9, pixels_per_cell=(2, 2), cells_per_block=(2, 2),
                                       block_norm='L1', transform_sqrt=True, visualize=True)
    im_tensor = torch.tensor(hog_image)
    mm = torch.max(im_tensor)
    mn = torch.min(im_tensor)
    distance = mm - mn
    for j in range(100):
        for k in range(100):
            im_tensor[j, k] = 255 * (im_tensor[j, k] - mn) / distance
    hog_tensor[i, 0, :, :] = im_tensor
out=net(hog_tensor)
db = MySQLdb.connect(host="127.0.0.1", user="root", passwd="12345678910abcd", db="hash_code", charset='utf8')
cursor=db.cursor()

for i in range(length):
    codestr = ""
    for j in range(16):
        if out[i,j]>0:
            codestr+="1"
        else:
            codestr+="0"
    print(codestr)
    codestr=int(codestr,2)
    codestr=hex(codestr)
    print(codestr)
    sql="INSERT INTO code_copy VALUES('%d','%s',"%(i+1,r"C:\\Users\\hzm\\Desktop\\hashface\\hashing_yalefaces\\yuhang\\traindata\\s" + str(i + 1) + ".bmp")+codestr+')'
    cursor.execute(sql)
    db.commit()