import numpy as np


def L(x, y, w, b):
    # 计算损失函数
    return y*(np.dot(x, w) + b)>0


def createDataSet():
    trainSets = np.array([[3, 3], [4, 3], [1, 1]])
    trainLabels = np.array([1, 1, -1])
    return trainSets, trainLabels


def perceptron(trainSets, trainLabels, learning_rate=1):
    # 取初值w=0, b=0
    w = np.zeros(len(trainSets[0]))
    b = 0

    while True:
        # 判断所有点是否都已经被完全分类
        isFind = True
        for index, trainSet in enumerate(trainSets):
            trainLabel = trainLabels[index]
            if not L(trainSet, trainLabel, w, b):
                # 误分类点，需要更新w,b
                isFind = False
                w = w + learning_rate * trainLabel * trainSet
                b = b + learning_rate * trainLabel

                print("未正确分类点：（{},{}），更新后地感知机模型为w={},b={}".format(trainSet[0], trainSet[1], w, b))
            else:
                print("正确分类点：（{},{}），更新后地感知机模型为w={},b={}".format(trainSet[0], trainSet[1], w, b))

        if isFind == True:
            print(w, b)
            break

def dual_perceptron(trainSets, trainLabels, learning_rate=1):
    alpha = np.zeros(len(trainSets))
    b = 0

    # 计算Gram矩阵
    gram = [[np.dot(i,j) for i in trainSets] for j in trainSets]
    print(gram)

    while True:
        # 判断所有点是否都已经被完全分类
        isFind = True
        for index, trainSet in enumerate(trainSets):
            trainLabel = trainLabels[index]

            if trainLabel * (np.sum([alpha[j]*trainLabels[j]*gram[j][index] for j in range(len(trainSets))])+b) <= 0:
                 # 误分类点，需要更新w,b
                isFind = False
                alpha[index] = alpha[index] + learning_rate
                b = b + learning_rate*trainLabel

                print("未正确分类点：（{},{}），更新后地感知机模型为alpha={},b={}".format(trainSet[0], trainSet[1], alpha, b))
            else:
                print("正确分类点：（{},{}），更新后地感知机模型为alpha={},b={}".format(trainSet[0], trainSet[1], alpha, b))

        if isFind == True:
            print(alpha, b)
            break

def main():
    trainSets, trainLabels = createDataSet()
    # perceptron(trainSets, trainLabels)
    dual_perceptron(trainSets, trainLabels)

if __name__ == '__main__':
    main()