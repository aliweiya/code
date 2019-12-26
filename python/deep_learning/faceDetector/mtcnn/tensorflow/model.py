import cv2
import numpy as np
from PIL import Image

import tensorflow as tf
from tensorflow.contrib import slim

import utils

"""定义MTCNN的模型

References:
    1. https://www.cnblogs.com/zyly/p/9703614.html
"""

def resize_image(img, scale):
    """
    # References
        1. http://www.sfinst.com/?p=1683
    """
    height, width, channel = img.shape
    new_height = int(height * scale)
    new_width = int(width * scale)
    # 注意！！！！这里是 (new_width, new_height)
    img_resized = cv2.resize(img, (new_width, new_height), interpolation=cv2.INTER_LINEAR)
    # 归一化操作，加快收敛速度。见引用1
    # 实践中发现，有正有负的输入，收敛速度更快。
    # 训练时候输入的图片需要先做这样的预处理，推断的时候也需要做这样的预处理才行。
    img_resized = (img_resized - 127.5) / 128
    return img_resized

def convert_to_square(bbox):
    """
    将框改为正方形
    """
    square_bbox = bbox.copy()

    h = bbox[:, 3] - bbox[:, 1] + 1
    w = bbox[:, 2] - bbox[:, 0] + 1
    max_side = np.maximum(h, w)
    square_bbox[:, 0] = bbox[:, 0] + w * 0.5 - max_side * 0.5
    square_bbox[:, 1] = bbox[:, 1] + h * 0.5 - max_side * 0.5
    square_bbox[:, 2] = square_bbox[:, 0] + max_side - 1
    square_bbox[:, 3] = square_bbox[:, 1] + max_side - 1
    return square_bbox

def pad(image, boxes):
    """限制框的大小
    """
    height, width, channel = image.shape
    boxes[:, 0][boxes[:, 0] < 0] = 1
    boxes[:, 1][boxes[:, 1] < 0] = 1
    boxes[:, 2][boxes[:, 2] > height] = height - 1
    boxes[:, 3][boxes[:, 3] > width] = width - 1
    return boxes

def nms(dets, thresh=0.7, mode="Union"):
    x1 = dets[:, 0]
    y1 = dets[:, 1]
    x2 = dets[:, 2]
    y2 = dets[:, 3]
    scores = dets[:, 4]

    areas = (x2 - x1 + 1) * (y2 - y1 + 1)
    order = scores.argsort()[::-1]

    keep = []
    while order.size > 0:
        i = order[0]
        keep.append(i)
        xx1 = np.maximum(x1[i], x1[order[1:]])
        yy1 = np.maximum(y1[i], y1[order[1:]])
        xx2 = np.minimum(x2[i], x2[order[1:]])
        yy2 = np.minimum(y2[i], y2[order[1:]])

        w = np.maximum(0.0, xx2 - xx1 + 1)
        h = np.maximum(0.0, yy2 - yy1 + 1)
        inter = w * h
        if mode == "Union":
            overlap = inter / (areas[i] + areas[order[1:]] - inter)
        elif mode == "Minimum":
            overlap = inter / np.minimum(areas[i], areas[order[1:]])

        inds = np.where(overlap <= thresh)[0]
        order = order[inds + 1]

    return keep

def prelu(inputs):
    """
           ┌─── alpha * x, x <= 0
    f(x) = │
           └─── x, x > 0

    alpha对应每个通道，原文初始化为0.25

    # References
        1. https://arxiv.org/abs/1502.01852
        2. https://stackoverflow.com/questions/39975676/how-to-implement-prelu-activation-in-tensorflow
    """
    alphas = tf.get_variable("alphas", shape=inputs.get_shape()[-1],
                             dtype=tf.float32, initializer=tf.constant_initializer(0.25))
    pos = tf.nn.relu(inputs)
    neg = alphas * (inputs-abs(inputs))*0.5
    return pos + neg

