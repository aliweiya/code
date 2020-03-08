from keras.models import Sequential
from keras.layers.convolutional import Conv2D
from keras.layers.convolutional import MaxPooling2D
from keras.layers.core import Activation, Flatten, Dense, Dropout
from keras.regularizers import l2

class VGG16:
    @staticmethod
    def build(width, height, depth=3, classes, rep=2e-3):
        model = Sequential()
        inputShape = (height, width, depth)
        chanDim = -1

        # if we are using "channels first", update the input shape
        # and channels dimension
        if K.image_data_format() == "channels_first":
            inputShape = (depth, height, width)
            chanDim = 1

        model.add(Conv2D(64, (3, 3), strides=(1, 1),
            input_shape=inputShape, padding="same",
            kernel_regularizer=l2(reg)))
        model.add(Activation("relu"))
        model.add(Conv2D(64, (3, 3), strides=(1, 1),
            input_shape=inputShape, padding="same",
            kernel_regularizer=l2(reg)))
        model.add(Activation("relu"))

        model.add(MaxPooling2D(pool_size=(2, 2), strides=(2, 2)))

        model.add(Conv2D(128, (3, 3), strides=(1, 1),
            input_shape=inputShape, padding="same",
            kernel_regularizer=l2(reg)))
        model.add(Activation("relu"))
        model.add(Conv2D(128, (3, 3), strides=(1, 1),
            input_shape=inputShape, padding="same",
            kernel_regularizer=l2(reg)))
        model.add(Activation("relu"))

        model.add(MaxPooling2D(pool_size=(2, 2), strides=(2, 2)))

        model.add(Conv2D(256, (3, 3), strides=(1, 1),
            input_shape=inputShape, padding="same",
            kernel_regularizer=l2(reg)))
        model.add(Activation("relu"))
        model.add(Conv2D(256, (3, 3), strides=(1, 1),
            input_shape=inputShape, padding="same",
            kernel_regularizer=l2(reg)))
        model.add(Activation("relu"))
        model.add(Conv2D(256, (3, 3), strides=(1, 1),
            input_shape=inputShape, padding="same",
            kernel_regularizer=l2(reg)))
        model.add(Activation("relu"))

        model.add(MaxPooling2D(pool_size=(2, 2), strides=(2, 2)))

        model.add(Conv2D(512, (3, 3), strides=(1, 1),
            input_shape=inputShape, padding="same",
            kernel_regularizer=l2(reg)))
        model.add(Activation("relu"))
        model.add(Conv2D(512, (3, 3), strides=(1, 1),
            input_shape=inputShape, padding="same",
            kernel_regularizer=l2(reg)))
        model.add(Activation("relu"))
        model.add(Conv2D(512, (3, 3), strides=(1, 1),
            input_shape=inputShape, padding="same",
            kernel_regularizer=l2(reg)))
        model.add(Activation("relu"))

        model.add(MaxPooling2D(pool_size=(2, 2), strides=(2, 2)))

        model.add(Conv2D(512, (3, 3), strides=(1, 1),
            input_shape=inputShape, padding="same",
            kernel_regularizer=l2(reg)))
        model.add(Activation("relu"))
        model.add(Conv2D(512, (3, 3), strides=(1, 1),
            input_shape=inputShape, padding="same",
            kernel_regularizer=l2(reg)))
        model.add(Activation("relu"))
        model.add(Conv2D(512, (3, 3), strides=(1, 1),
            input_shape=inputShape, padding="same",
            kernel_regularizer=l2(reg)))
        model.add(Activation("relu"))

        model.add(MaxPooling2D(pool_size=(2, 2), strides=(2, 2)))

        model.add(Flatten())
        model.add(Dense(4096, kernel_regularizer=l2(reg)))
        model.add(Dense(4096, kernel_regularizer=l2(reg)))
        model.add(Dropout(0.5))

        model.add(Dense(classes, kernel_regularizer=l2(reg)))
        model.add(Activation("softmax"))

        return model