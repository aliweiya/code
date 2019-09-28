# -*- coding: utf-8 -*-
import tensorflow as tf
from tensorflow.examples.tutorials.mnist import input_data

mnist = input_data.read_data_sets("MNIST_data/", 
    one_hot=True, source_url='http://yann.lecun.com/exdb/mnist')

# To create this model, we're going to need to create a lot of weights and biases. 
# One should generally initialize weights with a small amount of noise 
# for symmetry breaking, and to prevent 0 gradients. 
def weight_variable(shape):
    # tf.truncated_normal(shape, mean, stddev) :shape表示生成张量的维度，mean是均值，stddev是标准差。
    # 这个函数产生正态分布，均值和标准差自己设定。
    # 这是一个截断的产生正态分布的函数，就是说产生正太分布的值如果与均值的差值大于两倍的标准差，那就重新生成。
    initial = tf.truncated_normal(shape, stddev=0.1)
    return tf.Variable(initial)

# Since we're using ReLU neurons, it is also good practice to initialize them with a 
# slightly positive initial bias to avoid "dead neurons".
def bias_variable(shape):
    initial = tf.constant(0.1, shape=shape)
    return tf.Variable(initial)

# Our convolutions uses a stride of one and are zero padded so that the output is the same size as the input. 
def conv2d(x, W):
    # tf.nn.conv2d(input, filter, strides, padding, use_cudnn_on_gpu=None, name=None)

    # 第一个参数input：指需要做卷积的输入图像，
    # 它要求是一个Tensor，具有[batch, in_height, in_width, in_channels]这样的shape，
    # 具体含义是[训练时一个batch的图片数量, 图片高度, 图片宽度, 图像通道数]，注意这是一个4维的Tensor，要求类型为float32和float64其中之一

    # 第二个参数filter：相当于CNN中的卷积核，它要求是一个Tensor，
    # 具有[filter_height, filter_width, in_channels, out_channels]这样的shape，
    # 具体含义是[卷积核的高度，卷积核的宽度，图像通道数，卷积核个数]，要求类型与参数input相同，有一个地方需要注意，第三维in_channels，就是参数input的第四维

    # 第三个参数strides：卷积时在图像每一维的步长，这是一个一维的向量，长度4

    # 第四个参数padding：string类型的量，只能是"SAME","VALID"其中之一，这个值决定了不同的卷积方式（后面会介绍）

    # 第五个参数：use_cudnn_on_gpu:bool类型，是否使用cudnn加速，默认为true

    # 结果返回一个Tensor，这个输出，就是我们常说的feature map，shape仍然是[batch, height, width, channels]这种形式。
    return tf.nn.conv2d(x, W, strides=[1, 1, 1, 1], padding='SAME')

# Our pooling is plain old max pooling over 2x2 blocks.
def max_pool_2x2(x):
    # tf.nn.max_pool(value, ksize, strides, padding, name=None)

    # 第一个参数value：需要池化的输入，一般池化层接在卷积层后面，所以输入通常是feature map，依然是[batch, height, width, channels]这样的shape

    # 第二个参数ksize：池化窗口的大小，取一个四维向量，一般是[1, height, width, 1]，因为我们不想在batch和channels上做池化，所以这两个维度设为了1

    # 第三个参数strides：和卷积类似，窗口在每一个维度上滑动的步长，一般也是[1, stride,stride, 1]

    # 第四个参数padding：和卷积类似，可以取'VALID' 或者'SAME'

    # 返回一个Tensor，类型不变，shape仍然是[batch, height, width, channels]这种形式
    return tf.nn.max_pool(x, ksize=[1, 2, 2, 1],
                          strides=[1, 2, 2, 1], padding='SAME')

# input images
x = tf.placeholder(tf.float32, [None, 784])

# target output classes.
y_ = tf.placeholder(tf.float32, [None, 10])

# ----------------------------------------------------------------------------
# First Convolutional Layer
# It consists of convolution, followed by max pooling.

# The convolution will compute 32 features for each 5x5 patch. 
# Its weight tensor will have a shape of [5, 5, 1, 32]. 
# The first two dimensions are the patch size, 
# the next is the number of input channels, and the last is the number of output channels. 
W_conv1 = weight_variable([5, 5, 1, 32])

