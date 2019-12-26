import numpy as np

import sklearn.datasets as datasets
from sklearn import linear_model
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score, mean_squared_error, roc_curve, auc
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import PolynomialFeatures, StandardScaler


ss = StandardScaler()

Boston = datasets.load_boston()
reg = linear_model.LinearRegression()

x = Boston.data   #shape:(506, 13)
y = Boston.target   #shape:(506,)

# 特征缩放
x = ss.fit_transform(x)
# 添加系数
x = np.append(arr=np.ones((x.shape[0],1)), values=x, axis=1)
# 剔除特征
x = x[:,[0,1,2,4,5,6,8,9,10,11,12]]

# 分割数据集
x_train,x_test,y_train,y_test = train_test_split(x,y,test_size = 0.25,random_state = 0)

regressor = LinearRegression()
regressor = regressor.fit(x_train,y_train)

#预测测试集
y_pre = regressor.predict(x_test)

#（确定系数）回归分数函数。
print(r2_score(y_test,y_pre))
# 均方误差回归损失
print(mean_squared_error(y_test,y_pre))