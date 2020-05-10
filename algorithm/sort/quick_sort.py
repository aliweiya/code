class QuickSort:
    def __init__(self, data):
        self._data = data

    def sort(self):
        self.helper(0, len(self._data)-1)
        return self._data

    def helper(self, p, r):
        if p < r:
            q = self.partition(p, r)
            self.helper(p, q-1)
            self.helper(q+1, r)

    def partition(self, p, r):
        # pivot element
        x = self._data[r]
        for i in range(p, r):
            if self._data[i] < x:
                self._data[p], self._data[i] = self._data[i], self._data[p]
                p += 1

        self._data[p], self._data[r] = self._data[r], self._data[p]

        return p


if __name__ == '__main__':
    solution = QuickSort([1, 9, 2, 19, 8, 15, 24, 4, 2])
    print(solution.sort())