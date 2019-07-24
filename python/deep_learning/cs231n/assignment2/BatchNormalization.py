import numpy as np
import time

from cs231n.classifiers.fc_net import FullyConnectedNet
from cs231n.classifiers.layers import batchnorm_forward, batchnorm_backward, batchnorm_backward_alt
from cs231n.classifiers.solver import Solver
from cs231n.datasets.cifar10 import get_CIFAR10_data
from cs231n.gradient_check import eval_numerical_gradient, eval_numerical_gradient_array

def rel_error(x, y):
    """ returns relative error """
    return np.max(np.abs(x - y) / (np.maximum(1e-8, np.abs(x) + np.abs(y))))

def batchnorm_forward_test():
    X_train, y_train, X_val, y_val, X_test, y_test = get_CIFAR10_data()

    # Batch normalization: Forward
    N, D1, D2, D3 = 200, 50, 60, 3
    X = np.random.randn(N, D1)
    W1 = np.random.randn(D1, D2)
    W2 = np.random.randn(D2, D3)
    a = np.maximum(0, X.dot(W1)).dot(W2)

    print("Before batch normalization")
    print("means: {}".format(a.mean(axis=0)))
    print("stds: {}".format(a.std(axis=0)))

    # Means should be zero and stds close to one
    print("After batch normalization (gamm=1, beta=0)")
    a_norm, _ = batchnorm_forward(a, np.ones(D3), np.zeros(D3), {'mode': 'train'})
    print("mean: {}".format(a_norm.mean(axis=0)))
    print("std: {}".format(a_norm.std(axis=0)))

    # Now means should be close to beta and stds close to gamma
    gamma = np.array([1.0, 2.0, 3.0])
    beta = np.array([11.0, 12.0, 13.0])
    a_norm, _ = batchnorm_forward(a, gamma, beta, {'mode': 'train'})
    print("After batch normalization (nontrivial gamma, beta)")
    print("means: {}".format(a_norm.mean(axis=0)))
    print("stds: {}".format(a_norm.std(axis=0)))

    # Check the test-time forward pass by running the training-time forward
    # pass many times to warm up the running averages, and then checking the
    # means and variances of activations after a test-time forward pass
    N, D1, D2, D3 = 200, 50, 60, 3
    W1 = np.random.randn(D1, D2)
    W2 = np.random.randn(D2, D3)
    bn_param = {'mode': 'train'}

    gamma = np.ones(D3)
    beta = np.zeros(D3)

    for t in range(50):
        X = np.random.randn(N, D1)
        a = np.maximum(0, X.dot(W1)).dot(W2)
        batchnorm_forward(a, gamma, beta, bn_param)

    bn_param['mode'] = 'test'
    X = np.random.randn(N, D1)
    a = np.maximum(0, X.dot(W1)).dot(W2)
    a_norm, _ = batchnorm_forward(a, gamma, beta, bn_param)

    # Means should be close to zero and stds close to one, but will be noiser than
    # training-time forward passes.
    print("After batch normalization (test-time)")
    print("means: {}".format(a_norm.mean(axis=0)))
    print("stds: {}".format(a_norm.std(axis=0)))

def batchnorm_backward_test():
    N, D = 4, 5
    x = 5 * np.random.randn(N, D) + 12
    gamma = np.random.randn(D)
    beta = np.random.randn(D)
    dout = np.random.randn(N, D)

    bn_param = {'mode': 'train'}
    fx = lambda x: batchnorm_forward(x, gamma, beta, bn_param)[0]
    fg = lambda a: batchnorm_forward(x, gamma, beta, bn_param)[0]
    fb = lambda b: batchnorm_forward(x, gamma, beta, bn_param)[0]

    dx_num = eval_numerical_gradient_array(fx, x, dout)
    da_num = eval_numerical_gradient_array(fg, gamma, dout)
    db_num = eval_numerical_gradient_array(fb, beta, dout)

    _, cache = batchnorm_forward(x, gamma, beta, bn_param)
    dx, dgamma, dbeta = batchnorm_backward(dout, cache)
    print("dx error: {}".format(rel_error(dx_num, dx)))
    print("dgamma error: {}".format(rel_error(da_num, dgamma)))
    print("dbeta error: {}".format(rel_error(db_num, dbeta)))

