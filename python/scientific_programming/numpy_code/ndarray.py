import numpy as np

print np.__version__

# create
a = np.array([1, 2, 3, 4])
b = np.array([5, 6, 7, 8])
c = np.array([[1, 2, 3, 4], [5, 6, 7, 8], [9, 10, 11, 12]])

# (3, 4)
print c.shape 

c.shape = 4, 3
# c = np.array([
#       [1, 2, 3], 
#       [4, 5, 6],
#       [7, 8, 9], 
#       [10, 11, 12]])

d = a.reshape((2, 2))
# d = [[1, 2], [3, 4]]

print c.dtype
print set(np.typeDict.values())

a = np.int16(200)

t1 = np.array([1, 2, 3, 4], dtype=np.float)
t2 = t1.astype(np.int32)

a = np.arange(0, 1, 0.1)

# step is 1/9
a = np.linspace(0, 1, 10)
# step is 1/10
a = np.linspace(0, 1, 10, endpoint=False)

# five numbers in 10^0 - 10^2
a = np.logspace(0, 2, 5, base=10)

a = np.zeros(4, np.int)
a = np.ones(4, np.int)
a = np.empty((2, 3), np.int)

a = np.full(4, np.pi)

# equals to a = np.zeros(a.shape, a.dtype)
a = np.zeros_like(a)


def func(i):
    return i % 4 +1

a = np.fromfunction(func, (10, ))

def func2(i ,j):
    return (i + 1) * (j + 1)

a = np.fromfunction(func2, (9, 9))

# save and get

a[5]
a[3:5]
a[:5]
a[:-1]
# the third param stand for step
a[1:-1:2]
# resverse the array
a[::-1]
a[5:1:-2]

# modify the value
a[2:4] = 100, 101

x[[3,3,1,8,3,3,-3,8]].reshape(2,4)
# [[7, 7, 9, 2],
#  [7, 7, 4, 2]]

x[np.array([True, False, True, False, False])]

x[[True, True, False, False, False]]
# array([4, 5, 4, 5, 5])

x[np.array([True, False, True, True])] = -1, -2, -3

# generate a array from 0 to 9 with 6 elements
x = np.random.randint(0, 10, 6)
# x>5 return True or False array
x[x>5]

# multi-demension array
a[0, 3:5]
a[4:, 4:]
a[:, 2]
a[2::2, ::2]

a = np.arange(0, 60, 10).reshape(-1, 1) + np.arange(0, 6)

np.s_[::2, 2:]

a[(0, 1, 2, 3), (1, 2, 3, 4)] = a[0, 1], a[1, 2], a[2, 30, a[3, 4]

a[[1, 2], :] = a[[1, 2]]

# struct
# S30 means string with 30 bytes
# i means np.int32
# f means np.float32
persontype = np.dtype({
    'names':['name', 'age', 'weight'],
    'formats':['S30', 'i', 'f']
    }, align=True)

a = np.array([('Zhang', 32, 75.5), ('Wang', 24, 65.2)], dtype=persontype)

# describe type with many tuple
# I ignore order of bytes
# < little endian
# > big endian
dtype([('name', '|S30'), ('age', '<i4'), ('weight', '<f4')])
a[0]['name']

# convert to string or file
a.tostring()
a.tofile('test.bin')


# there can be another struct in a struct
np.dtype('f1', [('f2', np.int16)])

# when some field is an array, the third param in a tuple is used to describe the shape
np.dtype([('f0', 'i4'), ('f1', 'f8', (2, 3))])

# useing dict can also define a type
np.dtype({'surname':('S26', 0), 'age':(np.uint8, 25)})

