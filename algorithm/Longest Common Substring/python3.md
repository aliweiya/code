```python
def longest_common_substring(s1, s2):
    m = len(s1)
    n = len(s2)
    dp = [[0 for i in range(n+1)] for i in range(m+1)]

    max_length = 0

    for i in range(1, m+1):
        for j in range(1, n+1):
            if s1[i-1] == s2[j-1]:
                dp[i][j] = dp[i-1][j-1] + 1
                max_length = max(max_length, dp[i][j])

    for row in dp:
        for column in row:
            print(column, end=' ')

        print('')

    # 查找所有的max_length
    start = []
    for i in range(m):
        for j in range(n):
            if dp[i+1][j+1] == max_length:
                start.append(i)

    print("max length is: ", max_length)
    print("the number of max length is: ", len(start))
    for item in start:
        print(s1[item-max_length+1:item+1])

longest_common_substring('BCBWD', 'ABCBDEFBWD')
```