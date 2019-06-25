import matplotlib.pyplot as plt
import numpy as np

"""
In this exercise we will develop a neural network with fully-connected layers to perform classification, 
    and test it out on the CIFAR-10 dataset.
"""

from cs231n.classifier.neural_net import TwoLayerNet
from cs231n.datasets.cifar10 import get_CIFAR10_data
from cs231n.gradient_check import eval_numerical_gradient
from cs231n.vis_util import visualize_grid

# plt.rcParams['figure.figsize'] = (10.0, 8.0) # set default size of plots
# plt.rcParams['image.interpolation'] = 'nearest'
# plt.rcParams['image.cmap'] = 'gray'

def rel_error(x, y):
    """ returns relative error """
    return np.max(np.abs(x - y) / (np.maximum(1e-8, np.abs(x) + np.abs(y))))

def _init_toy_model(input_size, hidden_size, num_classes):
    np.random.seed(0)
    return TwoLayerNet(input_size, hidden_size, num_classes, std=1e-1)

def _init_toy_data(num_inputs, input_size):
    np.random.seed(1)
    # rand: Create an array of the given shape and populate 
    #   it with random samples from a uniform distribution over [0, 1).
    # randn: Return a sample (or samples) from the “standard normal” distribution.
    X = 10 * np.random.randn(num_inputs, input_size)
    y = np.array([0, 1, 2, 2, 1])
    return X, y

def toy_data():
    # Create a small net and some toy data
    input_size = 4
    hidden_size = 10
    num_classes = 3
    num_inputs = 5

    net = _init_toy_model(input_size, hidden_size, num_classes)
    X, y = _init_toy_data(num_inputs, input_size)

    # Forward pass: compute scores
    scores = net.loss(X)
    print('Your scores:')
    print(scores)
    print()
    correct_scores = np.asarray([
        [-0.81233741, -1.27654624, -0.70335995],
        [-0.17129677, -1.18803311, -0.47310444],
        [-0.51590475, -1.01354314, -0.8504215 ],
        [-0.15419291, -0.48629638, -0.52901952],
        [-0.00618733, -0.12435261, -0.15226949]])
    print('Current scores')
    print(correct_scores)

    print('Difference between your scores and correct scores:')
    print(np.sum(np.abs(scores - correct_scores)))

    # Forward pass: compute loss
    loss, _ = net.loss(X, y, reg=0.1)
    correct_loss = 1.30378789133

    print("Difference between your loss and correct loss.")
    print(np.sum(np.abs(loss - correct_loss)))

    # Backward pass
    loss, grads = net.loss(X, y, reg=0.1)
    for param_name in grads:
        f = lambda W: net.loss(X, y, reg=0.1)[0]
        param_grad_num = eval_numerical_gradient(f, net.params[param_name], verbose=False)
        print('{} max relative error: {}'.format(param_name, rel_error(param_grad_num, grads[param_name])))
    
    # Train the network
    net = _init_toy_model(input_size, hidden_size, num_classes)
    stats = net.train(X, y, X, y, 
                learning_rate=1e-1, reg=1e-5, 
                num_iters=100, verbose=False)

    print('Final training loss: {}'.format(stats['loss_history'][-1]))

    plt.plot(stats['loss_history'])
    plt.xlabel('iteration')
    plt.ylabel('training loss')
    plt.title('Training Loss history')
    plt.show()

def show_net_weights(net):
    W1 = net.params['W1']
    W1 = W1.reshape(32, 32, 3, -1).transpose(3, 0, 1, 2)
    plt.imshow(visualize_grid(W1, padding=3).astype('uint8'))
    # Get the current Axes instance on the current figure matching the given keyword args, or create one.
    plt.gca().axis('off')
    plt.show()

def main():
    # toy_data()

    # Load the data
    num_training, num_validation, num_test = 49000, 1000, 1000
    X_train, y_train, X_val, y_val, X_test, y_test = get_CIFAR10_data(num_training, num_validation)

    # Normalize the data: subtract the mean image
    mean_image = np.mean(X_train, axis=0)
    X_train -= mean_image
    X_val -= mean_image
    X_test -= mean_image

    # Reshape data to rows
    X_train = X_train.reshape(num_training, -1)
    X_val = X_val.reshape(num_validation, -1)
    X_test = X_test.reshape(num_test, -1)

    # Train a network
    input_size = 32 * 32 * 3
    hidden_size = 50
    num_classes = 10
    net = TwoLayerNet(input_size, hidden_size, num_classes)

    # Train the network
    # stats = net.train(X_train, y_train, X_val, y_val,
    #                   num_iters=1000, batch_size=200,
    #                   learning_rate=1e-4, learning_rate_decay=0.95,
    #                   reg=0.5, verbose=True)

    # val_acc = (net.predict(X_val) == y_val).mean()
    # print("Validation accuracy: {}".format(val_acc))

    # Debug the training
    # Plot the loss function and train / validation accuracies
    # plt.subplot(2, 1, 1)
    # plt.plot(stats['loss_history'], label='train')
    # plt.title('Loss history')
    # plt.xlabel('Iteration')
    # plt.ylabel('Loss')

    # plt.tight_layout()

    # plt.subplot(2, 1, 2)
    # plt.plot(stats['train_acc_history'], label='train')
    # plt.plot(stats['val_acc_history'], label='val')
    # plt.title('Classification accuracy history')
    # plt.xlabel('Epoch')
    # plt.ylabel('Classification accuracy')

    # plt.tight_layout()
    # plt.show()

    # Visualize the weights of the network
    # show_net_weights(net)

    # Below, you should experiment with different values of the various
    # hyperparameters, including hidden layer size, learning rate, numer
    # of training epochs, and regularization strength.
    best_net = None

    hidden_size = [75, 100, 125]

    results = {}
    best_val_acc = 0
    best_net = None

    learning_rates = np.array([0.7, 0.8, 0.9, 1, 1,1]) * 1e-3
    regularization_strengths = [0.75, 1, 1.25]

    print("Running...")
    for hs in hidden_size:
        for lr in learning_rates:
            for reg in regularization_strengths:
                print("Training with hs={}, lr={}, reg={}".format(hs, lr, reg))
                net = TwoLayerNet(input_size, hs, num_classes)
                stats = net.train(X_train, y_train, X_val, y_val, num_iters=1500, batch_size=200, learning_rate=lr)
                val_acc = (net.predict(X_val) == y_val).mean()
                if val_acc > best_val_acc:
                    best_val_acc = val_acc
                    best_net = net
                results[(hs, lr, reg)] = val_acc

    print('Finished!')
    for hs, lr, reg in sorted(results):
        val_acc = results[(hs, lr, reg)]
        print('hs {} lr {} reg {} val accuracy: {}'.format(hs, lr, reg, val_acc))

    print('best validation accuracy achieved during cross-validation: {}'.format(best_val_acc))
    # visualize the weights of the best network
    show_net_weights(best_net)

if __name__ == '__main__':
    main()