def calibrate(bbox, reg):
    """ 利用框回归结果对边框进行修正 """
    # TODO: 可能训练时有问题，这里宽和高需要调换一下
    reg = reg[:, [1, 0, 3, 2]]
    h = bbox[:, 2] - bbox[:, 0] + 1
    h = np.expand_dims(h, 1)
    w = bbox[:, 3] - bbox[:, 1] + 1
    w = np.expand_dims(w, 1)
    reg_m = np.hstack([h, w, h, w])
    aug = reg_m * reg
    bbox[:, 0:4] = bbox[:, 0:4] + aug
    return bbox

def draw(frame, boxes, landmarks):
    for box, landmark in zip(boxes, landmarks):
        cv2.rectangle(frame, (int(box[1]), int(box[0])), (int(box[3]), int(box[2])), (0,255,0), 2)
        for j in range(5):
            cv2.circle(frame, (int(landmark[2*j]),int(int(landmark[2*j+1]))), 2, (0,255, 0))

def landmark_to_location(boxes, landmarks):
    widths = boxes[:, 2] - boxes[:, 0]
    heights = boxes[:, 3] - boxes[:, 1]

    landmarks[:, 0::2] = np.tile(boxes[:, 1], (5, 1)).T + landmarks[:, 0::2] * np.tile(heights, (5,1)).T
    landmarks[:, 1::2] = np.tile(boxes[:, 0], (5, 1)).T + landmarks[:, 1::2] * np.tile(widths, (5,1)).T

    return landmarks

