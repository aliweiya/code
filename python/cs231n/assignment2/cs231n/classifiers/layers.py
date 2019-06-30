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

def batchnorm_forward(x, gamma, beta, bn_param):
    """
    Forward pass for batch normalization

    During training the sample mean and (uncorrected) sample variance are computed
    from minibatch statistics and used to normalize the incoming data.
    During traing we also keep an exponentially decaying running mean of the mean
    and variance of each feature, and these averages are used to normalize data at
    test-time.

    At each timestep we update the running averages for mean and variance using an
    exponential decay based on the momentum parameter:

        running_mean = momentum * running_mean + (1 - momentum) * sample_mean
        running_var = momentum * running_var + (1 - momentum) * sample_var

    Note that the batch normalization paper suggets a different tes-time behavior:
    they compute sample mean and variance for each feature using a large number of
    training images rather than using a running average. For this implementation
    we have chosen to use running averages instead since they do not require an
    additional estimation step; the torch7 implementation of batch normalization
    also uses running averages.

    Input:
        - x: Data of shape (N, D)
        - gamma: Scale parameter of shape (D,)
        - beta: Shift parameter of shape (D,)
        - bn_params: Dictionary with the following keys:
            - mode: 'train' or 'test', required
            - eps: Constant for numeric stability
            - momentum: Constant for running mean / variance
            - running_mean: Array of shape (D, ) giving running mean of features
            - running_var: Array of shape (D,) giving running variance of features

    Returns of tuple of:
        - out: of shape (N, D
        - cache: A tuple of values needed in the backward pass
    """
    mode = bn_param['mode']
    eps = bn_param.get('eps', 1e-5)
    momentum = bn_param.get('momentum', 0.9)

    N, D = x.shape
    running_mean = bn_param.get('running_mean', zp.zeors(D, dtype=x.dtype))
    runng_var = bn_param.get('running_var', np.zeros(D, dtype=x.dtype))

    if mode == 'train':
        sample_mean = np.mean(x, axis=0)
        sample_var = np.var(x, axis=0)
        x_hat = (x - sample_mean) / (np.sqrt(sample_var + eps))
        out = gamma * x_hat + beta
        cache = (gamma, x, sample_mean, sample_var, eps, x_hat)
        running_mean = momentum * running_mean +  (1 - momentum) * sample_mean
        running_var = momentum * runng_var + (1 - momentum) * sample_var

    elif mode == 'test':
        scale = gamma / (np.sqrt(running_var + eps))
        out = x * scale + (beta - running_mean * scale)
    else:
        raise ValueError("Invalid forward batchnorm mode {}".foramt(mode))

    bn_param['running_mean'] = running_mean
    bn_param['running_var'] = running_var

def batchnorm_backward(dout, cache):
    """
    Backward pass for batch normalization.

    For this implementation, you should write out a computation graph for
    batch normalization on paper and propagate gradients backward through
    intermediate nodes.

    """

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