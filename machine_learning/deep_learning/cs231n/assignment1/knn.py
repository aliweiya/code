import time

import numpy as np
import matplotlib.pyplot as plt

from cs231n.classifier.k_nearest_neighbor import KNearestNeighbor
from cs231n.datasets.cifar10 import CIFAR10

def visualize(X_train, y_train, X_test, y_test):
    classes = ['plane', 'car', 'bird', 'cat', 'deer', 'dog', 'frog', 'horse', 'ship', 'truck']
    num_classes = len(classes)
    samples_per_class = 7
    for y, c in enumerate(classes):
        # Return indices that are non-zero in the flattened version of a.
        idxs = np.flatnonzero(y_train == y)
        idxs = np.random.choice(idxs, samples_per_class, replace=False)
        for i, idx in enumerate(idxs):
            plt_idx = i * num_classes + y + 1
            plt.subplot(samples_per_class, num_classes, plt_idx)
            plt.imshow(X_train[idx].astype('uint8'))
            plt.axis('off')
            if i == 0:
                plt.title(c)

    plt.show()

def main():
    cifar10 = CIFAR10()
    X_train, y_train, X_test, y_test = cifar10.load_CIFAR10()

    # Visualize some examples from the dataset
    visualize(X_train, y_train, X_test, y_test)

    # Subsample the data for more efficient code execution
    num_training = 500
    mask = range(num_training)
    X_train = X_train[mask]
    y_train = y_train[mask]

    num_test = 500
    X_test = X_test[mask]
    y_test = y_test[mask]

    # Reshape the image data into rows
    X_train = np.reshape(X_train, (X_train.shape[0], -1))
    X_test = np.reshape(X_test, (X_test.shape[0], -1))

    # Create a kNN classifier instance 
    classifier = KNearestNeighbor()
    classifier.train(X_train, y_train)

    # classify the data
    start = time.time()
    dists = classifier.compute_distances_two_loops(X_test)
    end = time.time()
    print('compute_distances_two_loops cost {}'.format(end-start))

    # visualize the distance matrix: each row is a single test
    # example and its distances to training examples
    # plt.imshow(dists, interpolation='none')
    # plt.show()

    # Now implement the function predict_labels
    # We use  k=1 (which is Nearest Neighbor)
    y_test_pred = classifier.predict_labels(dists, k=1)

    # Compute and print the fraction of correctly predicted examples
    num_correct = np.sum(y_test_pred == y_test)
    accuracy = num_correct / num_test
    print('Got {} / {} correct => accuracy: {}'.format(num_correct, num_test, accuracy))

    # Now Let's speed up distance matrix computation by using partial vectorization
    # with one loop.
    start = time.time()
    dists_one = classifier.compute_distances_one_loop(X_test)
    end = time.time()
    print('compute_distances_one_loop cost {}'.format(end-start))

    # To ensure that our vectorized implementation is correct, we make sure that it
    # agrees with the naive implementation. There are many ways to decide whether
    # two matrices are similar; one of the simplest is the Frobenius norm. In case
    # you haven't seen it before, the Frobenius norm of two matrices is the square
    # root of the squared sum of differences of all elements; in other words, reshape
    # the matrices into vectors and compute the Euclidean distance between them.

    # Matrix or vector norm. (矩阵或向量的范数)
    difference = np.linalg.norm(dists - dists_one, ord='fro')
    if difference < 0.001:
        print('Good! The distance matrices are the same')
    else:
        print('Uh-oh! The distance matrices are different')

    # Now implement the fully vectorized version
    start = time.time()
    dists_two = classifier.compute_distances_no_loops(X_test)
    end = time.time()
    print('compute_distances_no_loops cost {}'.format(end-start))

    difference = np.linalg.norm(dists - dists_one, ord='fro')
    if difference < 0.001:
        print('Good! The distance matrices are the same')
    else:
        print('Uh-oh! The distance matrices are different')

    # Cross Validation
    # We will now determine the best value of hyperparameter k with cross-validation
    num_folds = 5
    k_choices = [1, 3, 5, 8, 10, 12, 20, 50, 100]
    
    X_train_folds = []
    y_train_folds = []
    y_train_ = y_train.reshape(-1, 1)
    X_train_folds, y_train_folds = np.array_split(X_train, num_folds), np.array_split(y_train_, num_folds)

    # A dictionary holding the accuracies for different values of k
    k_to_accuracies = {}

    for k_ in k_choices:
        k_to_accuracies.setdefault(k_, [])

    for i in range(num_folds):
        classifier = KNearestNeighbor()
        # X_val_train = np.vstack(X_train_folds[0:i] + X_train_folds[i+1:])
        # y_val_train = np.vstack(y_train_folds[0:i] + y_train_folds[i+1:])
        # y_val_train = y_val_train[:, 0]
        # Same as follows
        X_val_train = X_train
        y_val_train = y_train
        classifier.train(X_val_train, y_val_train)
        for k_ in k_choices:
            y_val_pred = classifier.predict(X_train_folds[i], k=k_)
            num_correct = np.sum(y_val_pred == y_train_folds[i][:, 0])
            accuracy =num_correct / len(y_val_pred)
            k_to_accuracies[k_] = k_to_accuracies[k_] + [accuracy]

    for k in sorted(k_to_accuracies):
        for accuracy in k_to_accuracies[k]:
            print('k = {}, accuracy = {}'.format(k, accuracy))

    # Plot the raw observations
    for k in k_choices:
        accuracies = k_to_accuracies[k]
        plt.scatter([k]*len(accuracies), accuracies)

    # Plot the trend line with error bars that correspond to standard deviation
    accuracies_mean = np.array([np.mean(v) for k, v in sorted(k_to_accuracies.items())])
    accuracies_std = np.array([np.std(v) for k, v in sorted(k_to_accuracies.items())])
    # plt.errorbar(k_choices, accuracies_mean, yerr=accuracies_std)
    # plt.title('Cross-validation on k')
    # plt.xlabel('k')
    # plt.ylabel('Cross-validation accuracy')
    # plt.show()

    # Choose the best value for k
    best_k = 10
    classifier = KNearestNeighbor()
    classifier.train(X_train, y_train)
    y_test_pred = classifier.predict(X_test, k=best_k)

    num_correct = np.sum(y_test_pred == y_test)
    accuracy = num_correct / num_test
    print('Got {} / {} correct => accuracy: {}'.format(num_correct, num_test, accuracy))

if __name__ == '__main__':
    main()