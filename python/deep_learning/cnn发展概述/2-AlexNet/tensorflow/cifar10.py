import tensorflow as tf

class AlexNet:
    def __init__(self):
        self.input_image = tf.placeholder(tf.float32, [None, 32 * 32 * 3])
        self.input_image = tf.reshape(self.input_image, [-1, 32, 32, 3])
        self.input_label = tf.placeholder(tf.int8, [None, 10])

        
