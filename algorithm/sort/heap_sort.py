def left(i):
    return 2 * i + 1


def right(i):
    return 2 * i + 2


def parent(i):
    return i // 2


class Heap:
    def __init__(self, data):
        """
        length 表示数组元素的个数
        heap_size 表示有多少个堆元素存储在该数组中
        0 <= heap_size <= length
        """
        self._data = data
        self.length = len(self._data)
        self.heap_size = self.length

    def max_heapify(self, i):
        """ 假定根节点为 left(i) 和right(i)的二叉树都是最大堆，但是A[i]可能小于其孩子

        通过让A[i]在最大堆中逐级下降，从而使得以下标i为根节点的子树重新遵循最大堆的性质

        每个孩子的子树的大小至多为2n/3

        T(n) <= T(2n/3) + Theta(1)

        a = 1, b = 3/2, k = 0, 满足 a=b^k, 时间复杂度为O(log n)
        """
        l = left(i)
        r = right(i)

        if l < self.heap_size and self._data[l] > self._data[i]:
            largest = l
        else:
            largest = i

        if r < self.heap_size and self._data[r] > self._data[largest]:
            largest = r

        if largest != i:
            self._data[i], self._data[largest] = self._data[largest], self._data[i]
            self.max_heapify(largest)

    def build_max_heap(self):
        """
        叶节点不用调整
        时间复杂度为 O(n)
        """
        for i in range(self.length // 2, -1, -1):
            self.max_heapify(i)

    def heap_sort(self):
        """ 时间复杂度 O(n log n) ，n-1次调用max_heapify，每次 O(log n) """
        self.build_max_heap()
        for i in range(self.length-1, 0, -1):
            self._data[0], self._data[i] = self._data[i], self._data[0]
            self.heap_size -= 1
            self.max_heapify(0)

        return self._data


if __name__ == '__main__':
    A = [1,2,4,3,19,2,44,29,190,24]
    solution = Heap(A)
    print(solution.heap_sort())
