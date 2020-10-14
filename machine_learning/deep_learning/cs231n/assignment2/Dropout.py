import time
import numpy as np
import matplotlib.pyplot as plt

from cs231n.classifiers.fc_net import FullyConnectedNet
from cs231n.classifiers.layers import dropout_forward, dropout_backward
from cs231n.classifiers.solver import Solver
from cs231n.datasets.cifar10 import get_CIFAR10_data
from cs231n.gradient_check import eval_numerical_gradient, eval_numerical_gradient_array

def rel_error(x, y):
  """ returns relative error """
  return np.max(np.abs(x - y) / (np.maximum(1e-8, np.abs(x) + np.abs(y))))

def dropout_forward_pass():
    x = np.random.randn(500, 500) + 10
    for p in [0.3, 0.6, 0.75]:
        out, _ = dropout_forward(x, {'mode': 'train', 'p': p})
        out_test, _ = dropout_forward(x, {'mode': 'test', 'p': p})

        print("Running test with p={}".format(p))
        print("Mean of input: {}".format(x.mean()))
        print("Mean of test-time output: {}".format(out_test.mean()))
        print("Fraction of train-time output set to zero: {}".format((out==0).mean()))
        print("Fraction of test-time output set to zero: {}".format((out_test==0).mean()))

def dropout_backward_pass():
    x = np.random.randn(10, 10) + 10
    dout = np.random.randn(*x.shape)

    dropout_param = {'mode': 'train', 'p': 0.8, 'seed': 123}
    out, cache = dropout_forward(x, dropout_param)
    dx = dropout_backward(dout, cache)
    dx_num = eval_numerical_gradient_array(lambda xx: dropout_forward(xx, dropout_param)[0], x, dout)

    print('dx relative error: ', rel_error(dx, dx_num))

def fully_connected_nets_with_dropout():
    N, D, H1, H2, C = 2, 15, 20, 30, 10
    X = np.random.randn(N, D)
    y = np.random.randint(C, size=(N,))

    for dropout in [0, 0.25, 0.5]:
        print("Running check with dropout={}".format(dropout))
        model = FullyConnectedNet([H1, H2], input_dim=D, num_classes=C,
                                  weight_scale=5e-2, dtype=np.float64,
                                  dropout=dropout, seed=123)
        loss, grads = model.loss(X, y)
        print("Initial loss: {}".format(loss))

        for name in sorted(grads):
            f = lambda _: model.loss(X, y)[0]
            grad_num = eval_numerical_gradient(f, model.params[name], verbose=False, h=1e-5)
            print("{} relative error: {}".format(name, rel_error(grad_num, grads[name])))

def regularization_expriment():
    """
    We will train a pair of two-layer networks on 500 training examples: one will use no dropout,
    and one will use a dropout probability of 0.75.
    """
    num_train = 500
    X_train, y_train, X_val, y_val, X_test, y_test = get_CIFAR10_data()
    small_data = {
        'X_train': X_train[:num_train],
        'y_train': y_train[:num_train],
        'X_val': X_val,
        'y_val': y_val,
        'X_test': y_test,
        'y_test': y_test
    }

    solvers = {}
    dropout_choices = [0, 0.25, 0.5, 0.75, 0.8, 0.9, 0.99]
    for dropout in dropout_choices:
        model = FullyConnectedNet([500], 
                        weight_scale=5e-2,
                        dropout=dropout)

        solver = Solver(model, small_data, num_epochs=25,
                        batch_size=100, update_rule="adam",
                        optim_config={'learning_rate': 5e-4,},
                        verbose=True, print_every=100)
        solver.train()
        solvers[dropout] = solver

    # Plot train and validation accuracies of the two models

    train_accs = []
    val_accs = []
    for dropout in dropout_choices:
        solver = solvers[dropout]
        train_accs.append(solver.train_acc_history[-1])
        val_accs.append(solver.val_acc_history[-1])

    plt.subplot(3, 1, 1)
    for dropout in dropout_choices:
        plt.plot(solvers[dropout].train_acc_history, 'o', label='%.2f dropout' % dropout)
    plt.title('Train accuracy')
    plt.xlabel('Epoch')
    plt.ylabel('Accuracy')
    plt.legend(ncol=2, loc='lower right')
    
    plt.subplot(3, 1, 2)
    for dropout in dropout_choices:
        plt.plot(solvers[dropout].val_acc_history, 'o', label='%.2f dropout' % dropout)
    plt.title('Val accuracy')
    plt.xlabel('Epoch')
    plt.ylabel('Accuracy')
    plt.legend(ncol=2, loc='lower right')

    plt.gcf().set_size_inches(15, 15)
    plt.show()

def main():
    """
    Dropout is a technique for regularizing neural networks by randomly setting
    some features to zero during the forward pass.
    """
    
    # Dropout forward pass
    # dropout_forward_pass()

    # Dropout backward pass
    # dropout_backward_pass()

    # Fully-connected nets with Dropout
    # fully_connected_nets_with_dropout()

    # Regularization experiment
    regularization_expriment()

if __name__ == '__main__':
    main()