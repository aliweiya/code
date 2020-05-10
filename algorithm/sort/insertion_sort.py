class InsertionSort:
    def __init__(self, data):
        self.data = data

    def insertion_sort(self):
        """ 将未排序元素插入到已排序元素中
        时间复杂度： O(n^2)
        """
        for current in range(1, len(self.data)):
            j = 0
            while self.data[current] > self.data[j]:
                j += 1

            self.data.insert(j, self.data[current])
            del self.data[current+1]

        return self.data


if __name__ == '__main__':
    data = [2, 34, 5, 1, 5, 8]
    sort = InsertionSort(data)
    print(sort.insertion_sort())