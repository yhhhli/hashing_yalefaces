import sys
import os
import torch
import argparse
import torch.nn as nn
import torch.optim as optim
import numpy as np

from model import LeNet, AlexNet, hash_loss, beta_schedule
from torch.autograd import Variable


class AverageMeter(object):
    """Computes and stores the average and current value"""

    def __init__(self):
        self.reset()

    def reset(self):
        self.val = 0
        self.avg = 0
        self.sum = 0
        self.count = 0

    def update(self, val, n=1):
        self.val = val
        self.sum += val * n
        self.count += n
        self.avg = self.sum / self.count


def save_hashcodes(model):
    model.inference = True
    if args.cpu:
        output = model(input).detach().cpu().numpy()
        test_output = model(test_input).detach().cpu().numpy()
    else:
        output = model(input.cuda()).detach().cpu().numpy()
        test_output = model(test_input.cuda()).detach().cpu().numpy()
    np.savez('hashing_code_'+str(args.bitnum)+'.npz', output=output, test_output=test_output)
    print('Hashing codes have been saved!')


def train(epoch, input, sim_mat, wgt_mat):
    model.train()
    if not args.cpu:
        input, sim_mat, wgt_mat = Variable(input.cuda()), Variable(sim_mat.cuda()), Variable(wgt_mat.cuda())
    else:
        input, sim_mat, wgt_mat = Variable(input), Variable(sim_mat), Variable(wgt_mat)
    optimizer.zero_grad()
    output = model(input)

    loss = criterion(output, sim_mat, wgt_mat, args.alpha)
    loss.backward()
    optimizer.step()

    beta_schedule(model)
    if epoch % 100 == 0:
        print('Train Epoch:  {} Loss: {}  LR: {}'.format(epoch, loss.data.item(),
                                                         optimizer.param_groups[0]['lr']))


def mAP(index):
    meanAveragePrec = AverageMeter()
    for i in range(30):
        Prec = AverageMeter()
        AveragePrec = AverageMeter()
        count = 0
        for j in range(135):
            if i // 2 == index[i][134 - j] // 9:
                Prec.update(1.0)
                AveragePrec.update(Prec.avg)
                count += 1
            else:
                Prec.update(0.0)
            if count == 9:
                break
        meanAveragePrec.update(AveragePrec.avg)
    return meanAveragePrec.avg


def evaluate():
    npzf = np.load('hashing_code_'+str(args.bitnum)+'.npz')
    output, test_output = npzf['output'], npzf['test_output']
    inner_product = np.matmul(test_output, output.transpose())
    index = np.argsort(inner_product, axis=1)
    print(index)

    MAP = mAP(index)
    print('mean Average Precision: {}'.format(MAP))


def adjust_learning_rate(optimizer, epoch):
    update_list = [2000, 2500]
    if epoch in update_list:
        for param_group in optimizer.param_groups:
            param_group['lr'] = param_group['lr'] * 0.2
    return


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--cpu', action='store_true',
                        help='set if only CPU is available')
    parser.add_argument('--data', action='store', default='.',
                        help='dataset path')
    parser.add_argument('--arch', action='store', default='lenet',
                        help='the architecture for the network: lenet')
    parser.add_argument('--epochs', default=3000, type=int, metavar='N',
                        help='number of total epochs to run')
    parser.add_argument('--lr', action='store', default=2e-4, type=float,
                        help='the intial learning rate')
    parser.add_argument('--weight-decay', '--wd', default=1e-6, type=float,
                        metavar='W', help='weight decay (default: 1e-6)')
    parser.add_argument('--momentum', default=0.90, type=float, metavar='M',
                        help='momentum')
    parser.add_argument('--pretrained', action='store', default=None,
                        help='the path to the pretrained model')
    parser.add_argument('--evaluate', action='store_true',
                        help='evaluate the model')
    parser.add_argument('--bitnum', action='store', default=32, type=int,
                        help='the bit numbers of hashing codes')
    parser.add_argument('--end-beta', action='store', default=1.0, type=float,
                        help='the end of the beta')
    parser.add_argument('--alpha', action='store', default=1.0, type=float,
                        help='control the shape of loss')

    args = parser.parse_args()
    print('==> Options:', args)

    # set the seek
    torch.manual_seed(1)
    torch.cuda.manual_seed(1)

    # data_loader
    traindata = np.load('traindata/traindata.npz')
    input = torch.from_numpy(traindata['hog_tensor'])
    sim_mat = torch.from_numpy(traindata['sim_mat'])
    wgt_mat = torch.from_numpy(traindata['wgt_mat'])

    testdata = np.load('testdata/testdata.npz')
    test_input = torch.from_numpy(testdata['test_tensor'])

    # initialize the model
    if args.arch == 'lenet':
        model = LeNet(args.bitnum, args.end_beta, args.epochs)
    elif args.arch == 'alexnet':
        model = AlexNet(args.bitnum, args.end_beta, args.epochs)
    else:
        raise Exception(args.arch + ' is currently not supported')

    if not args.pretrained:
        print('==> Initializing model parameters ...')
    else:
        print('==> Load pretrained model form', args.pretrained, '...')
        pretrained_model = torch.load(args.pretrained)
        model.load_state_dict(pretrained_model['state_dict'])

    if not args.cpu:
        model.cuda()
        # model = torch.nn.DataParallel(model, device_ids=range(torch.cuda.device_count()))
    # print(model)

    learning_rate = float(args.lr)
    criterion = hash_loss
    optimizer = torch.optim.SGD(model.parameters(), args.lr, weight_decay=args.weight_decay, momentum=args.momentum)

    if args.evaluate:
        evaluate()
        exit(0)

    # start training
    for epoch in range(args.epochs):
        adjust_learning_rate(optimizer, epoch)
        train(epoch, input, sim_mat, wgt_mat)
    save_hashcodes(model)
    evaluate()

