import matplotlib.pyplot as plt
import numpy as np

X = np.concatenate([np.random.normal(0.5, 0.1, 50), np.random.normal(1, 0.1, 50)])
y = np.concatenate([np.random.normal(0.5, 0.1, 50), np.random.normal(1, 0.1, 50)])

plt.axis([0, 2, 0, 2])

plt.subplot(2, 3, 1)
plt.plot(X, y, '.')
plt.xlabel('(1)')

# 随机选择两个中心点
center = [(np.random.normal(1, 0.2, 2)) for i in range(2)]

plt.subplot(2, 3, 2)
plt.plot(X, y, '.')
plt.plot(*center[0], 'rx')
plt.plot(*center[1], 'bx')
fig_index = 3
plt.xlabel('(2)')


def compute():
    global center
    global fig_index

    # 计算距离
    d1 = np.sqrt(np.square(X - center[0][0]) + np.square(y - center[0][1]))
    d2 = np.sqrt(np.square(X - center[1][0]) + np.square(y - center[1][1]))

    c1 = d1 < d2
    c2 = d1 > d2

    c1_X = X[c1]
    c1_y = y[c1]

    c2_X = X[c2]
    c2_y = y[c2]

    plt.subplot(2, 3, fig_index)
    plt.plot(c1_X, c1_y, 'r.')
    plt.plot(c2_X, c2_y, 'b.')

    plt.plot(*center[0], 'rx')
    plt.plot(*center[1], 'bx')

    plt.xlabel('({})'.format(fig_index))

    center = np.array([[np.mean(c1_X), np.mean(c1_y)],
                       [np.mean(c2_X), np.mean(c2_y)]])

    fig_index += 1


compute()
compute()
compute()
compute()
plt.show()