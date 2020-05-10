import sys


class MaximumSubArray:
    def __init__(self, data):
        self._data = data

    def find_maximum_sub_array(self, low, high):
        if high == low:
            return low, high, self._data[low]
        else:
            mid = (low + high) // 2
            left_low, left_high, left_sum = self.find_maximum_sub_array(low, mid)
            right_low, right_high, right_sum = self.find_maximum_sub_array(mid+1, high)
            cross_low, cross_high, cross_sum = self.find_maximum_crossing_array(low, mid, high)

        if left_sum > right_sum and left_sum > cross_sum:
            return left_low, left_high, left_sum
        elif right_sum > left_sum and right_sum > cross_sum:
            return right_low, right_high, right_sum
        else:
            return cross_low, cross_high, cross_sum

    def find_maximum_crossing_array(self, low, mid, high):
        left_sum = -sys.maxsize
        _sum = 0
        for i in range(mid, low-1, -1):
            _sum += self._data[i]
            if _sum > left_sum:
                left_sum = _sum
                max_left = i

        right_sum = -sys.maxsize
        _sum = 0
        for j in range(mid+1, high+1):
            _sum += self._data[j]
            if _sum > right_sum:
                right_sum = _sum
                max_right = j

        return max_left, max_right, left_sum + right_sum


if __name__ == '__main__':
    A = [-5, -4, -1, -2, 8, -3, 13, -4, 28, -5]
    solution = MaximumSubArray(A)
    print(solution.find_maximum_sub_array(0, len(A)-1))