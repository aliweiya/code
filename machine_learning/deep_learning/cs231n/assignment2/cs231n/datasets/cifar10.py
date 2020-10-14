import os
import pickle

import numpy as np

class CIFAR10:
    """CIFAR-10 dataset

    The CIFAR-10 dataset consists of 60000 32x32 images in 10 classes,
    with 6000 images per class.

    There are 50000 training images and 10000 test images.

    The dataset is divided into five training batches and one test batch,
    the test batch contains exactly 1000 randomly-selected images from each class.

    The data is a 1000x3072 numpy array of uint8. Each row of the array stores 32x32 image.
    The first 1024 entries contain the red channel values, the next 1024 the green, and the final
    1024 the blue.

    The labels is a list of 10000 numbers in the range 0-9 (label name can be found in batches.meta)

    Links:
        - Download at: https://www.cs.toronto.edu/~kriz/cifar-10-python.tar.gz
        - https://www.cs.toronto.edu/~kriz/cifar.html
    """
    def __init__(self, cifar_root=None):
        self.cifar_root = cifar_root
        if not self.cifar_root:
            self.cifar_root = 'D:\\personal\\dataset\\cifar-10-batches-py'

    def load_CIFAR10_batch(self, filename):
        with open(filename, 'rb') as f:
            datadict = pickle.load(f, encoding='bytes')
            X = datadict[b'data']
            Y = datadict[b'labels']
            # 1000个样本，每个是3*32*32的图片，改成32*32*3的
            X = X.reshape(10000, 3, 32, 32).transpose(0,2,3,1).astype("float")
            Y = np.array(Y)
            return X, Y

    def load_CIFAR10(self, cifar_root=None):
        if cifar_root:
            self.cifar_root = cifar_root

        assert self.cifar_root, 'Please supply the root of CIFAR10 dataset.'
        xs = []
        ys = []

        for batch in range(1, 6):
            f = os.path.join(self.cifar_root, 'data_batch_{}'.format(batch))
            X, Y = self.load_CIFAR10_batch(f)
            xs.append(X)
            ys.append(Y)

        # 对数组进行拼接
        # 在拼接方向axis轴上数组间的形状一致
        Xtr = np.concatenate(xs)
        Ytr = np.concatenate(ys)

        # 加载测试集
        Xte, Yte = self.load_CIFAR10_batch(os.path.join(self.cifar_root, 'test_batch'))
        return Xtr, Ytr, Xte, Yte


def get_CIFAR10_data(num_training=49000, num_validation=1000, num_test=1000):
    cifar10 = CIFAR10()
    X_train, y_train, X_test, y_test = cifar10.load_CIFAR10()

    # Subsample the data
    # mask = range(num_training, num_training + num_validation)
    # X_val = X_train[mask]
    # y_val = y_train[mask]
    # mask = range(num_training)
    # X_train = X_train[mask]
    # y_train = y_train[mask]
    # mask = range(num_test)
    # X_test = X_test[mask]
    # y_test = y_test[mask]
    X_val = X_train[num_training:]
    y_val = y_train[num_training:]
    X_train = X_train[:num_training]
    y_train = y_train[:num_training]

    return X_train, y_train, X_val, y_val, X_test, y_test

if __name__ == '__main__':
    cifar10 = CIFAR10()
    cifar10.load_CIFAR10()