class PNet:
    """
    主要目的是为了生成一些候选框，通过使用P-Net网络，对图像金字塔图像上不同尺度下的图像的每一个12×12区域
    都做一个人脸检测(实际上在使用卷积网络实现时，一般会把一张h×w的图像送入P-Net中，
    最终得到的特征图每一点都对应着一个大小为12×12的感受野，但是并没有遍历全一张图像每一个12×12的图像

    输入是任意形状的图像，高和宽定义为placeholder，在预测时根据图片获取大小。

    因为输入的图片尺寸大小不定，而且slim的输入形状为 [batch_size, height, width, channel]

    有两种处理方式
    1. 将所有图片设置为同一大小
    2. batch_size设置为1

    还可以将宽高的placeholder设置为 [batch_size, None], 但是处理有点麻烦
    """
    def __init__(self, batch_size=1, restore=True):
        self.threshold = 0.9
        self.net_size = 12

        with tf.Graph().as_default():
            self.sess = tf.Session()
            self.image_placeholder = tf.placeholder(tf.float32, name='input_image')
            self.width_placeholder = tf.placeholder(tf.int32, name='image_width')
            self.height_placeholder = tf.placeholder(tf.int32, name='image_height')
            inputs = tf.reshape(self.image_placeholder, [batch_size, self.height_placeholder,
                                                         self.width_placeholder, 3])
            
            self.build(inputs)

            if restore:
                saver = tf.train.Saver()
                saver.restore(self.sess, 'checkpoints\\PNet_landmark\\PNet-18')

    def generate_bbox(self, image, cls_prob, bbox, scale, threshold):
        """根据网络输出结果，返回人脸框在原图的位置

        Args
            - image: [batch_size, height, width, channel] 输入图像
            - cls_prob: [batch_size, height, width, channel] 每个输入框中可能有人脸的概率
            - bbox:  表示框左上角的横坐标的相对偏移，框左上角的纵坐标的相对偏移、框的宽度的误差、框的高度的误差。
            - scale: 金字塔缩放比例
            - threshold: 保留大于该值的概率对应的框
        Returns
            - 根据阈值，选出可能的框，返回
        References:
            1. 如何根据结果还原到原图：http://www.sfinst.com/?p=1683
        """
        # 根据卷积过程推断出来的
        stride = 2
        # 得分矩阵大于threshold的下标
        cls_index = np.where(cls_prob[0, :, :, 1] > threshold)
        # 还原原位置
        boundingbox = np.vstack([(stride * cls_index[0]) / scale,
                                (stride * cls_index[1]) / scale,
                                (stride * cls_index[0] + self.net_size) / scale,
                                (stride * cls_index[1] + self.net_size) / scale,
                                cls_prob[0, cls_index[0], cls_index[1], 1]])

        # calibration（修正），见引用1
        boundingbox = calibrate(boundingbox.T, bbox[0, cls_index[0], cls_index[1]])

        return boundingbox

    def build(self, inputs):
        """
        input size is [batch_size, height, width, channel]
        """
        with slim.arg_scope([slim.conv2d],
                            activation_fn=prelu,
                            weights_initializer=slim.xavier_initializer(),
                            biases_initializer=tf.zeros_initializer(),
                            weights_regularizer=slim.l2_regularizer(0.0005), 
                            padding='valid'):
            
            # input, out_channel, stride
            # tf.nn.conv2d(input, filter, strides, padding, use_cudnn_on_gpu=None, data_format=None, name=None)
            # ( x - 3 ) / 1 + 1, (y - 3) / 1 + 1
            net = slim.conv2d(inputs, 10, 3, stride=1, scope='conv1')

            # tf.nn.max_pool(value, ksize, strides, padding, name=None)
            # x / 2, y / 2
            net = slim.max_pool2d(net, kernel_size=[2, 2], stride=2, scope='pool1', padding='SAME')
            # (x - 3) / 1 + 1, (y - 3) / 1 + 1
            net = slim.conv2d(net, num_outputs=16, kernel_size=[3, 3], stride=1, scope='conv2')
            # （x - 3) / 1 + 1, (y - 3) / 1 + 1
            net = slim.conv2d(net,num_outputs=32,kernel_size=[3,3],stride=1,scope='conv3')
            # face classification
            # total_input: x / 2 - 5, y / 2 - 5
            # total_output: x / 2 -5, y / 2 - 5
            self.cls_prob = slim.conv2d(net, num_outputs=2, kernel_size=[1, 1],
                                        stride=1,scope='conv4_1',activation_fn=tf.nn.softmax)

            # bounding box regression
            self.bbox_pred = slim.conv2d(net, num_outputs=4, kernel_size=[1, 1],
                                         stride=1,scope='conv4_2',activation_fn=None)
            # facial landmark localization
            self.landmark_pred = slim.conv2d(net, num_outputs=10, kernel_size=[1, 1],
                                             stride=1,scope='conv4_3',activation_fn=None)

    def detect(self, image):
        """
        进行金字塔变换，然后识别出人脸位置

        先把原图等比缩放`12/minsize`，再按缩放因子`factor`用上一次的缩放结果不断缩放，直至最短边小于或等于12。

        # Args:
            - image: [batch_size, height, width, channel], batch_size应该是1

        # Returns:
            经金字塔变化后所有可能的位置
        # References
            1. http://www.sfinst.com/?p=1683
        """
        # 识别的脸的最小尺寸
        minsize = 24
        # 让面积缩小一倍，所以宽和高各乘以 sqrt{2} / 2，见引用1
        factor = 0.79
        # 先把原图等比缩放，然后再按factor缩放
        scale = self.net_size / minsize
        current_height, current_width, _ = image.shape
        # 检测出的人脸框
        boxes = []
        image_resized = resize_image(image, scale)
        
        current_height, current_width, _ = image_resized.shape
        while min(current_height, current_width) > self.net_size:

            cls_prob, bbox_pred, landmark_pred = self.predict(image_resized)
            bbox = self.generate_bbox(image, cls_prob, bbox_pred, scale, self.threshold)
            boxes.append(bbox)

            scale *= factor
            image_resized = resize_image(image, scale)
            current_height, current_width, _ = image_resized.shape

        boxes = np.vstack(boxes)
        # 利用NMS去除冗余框
        boxes = boxes[nms(boxes)]
        boxes = convert_to_square(boxes)
        boxes = pad(image, boxes)
        return boxes

    def predict(self, image):
        """ image should be of shpae [batch_size, height, width, channel] """
        height, width, channel = image.shape
        # 输出的是每个框中有人脸的概率
        cls_prob, bbox_pred, landmark_pred = self.sess.run([self.cls_prob, self.bbox_pred, self.landmark_pred],
                                                feed_dict={self.image_placeholder: image, self.width_placeholder: width,
                                                        self.height_placeholder: height})
        return cls_prob, bbox_pred, landmark_pred

    def export_to_pb(self):
        tf.train.write_graph(self.sess.graph_def, 'protobuf/', 'pnet.pb', as_text=False)

