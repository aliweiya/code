# -*- coding: utf-8 -*-

import matplotlib.pyplot as plt
import numpy as np

from constants import *
from emotion_recognition import EmotionRecognition
from dataset_loader import DatasetLoader

# Load Model
network = EmotionRecognition()
network.build_network(loadModel=True)

data = DatasetLoader()
data.load_from_save(data_source='fer2013')

images = data.images_test
labels = data.labels_test

print('[+] Loading Data')
data = np.zeros((len(EMOTIONS),len(EMOTIONS)))

for i in range(images.shape[0]):
    if i % 1000 == 0:
        print("Progress: {}/{} {:.2f}%".format(i, images.shape[0], i * 100.0 / images.shape[0]))
    result = network.predict(images[i])
    data[np.argmax(labels[i]), np.argmax(result[0])] += 1

print("Accuracy: %f" % (np.sum(data.diagonal())/np.sum(data)))
# Take % by column
# 生成混淆矩阵
for i in range(len(data)):
    total = np.sum(data[i])
    for x in range(len(data[0])):
        data[i][x] = data[i][x] / total

print('[+] Generating graph')
# Create a pseudocolor plot of a 2-D array.
# https://matplotlib.org/api/_as_gen/matplotlib.pyplot.pcolor.html
c = plt.pcolor(data, edgecolors='k', linewidths=4, cmap='Blues', vmin=0.0, vmax=1.0)
 
def show_values(pc, fmt="%.2f", **kw):
    # from itertools import zip
    # https://matplotlib.org/api/collections_api.html?highlight=update_scalarmappable#matplotlib.collections.PolyCollection.update_scalarmappable
    pc.update_scalarmappable()
    ax = pc.axes
    # arange函数用于创建等差数组，支持步长为小数
    # https://matplotlib.org/api/_as_gen/matplotlib.axes.Axes.set_yticks.html#matplotlib.axes.Axes.set_yticks
    ax.set_yticks(np.arange(len(EMOTIONS)) + 0.5, minor = False)
    ax.set_xticks(np.arange(len(EMOTIONS)) + 0.5, minor = False)
    # https://matplotlib.org/api/_as_gen/matplotlib.axes.Axes.set_yticklabels.html#matplotlib.axes.Axes.set_yticklabels
    ax.set_xticklabels(EMOTIONS, minor = False)
    ax.set_yticklabels(EMOTIONS, minor = False)
    for p, color, value in zip(pc.get_paths(), pc.get_facecolors(), pc.get_array()):
        x, y = p.vertices[:-2, :].mean(0)
        # np.all比较矩阵所有元素是否满足条件
        if np.all(color[:3] > 0.5):
            color = (0.0, 0.0, 0.0)
        else:
            color = (1.0, 1.0, 1.0)
        ax.text(x, y, fmt % value, ha="center", va="center", color=color, **kw)

show_values(c)
plt.xlabel('Predicted Emotion')
plt.ylabel('Real Emotion')
plt.show()