def batchnorm_backward_alt_test():
    """
    For the sigmoid function, you can derive a very simple formula for the backward pass
    by simplifying gradients on paper.
    """
    N, D = 100, 500
    x = 5 * np.random.randn(N, D) + 12
    gamma = np.random.randn(D)
    beta = np.random.randn(D)
    dout = np.random.randn(N, D)

    bn_param = {'mode': 'train'}
    out, cache = batchnorm_forward(x, gamma, beta, bn_param)

    t1 = time.time()
    dx1, dgamma1, dbeta1 = batchnorm_backward(dout, cache)
    t2 = time.time()
    dx2, dgamma2, dbeta2 = batchnorm_backward_alt(dout, cache)
    t3 = time.time()
    
    print("dx difference: {}".format(rel_error(dx1, dx2)))
    print("dgamma difference: {}".format(rel_error(dgamma1, dgamma2)))
    print("dbeta difference: {}".format(rel_error(dbeta1, dbeta2)))
    print("speedup: {}".format((t2-t1)/(t3-t2)))

def fully_connected_nets_with_batch_normalization():
    N, D, H1, H2, C = 2, 15, 20, 30, 10
    X = np.random.randn(N, D)
    y = np.random.randint(C, size=(N, ))

    for reg in [0, 3.14]:
        print("Running check with reg={}".format(reg))
        model = FullyConnectedNet([H1, H2], input_dim=D, num_classes=C,
                                  reg=reg, weight_scale=5e-2, dtype=np.float64,
                                  use_batchnorm=True)

        loss, grads = model.loss(X, y)
        print("Initial loss: {}".format(loss))

        for name in sorted(grads):
            f = lambda _: model.loss(X, y)[0]
            grad_num = eval_numerical_gradient(f, model.params[name], verbose=False, h=1e-5)
            print("{} relative error: {}".format(name, rel_error(grad_num, grads[name])))

def batchnorm_for_deep_networks():
    X_train, y_train, X_val, y_val, X_test, y_test = get_CIFAR10_data()
    hidden_dims = [100, 100, 100, 100, 100]
    num_train = 1000
    small_data = {
        'X_train': X_train[:num_train],
        'y_train': y_train[:num_train],
        'X_val': X_val,
        'y_val': y_val
    }
    weight_scale = 2e-2
    bn_model = FullyConnectedNet(hidden_dims, weight_scale=weight_scale, use_batchnorm=True)
    model = FullyConnectedNet(hidden_dims, weight_scale=weight_scale, use_batchnorm=False)

    bn_solver = Solver(bn_model, small_data,
                    num_epochs=10, batch_size=50,
                    update_rule='adam',
                    optim_config={
                    'learning_rate': 1e-3,
                    },
                    verbose=True, print_every=200)
    bn_solver.train()

    solver = Solver(model, small_data,
                    num_epochs=10, batch_size=50,
                    update_rule='adam',
                    optim_config={
                    'learning_rate': 1e-3,
                    },
                    verbose=True, print_every=200)
    solver.train()

def main():
    """
    One way to make deep networks easier to train is more sophisticated
    optimization procedures such SGD+momentum, RMSprop, or Adam. Another
    strategy is to change the architecture of the network to make it easier
    to train. One idea along these lines is batch normalization which was
    recently proposed
    """
    # batchnorm_forward_test()

    # batchnorm_backward_test()

    # batchnorm_backward_alt_test()

    # Fully connected Nets with Batch Normalization
    # fully_connected_nets_with_batch_normalization()

    batchnorm_for_deep_networks()

if __name__ == '__main__':
    main()