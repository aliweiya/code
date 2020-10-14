import time

import numpy as np

from cs231n.classifier.softmax import softmax_loss_naive, softmax_loss_vectorized
from cs231n.datasets.cifar10 import get_CIFAR10_data
from cs231n.gradient_check import grad_check_sparse
from cs231n.classifier.linear_classifier import Softmax

def main():
    X_train, y_train, X_val, y_val, X_test, y_test = get_CIFAR10_data()

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
    
    # Normalize the data: subtract the mean image
    mean_image = np.mean(X_train, axis = 0)
    X_train -= mean_image
    X_val -= mean_image
    X_test -= mean_image
    X_dev -= mean_image
    
    # add bias dimension and transform into columns
    X_train = np.hstack([X_train, np.ones((X_train.shape[0], 1))])
    X_val = np.hstack([X_val, np.ones((X_val.shape[0], 1))])
    X_test = np.hstack([X_test, np.ones((X_test.shape[0], 1))])
    X_dev = np.hstack([X_dev, np.ones((X_dev.shape[0], 1))])

    # Generate a random softmax weight matrix and use it to compute the loss.
    W = np.random.randn(3073, 10) * 0.0001
    loss, grad = softmax_loss_naive(W, X_dev, y_dev, 0.0)

    # As a rough sanity check, our loss should be something close to -log(0.1).
    # Since the weight matrix W is uniform randomly selected, the predicted probability 
    # of each class is uniform distribution and identically equals 1/10, where 10 is the number of classes
    print('loss: %f' % loss)
    print('sanity check: %f' % (-np.log(0.1)))

    f = lambda w: softmax_loss_naive(w, X_dev, y_dev, 0.0)[0]
    grad_numerical = grad_check_sparse(f, W, grad, 10)

    # similar to SVM case, do another gradient check with regularization
    loss, grad = softmax_loss_naive(W, X_dev, y_dev, 1e2)
    f = lambda w: softmax_loss_naive(w, X_dev, y_dev, 1e2)[0]
    grad_numerical = grad_check_sparse(f, W, grad, 10)

    # implement a vectorized version in softmax_loss_vectorized.
    tic = time.time()
    loss_naive, grad_naive = softmax_loss_naive(W, X_dev, y_dev, 0.00001)
    toc = time.time()
    print('Naive loss: {} computed in {}'.format(loss_naive, toc - tic))

    tic = time.time()
    loss_vectorized, grad_vectorized = softmax_loss_vectorized(W, X_dev, y_dev, 0.00001)
    toc = time.time()
    print('Vectorized loss: {} computed in {}'.format(loss_naive, toc - tic))

    grad_difference = np.linalg.norm(grad_naive - grad_vectorized, ord='fro')
    print('Loss difference: %f' % np.abs(loss_naive - loss_vectorized))
    print('Gradient difference: %f' % grad_difference)

    # Use the validation set to tune hyperparameters (regularization strength and
    # learning rate). You should experiment with different ranges for the learning
    # rates and regularization strengths; if you are careful you should be able to
    # get a classification accuracy of over 0.35 on the validation set.
    results = {}
    best_val = -1
    best_softmax = None
    learning_rates = [1e-7, 2e-7, 5e-7]
    #regularization_strengths = [5e4, 1e8]
    regularization_strengths =[(1+0.1*i)*1e4 for i in range(-3,4)] + [(5+0.1*i)*1e4 for i in range(-3,4)]

    for lr in learning_rates:
        for rs in regularization_strengths:
            print('Traing SVM with rs {} and lr {}'.format(rs, lr))
            softmax = Softmax()
            softmax.train(X_train, y_train, lr, rs, num_iters=2000)
            y_train_pred = softmax.predict(X_train)
            train_accuracy = np.mean(y_train == y_train_pred)
            y_val_pred = softmax.predict(X_val)
            val_accuracy = np.mean(y_val == y_val_pred)
            if val_accuracy > best_val:
                best_val = val_accuracy
                best_softmax = softmax           
            results[(lr,rs)] = train_accuracy, val_accuracy
        
    # Print out results.
    for lr, reg in sorted(results):
        train_accuracy, val_accuracy = results[(lr, reg)]
        print('lr %e reg %e train accuracy: %f val accuracy: %f' % (
                    lr, reg, train_accuracy, val_accuracy))
        
    print('best validation accuracy achieved during cross-validation: %f' % best_val)

    # Evaluate the best softmax on test set
    y_test_pred = best_softmax.predict(X_test)
    test_accuracy = np.mean(y_test == y_test_pred)
    print('softmax on raw pixels final test set accuracy: %f' % (test_accuracy, ))

    # Visualize the learned weights for each class
    w = best_softmax.W[:-1,:] # strip out the bias
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