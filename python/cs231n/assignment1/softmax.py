import time

from cs231n.classifiers.softmax import softmax_loss_naive
from cs231n.datasets.cifar10 import get_CIFAR10_data

def main():
    X_train, y_train, X_val, y_val, X_test, y_test = get_CIFAR10_data()

    # Generate a random softmax weight matrix and use it to compute the loss.
    W = np.random.randn(3073, 10) * 0.0001
    loss, grad = softmax_loss_naive(W, X_dev, y_dev, 0.0)

if __name__ == '__main__':
    main()