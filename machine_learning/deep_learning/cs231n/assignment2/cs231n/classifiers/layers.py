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
    """
    链式法则，df = w
    """
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
    out, cache = None, None
    running_mean = bn_param.get('running_mean', np.zeros(D, dtype=x.dtype))
    running_var = bn_param.get('running_var', np.zeros(D, dtype=x.dtype))

    if mode == 'train':
        sample_mean = np.mean(x, axis=0)
        sample_var = np.var(x, axis=0)
        x_hat = (x - sample_mean) / (np.sqrt(sample_var + eps))
        out = gamma * x_hat + beta
        cache = (gamma, x, sample_mean, sample_var, eps, x_hat)
        running_mean = momentum * running_mean +  (1 - momentum) * sample_mean
        running_var = momentum * running_var + (1 - momentum) * sample_var

    elif mode == 'test':
        scale = gamma / (np.sqrt(running_var + eps))
        out = x * scale + (beta - running_mean * scale)
    else:
        raise ValueError("Invalid forward batchnorm mode {}".foramt(mode))

    bn_param['running_mean'] = running_mean
    bn_param['running_var'] = running_var

    return out, cache

def batchnorm_backward(dout, cache):
    """
    Backward pass for batch normalization.

    For this implementation, you should write out a computation graph for
    batch normalization on paper and propagate gradients backward through
    intermediate nodes.

    Inputs:
        - dout: Upstream derivatives, of shape (N, D)
        - cache: Variable of intermediates from batchnorm_forward

    Returns a tuple of:
        - dx: Gradient with respect to inputs x, of shape (N, D)
        - dgamma: Gradient with respect to scale parameter gamma, of shape (D,)
        - dbeta: Gradient with respect to shift parameter beta, of shape (D,)
    """
    gamma, x, u_b, sigma_squared_b, eps, x_hat = cache
    N = x.shape[0]

    dx_1 = gamma * dout
    dx_2_b = np.sum((x - u_b) * dx_1, axis=0)
    dx_2_a = ((sigma_squared_b + eps) ** -0.5) * dx_1
    dx_3_b = (-0.5) * ((sigma_squared_b + eps) ** -1.5) * dx_2_b
    dx_4_b = dx_3_b * 1
    dx_5_b = np.ones_like(x) / N * dx_4_b
    dx_6_b = 2 * (x - u_b) * dx_5_b
    dx_7_a = dx_6_b * 1 + dx_2_a * 1
    dx_7_b = dx_6_b * 1 + dx_2_a * 1
    dx_8_b = -1 * np.sum(dx_7_b, axis=0)
    dx_9_b = np.ones_like(x) / N * dx_8_b
    dx_10 = dx_9_b + dx_7_a

    dgamma = np.sum(x_hat * dout, axis=0)
    dbeta = np.sum(dout, axis=0)
    dx = dx_10
    return dx, dgamma, dbeta

def batchnorm_backward_alt(dout, cache):
    """
    Alternative backward pass for batch normalization.
    
    For this implementation you should work out the derivatives for the batch
    normalizaton backward pass on paper and simplify as much as possible. You
    should be able to derive a simple expression for the backward pass.
    
    Note: This implementation should expect to receive the same cache variable
    as batchnorm_backward, but might not use all of the values in the cache.
    
    Inputs / outputs: Same as batchnorm_backward
    """
    dx, dgamma, dbeta = None, None, None
    gamma, x, sample_mean, sample_var, eps, x_hat = cache
    N = x.shape[0]
    dx_hat = dout * gamma
    dvar = np.sum(dx_hat* (x - sample_mean) * -0.5 * np.power(sample_var + eps, -1.5), axis = 0)
    dmean = np.sum(dx_hat * -1 / np.sqrt(sample_var +eps), axis = 0) + dvar * np.mean(-2 * (x - sample_mean), axis =0)
    dx = 1 / np.sqrt(sample_var + eps) * dx_hat + dvar * 2.0 / N * (x-sample_mean) + 1.0 / N * dmean
    dgamma = np.sum(x_hat * dout, axis = 0)
    dbeta = np.sum(dout , axis = 0)
    
    return dx, dgamma, dbeta

def dropout_forward(x, dropout_param):
    """
    Performs the forward pass for (inverted) dropout.

    Inputs:
    - x: Input data, of any shape
    - dropout_param: A dictionary with the following keys:
        - p: Dropout parameter. We drop each neuron output with probability p.
        - mode: 'test' or 'train'. If the mode is train, then perform dropout;
        if the mode is test, then just return the input.
        - seed: Seed for the random number generator. Passing seed makes this
        function deterministic, which is needed for gradient checking but not in
        real networks.

    Outputs:
    - out: Array of the same shape as x.
    - cache: A tuple (dropout_param, mask). In training mode, mask is the dropout
        mask that was used to multiply the input; in test mode, mask is None.
    """
    p, mode = dropout_param['p'], dropout_param['mode']
    if 'seed' in dropout_param:
        np.random.seed(dropout_param['seed'])

    mask = None
    out = None

    if mode == 'train':
        mask = (np.random.rand(*x.shape) >= p) / (1 - p)
        #mask = (np.random.rand(x.shape[1]) >= p) / (1 - p)
        out = x * mask
    elif mode == 'test':
        out = x

    cache = (dropout_param, mask)
    out = out.astype(x.dtype, copy=False)

    return out, cache

def dropout_backward(dout, cache):
    """
    Perform the backward pass for (inverted) dropout.

    Inputs:
    - dout: Upstream derivatives, of any shape
    - cache: (dropout_param, mask) from dropout_forward.
    """
    dropout_param, mask = cache
    mode = dropout_param['mode']
    
    dx = None
    if mode == 'train':
        dx = dout * mask
    elif mode == 'test':
        dx = dout
    return dx

