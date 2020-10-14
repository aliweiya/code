from time import time

import numpy as np
import matplotlib.pyplot as plt
from scipy.misc import imread, imresize

from cs231n.classifiers.fast_layers import conv_forward_fast, conv_backward_fast,\
    max_pool_forward_fast, max_pool_backward_fast
from cs231n.classifiers.layers import conv_forward_naive, conv_backward_naive,\
    max_pool_forward_naive, max_pool_backward_naive
from cs231n.classifiers.layer_utils import conv_relu_pool_forward, conv_relu_pool_backward,\
    conv_relu_forward, conv_relu_backward
from cs231n.gradient_check import eval_numerical_gradient, eval_numerical_gradient_array
from cs231n.classifiers.cnn import ThreeLayerConvNet
from cs231n.datasets.cifar10 import get_CIFAR10_data
from cs231n.classifiers.solver import Solver

def rel_error(x, y):
    """ returns relative error """
    return np.max(np.abs(x - y) / (np.maximum(1e-8, np.abs(x) + np.abs(y))))

def naive_forward_pass():
    # N, C, H, W
    x_shape = (2, 3, 4, 4)
    # F, C, HH, WW
    w_shape = (3, 3, 4, 4)
    x = np.linspace(-0.1, 0.5, num=np.prod(x_shape)).reshape(x_shape)
    w = np.linspace(-0.2, 0.3, num=np.prod(w_shape)).reshape(w_shape)
    # F
    b = np.linspace(-0.1, 0.2, num=3)

    conv_param = {'stride': 2, 'pad': 1}
    out, _ = conv_forward_naive(x, w, b, conv_param)
    correct_out = np.array([[[[[-0.08759809, -0.10987781],
                            [-0.18387192, -0.2109216 ]],
                            [[ 0.21027089,  0.21661097],
                            [ 0.22847626,  0.23004637]],
                            [[ 0.50813986,  0.54309974],
                            [ 0.64082444,  0.67101435]]],
                            [[[-0.98053589, -1.03143541],
                            [-1.19128892, -1.24695841]],
                            [[ 0.69108355,  0.66880383],
                            [ 0.59480972,  0.56776003]],
                            [[ 2.36270298,  2.36904306],
                            [ 2.38090835,  2.38247847]]]]])

    # Compare your output to ours; difference should be around 1e-8
    print('Testing conv_forward_naive')
    print('difference: ', rel_error(out, correct_out))

