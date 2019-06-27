import numpy as np

def affine_forward(x, w, b):
    """
    Computes the forward pass for an affline (fully-connected) layer

    The input x has shape (N, d_1,...,d_k) and contains a minibtach of N
    examples, where each example x[i] has shape (d_1,...,d_k). We will
    reshape each input into a vector of dimension D=d1 * ... * dk, and
    then transform it to an output vector of dimension M.

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