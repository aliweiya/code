import os
import pickle

import numpy as np

import tensorflow as tf

class CIFAR10:
    """CIFAR-10 dataset

    The CIFAR-10 dataset consists of 60000 32x32 images in 10 classes,
    with 6000 images per class.

    There are 50000 training images and 10000 test images.

    The dataset is divided into five training batches and one test batch,
    the test batch contains exactly 1000 randomly-selected images from each class.

    The data is a 1000x3072 numpy array of uint8. Each row of the array stores 32x32 image.
    The first 1024 entries contain the red channel values, the next 1024 the green, and the final
    1024 the blue.

    The labels is a list of 10000 numbers in the range 0-9 (label name can be found in batches.meta)

    Links:
        - Download at: https://www.cs.toronto.edu/~kriz/cifar-10-python.tar.gz
        - https://www.cs.toronto.edu/~kriz/cifar.html
    """
    def __init__(self, cifar_root=None, one_hot=False):
        self.cifar_root = cifar_root
        self.one_hot = one_hot
        if not self.cifar_root:
            self.cifar_root = 'D:\\personal\\dataset\\cifar-10-batches-py'

    def load_CIFAR10_batch(self, filename):
        with open(filename, 'rb') as f:
            datadict = pickle.load(f, encoding='bytes')
            X = datadict[b'data']
            Y = datadict[b'labels']
            # 1000个样本，每个是3*32*32的图片，改成32*32*3的
            X = X.reshape(10000, 3, 32, 32).transpose(0,2,3,1).astype("float")
            Y = np.array(Y)
            if self.one_hot:
                temp = np.zeros((Y.shape[0], 10))
                temp[np.arange(Y.shape[0]),Y]=1
                return X, temp
            return X, Y

    def load_CIFAR10(self, cifar_root=None):
        if cifar_root:
            self.cifar_root = cifar_root

        assert self.cifar_root, 'Please supply the root of CIFAR10 dataset.'
        xs = []
        ys = []

        for batch in range(1, 6):
            f = os.path.join(self.cifar_root, 'data_batch_{}'.format(batch))
            X, Y = self.load_CIFAR10_batch(f)
            xs.append(X)
            ys.append(Y)

        # 对数组进行拼接
        # 在拼接方向axis轴上数组间的形状一致
        Xtr = np.concatenate(xs)
        Ytr = np.concatenate(ys)

        # 加载测试集
        Xte, Yte = self.load_CIFAR10_batch(os.path.join(self.cifar_root, 'test_batch'))
        return Xtr, Ytr, Xte, Yte

def get_CIFAR10_data(num_training=49000, num_validation=1000, num_test=1000, one_hot=False):
    cifar10 = CIFAR10(one_hot=one_hot)
    X_train, y_train, X_test, y_test = cifar10.load_CIFAR10()

    X_val = X_train[num_training:]
    y_val = y_train[num_training:]
    X_train = X_train[:num_training]
    y_train = y_train[:num_training]

    return X_train, y_train, X_val, y_val, X_test, y_test

def main():
    X_train, y_train, X_val, y_val, X_test, y_test = get_CIFAR10_data(one_hot=True)
    
    X = tf.placeholder(tf.float32, [None, 3072])
    y = tf.placeholder(tf.float32, [None, 10])
    # Hidden layer 1
    W1 = tf.Variable(tf.random_normal([3072, 100]))
    b1 = tf.Variable(tf.random_normal([100,]))
    Wb1 = tf.matmul(X, W1) + b1

    # Hidden layer 2
    W2 = tf.Variable(tf.random_normal([100, 100]))
    b2 =  tf.Variable(tf.random_normal([100,]))
    Wb2 = tf.matmul(Wb1, W2) + b2

    # Output layer
    W3 = tf.Variable(tf.random_normal([100, 10]))
    b3 =  tf.Variable(tf.random_normal([10,]))
    prediction = tf.matmul(Wb2, W3) + b3

    cross_entropy = tf.reduce_mean(tf.nn.softmax_cross_entropy_with_logits(logits=prediction, labels=y))
    train_step = tf.train.AdamOptimizer(1e-4).minimize(cross_entropy)
    correct_prediction = tf.equal(tf.argmax(prediction,1), tf.argmax(y,1))
    accuracy = tf.reduce_mean(tf.cast(correct_prediction, tf.float32))

    init = tf.global_variables_initializer()

    sess = tf.InteractiveSession()
    sess.run(init)

    batch_size = 50
    for i in range(1000):
        mask = np.random.choice(X_train.shape[0], batch_size)
        X_batch = X_train[mask].reshape(-1,3072)
        y_batch = y_train[mask]
        if i%100 == 0:
            train_accuracy = accuracy.eval(feed_dict={
                X:X_val.reshape(-1,3072), y: y_val})
            print("step %d, training accuracy %g"%(i, train_accuracy))
        train_step.run(feed_dict={X: X_batch, y: y_batch})

    print("test accuracy %g"%accuracy.eval(feed_dict={
        X: X_test.reshape(-1,3072), y: y_test}))

if __name__ == '__main__':
    main()