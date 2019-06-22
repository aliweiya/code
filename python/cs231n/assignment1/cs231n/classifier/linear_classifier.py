import numpy as np

from .linear_svm import svm_loss_vectorized

class LinearClassifier:
    def __init__(self):
        self.W = None

    def train(self, X, y, learning_rate=1e-3, reg=1e-5, num_iters=100, batch_size=200, verbose=False):
        """
        Train this linear classifier using SGD
        
        Inputs:
            - X: A numpy array of shape (N, D) containing training data;
                there are N training samples each of dimension D.
            - y: A numpy array of shape (N, ) containing training labels;
                y[i] = c means that X[i] has label 0 <= c < C for c classes
            - learning_rate: (float) learning rate for optimization.
            - reg: (float) regularization strength.
            - num_iters: (integer) number of steps to take when optimizing
            - batch_size: (integer) number of training examples to use at each step.
            - verbose: (boolean) If true, print progress during optimization.

        Outputs:
            A list containing the value of the loss function at each training iteration.
        """
        num_train, dim = X.shape
        num_classes = np.max(y) + 1
        if self.W is None:
            # lazily initialize W
            self.W = 0.001 * np.random.randn(dim, num_classes)

        # Run SGD to optimize W
        loss_history = []
        for it in range(num_iters):
            batch_idx = np.random.choice(num_train, batch_size, replace=True)
            X_batch = X[batch_idx]
            y_batch = y[batch_idx]

            # evaluate loss and gradient
            loss, grad = self.loss(X_batch, y_batch, reg)
            loss_history.append(loss)

            # perform parameter update
            self.W += - learning_rate * grad

            if verbose and it % 100 == 0:
                print("iteration {} / {}: loss of {}".format(it, num_iters, loss))

        return loss_history

    def predict(self, X):
        """
        Use the trained weights of this linear classifier to predict labels for
        data points.

        Args:
            - X: D x N array of training data. Each column is a D-dimensional point.

        Returns:
            - y_pred: Predicted labels for the data in X. y_pred is a 1-dimensional
                array of length N, and each element is an integer giving the predicted
                class.
        """
        y_pred = np.zeros(X.shape[1])
        scores = X.dot(self.W)
        y_pred = np.argmax(scores, axis=1)
        return y_pred

class LinearSVM(LinearClassifier):
    def loss(self, X_batch, y_batch, reg):
        return svm_loss_vectorized(self.W, X_batch, y_batch, reg)