import numpy as np

true_w = [2, 3, 4]
true_b = 3.4

num_samples = 20
num_features = 3

iterations = 10000
learning_rate = 0.0007
learning_rate_b = 0.03

# train[i]为样本，train[:, 0]为第一个特征。
train =  np.random.rand(num_samples, num_features) * 20
# equal to np.dot(train[i], true_w)
y = np.array([np.dot(true_w, sample) for i, sample in enumerate(train)]) + true_b

# 随机初始化参数
pred_w = np.random.normal(0, 1, num_features)
pred_b = np.random.normal(0, 1)

# 梯度下降
for i in range(iterations):
    h_theta = np.array([np.dot(pred_w, train[i]) for i in range(len(train))]) + pred_b
    loss = np.sum(np.square(h_theta - y))/ (2*num_samples)
    print('loss: {}'.format(loss))
    grad_w = np.sum([epsilon * train[i] for i, epsilon in enumerate(h_theta - y)], axis=0) / num_samples
    grad_b = np.sum(h_theta - y) / num_samples

    pred_w -= learning_rate * grad_w
    pred_b -= learning_rate_b * grad_b
    print('pred b: {}'.format(pred_b))

print('predicted w:', pred_w)
print('predicted b:', pred_b)