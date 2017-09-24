import numpy as np
import math

x = np.linspace(0, 2*np.pi, 10)
y = np.sin(x)

# using parameter out to save the result
t = np.sin(x, out=x)
# t is x

# list list comprehension is faster than for operation
# but it generate a new list
x = [math.sin(t) for t in x]

a = np.arange(6.0).reshape(2, 3)
print a.item(1, 2), type(a.item(1, 2))

# add
a = np.arange(0, 4)
b = np.arange(1, 5)
np.add(a, b, out=a)
np.substract(a, b)
np.divide(a, b)
np.floor_divide(a, b)
np.negative(a)
np.power(a, b)
# %
np.remainder(a, b)
np.mod(a, b)

# ==
np.equal(a, b [,y])
# !=
np.not_equal(a, b [,y])

# <
np.less(a, b[,y])

# <=
np.less_equal(a, b[,y])

# >
np.greater(a, b[,y])

# >=
np.greater_equal(a, b[,y])

# boolean operation
np.logical_and()
np.logical_or()
np.logical_not()
np.logical_xor()

# frompyfunc()
de triangle_wave(x, c, c0, hc):
    x = x - int(x)
    if x >= c:
        r = 0.0
    elif x< c0:
        r = x / c0 * hc
    else:
        r = (c-x) / (c-c0) * hc

    return r

x = np.linspace(0, 2, 1000)
y1 = np.array([triangle_wave(t, 0.6, 0.4, 1.0) for t in x])

# or
# the type of the trianle_ufunc1's return value is object
triangle_ufunc1 = np.frompyfunc(triangle_wave, 4, 1)
y2 = triangle_ufunc1(x, 0.6, 0.4, 1.0)
y1.astype(np.float)

