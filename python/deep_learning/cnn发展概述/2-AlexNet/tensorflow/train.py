import tensorflow as tf

IMAGE_SIZE = 28 * 28 * 3

def main():
    X = tf.placeholder(tf.loat32, [None, IMAGE_SIZE])
    y_ = tf.placeholder(tf.float32, [None, 10])

    