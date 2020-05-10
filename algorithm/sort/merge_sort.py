import sys


class MergeSort:
    def merge_sort(self, _list):
        if len(_list) <= 1:
            return _list

        middle = len(_list) // 2
        left = self.merge_sort(_list[:middle])
        right = self.merge_sort(_list[middle:])
        return self.merge(left, right)

    def merge(self, left, right):
        result = []

        length_left = len(left)
        length_right = len(right)

        i = j = 0

        left.append(sys.maxsize)
        right.append(sys.maxsize)

        while i < length_left or j < length_right:
            if left[i] <= right[j]:
                result.append(left[i])
                i += 1
            else:
                result.append(right[j])
                j += 1

        return result


if __name__ == '__main__':
    data = [2, 5, 4]
    sort = MergeSort()
    print(sort.merge_sort(data))
