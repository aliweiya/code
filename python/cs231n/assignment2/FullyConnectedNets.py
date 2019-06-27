import numpy as np

from cs231n.classifiers.layers import affine_forward, affine_backward
from cs231n.datasets.cifar10 import get_CIFAR10_data
from cs231n.gradient_check import eval_numerical_gradient_array

def rel_error(x, y):
    """ returns relative error """
    return np.max(np.abs(x - y) / (np.maximum(1e-8, np.abs(x) + np.abs(y))))

def main():
    data = get_CIFAR10_data()

    # for v in data:
    #     print('{}'.format(v.shape))

    # Affine layer: forward
    # Test the affine_forward function
    num_inputs = 2
    input_shape = (4, 5, 6)
    output_dim = 3

    # Return the product of array elements over a given axis.
    input_size = num_inputs * np.prod(input_shape)
    weight_size = output_dim * np.prod(input_shape)

    x = np.linspace(-0.1, 0.5, num=input_size).reshape(num_inputs, *input_shape)
    w = np.linspace(-0.2, 0.3, num=weight_size).reshape(np.prod(input_shape), output_dim)
    b = np.linspace(-0.3, 0.1, num=output_dim)

    out, _ = affine_forward(x, w, b)
    correct_out = np.array([[1.49834967, 1.70660132,  1.91485297],
                            [3.25553199,  3.5141327,   3.77273342]])

    print("Testing affine_forward function:")
    print("difference: {}".format(rel_error(out, correct_out)))

    # Affine layer: backward
    x = np.random.randn(10, 2, 3)
    w = np.random.randn(6, 5)
    b = np.random.randn(5)
    dout = np.random.randn(10, 5)

    dx_num = eval_numerical_gradient_array(lambda x: affine_forward(x, w, b)[0], x, dout)
    dw_num = eval_numerical_gradient_array(lambda w: affine_forward(x, w, b)[0], w, dout)
    db_num = eval_numerical_gradient_array(lambda b: affine_forward(x, w, b)[0], b, dout)

    _, cache = affine_forward(x, w, b)
    dx, dw, db = affine_backward(dout, cache)
    print("Testing affine_backward functions.")
    print("dx error: {}".format(rel_error(dx_num, dx)))
    print("dw error: {}".format(rel_error(dw_num, dw)))
    print("db error: {}".format(rel_error(db_num, db)))

if __name__ == '__main__':
    main()