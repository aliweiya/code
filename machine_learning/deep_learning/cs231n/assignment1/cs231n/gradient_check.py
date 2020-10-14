from random import randrange

import numpy as np

def grad_check_sparse(f, x, analytic_grad, num_checks=10, h=1e-5):
    """
    sample a few random elements on only return numerical in this dimensions.
    """
    for i in range(num_checks):
        # The method randrange() returns a randomly selected element from range(start, stop, step).
        # = random.choice(range(m))
        ix = tuple([randrange(m) for m in x.shape])
        oldval = x[ix]

        x[ix] = oldval + h
        fxph = f(x)         # evaluate f(x+h)
        x[ix] = oldval - h
        fxmh = f(x)         # evaluate f(x-h)
        x[ix] = oldval      # reset

        grad_numerical = (fxph - fxmh) / (2 * h)
        grad_analytic = analytic_grad[ix]
        rel_error = abs(grad_numerical - grad_analytic) / (abs(grad_numerical) + abs(grad_analytic))
        print('numerical: {} analytic: {}, relative error: {}'.format(grad_numerical, grad_analytic, rel_error))

def eval_numerical_gradient(f, x, verbose=True, h=0.00001):
    """
    a naive implementation of numerical gradient of f at x

    Args:
        - f should be a function that takes a single argument
        - x is the point (numpy array) to evaluate the gradient at
    """
    fx = f(x)
    grad = np.zeros_like(x)
    # iterate over all indexes in x
    it = np.nditer(x, flags=['multi_index'], op_flags=['readwrite'])
    while not it.finished:
        # evaluate function at x+h
        ix = it.multi_index
        oldval = x[ix]
        x[ix] = oldval + h
        fxph = f(x) # evaluate f(x+h)
        x[ix] = oldval - h
        fxmh = f(x) # evaluate f(x-h)
        x[ix] = oldval

        # compute the partial derivative with centered formula
        grad[ix] = (fxph-fxmh) / (2*h)
        if verbose:
            print(ix, grad[ix])
        it.iternext()

    return grad