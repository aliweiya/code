import time

from cifar10 import AlexNet
import torch
import torch.nn as nn
import torch.optim as optim
from torchvision.datasets.cifar import CIFAR10
import torchvision.transforms as transforms
from torch.utils.data import DataLoader

dataset_path = 'G:\\dataset\\cifar10'

"""
    The CIFAR-10 dataset consists of 60000 32x32 colour images in 10 classes, 
with 6000 images per class. There are 50000 training images and 10000 test images. 
    The dataset is divided into five training batches and one test batch, each
with 10000 images. The test batch contains exactly 1000 randomly-selected images
from each class. The training batches contain the remaining images in random order,
but some training batches may contain more images from one class than another.
Between them, the training batches contain exactly 5000 images from each class. 

"""

data_train = CIFAR10(dataset_path,
                   download=True,
                   transform=transforms.Compose([
                       transforms.RandomHorizontalFlip(), # data augmentation: random horizontal flip
                       transforms.ToTensor(),
                       # 数据归一化处理，调用前数据需处理成Tensor
                       transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])]))
data_test = CIFAR10(dataset_path,
                  train=False,
                  download=True,
                  transform=transforms.Compose([
                        transforms.ToTensor(),
                        transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])]))
data_train_loader = DataLoader(data_train, batch_size=256, shuffle=True, num_workers=1)
data_test_loader = DataLoader(data_test, batch_size=1024, num_workers=1)

net = AlexNet()
criterion = nn.CrossEntropyLoss()
optimizer = optim.Adam(net.parameters(), lr=2.5e-3)

def train(epoch):
    global cur_batch_win
    net.train()
    loss_list, batch_list = [], []
    tic = time.time()
    for i, (images, labels) in enumerate(data_train_loader):
        optimizer.zero_grad()

        output = net(images)

        loss = criterion(output, labels)

        loss_list.append(loss.detach().cpu().item())
        batch_list.append(i+1)

        if i % 10 == 0:
            toc = time.time()
            print('Train - Epoch %d, Batch: %d, Loss: %f, time: %f' % (epoch, i, loss.detach().cpu().item(), toc-tic))
            tic = time.time()

        loss.backward()
        optimizer.step()


def test():
    net.eval()
    total_correct = 0
    avg_loss = 0.0
    for i, (images, labels) in enumerate(data_test_loader):
        output = net(images)
        avg_loss += criterion(output, labels).sum()
        pred = output.detach().max(1)[1]
        total_correct += pred.eq(labels.view_as(pred)).sum()

    avg_loss /= len(data_test)
    print('Test Avg. Loss: %f, Accuracy: %f' % (avg_loss.detach().cpu().item(), float(total_correct) / len(data_test)))


def train_and_test(epoch):
    train(epoch)
    test()


def main():
    for e in range(1, 100):
        train_and_test(e)
    # train_and_test(1)


if __name__ == '__main__':
    main()