class RNet:
    """
    R-Net和P-Net类似，不过这一步的输入是前面P-Net生成的边界框，不管实际边界框的大小，在输入R-Net之前，
    都需要缩放到24×24×3。网络的输出和P-Net是一样的。这一步的目的主要是为了去除大量的非人脸框。
    """
    def __init__(self, restore=True):
        self.threshold = 0.6
        with tf.Graph().as_default():
            self.sess = tf.Session()
            self.image_placeholder = tf.placeholder(tf.float32, shape=[None, 24, 24, 3], name='input_image')
            self.build(self.image_placeholder)

            if restore:
                saver = tf.train.Saver()
                saver.restore(self.sess, 'checkpoints\\RNet_landmark\\RNet-14')

    def build(self, inputs):
        with slim.arg_scope([slim.conv2d],
                            activation_fn = prelu,
                            weights_initializer=slim.xavier_initializer(),
                            biases_initializer=tf.zeros_initializer(),
                            weights_regularizer=slim.l2_regularizer(0.0005),                        
                            padding='valid'):

            net = slim.conv2d(inputs, num_outputs=28, kernel_size=[3,3], stride=1, scope="conv1")
            net = slim.max_pool2d(net, kernel_size=[3, 3], stride=2, scope="pool1", padding='SAME')
            net = slim.conv2d(net,num_outputs=48,kernel_size=[3,3],stride=1,scope="conv2")
            net = slim.max_pool2d(net,kernel_size=[3,3],stride=2,scope="pool2")
            net = slim.conv2d(net,num_outputs=64,kernel_size=[2,2],stride=1,scope="conv3")
            fc_flatten = slim.flatten(net)
            fc1 = slim.fully_connected(fc_flatten, num_outputs=128,scope="fc1")
            # face classification
            self.cls_prob = slim.fully_connected(fc1,num_outputs=2,scope="cls_fc",activation_fn=tf.nn.softmax)
            # bounding box regression
            self.bbox_pred = slim.fully_connected(fc1,num_outputs=4,scope="bbox_fc",activation_fn=None)
            # face landmark localization
            self.landmark_pred = slim.fully_connected(fc1,num_outputs=10,scope="landmark_fc",activation_fn=None)

    def detect(self, image, boxes):
        """输入是PNet的结果，需要缩放到24x24x3
        """
        cropped_images = []
        for box in boxes:
            cropped = image[int(box[0]):int(box[2]), int(box[1]):int(box[3]), :]

            cropped = (cv2.resize(cropped, (24, 24)) - 127.5) / 128
            cropped_images.append(cropped)

        cropped_images = np.array(cropped_images)
        cls_prob, bbox_pred, landmark_pred = self.predict(cropped_images)
        cls_index = np.where(cls_prob[:, 1] > self.threshold)[0]
        # TODO: 判断是否为空
        boxes = boxes[cls_index]
        # 修正
        boxes = calibrate(boxes, bbox_pred[cls_index])
        boxes = convert_to_square(boxes)
        boxes = pad(image, boxes)
        boxes = boxes[nms(boxes, 0.6)]
        return boxes

    def predict(self, image):
        cls_prob, bbox_pred, landmark_pred = self.sess.run([self.cls_prob, self.bbox_pred, self.landmark_pred],
                                                feed_dict={self.image_placeholder: image})
        return cls_prob, bbox_pred, landmark_pred

    def export_to_pb(self):
        tf.train.write_graph(self.sess.graph_def, 'protobuf/', 'rnet.pb', as_text=False)

