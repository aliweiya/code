import tensorflow as tf
# Pre-trained models and datasets built by Google and the community
import tensorflow.contrib.slim as slim
import config as cfg

class Lenet:
    def __init__(self):
        self.raw_input_image = tf.placeholder(tf.float32, [None, 784])
        self.input_images = tf.reshape(self.raw_input_image, [-1, 28, 28, 1])
        self.raw_input_label = tf.placeholder("float", [None, 10])
        # tf.cast 类型转换
        self.input_labels = tf.cast(self.raw_input_label,tf.int32)
        self.dropout = cfg.KEEP_PROB

        with tf.variable_scope("Lenet") as scope:
            self.train_digits = self.construct_net(True)
            scope.reuse_variables()
            self.pred_digits = self.construct_net(False)

        self.prediction = tf.argmax(self.pred_digits, 1)
        self.correct_prediction = tf.equal(tf.argmax(self.pred_digits, 1), tf.argmax(self.input_labels, 1))
        self.train_accuracy = tf.reduce_mean(tf.cast(self.correct_prediction, "float"))


        self.loss = slim.losses.softmax_cross_entropy(self.train_digits, self.input_labels)
        self.lr = cfg.LEARNING_RATE
        self.train_op = tf.train.AdamOptimizer(self.lr).minimize(self.loss)



    def construct_net(self,is_trained = True):
        # 常用于为tensorflow里的layer函数提供默认值以使构建模型的代码更加紧凑苗条
        # padding为VALID表示 without padding
        # 后面多的会被丢弃
        with slim.arg_scope([slim.conv2d], padding='VALID',
                            weights_initializer=tf.truncated_normal_initializer(stddev=0.01),
                            weights_regularizer=slim.l2_regularizer(0.0005)):
            net = slim.conv2d(self.input_images,6,[5,5],1,padding='SAME',scope='conv1')
            net = slim.max_pool2d(net, [2, 2], scope='pool2')
            net = slim.conv2d(net,16,[5,5],1,scope='conv3')
            net = slim.max_pool2d(net, [2, 2], scope='pool4')
            net = slim.conv2d(net,120,[5,5],1,scope='conv5')
            # 给定一个输入A， 此函数将其每个样本转化为一维的向量，然后返回一个tensor，其维度为（batchsize,k）,
            # 一般应用在卷积神经网络全连接层前，因为全连接层需要将输入数据变为一个向量。
            net = slim.flatten(net, scope='flat6')
            net = slim.fully_connected(net, 84, scope='fc7')
            net = slim.dropout(net, self.dropout,is_training=is_trained, scope='dropout8')
            digits = slim.fully_connected(net, 10, scope='fc9')
        return digits