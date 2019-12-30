from alexnet import AlexNet

height, width, channel, num_class = 227, 227, 3, 2

dataset_path = 'G:\\dataset\\kaggle\dog-vs-cat\\dogs-vs-cats-redux-kernels-edition\\train'

alexNet = AlexNet(height, width, channel, num_class, dataset_path)
alexNet.train()