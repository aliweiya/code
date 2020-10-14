import random
import string

from captcha.image import ImageCaptcha
import matplotlib.pyplot as plt
import numpy as np

import tensorflow as tf

import keras.backend as K
from keras.callbacks import EarlyStopping, CSVLogger, ModelCheckpoint
from keras.layers import Input, Convolution2D, MaxPool2D, Flatten, Dense, Dropout
from keras.models import Model
from keras.optimizers import Adam
from keras.utils import Sequence

# from keras.utils import plot_model
# from IPython.display import Image

# 防止tensorflow占用所有显存
config = tf.ConfigProto()
config.gpu_options.allow_growth=True
sess = tf.Session(config=config)
K.set_session(sess)


class CaptchaSequence(Sequence):
    def __init__(self, characters, batch_size, steps):
        self.characters = string.digits + string.ascii_uppercase
        self.batch_size = batch_size
        self.steps = steps
        self.n_len = 4
        self.width = 32 * self.n_len
        self.height = 64
        self.n_class = len(characters)
        self.channels = 3
        self.generator = ImageCaptcha(width=width, height=height)
    
    def __len__(self):
        return self.steps

    def __getitem__(self, idx):
        X = np.zeros((self.batch_size, self.height, self.width, self.channels), dtype=np.float32)
        y = [np.zeros((self.batch_size, self.n_class), dtype=np.uint8) for i in range(self.n_len)]
        for i in range(self.batch_size):
            random_str = ''.join([random.choice(self.characters) for j in range(self.n_len)])
            X[i] = np.array(self.generator.generate_image(random_str)) / 255.0
            for j, ch in enumerate(random_str):
                y[j][i, :] = 0
                y[j][i, self.characters.find(ch)] = 1
        return X, y

    @staticmethod
    def decode(y):
        y = np.argmax(np.array(y), axis=2)[:,0]
        return ''.join([characters[x] for x in y])

input_tensor = Input((height, width, 3))
x = input_tensor
for i, n_cnn in enumerate([2, 2, 2, 2, 2]):
    for j in range(n_cnn):
        x = Conv2D(32*2**min(i, 3), kernel_size=3, padding='same', kernel_initializer='he_uniform')(x)
        x = BatchNormalization()(x)
        x = Activation('relu')(x)
    x = MaxPooling2D(2)(x)

x = Flatten()(x)
x = [Dense(n_class, activation='softmax', name='c%d'%(i+1))(x) for i in range(n_len)]
model = Model(inputs=input_tensor, outputs=x)

# plot_model(model, to_file='cnn.png', show_shapes=True)
# Image('cnn.png')

# model.summary()

train_data = CaptchaSequence(characters, batch_size=128, steps=1000)
valid_data = CaptchaSequence(characters, batch_size=128, steps=100)
callbacks = [EarlyStopping(patience=3), CSVLogger('cnn.csv'), ModelCheckpoint('cnn_best.h5', save_best_only=True)]

model.compile(loss='categorical_crossentropy',
              optimizer=Adam(1e-3, amsgrad=True), 
              metrics=['accuracy'])
model.fit_generator(train_data, epochs=100, validation_data=valid_data, workers=4, use_multiprocessing=True,
                    callbacks=callbacks)

# 测试模型
# X, y = data[0]
# y_pred = model.predict(X)
# plt.title('real: %s\npred:%s'%(decode(y), decode(y_pred)))
# plt.imshow(X[0], cmap='gray')
# plt.axis('off')