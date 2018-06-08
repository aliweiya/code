from __future__ import division, absolute_import
import re
import numpy as np
from dataset_loader import DatasetLoader
import tflearn
from tflearn.layers.core import input_data, dropout, fully_connected, flatten
from tflearn.layers.conv import conv_2d, max_pool_2d, avg_pool_2d, global_avg_pool
from tflearn.data_augmentation import ImageAugmentation
from tflearn.layers.merge_ops import merge
from tflearn.layers.estimator import regression
from constants import *
from os.path import isfile, join
import os
import random
import sys

class EmotionRecognition:

    def __init__(self):
        """
            初始化：读取数据
        """
        self.dataset = DatasetLoader()

    def build_network(self, loadModel=False):
        """
            构建模型
        """
        # Smaller 'AlexNet'
        # https://github.com/tflearn/tflearn/blob/master/examples/images/alexnet.py
        print('[+] Building CNN')
        img_aug = ImageAugmentation()
        img_aug.add_random_flip_leftright()
        # img_aug.add_random_rotation(max_angle=25.)
        img_aug.add_random_blur(sigma_max=0.3)
        # 输入数据 http://tflearn.org/layers/core/#input-data
        self.network = input_data(shape=[None, SIZE_FACE, SIZE_FACE, 1], data_augmentation=img_aug)
        # self.network = input_data(shape=[None, SIZE_FACE, SIZE_FACE, 1])
        # 卷积层 http://tflearn.org/layers/conv/#convolution-2d
        # 激活函数 http://tflearn.org/activations/
        self.network = conv_2d(self.network, 64, 3, activation='relu')
        # self.gap1 = global_avg_pool(self.network)
        # 池化层 http://tflearn.org/layers/conv/#max-pooling-2d
        self.network = max_pool_2d(self.network, 2, strides=2)
        # 卷积层
        self.network = conv_2d(self.network, 96, 3, activation='relu')
        # self.gap2 = global_avg_pool(self.network)
        # 池化层
        self.network = max_pool_2d(self.network, 2, strides=2)
        # 卷积层
        self.network = conv_2d(self.network, 128, 3, activation='relu')
        self.network = global_avg_pool(self.network)
        # 全连接层 http://tflearn.org/layers/core/#fully-connected
        self.network = fully_connected(self.network, 2048, activation='relu',
            weight_decay=0.001)

        # dropout随机将部分输出改为0，避免过拟合 http://tflearn.org/layers/core/#dropout
        self.network = dropout(self.network, 0.8)
        # 全连接层：softmax分类
        # self.network = merge([self.gap1, self.gap2, self.gap3], mode="concat", name="concat")
        self.network = fully_connected(self.network, len(EMOTIONS), activation='softmax')

        # 定义损失函数和优化器 http://tflearn.org/layers/estimator/#regression
        self.network = regression(self.network,
            # http://tflearn.org/optimizers/
            optimizer='Adam',
            # optimizer='SGD',
            # http://tflearn.org/objectives/
            loss='categorical_crossentropy',
            learning_rate=0.001)
        # 定义模型 http://tflearn.org/models/dnn/#deep-neural-network-model
        self.model = tflearn.DNN(
            self.network,
            checkpoint_path=SAVE_DIRECTORY + '/emotion_recognition',
            tensorboard_dir='c:\\tmp\\tflearn_logs',
            max_checkpoints=1,
            tensorboard_verbose=2
        )
        if loadModel:
            self.load_model()

    def load_saved_dataset(self):
        self.dataset.load_from_save(data_source='fer2013')
        print('[+] Dataset found and loaded')

    def start_training(self):
        """
            训练模型
        """
        self.load_saved_dataset()
        self.build_network(loadModel=True)
        if self.dataset is None:
            self.load_saved_dataset()
        # Training
        print('[+] Training network')
        # 训练模型 http://tflearn.org/models/dnn/#deep-neural-network-model
        self.model.fit(
            self.dataset.images, self.dataset.labels,
            validation_set = (self.dataset.images_test, self.dataset.labels_test),
            n_epoch=100,
            batch_size=256,
            shuffle=True,
            show_metric=True,
            snapshot_step=200,
            snapshot_epoch=True,
            run_id='emotion_recognition'
        )

    def predict(self, image):
        """
            预测
        """
        if image is None:
            return None
        image = image.reshape([-1, SIZE_FACE, SIZE_FACE, 1])
        return self.model.predict(image)

    def save_model(self):
        self.model.save(join(SAVE_DIRECTORY, SAVE_MODEL_FILENAME))
        print('[+] Model trained and saved at ' + SAVE_MODEL_FILENAME)

    def load_model(self):
        model_path = join('.\\', SAVE_DIRECTORY, SAVE_MODEL_FILENAME)
        self.model.load(model_path)


if __name__ == "__main__":
    network = EmotionRecognition()
    network.start_training()
    network.save_model()
