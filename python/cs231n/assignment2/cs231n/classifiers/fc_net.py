import numpy as np

from .layer_utils import affine_relu_forward, affine_relu_backward
from .layers import affine_forward, affine_backward, softmax_loss

class TwoLayerNet:
    """
    A two-layer fully-connected neural network with ReLU nonlinearity and
    softmax loss that uses a modular layer design. We assume an input dimension
    of D, a hidden dimension of H, and perform classification over C classes.

    The architecture should be affine - relu - affine - softmax

    Note that this class does not implement gradient descent; instead, it will
    interact with a separate Solver object that is responsible for running optimization

    The learning parameters of the model are stored in the dictionary self.params that
    maps parameter names to numpy arrays.
    """
    def __init__(self, input_dim=3*32*32, hidden_dim=100, num_classes=10,
                       weight_scale=1e-3, reg=0.0):
        """
        Initialize a new network

        Inputs:
            - input_dim: An integer giving the size of the input
            - hidden_dim: An integer giving the size of the hidden layer
            - num_classes: An integer giving the number of classes to classify
            - dropout: Scalar between 0 and 1 giving dropout strength
            - weight-scale: Scalar giving the standard deviation for random
                initialization of the weights
            - reg: Scalar giving L2 regularization strength
        """
        self.params = {}
        self.reg = reg

        self.params['W1'] = weight_scale * np.random.randn(input_dim, hidden_dim)
        self.params['b1'] = np.zeros(hidden_dim)
        self.params['W2'] = weight_scale * np.random.randn(hidden_dim, num_classes)
        self.params['b2'] = np.zeros(num_classes)

    def loss(self, X, y=None):
        """
        Compute the loss and gradient for a minibatch of data.

        Inputs:
            - X: Array of input data of shape (N, d1, ..., d_k)
            - y: Array of labels, of shape (N,) y[i] gives the label of X[i]

        Returns:
            If y is None, then run a test-time forward pass for the model and return:
            - scores: Array of shape (N, C) giving classification scores, where scores[i, c]
                is the classification score for N[i] and class c
            If y is not None, then run a training-time forward and backward pass and return
            a tuple of
            - loss: Scalar value giving the loss
            - grads: Dictionary with the same keys as self.params, mapping parameter names 
                to gradients of the loss with respect to those parameters.
        """
        ar1_out, ar1_cache = affine_relu_forward(X, self.params['W1'], self.params['b1'])
        a2_out, a2_cache = affine_forward(ar1_out, self.params['W2'], self.params['b2'])
        scores = a2_out

        if y is None:
            return scores

        grads = {}
        loss, dscores = softmax_loss(scores, y)
        loss = loss + 0.5 * self.reg * np.sum(self.params['W1'] * self.params['W1']) + 0.5 * self.reg * np.sum(self.params['W2'] * self.params['W2'])
        dx2, dw2, db2 = affine_backward(dscores, a2_cache)
        grads['W2'] = dw2 + self.reg * self.params['W2']
        grads['b2'] = db2

        dx1, dw1, db1 = affine_relu_backward(dx2, ar1_cache)
        grads['W1'] = dw1 + self.reg * self.params['W1']
        grads['b1'] = db1

        return loss, grads