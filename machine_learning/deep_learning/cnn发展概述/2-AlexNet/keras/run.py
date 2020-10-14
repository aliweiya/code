from keras.callbacks import TensorBoard
from keras.preprocessing.image import ImageDataGenerator
from keras.optimizers import Adam

from alexnet import AlexNet

dataset_path = '/root/M/datasets/dogs-vs-cats-redux-kernels-edition/train_keras'
height, width, channel, num_class = 227, 227, 3, 2
batch_size = 32
nb_epochs = 100

CLASSES = ['cat', 'dog']

# construct the training image generator for data augmentation
aug = ImageDataGenerator(rescale=1./255, rotation_range=20, zoom_range=0.15,
	width_shift_range=0.2, height_shift_range=0.2, shear_range=0.15,
	horizontal_flip=True, fill_mode="nearest",
	validation_split=0.2)

train_generator = aug.flow_from_directory(
	dataset_path, target_size=(height, width),
	batch_size=batch_size,
	class_mode='categorical',
	subset='training',
	classes=CLASSES
)

# TODO: keras也会对验证集进行数据增强
validation_generator = aug.flow_from_directory(
	dataset_path, target_size=(height, width),
	batch_size=batch_size,
	class_mode='categorical',
	subset='validation',
	classes=CLASSES
)

tbCallBack = TensorBoard(log_dir='./logs', histogram_freq=0, write_graph=True, write_images=True)

# initialize the optimizer
print("[INFO] compiling model...")
opt = Adam(lr=0.5e-3)
model = AlexNet.build(width=height, height=width, depth=channel, classes=num_class, reg=0.0002)
model.compile(loss="categorical_crossentropy", optimizer=opt, metrics=["accuracy"])

# train the network
model.fit_generator(
    train_generator,
    steps_per_epoch = train_generator.samples // batch_size,
    validation_data = validation_generator, 
    validation_steps = validation_generator.samples // batch_size,
    epochs = nb_epochs,
	# 0 = silent, 1 = progress bar, 2 = one line per epoch.
	callbacks=[tbCallBack], verbose=2)

# save the model to file
print("[INFO] serializing model...")
model.save("model", overwrite=True)