# We will also have a bias vector with a component for each output channel.
b_conv1 = bias_variable([32])

# To apply the layer, we first reshape x to a 4d tensor,
# with the second and third dimensions corresponding to image width and height, 
# and the final dimension corresponding to the number of color channels.
x_image = tf.reshape(x, [-1,28,28,1])

# We then convolve x_image with the weight tensor, add the bias, apply the ReLU function, and finally max pool.
h_conv1 = tf.nn.relu(conv2d(x_image, W_conv1) + b_conv1)

# The max_pool_2x2 method will reduce the image size to 14x14.
h_pool1 = max_pool_2x2(h_conv1)

# ----------------------------------------------------------------------------
# Second Convolutional Layer
# In order to build a deep network, we stack several layers of this type.
# The second layer will have 64 features for each 5x5 patch.

W_conv2 = weight_variable([5, 5, 32, 64])
b_conv2 = bias_variable([64])

h_conv2 = tf.nn.relu(conv2d(h_pool1, W_conv2) + b_conv2)
h_pool2 = max_pool_2x2(h_conv2)
# ----------------------------------------------------------------------------

# Densely Connected Layer
# Now that the image size has been reduced to 7x7, 
# we add a fully-connected layer with 1024 neurons to allow processing on the entire image. 
# We reshape the tensor from the pooling layer into a batch of vectors,
# multiply by a weight matrix, add a bias, and apply a ReLU.
W_fc1 = weight_variable([7 * 7 * 64, 1024])
b_fc1 = bias_variable([1024])

h_pool2_flat = tf.reshape(h_pool2, [-1, 7*7*64])

# 计算修正线性单元(非常常用)：max(features, 0).并且返回和feature一样的形状的tensor。
# 参数： 
#   features: tensor类型，必须是这些类型：A Tensor. float32, float64, int32, int64, uint8, int16, int8, uint16, half. 
#   name: ：操作名称（可选）
h_fc1 = tf.nn.relu(tf.matmul(h_pool2_flat, W_fc1) + b_fc1)

# Dropout
# To reduce overfitting, we will apply dropout before the readout layer. 
# We create a placeholder for the probability that a neuron's output is kept during dropout. 
# This allows us to turn dropout on during training, and turn it off during testing. 
# TensorFlow's tf.nn.dropout op automatically handles scaling neuron outputs in addition to masking them, 
# so dropout just works without any additional scaling.1
keep_prob = tf.placeholder(tf.float32)

# tf.nn.dropout(x, keep_prob, noise_shape=None, seed=None, name=None)
# 根据给出的keep_prob参数，将输入tensor x按比例输出。
#   x           :  输入tensor
#   keep_prob   :  float类型，每个元素被保留下来的概率
#   noise_shape :  一个1维的int32张量，代表了随机产生“保留/丢弃”标志的shape。
#   seed        :  整形变量，随机数种子。
#   name        :  名字，没啥用。 
h_fc1_drop = tf.nn.dropout(h_fc1, keep_prob)

# Readout Layer
# Finally, we add a layer, just like for the one layer softmax regression above.
W_fc2 = weight_variable([1024, 10])
b_fc2 = bias_variable([10])

y_conv = tf.matmul(h_fc1_drop, W_fc2) + b_fc2

# Train and Evaluate the Model
cross_entropy = tf.reduce_mean(tf.nn.softmax_cross_entropy_with_logits(logits=y_conv, labels=y_))
train_step = tf.train.AdamOptimizer(1e-4).minimize(cross_entropy)
correct_prediction = tf.equal(tf.argmax(y_conv,1), tf.argmax(y_,1))
accuracy = tf.reduce_mean(tf.cast(correct_prediction, tf.float32))

init = tf.global_variables_initializer()

sess = tf.InteractiveSession()
sess.run(init)

for i in range(20000):
    batch = mnist.train.next_batch(50)
    if i%100 == 0:
        train_accuracy = accuracy.eval(feed_dict={
            x:batch[0], y_: batch[1], keep_prob: 1.0})
        print("step %d, training accuracy %g"%(i, train_accuracy))
    train_step.run(feed_dict={x: batch[0], y_: batch[1], keep_prob: 0.5})

print("test accuracy %g"%accuracy.eval(feed_dict={
    x: mnist.test.images, y_: mnist.test.labels, keep_prob: 1.0}))