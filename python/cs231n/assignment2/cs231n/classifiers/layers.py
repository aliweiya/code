import numpy as np

def affine_forward(x, w, b):
    """
    Computes the forward pass for an affline (fully-connected) layer

    The input x has shape (N, d_1,...,d_k) and contains a minibtach of N
    examples, where each example x[i] has shape (d_1,...,d_k). We will
    reshape each input into a vector of dimension D=d1 * ... * dk, and
    then transform it to an output vector of dimension M.

    N is the number of input neurons, M is the number of output neurons.

    Inputs:
    - x: A numpy array containing input data, of shape (N, d_1, ..., d_k)
    - w: A numpy array of weights, of shape (D, M)
    - b: A numpy array of biases, of shape (M,)

    Returns a tuple of:
    - out: output, of shape(N, M)
    - cache: (x, w, b)
    """
    
    N = x.shape[0]
    x_rsp = x.reshape(N, -1)
    out = x_rsp.dot(w) + b

    cache = (x, w, b)
    return out, cache

def affine_backward(dout, cache):
    """
    Computes the backward pass for an affine layer

    Inputs:
        - dout: Upstream derivative, of shape (N, M)
        - cache: Tuple of:
            - x: Input data, of shape (N, d_1, ..., d_k)
            - w: Weights, of shape (D, M)
    Returns of tuple of:
        - dx: Gradient with respect to x, of shape (N, d1, ..., dk)
        - dw: Gradient with respect to w, of shape (D, M)
        - db: Gradient with respect to b, of shape (M,)
    """
    x, w, b = cache
    N = x.shape[0]
    x_rsp = x.reshape(N, -1)
    dx = dout.dot(w.T)
    dx = dx.reshape(*x.shape)
    dw = x_rsp.T.dot(dout)
    db = np.sum(dout, axis=0)
    return dx, dw, db

def relu_forward(x):
    """
    Computes the forward pass for a layer of rectified linear units(ReLUs)

    Inputs:
        - x: Inputs of any shape

    Returns a tuple of:
        - out: Output, of the same shape as x
        - cache: x
    """
    out = x * (x > 0)
    cache = x
    return out, cache

def relu_backward(dout, cache):
    """
    Computes the backward pass for a layer of rectified linear units (ReLUs)

    Input:
        - dout: Upstream derivatives, of any shape
        - cache: Input x, of same shape as dout

    Returns:
        - dx: Gradient with respect to x
    """
    x = cache
    dx = (x > 0) * dout

    return dx

def svm_loss(X, y):
    """
    Computes the loss and gradient using for multiclass SVM classification
    
    Inputs:
        - X: Input data, of shape (N, C) where X[i, j] is the score for the jth class
            for the ith input
        - y: Vector of labels, of shape (N,) where y[i] is the label for x[i] and 
            0 <= y[i] < C
    Returns a tuple of:
        - loss: Scalar giving the loss
        - dx: Gradient of the loss with respect to x
    """
    N = X.shape[0]
    correct_class_scores = X[np.arange(N), y]
    margins = np.maximum(0, X-correct_class_scores[:, np.newaxis] + 1.0)
    margins[np.arange(N), y] = 0
    loss = np.sum(margins) / N
    num_pos = np.sum(margins > 0, axis=1)
    dx = np.zeros_like(X)
    dx[margins > 0] = 1
    dx[np.arange(N),  y] -= num_pos
    dx /= N
    return loss, dx

def softmax_loss(X, y):
    """
    Computes the loss and gradient using for multiclass softmax classification
    
    Inputs:
        - X: Input data, of shape (N, C) where X[i, j] is the score for the jth class
            for the ith input
        - y: Vector of labels, of shape (N,) where y[i] is the label for x[i] and 
            0 <= y[i] < C
    Returns a tuple of:
        - loss: Scalar giving the loss
        - dx: Gradient of the loss with respect to x
    """
    probs = np.exp(X - np.max(X, axis=1, keepdims=True))
    probs /= np.sum(probs, axis=1, keepdims=True)
    N = X.shape[0]
    loss = -np.sum(np.log(probs[np.arange(N), y])) / N
    dx = probs.copy()
    dx[np.arange(N), y] -= 1
    dx /= N
    return loss, dx