def conv_forward_naive(x, w, b, conv_param):
    """
    A naive implementation of the forward pass for a convolutional layer

    The input consists of N data points, each with C channels. height H
    and width W. We convolve each input with F difference filters, where
    each filter spans all C channels and has height HH and width WW.

    Input:
        - x: Input data of shape (N, C, H, W)
        - w: Filter weights of shape (F, C, HH, WW)
        - b: Biases, of shape (F,)
        - conv_param: A dictionary with the following keys:
            - stride: The number of pixels between adjacent receptive fields
                in the horizontal and vertical directions.
            - pad: The number of pixels that will be used to zero-pad the input.

    Return a tuple of:
        - out: Output data, of shape (N, F, H', W') where H' and W' are given by
            - H' = 1 + (H + 2 * pad - HH) / stride
            - H' = 1 + (W + 2 * pad - WW) / stride
        - cache: (x, w, b, conv_param)
    """
    import pdb;pdb.set_trace()
    N, C, H, W = x.shape
    F, _, HH, WW = w.shape
    stride, pad = conv_param['stride'], conv_param['pad']
    # (N - F) / stride + 1 from cs231n
    H_out = 1 + int((H + 2 * pad - HH) / stride)
    W_out = 1 + int((W + 2 * pad - WW) / stride)

    out = np.zeros((N, F, H_out, W_out))
    x_pad = np.pad(x, ((0,), (0,), (pad,), (pad,)), mode='constant', constant_values=0)
    for i in range(H_out):
        for j in range(W_out):
            x_pad_masked = x_pad[:, :, i*stride:i*stride+HH, j*stride: j*stride+WW]
            for k in range(F):
                out[:, k, i, j] = np.sum(x_pad_masked * w[k, :, :, :], axis=(1,2,3))

    # Use None or np.newaxis to expand dimension
    out = out + b[None, :, None, None]
    cache = (x, w, b, conv_param)
    return out, cache

def conv_backward_naive(dout, cache):
    """
    A naive implementation of the backward pass for a convolutional layer.
    Inputs:
        - dout: Upstream derivatives
        - cache: A tuple of (x, w, b, conv_param) as in conv_forward_naive
    
    Returns a tuple of:
        - dx: Gradient with respect to x
        - dy: Gradient with respect to w
        - db: Gradient with respect to b
    """
    x, w, b, conv_param = cache
    N, C, H, W = x.shape
    F, _, HH, WW = w.shape
    stride, pad = conv_param['stride'], conv_param['pad']

    H_out = 1 + (H + 2 * pad - HH) // stride
    W_out = 1 + (W + 2 * pad - WW) // stride

    x_pad = np.pad(x, ((0,), (0,), (pad,), (pad,)), mode='constant', constant_values=0)
    dx = np.zeros_like(x)
    dx_pad = np.zeros_like(x_pad)
    dw = np.zeros_like(w)
    db = np.zeros_like(b)
    
    db = np.sum(dout, axis = (0,2,3))
    for i in range(H_out):
        for j in range(W_out):
            x_pad_masked = x_pad[:, :, i*stride:i*stride+HH, j*stride:j*stride+WW]
            for k in range(F): #compute dw
                dw[k ,: ,: ,:] += np.sum(x_pad_masked * (dout[:, k, i, j])[:, None, None, None], axis=0)
            for n in range(N): #compute dx_pad
                dx_pad[n, :, i*stride:i*stride+HH, j*stride:j*stride+WW] += np.sum((w[:, :, :, :] * 
                                                    (dout[n, :, i, j])[:,None ,None, None]), axis=0)
    dx = dx_pad[:,:,pad:-pad,pad:-pad]

    return dx, dw, db

def max_pool_forward_naive(x, pool_param):
    """
    A naive implementation of the forward pass for a max pooling layer.

    Inputs:
    - x: Input data, of shape (N, C, H, W)
    - pool_param: dictionary with the following keys:
        - 'pool_height': The height of each pooling region
        - 'pool_width': The width of each pooling region
        - 'stride': The distance between adjacent pooling regions

    Returns a tuple of:
    - out: Output data
    - cache: (x, pool_param)
    """
    N, C, H, W = x.shape
    HH, WW, stride = pool_param['pool_height'], pool_param['pool_width'], pool_param['stride']
    H_out = (H-HH)//stride+1
    W_out = (W-WW)//stride+1
    out = np.zeros((N,C,H_out,W_out))
    for i in range(H_out):
        for j in range(W_out):
            x_masked = x[:,:,i*stride : i*stride+HH, j*stride : j*stride+WW]
            out[:,:,i,j] = np.max(x_masked, axis=(2,3)) 
    cache = (x, pool_param)
    return out, cache

def max_pool_backward_naive(dout, cache):
    """
    A naive implementation of the backward pass for a max pooling layer.

    Inputs:
    - dout: Upstream derivatives
    - cache: A tuple of (x, pool_param) as in the forward pass.

    Returns:
    - dx: Gradient with respect to x
    """
    x, pool_param = cache
    N, C, H, W = x.shape
    HH, WW, stride = pool_param['pool_height'], pool_param['pool_width'], pool_param['stride']
    H_out = (H-HH)//stride+1
    W_out = (W-WW)//stride+1
    dx = np.zeros_like(x)
    
    for i in range(H_out):
        for j in range(W_out):
            x_masked = x[:,:,i*stride : i*stride+HH, j*stride : j*stride+WW]
            max_x_masked = np.max(x_masked,axis=(2,3))
            temp_binary_mask = (x_masked == (max_x_masked)[:,:,None,None])
            dx[:,:,i*stride : i*stride+HH, j*stride : j*stride+WW] += temp_binary_mask * (dout[:,:,i,j])[:,:,None,None]
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