def image_processing_via_convolutions():
    """
    As fun way to both check the implementation and gain a better understanding of the
    type of operation that convolutional layers can perform, we will set up an input
    containing two images and manually set up filters that perform common image processing
    operations(grayscale conversion and edge detection). The convolution forwward pass will
    apply these operations to each of the input images. We can then visualize the rsults as
    a sanity check.
    """
    kitten, puppy = imread('kitten.jpg'), imread('puppy.jpg')

    # kitten is wide, and puppy is already square
    print(kitten.shape, puppy.shape)
    d = kitten.shape[1] - kitten.shape[0]
    kitten_cropped = kitten[:, d//2:-d//2, :]
    print(kitten_cropped.shape, puppy.shape)
    # Make this smaller if it runs too slow
    img_size = 200
    x = np.zeros((2, 3, img_size, img_size))
    # Equals to x[0]
    x[0, :, :, :] = imresize(puppy, (img_size, img_size)).transpose((2, 0, 1))
    x[1, :, :, :] = imresize(kitten_cropped, (img_size, img_size)).transpose((2, 0, 1))
    
    # Set up a convolutional weights holding 2 filters, each 3x3
    w = np.zeros((2, 3, 3, 3))

    # The first filter converts the image to grayscale
    # Set up the red, green, and blue channels of the filter
    w[0, 0, :, :] = [[0, 0, 0], [0, 0.3, 0], [0, 0, 0]]
    w[0, 1, :, :] = [[0, 0, 0], [0, 0.6, 0], [0, 0, 0]]
    w[0, 2, :, :] = [[0, 0, 0], [0, 0.1, 0], [0, 0, 0]]

    # Second filter detects horizontal edges in the blue channel.
    w[1, 2, :, :] = [[1, 2, 1], [0, 0, 0], [-1, -2, -1]]

    # Vectort of biases. We don't need any bias for the grayscale
    # filter, but for the edge detection filter we want to add 128
    # to each output so that nothing is negative
    b = np.array([0, 128])

    # Compute the result of convolving each input in x with each filter in w,
    # offsetting by b, and storing the results in out.
    out, _ = conv_forward_naive(x, w, b, {'stride': 1, 'pad': 1})

    def imshow_noax(img, normalize=True):
        """ Tiny helper to show images as uint8 and remove axis labels """
        if normalize:
            img_max, img_min = np.max(img), np.min(img)
            img = 255.0 * (img - img_min) / (img_max - img_min)
        plt.imshow(img.astype('uint8'))
        plt.gca().axis('off')

    # Show the original images and the results of the conv operation
    plt.subplot(2, 3, 1)
    imshow_noax(puppy, normalize=False)
    plt.title('Original image')
    plt.subplot(2, 3, 2)
    imshow_noax(out[0, 0])
    plt.title('Grayscale')
    plt.subplot(2, 3, 3)
    imshow_noax(out[0, 1])
    plt.title('Edges')
    plt.subplot(2, 3, 4)
    imshow_noax(kitten_cropped, normalize=False)
    plt.subplot(2, 3, 5)
    imshow_noax(out[1, 0])
    plt.subplot(2, 3, 6)
    imshow_noax(out[1, 1])
    plt.show()

def naive_backward_pass():
    x = np.random.randn(4, 3, 5, 5)
    w = np.random.randn(2, 3, 3, 3)
    b = np.random.randn(2,)
    dout = np.random.randn(4, 2, 5, 5)
    conv_param = {'stride': 1, 'pad': 1}

    dx_num = eval_numerical_gradient_array(lambda x: conv_forward_naive(x, w, b, conv_param)[0], x, dout)
    dw_num = eval_numerical_gradient_array(lambda w: conv_forward_naive(x, w, b, conv_param)[0], w, dout)
    db_num = eval_numerical_gradient_array(lambda b: conv_forward_naive(x, w, b, conv_param)[0], b, dout)

    out, cache = conv_forward_naive(x, w, b, conv_param)
    dx, dw, db = conv_backward_naive(dout, cache)

    # Your errors should be around 1e-9'
    print('Testing conv_backward_naive function')
    print('dx error: ', rel_error(dx, dx_num))
    print('dw error: ', rel_error(dw, dw_num))
    print('db error: ', rel_error(db, db_num))

def max_pooling_naive_forward_test():
    x_shape = (2, 3, 4, 4)
    x = np.linspace(-0.3, 0.4, num=np.prod(x_shape)).reshape(x_shape)
    pool_param = {'pool_width': 2, 'pool_height': 2, 'stride': 2}

    out, _ = max_pool_forward_naive(x, pool_param)

    correct_out = np.array([[[[-0.26315789, -0.24842105],
                            [-0.20421053, -0.18947368]],
                            [[-0.14526316, -0.13052632],
                            [-0.08631579, -0.07157895]],
                            [[-0.02736842, -0.01263158],
                            [ 0.03157895,  0.04631579]]],
                            [[[ 0.09052632,  0.10526316],
                            [ 0.14947368,  0.16421053]],
                            [[ 0.20842105,  0.22315789],
                            [ 0.26736842,  0.28210526]],
                            [[ 0.32631579,  0.34105263],
                            [ 0.38526316,  0.4       ]]]])

    # Compare your output with ours. Difference should be around 1e-8.
    print('Testing max_pool_forward_naive function:')
    print('difference: ', rel_error(out, correct_out))

def max_pooling_naive_backward_test():
    x = np.random.randn(3, 2, 8, 8)
    dout = np.random.randn(3, 2, 4, 4)
    pool_param = {'pool_height': 2, 'pool_width': 2, 'stride': 2}

    dx_num = eval_numerical_gradient_array(lambda x: max_pool_forward_naive(x, pool_param)[0], x, dout)

    out, cache = max_pool_forward_naive(x, pool_param)
    dx = max_pool_backward_naive(dout, cache)

    # Your error should be around 1e-12
    print('Testing max_pool_backward_naive function:')
    print('dx error: ', rel_error(dx, dx_num))

def fast_layers_test():
    x = np.random.randn(100, 3, 31, 31)
    w = np.random.randn(25, 3, 3, 3)
    b = np.random.randn(25,)
    dout = np.random.randn(100, 25, 16, 16)
    conv_param = {'stride': 2, 'pad': 1}

    t0 = time()
    out_naive, cache_naive = conv_forward_naive(x, w, b, conv_param)
    t1 = time()
    out_fast, cache_fast = conv_forward_fast(x, w, b, conv_param)
    t2 = time()

    print('Testing conv_forward_fast:')
    print('Naive: %fs' % (t1 - t0))
    print('Fast: %fs' % (t2 - t1))
    print('Speedup: %fx' % ((t1 - t0) / (t2 - t1)))
    print('Difference: ', rel_error(out_naive, out_fast))

    t0 = time()
    dx_naive, dw_naive, db_naive = conv_backward_naive(dout, cache_naive)
    t1 = time()
    dx_fast, dw_fast, db_fast = conv_backward_fast(dout, cache_fast)
    t2 = time()

    print('\nTesting conv_backward_fast:')
    print('Naive: %fs' % (t1 - t0))
    print('Fast: %fs' % (t2 - t1))
    print('Speedup: %fx' % ((t1 - t0) / (t2 - t1)))
    print('dx difference: ', rel_error(dx_naive, dx_fast))
    print('dw difference: ', rel_error(dw_naive, dw_fast))
    print('db difference: ', rel_error(db_naive, db_fast))

    x = np.random.randn(100, 3, 32, 32)
    dout = np.random.randn(100, 3, 16, 16)
    pool_param = {'pool_height': 2, 'pool_width': 2, 'stride': 2}

    t0 = time()
    out_naive, cache_naive = max_pool_forward_naive(x, pool_param)
    t1 = time()
    out_fast, cache_fast = max_pool_forward_fast(x, pool_param)
    t2 = time()

    print('Testing pool_forward_fast:')
    print('Naive: %fs' % (t1 - t0))
    print('fast: %fs' % (t2 - t1))
    print('speedup: %fx' % ((t1 - t0) / (t2 - t1)))
    print('difference: ', rel_error(out_naive, out_fast))

    t0 = time()
    dx_naive = max_pool_backward_naive(dout, cache_naive)
    t1 = time()
    dx_fast = max_pool_backward_fast(dout, cache_fast)
    t2 = time()

    print('\nTesting pool_backward_fast:')
    print('Naive: %fs' % (t1 - t0))
    print("fast: %fs" % (t2 - t1))
    print('speedup: %fx' % ((t1 - t0) / (t2 - t1)))
    print('dx difference: ', rel_error(dx_naive, dx_fast))

def convolutional_sandwich_layers_test():
    x = np.random.randn(2, 3, 16, 16)
    w = np.random.randn(3, 3, 3, 3)
    b = np.random.randn(3,)
    dout = np.random.randn(2, 3, 8, 8)
    conv_param = {'stride': 1, 'pad': 1}
    pool_param = {'pool_height': 2, 'pool_width': 2, 'stride': 2}

    out, cache = conv_relu_pool_forward(x, w, b, conv_param, pool_param)
    dx, dw, db = conv_relu_pool_backward(dout, cache)

    dx_num = eval_numerical_gradient_array(lambda x: conv_relu_pool_forward(x, w, b, conv_param, pool_param)[0], x, dout)
    dw_num = eval_numerical_gradient_array(lambda w: conv_relu_pool_forward(x, w, b, conv_param, pool_param)[0], w, dout)
    db_num = eval_numerical_gradient_array(lambda b: conv_relu_pool_forward(x, w, b, conv_param, pool_param)[0], b, dout)

    print('Testing conv_relu_pool')
    print('dx error: ', rel_error(dx_num, dx))
    print('dw error: ', rel_error(dw_num, dw))
    print('db error: ', rel_error(db_num, db))

    x = np.random.randn(2, 3, 8, 8)
    w = np.random.randn(3, 3, 3, 3)
    b = np.random.randn(3,)
    dout = np.random.randn(2, 3, 8, 8)
    conv_param = {'stride': 1, 'pad': 1}

    out, cache = conv_relu_forward(x, w, b, conv_param)
    dx, dw, db = conv_relu_backward(dout, cache)

    dx_num = eval_numerical_gradient_array(lambda x: conv_relu_forward(x, w, b, conv_param)[0], x, dout)
    dw_num = eval_numerical_gradient_array(lambda w: conv_relu_forward(x, w, b, conv_param)[0], w, dout)
    db_num = eval_numerical_gradient_array(lambda b: conv_relu_forward(x, w, b, conv_param)[0], b, dout)

    print('Testing conv_relu:')
    print('dx error: ', rel_error(dx_num, dx))
    print('dw error: ', rel_error(dw_num, dw))
    print('db error: ', rel_error(db_num, db))

def three_layer_convnet_test():
    # model = ThreeLayerConvNet()

    # N = 50
    # X = np.random.randn(N, 3, 32, 32)
    # y = np.random.randint(10, size=N)

    # loss, grads = model.loss(X, y)
    # print('Initial loss (no regularization): {}'.format(loss))

    # model.reg = 0.5
    # loss, grads = model.loss(X, y)
    # print("Initial loss(with regularization: {}".format(loss))

    # # Gradient check
    # num_inputs = 2
    # input_dim = (3, 16, 16)
    # reg = 0.0
    # num_classes = 10
    # X = np.random.randn(num_inputs, *input_dim)
    # y = np.random.randint(num_classes, size=num_inputs)

    # model = ThreeLayerConvNet(num_filters=3, filter_size=3,
    #                         input_dim=input_dim, hidden_dim=7,
    #                         dtype=np.float64)
    # loss, grads = model.loss(X, y)
    # for param_name in sorted(grads):
    #     f = lambda _: model.loss(X, y)[0]
    #     param_grad_num = eval_numerical_gradient(f, model.params[param_name], verbose=False, h=1e-6)
    #     e = rel_error(param_grad_num, grads[param_name])
    #     print('%s max relative error: %e' % (param_name, rel_error(param_grad_num, grads[param_name])))

    # Overfit small data
    X_train, y_train, X_val, y_val, X_test, y_test = get_CIFAR10_data()
    num_train = 100
    small_data = {
        'X_train': X_train[:num_train].transpose(0, 3, 1, 2),
        'y_train': y_train[:num_train],
        'X_val': X_val.transpose(0, 3, 1, 2),
        'y_val': y_val
    }
    model = ThreeLayerConvNet(weight_scale=1e-2)

    solver = Solver(model, small_data,
                    num_epochs=20, batch_size=50,
                    update_rule='adam',
                    optim_config={
                    'learning_rate': 4e-4,
                    },
                    verbose=True, print_every=1)
    solver.train()

    plt.subplot(2, 1, 1)
    plt.plot(solver.loss_history, 'o')
    plt.xlabel('iteration')
    plt.ylabel('loss')

    plt.subplot(2, 1, 2)
    plt.plot(solver.train_acc_history, '-o')
    plt.plot(solver.val_acc_history, '-o')
    plt.legend(['train', 'val'], loc='upper left')
    plt.xlabel('epoch')
    plt.ylabel('accuracy')
    plt.show()

def main():
    # Naive forward pass
    # naive_forward_pass()

    # Image processing via convolutions
    # image_processing_via_convolutions()

    # naive_backward_pass()

    # max_pooling_naive_forward_test()

    # max_pooling_naive_backward_test()

    """
    Fast Layers

    The fast convolution implementation depends on a Cython extention; To compile it you
    need to run the following code:

        python setup.py build_ext --inplace
    """
    # fast_layers_test()

    # convolutional_sandwich_layers_test()

    three_layer_convnet_test()

if __name__ == '__main__':
    main()