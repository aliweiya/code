import time

from vgg import VGG16
import torch
import torch.nn as nn
import torch.optim as optim
from torchvision.datasets.cifar import CIFAR10
import torchvision.transforms as transforms
from torch.utils.data import DataLoader

dataset_path = '/root/M/datasets/cifar10'

data_train = CIFAR10(dataset_path,
                   download=True,
                   transform=transforms.Compose([
                       transforms.RandomHorizontalFlip(), # data augmentation: random horizontal flip
                       transforms.Resize((224,224)),
                       transforms.ToTensor(),
                       # 数据归一化处理，调用前数据需处理成Tensor
                       transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])]))
data_test = CIFAR10(dataset_path,
                  train=False,
                  download=True,
                  transform=transforms.Compose([
                        transforms.Resize((224,224)),
                        transforms.ToTensor(),
                        transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])]))
data_train_loader = DataLoader(data_train, batch_size=32, shuffle=True, num_workers=1)
data_test_loader = DataLoader(data_test, batch_size=32, num_workers=1)

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

net = VGG16(device)
net.to(device)
criterion = nn.CrossEntropyLoss()
optimizer = optim.Adam(net.parameters(), lr=1e-5)

def train(epoch):
    global cur_batch_win
    net.train()
    loss_list, batch_list = [], []
    tic = time.time()
    for i, (images, labels) in enumerate(data_train_loader):
        optimizer.zero_grad()

        output = net(images)

        loss = criterion(output, labels.to(device))

        loss_list.append(loss.detach().cpu().item())
        batch_list.append(i+1)

        toc = time.time()
        print('Train - Epoch %d, Batch: %d, Loss: %f, time: %f' % (epoch, i, loss.detach().cpu().item(), toc-tic))
        tic = time.time()

        # 这里需要在GPU上计算，所以loss不能转CPU
        loss.backward()
        optimizer.step()

def test():
    net.eval()
    total_correct = 0
    avg_loss = 0.0
    for i, (images, labels) in enumerate(data_test_loader):
        output = net(images)
        avg_loss += criterion(output.detach().cpu(), labels).sum()
        pred = output.detach().cpu().max(1)[1]
        total_correct += pred.eq(labels.view_as(pred)).sum()

    avg_loss /= len(data_test)
    print('Test Avg. Loss: %f, Accuracy: %f' % (avg_loss.item(), float(total_correct) / len(data_test)))


def train_and_test(epoch):
    train(epoch)
    test()

def main():
    for e in range(1, 100):
        train_and_test(e)
    # train_and_test(1)

if __name__ == '__main__':
    main()