class ONet:
    """
    进一步将R-Net的所得到的区域缩放到48×48×3，输入到最后的O-Net，O-Net的结构与P-Net类似，
    只不过在测试输出的时候多了关键点位置的输出
    """
    def __init__(self, restore=True):
        self.threshold = 0.7
        with tf.Graph().as_default():
            self.sess = tf.Session()
            self.image_placeholder = tf.placeholder(tf.float32, shape=[None, 48, 48, 3], name='input_image')
            self.build(self.image_placeholder)

            if restore:
                saver = tf.train.Saver()
                saver.restore(self.sess, 'checkpoints\\ONet_landmark\\ONet-16')

    def build(self, inputs):
        with slim.arg_scope([slim.conv2d],
                            activation_fn = prelu,
                            weights_initializer=slim.xavier_initializer(),
                            biases_initializer=tf.zeros_initializer(),
                            weights_regularizer=slim.l2_regularizer(0.0005),                        
                            padding='valid'):
            net = slim.conv2d(inputs, num_outputs=32, kernel_size=[3,3], stride=1, scope="conv1")
            net = slim.max_pool2d(net, kernel_size=[3, 3], stride=2, scope="pool1", padding='SAME')
            net = slim.conv2d(net,num_outputs=64,kernel_size=[3,3],stride=1,scope="conv2")
            net = slim.max_pool2d(net, kernel_size=[3, 3], stride=2, scope="pool2")
            net = slim.conv2d(net,num_outputs=64,kernel_size=[3,3],stride=1,scope="conv3")
            net = slim.max_pool2d(net, kernel_size=[2, 2], stride=2, scope="pool3", padding='SAME')
            net = slim.conv2d(net,num_outputs=128,kernel_size=[2,2],stride=1,scope="conv4")
            fc_flatten = slim.flatten(net)
            fc1 = slim.fully_connected(fc_flatten, num_outputs=256,scope="fc1")
            # face classification
            self.cls_prob = slim.fully_connected(fc1,num_outputs=2,scope="cls_fc",activation_fn=tf.nn.softmax)
            # bounding box regression
            self.bbox_pred = slim.fully_connected(fc1,num_outputs=4,scope="bbox_fc",activation_fn=None)
            # face landmark localization
            self.landmark_pred = slim.fully_connected(fc1,num_outputs=10,scope="landmark_fc",activation_fn=None)

    def detect(self, image, boxes):
        """输入是ONet的结果，需要缩放到48x48x3
        """
        cropped_images = []
        for box in boxes:
            cropped = image[int(box[0]):int(box[2]), int(box[1]):int(box[3]), :]
            cropped = (cv2.resize(cropped, (48, 48)) - 127.5) / 128
            cropped_images.append(cropped)

        cropped_images = np.array(cropped_images)
        cls_prob, bbox_pred, landmark_pred = self.predict(cropped_images)
        cls_index = np.where(cls_prob[:, 1] > self.threshold)[0]
        # TODO: 判断是否为空
        boxes = boxes[cls_index]
        # 修正
        boxes = calibrate(boxes, bbox_pred[cls_index])
        keep = nms(boxes, 0.6, 'Minimum')
        boxes = boxes[keep]
        boxes = pad(image, boxes)
        landmarks = landmark_pred[cls_index][keep]

        landmarks = landmark_to_location(boxes, landmarks)

        # for box in boxes:
        #     image = cv2.rectangle(image, (int(box[1]), int(box[0])), (int(box[3]), int(box[2])), (0,255,0), 2)

        # cv2.imshow('image', image)
        # cv2.waitKey()
        return boxes, landmarks

    def predict(self, image):
        cls_prob, bbox_pred, landmark_pred = self.sess.run([self.cls_prob, self.bbox_pred, self.landmark_pred],
                                                feed_dict={self.image_placeholder: image})
        return cls_prob, bbox_pred, landmark_pred

    def export_to_pb(self):
        tf.train.write_graph(self.sess.graph_def, 'protobuf/', 'onet.pb', as_text=False)