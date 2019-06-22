from random import randrange

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
