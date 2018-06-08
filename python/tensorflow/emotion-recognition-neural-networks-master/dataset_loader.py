from os.path import join
import numpy as np
from constants import *
import cv2

class DatasetLoader(object):
    def load_from_save(self, data_source='fer2013'):
        """
            加载npy文件作为训练集和测试集
        """
        self.data_source = data_source

        assert self.data_source in DATA_SOURCE, '不支持的数据源：{0}，支持的数据源有：{1}'.format(self.data_source, '，'.join(DATA_SOURCE.keys()))

        data = DATA_SOURCE[self.data_source]

        self._images      = np.load(join(DATA_DIRECTORY, data['SAVE_DATASET_IMAGES_FILENAME']))
        self._labels      = np.load(join(DATA_DIRECTORY, data['SAVE_DATASET_LABELS_FILENAME']))
        self._images_test = np.load(join(DATA_DIRECTORY, data['SAVE_DATASET_IMAGES_TEST_FILENAME']))
        self._labels_test = np.load(join(DATA_DIRECTORY, data['SAVE_DATASET_LABELS_TEST_FILENAME']))

        self._images      = self._images.reshape([-1, SIZE_FACE, SIZE_FACE, 1])
        self._images_test = self._images_test.reshape([-1, SIZE_FACE, SIZE_FACE, 1])
        self._labels      = self._labels.reshape([-1, len(EMOTIONS)])
        self._labels_test = self._labels_test.reshape([-1, len(EMOTIONS)])

    @property
    def images(self):
        return self._images

    @property
    def labels(self):
        return self._labels

    @property
    def images_test(self):
        return self._images_test

    @property
    def labels_test(self):
        return self._labels_test

    @property
    def num_examples(self):
        return self._num_examples