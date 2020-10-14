import glob
from io import BytesIO
import os
import time

import numpy as np
from PIL import Image

import skimage
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import OneHotEncoder  
from sklearn.utils import shuffle

from tensorflow.contrib.layers import xavier_initializer

import tensorflow as tf

VGG_MEAN = [104, 117, 123]

class AlexNet:

    def __init__(self, height, width, channel, num_classes, dataset_path):
        self.keep_prob = 0.5
        self.filewriter_path = 'tensorboard'
        self.ckpt_path = 'ckpt/alexnet.ckpt'
        self.learning_rate = 3e-5
        self.epochs = 100
        self.dataset_path = dataset_path

        self.height = height
        self.width = width
        self.channel = channel
        self.num_classes = num_classes

        # L2 正则化
        # lambda * W^2
        # 可以使得W的每个元素都很小，都接近于0，但与L1范数不同，它不会让它等于0，而是接近于0
        # 而越小的参数说明模型越简单，越简单的模型则越不容易产生过拟合现象。
        self.l2_regularizer=tf.contrib.layers.l2_regularizer(0.1) 

        self.x = tf.placeholder(tf.float32, [None, height, width, channel], name='x')
        self.y_ = tf.placeholder(tf.int32, [None, num_classes], name='y')
        self.keep_prob_placeholder = tf.placeholder(tf.float32, name='keep_prob')

        graph = tf.get_default_graph()
        self.sess = tf.Session(graph=graph)

        self.build()

        self.saver = tf.train.Saver()

    def build(self):
        with tf.name_scope("conv1") as scope:
            """
            if (input_height % strides[1] == 0):
                pad_along_height = max(filter_height - strides[1], 0)
            else:
                pad_along_height = max(filter_height - (input_height % strides[1]), 0)

            if input_height = 227, pad_along_height = 8

            after convolution, the size is [?, (227 + 8 - 11) / 4 + 1, (227 + 8 - 11) / 4 + 1, 96],
            = [?, 57, 57, 96]
            """
            # [kernel_height, kernel_width, channel_in, channel_out]
            # kernel = tf.Variable(tf.truncated_normal([11, 11, 3, 96],
            #                                           mean=0,
            #                                           stddev=0.1,
            #                                           dtype=tf.float32), name="weights")
            kernel = tf.get_variable(name='weights1', shape=[11, 11, 3, 96], dtype=tf.float32,
                                     initializer=xavier_initializer(), regularizer=self.l2_regularizer)
            # SAME: padding with inf, VALID: no padding
            # batch, height, width, channel
            conv = tf.nn.conv2d(self.x, kernel, [1, 4, 4, 1], padding="VALID")
            biases = tf.Variable(tf.constant(0.0, shape=[96], dtype=tf.float32),
                                 trainable=True, name='biases')
            bias = tf.nn.bias_add(conv, biases)
            conv1 = tf.nn.relu(bias, name=scope)

            print(conv1.shape)

        with tf.name_scope('lrn1') as scope:
            """
            Hinton在2012年的Alexnet网络中提出

            在2015年 Very Deep Convolutional Networks for Large-Scale Image Recognition.提到LRN基本没什么用。
            """
            lrn1 = tf.nn.lrn(conv1, alpha=2e-5, beta=0.75,
                             depth_radius=2, bias=1.0)

        with tf.name_scope("pool1") as scope:
            """
            Input size: [?, 57, 57, 96]
            Output Size: [?, (57 - 3) / 2 + 1, (57 - 3) / 2 + 1, 96] = [?, 28, 28, 96]
            """
            pool1 = tf.nn.max_pool(lrn1,
                                   ksize=[1, 3, 3, 1],
                                   strides=[1, 2, 2, 1],
                                   padding='VALID')

            print(pool1.shape)

        with tf.name_scope('conv2') as scope:
            """
            Input size: [?, 28, 28, 96]
            Output size: [?, (28 + 4 - 5) / 1 + 1, (28 + 4 - 5) / 1 + 1, 256] = [?, 28, 28, 256]
            """
            # kernel = tf.Variable(tf.truncated_normal([5, 5, 96, 256],
            #                                          dtype=tf.float32,
            #                                          mean=0,
            #                                          stddev=1e-1), name='weights')
            kernel = tf.get_variable(name='weights2', shape=[5, 5, 96, 256], dtype=tf.float32,
                                     initializer=xavier_initializer(), regularizer=self.l2_regularizer)
            conv = tf.nn.conv2d(pool1, kernel, [1, 1, 1, 1], padding="SAME")
            biases = tf.Variable(tf.constant(0.0, shape=[256], dtype=tf.float32),
                                 trainable=True, name='biases')

            bias = tf.nn.bias_add(conv, biases)
            conv2 = tf.nn.relu(bias, name=scope)

            print(conv2.shape)

        with tf.name_scope('lrn2') as scope:
            lrn2 = tf.nn.lrn(conv2,
                             alpha=2e-5,
                             beta=0.75,
                             depth_radius=2,
                             bias=1.0)

        with tf.name_scope('pool2') as scope:
            """
            Input size: [?, 28, 28, 256]
            Output size: [?, (28 - 3) / 2 + 1, (28 - 3) / 2 + 1, 256] = [?, 13, 13, 256]
            """
            pool2 = tf.nn.max_pool(lrn2, ksize=[1, 3, 3, 1],
                                   strides=[1, 2, 2, 1],
                                   padding="VALID")

            print(pool2.shape)

        with tf.name_scope('conv3') as scope:
            """
            Input size: [?, 13, 13, 256]
            Outpuy size: [?, 13, 13, 384]
            """
            # kernel = tf.Variable(tf.truncated_normal([3, 3, 256, 384],
            #                                          dtype=tf.float32,
            #                                          mean=0,
            #                                          stddev=1e-1), name='weights')
            kernel = tf.get_variable(name='weights3', shape=[3, 3, 256, 384], dtype=tf.float32,
                                     initializer=xavier_initializer(), regularizer=self.l2_regularizer)
            conv = tf.nn.conv2d(pool2, kernel, [1, 1, 1, 1], padding="SAME")
            biases = tf.Variable(tf.constant(0.0, shape=[384], dtype=tf.float32),
                                 trainable=True, name='biases')

            bias = tf.nn.bias_add(conv, biases)
            conv3 = tf.nn.relu(bias, name=scope)

            print(conv3.shape)

        with tf.name_scope('conv4') as scope:
            """
            Input size: [?, 13, 13, 384]
            Output size: [?, 13, 13, 384]
            """
            # kernel = tf.Variable(tf.truncated_normal([3, 3, 384, 384],
            #                                          dtype=tf.float32,
            #                                          mean=0,
            #                                          stddev=1e-1), name='weights')
            kernel = tf.get_variable(name='weights4', shape=[3, 3, 384, 384], dtype=tf.float32,
                                     initializer=xavier_initializer(), regularizer=self.l2_regularizer)
            conv = tf.nn.conv2d(conv3, kernel, [1, 1, 1, 1], padding="SAME")
            biases = tf.Variable(tf.constant(0.0, shape=[384], dtype=tf.float32),
                                 trainable=True, name='biases')

            bias = tf.nn.bias_add(conv, biases)
            conv4 = tf.nn.relu(bias, name=scope)

            print(conv4.shape)

        with tf.name_scope('conv5') as scope:
            """
            Input size: [?, 13, 13, 384]
            Output size: [?, 13, 13, 256]
            """
            # kernel = tf.Variable(tf.truncated_normal([3, 3, 384, 256],
            #                                          dtype=tf.float32,
            #                                          mean=0,
            #                                          stddev=1e-1), name='weights')
            kernel = tf.get_variable(name='weights5', shape=[3, 3, 384, 256], dtype=tf.float32,
                                     initializer=xavier_initializer(), regularizer=self.l2_regularizer)
            conv = tf.nn.conv2d(conv4, kernel, [1, 1, 1, 1], padding="SAME")
            biases = tf.Variable(tf.constant(0.0, shape=[256], dtype=tf.float32),
                                 trainable=True, name='biases')

            bias = tf.nn.bias_add(conv, biases)
            conv5 = tf.nn.relu(bias, name=scope)

            print(conv5.shape)

        with tf.name_scope('pool5') as scope:
            """
            Input size: [?, 13, 13, 256]
            Output size: [?, 6, 6, 256]
            """
            pool5 = tf.nn.max_pool(conv5, ksize=[1, 3, 3, 1],
                                   strides=[1, 2, 2, 1],
                                   padding="VALID")

            print(pool5.shape)

        with tf.name_scope('flattened') as scope:
            flattened = tf.reshape(pool5, shape=[-1, 6 * 6 * 256])
            print(flattened.shape)

        with tf.name_scope("fc6") as scope:
            # weights = tf.Variable(tf.truncated_normal([6 * 6 * 256, 4096],
            #                                           dtype=tf.float32,
            #                                           mean=0,
            #                                           stddev=1e-1), name='weights')
            kernel = tf.get_variable(name='weights6', shape=[6 * 6 * 256, 4096], dtype=tf.float32,
                                     initializer=xavier_initializer(), regularizer=self.l2_regularizer)
            biases = tf.Variable(tf.constant(0.0, shape=[4096], dtype=tf.float32),
                                 trainable=True, name='biases')
            bias = tf.nn.xw_plus_b(flattened, kernel, biases)
            fc6 = tf.nn.relu(bias)
            print(fc6.shape)

        with tf.name_scope('dropout6') as scope:
            dropout6 = tf.nn.dropout(fc6, self.keep_prob_placeholder)

        with tf.name_scope('fc7') as scope:
            # weights = tf.Variable(tf.truncated_normal([4096, 4096],
            #                                           dtype=tf.float32,
            #                                           mean=0,
            #                                           stddev=1e-1), name='weights')

            kernel = tf.get_variable(name='weights7', shape=[4096, 4096], dtype=tf.float32,
                                     initializer=xavier_initializer(), regularizer=self.l2_regularizer)
            biases = tf.Variable(tf.constant(0.0, shape=[4096], dtype=tf.float32),
                                 trainable=True, name='biases')
            bias = tf.nn.xw_plus_b(dropout6, kernel, biases)
            fc7 = tf.nn.relu(bias)
            print(fc7.shape)

        with tf.name_scope('dropout7') as scope:
            dropout7 = tf.nn.dropout(fc7, self.keep_prob_placeholder)

        with tf.name_scope('fc8') as scope:
            # weights = tf.Variable(tf.truncated_normal([4096, self.num_classes],
            #                                           dtype=tf.float32,
            #                                           mean=0,
            #                                           stddev=1e-1), name='weights')
            kernel = tf.get_variable(name='weights8', shape=[4096, self.num_classes], dtype=tf.float32,
                                     initializer=xavier_initializer(), regularizer=self.l2_regularizer)
            biases = tf.Variable(tf.constant(0.0, shape=[self.num_classes], dtype=tf.float32),
                                 trainable=True, name='biases')
            self.fc8 = tf.nn.xw_plus_b(dropout7, kernel, biases)
            print(self.fc8.name)

    def load_image(self, filename):
        im = Image.open(filename, 'r')

        if im.mode != "RGB":
            im = im.convert('RGB')

        imr = im.resize((256, 256), resample=Image.BILINEAR)

        fh_im = BytesIO()
        imr.save(fh_im, format='JPEG')
        fh_im.seek(0)

        image = (skimage.img_as_float(skimage.io.imread(fh_im, as_grey=False))
                        .astype(np.float32))

        H, W, _ = image.shape
        h, w = (self.height, self.width)

        h_off = max((H - h) // 2, 0)
        w_off = max((W - w) // 2, 0)
        image = image[h_off:h_off + h, w_off:w_off + w, :]

        # RGB to BGR
        image = image[:, :, :: -1]

        image = image.astype(np.float32, copy=False)
        image = image * 255.0
        image -= np.array(VGG_MEAN, dtype=np.float32)

        return image.astype(np.int8)

    def get_batch(self, batch_size=32, train=True):
        if train:
            x, y = self.x_train, self.y_train
        else:
            x, y = self.x_test, self.y_test

        offset = 0
        while True:
            data_batch = x[offset:offset + batch_size]
            label_batch = y[offset:offset + batch_size]
            offset += batch_size

            image_batch = []
            for image in data_batch:
                image_batch.append(self.load_image(image))

            if image_batch:
                yield np.array(image_batch), label_batch
            else:
                raise StopIteration

    def load_dataset(self):
        datasets = glob.glob(os.path.join(self.dataset_path, '*.jpg'))
        # tf.train.shuffle_batch
        datasets = shuffle(datasets)

        labels = [1 if sample.split(os.path.sep)[-1].split('.')[0] == 'dog' else 0 for sample in datasets]
        labels = np.array(labels).reshape(-1, 1)

        onehotEncoder = OneHotEncoder()
        onehotEncoder.fit([[0], [1]])
        labels = onehotEncoder.transform(labels).toarray()
        self.x_train, self.x_test, self.y_train, self.y_test = train_test_split(datasets, labels, test_size=0.3, random_state=0)

    def load(self):
        saver = tf.train.Saver()
        saver.restore(self.sess, self.ckpt_path)

    def train(self):
        if not hasattr(self, 'x_train'):
            self.load_dataset()

        with tf.name_scope('loss'):
            loss = tf.reduce_mean(tf.nn.softmax_cross_entropy_with_logits_v2(logits=self.fc8, labels=self.y_))

        with tf.name_scope('optimizer'):
            optimizer = tf.train.AdamOptimizer(learning_rate=self.learning_rate)
            train_op = optimizer.minimize(loss)

        with tf.name_scope('accuracy'):
            correct_pred = tf.equal(tf.argmax(self.fc8, 1), tf.argmax(self.y_, 1))
            accuracy = tf.reduce_mean(tf.cast(correct_pred, tf.float32))

        tf.summary.scalar('loss', loss)
        tf.summary.scalar('accuracy', accuracy)
        merged_summary = tf.summary.merge_all()
        writer = tf.summary.FileWriter(self.filewriter_path, self.sess.graph)

        self.sess.run(tf.global_variables_initializer())

        total_batch = 0
        for epoch in range(self.epochs):
            for batch, (train_data_batch, train_label_batch) in enumerate(self.get_batch()):
                time_start = time.time()
                _, _loss, _acc, _summary = self.sess.run([train_op, loss, accuracy, merged_summary], feed_dict={self.x: train_data_batch, self.y_: train_label_batch, self.keep_prob_placeholder: self.keep_prob})
                time_end = time.time()
                print('Epoch: {}, train batch: {}, loss: {}, acc: {}, time: {}'.format(epoch, batch, _loss, _acc, time_end-time_start))
                writer.add_summary(_summary, total_batch)
                total_batch += 1

            total_loss, total_acc = 0, 0
            for batch, (test_data_batch, test_label_batch) in enumerate(self.get_batch(train=False)):
                time_start = time.time()
                _loss, _acc = self.sess.run([loss, accuracy], feed_dict={self.x:test_data_batch, self.y_: test_label_batch, self.keep_prob_placeholder: 1})
                time_end = time.time()
                print('Epoch: {}, test batch: {}, loss: {}, acc: {}, time: {}'.format(epoch, batch, _loss, _acc, time_end - time_start))
                total_loss += _loss
                total_acc += _acc

            print('Test loss: {}, acc: {}'.format(total_loss / (batch + 1), total_acc / (batch + 1)))
            self.saver.save(self.sess, self.ckpt_path, global_step=epoch)

    def predict(self, data):
        y = self.sess.run(self.outputs, feed_dict={self.x: data})
        return y
