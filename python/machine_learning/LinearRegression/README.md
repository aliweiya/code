假设要训练的模型为

```math
f(x_1,x_2,\cdots,x_n)=w_1x_1+w_2x_2+\cdots+w_nx_n+b
```

写称向量形式为

```math
f(\bold{x}) = \vec{W}\vec{x}+b
```

训练数据：

```math
y_1=w_1x_{11}+w_2x_{12}+\cdots+w_nx_{1n}+b=\vec{W}\vec{x_1}+b\\
y_2=w_1x_{21}+w_2x_{22}+\cdots+w_nx_{2n}+b=\vec{W}\vec{x_2}+b\\
\cdots\\
y_n=w_1x_{n1}+w_1x_{n2}+\cdots+w_nx_{nn}+b=\vec{W}\vec{x_n}+b
```

# 梯度下降

损失函数为

```math
\begin{aligned}
\mathcal{L}&=\frac{1}{2n}\sum_{i=1}^n(y_i-\hat{y}_i)^2\\
&=\frac{1}{2n}\sum_{i=1}^n(y_i-h_\theta(\vec{x_i}))^2\\
&=\frac{1}{2n}\sum_{i=1}^n(\vec{w}\vec{x_i}+b-y_i)^2
\end{aligned}
```

对损失函数进行求导

```math
\begin{aligned}
\frac{\partial\mathcal{L}}{\partial w}&=\frac{1}{n}\sum_{i=1}^n(h_\theta(\vec{x}_i)-y_i)\cdot \vec{x}_i\\
\frac{\partial \mathcal{L}}{\partial b}&=\frac{1}{n}\sum_{i=1}^n(h_\theta(\vec{x}_i)-y_i)
\end{aligned}
```


参数更新：

```math
\vec{w}_j=\vec{w}_j-\alpha \frac{\partial \ell}{\partial \vec{w}_j}\\
b = b - \alpha\frac{\partial \ell}{\partial b}
```

# 求解方程组

