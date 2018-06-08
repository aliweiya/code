import os
import random
import sys

import traceback

import cv2
import pandas as pd
import numpy as np
from PIL import Image

sys.path.append(os.getcwd()+os.path.sep+"..")

from constants import *

cascade_classifier = cv2.CascadeClassifier(CASC_PATH)


def format_image(image):
    """
        找出人脸，并放大至需要的尺寸
    """
    image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    gray_border = np.zeros((150, 150), np.uint8)
    gray_border[:,:] = 200
    gray_border[int((150 / 2) - (SIZE_FACE/2)):int((150/2)+(SIZE_FACE/2)), int((150/2)-(SIZE_FACE/2)):int((150/2)+(SIZE_FACE/2))] = image
    image = gray_border

    faces = cascade_classifier.detectMultiScale(
        image,
        scaleFactor = 1.3,
        minNeighbors = 5
    )

    if not len(faces) > 0:
        return None
    max_area_face = faces[0]
    for face in faces:
        if face[2] * face[3] > max_area_face[2] * max_area_face[3]:
            max_area_face = face

    face = max_area_face
    image = image[face[1]:(face[1] + face[2]), face[0]:(face[0] + face[3])]

    try:
        image = cv2.resize(image, (SIZE_FACE, SIZE_FACE), interpolation=cv2.INTER_CUBIC) / 255.
    except Exception:
        print("[+] Problem during resize")
        return None
    return image


def emotion_to_vec(x):
    d = np.zeros(len(EMOTIONS))
    d[x] = 1.0
    return d


def image_to_npy(file):
    im = Image.open(file).resize((48, 48)).convert("RGB")
    data_image = np.array(im)[:, :, ::-1].copy() 
    return format_image(data_image)


class Data():
    def save(self):
        print("Total train: {0}".format(len(self.images_train)))
        print("Total test: {0}".format(len(self.images_test)))
        np.save(self.data['SAVE_DATASET_IMAGES_FILENAME'], self.images_train)
        np.save(self.data['SAVE_DATASET_LABELS_FILENAME'], self.labels_train)
        np.save(self.data['SAVE_DATASET_IMAGES_TEST_FILENAME'], self.images_test)
        np.save(self.data['SAVE_DATASET_LABELS_TEST_FILENAME'], self.labels_test)


class Fer2013(Data):
    def __init__(self):
        self.data = DATA_SOURCE['fer2013']

    def flip_image(self, image):
        return cv2.flip(image, 1)

    def data_to_image(self, data):
        """
            csv文件中的像素转人脸图像
        """
        data_image = np.fromstring(str(data), dtype = np.uint8, sep = ' ').reshape((SIZE_FACE, SIZE_FACE))
        data_image = Image.fromarray(data_image).convert('RGB')
        data_image = np.array(data_image)[:, :, ::-1].copy() 
        data_image = format_image(data_image)
        return data_image

    def save_npy(self):
        data = pd.read_csv(self.data['FILE_PATH'])

        self.labels_train = []
        self.images_train = []
        self.labels_test = []
        self.images_test = []
        total = data.shape[0]

        # 读取csv文件，转换为图片，并保存到训练集和测试集
        for index, row in data.iterrows():
            emotion = emotion_to_vec(row['emotion'])
            image = self.data_to_image(row['pixels'])
            if image is not None:
                if row['Usage'] == "Training":
                    self.labels_train.append(emotion)
                    self.images_train.append(image)
                else:
                    self.labels_test.append(emotion)
                    self.images_test.append(image)
            print("Progress: {}/{} {:.2f}%".format(index, total, index * 100.0 / total))

        super().save()


class Jaffe(Data):
    def __init__(self):
        self.data = DATA_SOURCE['jaffe']
        self.emotion_mapping = {
            'DI': 1,
            'HA': 3,
            'NE': 6,
            'SA': 4,
            'AN': 0,
            'SU': 5,
            'FE': 2,
        }

    def save_npy(self):
        self.labels_train = []
        self.images_train = []
        self.labels_test = []
        self.images_test = []

        for rt, dirs, files in os.walk(self.data['FILE_PATH']):
            for file in files:
                if file.endswith('.tiff'):
                    short_emotion = file.split('.')[1][0:2]
                    emotion = emotion_to_vec(self.emotion_mapping[short_emotion])
                    image = image_to_npy(rt + os.sep + file)
                    if image is not None:
                        rand = random.randint(0, 9)
                        if rand > 8:
                            self.images_test.append(image)
                            self.labels_test.append(emotion)
                        else:
                            self.images_train.append(image)
                            self.labels_train.append(emotion)
        super().save()

class CKPLUS(Data):
    def __init__(self):
        self.data = DATA_SOURCE['CK+']
        self.emotion_mapping = {
            '厌恶-003': 1,
            '高兴-005': 3,
            '伤心-006': 4,
            '生气-001': 0,
            '惊讶-007': 5,
            '害怕-004': 2,
        }


    def save_npy(self):
        self.labels_train = []
        self.images_train = []
        self.labels_test = []
        self.images_test = []

        index = 1
        for rt, dirs, files in os.walk(self.data['FILE_PATH']):
            for file in files:
                if file.endswith('.png'):
                    emotion = emotion_to_vec(self.emotion_mapping[rt.split('\\')[1]])
                    image = image_to_npy(rt + os.sep + file)
                    rand = random.randint(0, 9)
                    if image is not None:
                        if rand > 8:
                            self.images_test.append(image)
                            self.labels_test.append(emotion)
                        else:
                            self.images_train.append(image)
                            self.labels_train.append(emotion)
                if index % 100 == 0:
                    print("Progress: {0}".format(index))
                index += 1

        super().save()

if __name__ == '__main__':

    fer2013 = Fer2013()
    fer2013.save_npy()

    # jaffe = Jaffe()
    # jaffe.save_npy()
    # ck_plus = CKPLUS()
    # ck_plus.save_npy()