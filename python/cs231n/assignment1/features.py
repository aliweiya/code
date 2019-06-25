import numpy as np

from cs231n.classifier.linear_classifier import LinearSVM
from cs231n.datasets.cifar10 import get_CIFAR10_data
from cs231n.features import hog_feature, color_histogram_hsv, extract_features
from cs231n.classifier.neural_net import TwoLayerNet

def main():
    X_train, y_train, X_val, y_val, X_test, y_test = get_CIFAR10_data()

    feature_fns = [hog_feature, color_histogram_hsv]
    X_train_features = extract_features(X_train, feature_fns, verbose=True)
    X_val_features = extract_features(X_val, feature_fns, verbose=True)
    X_test_features = extract_features(X_test, feature_fns, verbose=True)

    # Preprocessing: Substract the mean feature
    mean_feature = np.mean(X_train_features, axis=0, keepdims=True)
    X_train_features -= mean_feature
    X_val_features -= mean_feature
    X_test_features -= mean_feature

    # Preprocessing: Divide by standard deviation. This ensures that each feature
    # has roughly the same scale.
    std_feature = np.std(X_train_features, axis=0, keepdims=True)
    X_train_features /= std_feature
    X_val_features /= std_feature
    X_test_features /= std_feature

    # Preprocessing: Add a bias dimension
    X_train_features = np.hstack([X_train_features, np.ones((X_train_features.shape[0], 1))])
    X_val_features = np.hstack([X_val_features, np.ones((X_val_features.shape[0], 1))])
    X_test_features = np.hstack([X_test_features, np.ones((X_test_features.shape[0], 1))])

    # Train SVM on features
    learning_rates = [5e-9, 1e-8, 5e-7]
    regularization_strengths = [(5+i)*1e6 for i in range(-3, 4)]

    results = {}
    best_val = -1
    best_svm = None

    for rs in regularization_strengths:
        for lr in learning_rates:
            svm = LinearSVM()
            loss_hist = svm.train(X_train_features, y_train, lr, rs, num_iters=6000)
            y_train_pred = svm.predict(X_train_features)
            train_accuracy = np.mean(y_train == y_train_pred)
            y_val_pred = svm.predict(X_val_features)
            val_accuracy = np.mean(y_val == y_val_pred)
            if val_accuracy > best_val:
                best_val = val_accuracy
                best_svm = svm           
            results[(lr,rs)] = train_accuracy, val_accuracy

    for lr, reg in sorted(results):
        train_accuracy, val_accuracy = results[(lr, reg)]
        print('lr %e reg %e train accuracy: %f val accuracy: %f' % (
                    lr, reg, train_accuracy, val_accuracy))

    print('best validation accuracy achieved during cross-validation: %f' % best_val)

    # Evaluate your trained SVM on the test set
    y_test_pred = best_svm.predict(X_test_features)
    test_accuracy = np.mean(y_test == y_test_pred)
    print(test_accuracy)

    # Neural Network on image features
    input_dim = X_train_features.shape[1]
    hidden_dim = 500
    num_classes = 10

    net = TwoLayerNet(input_dim, hidden_dim, num_classes)
    best_net = None

    results = {}
    best_val = -1
    best_net = None

    learning_rates = [1e-2, 1e-1, 5e-1, 1, 5]
    regularization_strengths = [1e-3, 5e-3, 1e-2, 1e-1, 0.5, 1]

    for lr in learning_rates:
        for reg in regularization_strengths:
            net = TwoLayerNet(input_dim, hidden_dim, num_classes)
            print("Training with lr={}, reg={}".format(lr, reg))
            stats = net.train(X_train_features, y_train, X_val_features, y_val, num_iters=1500, batch_size=200, learning_rate=lr, reg=reg)
            val_acc = (net.predict(X_val_features) == y_val).mean()
            if val_acc > best_val:
                best_val = val_acc
                best_net = net
            results[(lr, reg)] = val_acc

    for lr, reg in sorted(results):
        val_acc = results[(lr, reg)]
        print('lr {} reg {} val accuracy: {}'.format(lr, reg, val_acc))

    print('best validation accuracy achieved during cross-validation: {}'.format(best_val))

if __name__ == '__main__':
    main()