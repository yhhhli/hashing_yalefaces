from torch.utils.data import DataLoader
from torchvision import transforms
from torchvision import datasets
import winsound
from torch import optim
from torch.autograd import variable
import torch
import torch.nn.functional as func
import torch.nn as nn
import hog_for_person

class Latonha(nn.Module):
    def __init__(self):
        super(Latonha,self).__init__()

    def forward(self, simMat,hashTable):
        hashTableT=hashTable.t()
        innerMat=hashTable.mm(hashTableT)
        hDisMat=(16-innerMat)/2
        output = torch.sum(simMat.mul(hDisMat))/(135*135)
        return output

class model(nn.Module):
    def __init__(self):
        super(model,self).__init__()
        self.conv=nn.Sequential(
            nn.Conv2d(1,6,5),
            nn.ReLU(True),
            nn.MaxPool2d(2,2),
            nn.Conv2d(6,16,3),
            nn.ReLU(True),
            nn.MaxPool2d(2,2),
        )

        self.linear=nn.Sequential(
            nn.Linear(23*23*16,1200),
            nn.Linear(1200,200),
            nn.Linear(200,16),
            nn.Tanh()
        )

    def forward(self, x):
        x = self.conv(x)
        x = x.view(x.size(0), -1)
        x = self.linear(x)
        return x

def training():
    num_epoch=10000
    learining_rate=0.001
    print(torch.cuda.is_available())
    net=model()
    net.cuda()
    criterion=Latonha()
    optimizer=optim.SGD(net.parameters(),learining_rate)
    hog_tensor,sim_mat=hog_for_person.get_hog_tensor()
    hog_tensor=variable(hog_tensor)
    hog_tensor = hog_tensor.cuda()
    sim_mat=variable(sim_mat)
    sim_mat=sim_mat.cuda()

    for epoch in range(num_epoch):
        out=net(hog_tensor)
        print(sum(out[0].mul(out[1])))
        loss=criterion(sim_mat,out)
        optimizer.zero_grad()
        loss.backward()
        optimizer.step()
        #print(loss.data)
        '''
    max_error=0
    min_right=16
    for i in range(135):
        for j in range(16):
            if out[i,j]>0:
                out[i,j]=1
            else:
                out[i,j]=-1
    for i in range(135):
        for j in range(135):
            if (i//9!=j//9)and(sum(out[i].mul(out[j]))>max_error):
                max_error=sum(out[i].mul(out[j]))
            elif (i//9==j//9)and(sum(out[i].mul(out[j]))<min_right):
                min_right=sum(out[i].mul(out[j]))
        print('for %d the max error is %.2f min right is %.2f'%(i,max_error,min_right))
        max_error = 0
        min_right = 16
        '''
    torch.save(net.state_dict(), 'parameters_16.pkl')
    torch.cuda.empty_cache()

if __name__=='__main__':
    training()
    duration = 1000  # millisecond
    freq = 440  # Hz
    winsound.Beep(freq, duration)