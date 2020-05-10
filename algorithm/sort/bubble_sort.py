class BubbleSort:
    def __init__(self, data):
        self._data = data

    def bubble_sort(self):
        for i in range(len(self._data)-2):
            for j in range(i, len(self._data)-1):
                if self._data[j] > self._data[j+1]:
                    self._data[j], self._data[j+1] = self._data[j+1], self._data[j]

        return self._data


if __name__ == '__main__':
    A = [1,2,419999,3,19,2,44,29,190,24]
    solution = BubbleSort(A)
    print(solution.bubble_sort())