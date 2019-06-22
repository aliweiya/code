import math
import random
import time

import numpy as np
import matplotlib.pyplot as plt

from cs231n.datasets.cifar10 import get_CIFAR10_data
from cs231n.classifier.linear_svm import svm_loss_naive,svm_loss_vectorized
from cs231n.classifier.linear_classifier import LinearSVM
from cs231n.gradient_check import grad_check_sparse

from knn import visualize

"""
Multiclass Support Vector Machine
"""

def main():
    X_train, y_train, X_val, y_val, X_test, y_test = get_CIFAR10_data()
    # visualize(X_train, y_train, X_test, y_test)

    # We will also make a development set, which is a small subset of
    # the training set.
    num_training = 49000
    num_dev = 500
    mask = np.random.choice(num_training, num_dev, replace=False)
    X_dev = X_train[mask]
    y_dev = y_train[mask]

    # Preprocessing: reshape the image data into rows
    X_train = np.reshape(X_train, (X_train.shape[0], -1))
    X_val = np.reshape(X_val, (X_val.shape[0], -1))
    X_test = np.reshape(X_test, (X_test.shape[0], -1))
    X_dev = np.reshape(X_dev, (X_dev.shape[0], -1))

    # Preprocessing: substract the mean image
    # first: compute the image mean based on the training data
    # 如果不提供axis参数，则计算所有元素平均值
    mean_image = np.mean(X_train, axis=0)
    # plt.figure(figsize=(4, 4))
    # plt.imshow(mean_image.reshape(32, 32, 3).astype('uint8'))
    # plt.show()

    # second: subtract the mean image from train and test data
    X_train -= mean_image
    X_val -= mean_image
    X_test -= mean_image
    X_dev -= mean_image

    # third: append the bias dimension of ones so that our SVM
    # only has to worry about optimizing a single weight matrix W
    X_train = np.hstack([X_train, np.ones((X_train.shape[0], 1))])
    X_val = np.hstack([X_val, np.ones((X_val.shape[0], 1))])
    X_test = np.hstack([X_test, np.ones((X_test.shape[0], 1))])
    X_dev = np.hstack([X_dev, np.ones((X_dev.shape[0], 1))])

    # SVM Classifier
    # Start with random W and find a W that minimizes the loss
    W = np.random.randn(3073, 10) * 0.0001
    loss, grad = svm_loss_naive(W, X_dev, y_dev, 0.0)
    print('loss: {}'.format(loss))

    # To check that you have correctly implemented the gradient correctly,
    # you can numerically estimate the gradient of the loss function and
    # compare the numeric estimate to the gradient that you computed. 
    # f = lambda w: svm_loss_naive(w, X_dev, y_dev, 1e2)[0]
    # grad_numerical = grad_check_sparse(f, W, grad)

    # Next implement the function svm_loss_vectorized; for now only compute the loss;
    tic = time.time()
    loss_naive, grad_naive = svm_loss_naive(W, X_dev, y_dev, 0.00001)
    toc = time.time()
    print('Naive loss: {} computed in {}'.format(loss_naive, toc-tic))

    tic = time.time()
    loss_vectorized, grad_vectorized = svm_loss_vectorized(W, X_dev, y_dev, 0.00001)
    toc = time.time()
    print('Vectorized loss: {} computed in {}'.format(loss_vectorized, toc-tic))

    print('difference: {}'.format(loss_naive - loss_vectorized))

    # Compute the gradient of the loss function in a vectorized way
    difference = np.linalg.norm(grad_naive - grad_vectorized, ord='fro')
    print('difference: {}'.format(difference))

    # SGD
    svm = LinearSVM()
    tic = time.time()
    loss_hist = svm.train(X_train, y_train, learning_rate=1e-7, reg=5e4, num_iters=1500, verbose=True)
    toc = time.time()
    print("That took {}".format(toc-tic))

    # plot the loss
    # plt.plot(loss_hist)
    # plt.xlabel("Iteration number")
    # plt.ylabel("Loss value")
    # plt.show()

    # Evaluate the performance on both the training and validation set
    y_train_pred = svm.predict(X_train)
    print('Training accuracy: {}'.format(np.mean(y_train == y_train_pred)))
    y_val_pred = svm.predict(X_val)
    print("Validation accuracy: {}".format(np.mean(y_val == y_val_pred)))

    # Use the validation set to tune hyperparameters
    learing_rate = [1.4e-7, 1.5e-7, 1.6e-7]
    regulartization_strengths = [(1+i*0.1)*1e-4 for i in range(-3, 3)] + [(2+0.1*i)*1e-4 for i in range(-3,3)]

    results = {}
    best_val = -1
    best_svm = None

    for rs in regulartization_strengths:
        for lr in learing_rate:
            print('Traing SVM with rs {} and lr {}'.format(rs, lr))
            svm = LinearSVM()
            loss_hist = svm.train(X_train, y_train, lr, rs, num_iters=3000)
            y_train_pred = svm.predict(X_train)
            train_accuracy = np.mean(y_train == y_train_pred)
            y_val_pred = svm.predict(X_val)
            val_accuracy = np.mean(y_val == y_val_pred)
            if val_accuracy > best_val:
                best_val = val_accuracy
                best_svm = svm
            results[(lr, rs)] = train_accuracy, val_accuracy

    # Print the results
    for lr, reg in sorted(results):
        train_accuracy, val_accuracy = results[(lr, reg)]
        print('lr {} reg {} train accuracy {} val accuracy: {}'.format(lr, reg, train_accuracy, val_accuracy))
    
    print('best validation accuracy achieved during cross-validation: {}'.format(best_val))

    # Visualize the cross-validation results
    x_scatter = [math.log10(x[0]) for x in results]
    y_scatter = [math.log10(x[1]) for x in results]
    # plot training accuracy
    marker_size = 100
    colors = [results[x][0] for x in results]
    plt.subplot(2, 1, 1)
    plt.scatter(x_scatter, y_scatter, marker_size, c=colors)
    plt.colorbar()
    plt.xlabel('log learning rate')
    plt.ylabel('log retgularization strength')
    plt.title('CIFAR-10 training accuracy')

    # plot validation accuracy
    colors = [results[x][1] for x in results]
    plt.subplot(2, 1, 2)
    plt.scatter(x_scatter, y_scatter, marker_size, c=colors)
    plt.colorbar()
    plt.xlabel('log learning rate')
    plt.ylabel('log retgularization strength')
    plt.title('CIFAR-10 validation accuracy')
    plt.show()

    # Evaluate the best svm on test set
    y_test_pred = best_svm.predict(X_test)
    test_accuracy = np.mean(y_test == y_test_pred)
    print('Linear SVM on raw pixels final test set accuracy: {}'.format(test_accuracy))

    # Visualize the learned weights for each class.
    # Depending on your choice of learning rate and regularization strength, these may
    # or may not be nice to look at.
    w = best_svm.W[:-1,:] # strip out the bias
    w = w.reshape(32, 32, 3, 10)
    w_min, w_max = np.min(w), np.max(w)
    classes = ['plane', 'car', 'bird', 'cat', 'deer', 'dog', 'frog', 'horse', 'ship', 'truck']
    for i in range(10):
        plt.subplot(2, 5, i + 1)
            
        # Rescale the weights to be between 0 and 255
        wimg = 255.0 * (w[:, :, :, i].squeeze() - w_min) / (w_max - w_min)
        plt.imshow(wimg.astype('uint8'))
        plt.axis('off')
        plt.title(classes[i])

if __name__ == '__main__':
    main()