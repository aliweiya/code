```python
def lcs_length(s1, s2):
    m = len(s1)
    n = len(s2)

    c = [[0 for i in range(n+1)] for i in range(m+1)]
    b = [[0 for i in range(n)] for i in range(m)]

    for i in range(1, m+1):
        for j in range(1, n+1):
            if s1[i-1] == s2[j-1]:
                c[i][j] = c[i-1][j-1] + 1
                b[i-1][j-1] = 'lu'
            elif c[i-1][j] >= c[i][j-1]:
                c[i][j] = c[i-1][j]
                b[i-1][j-1] = 'up'
            else:
                c[i][j] = c[i][j-1]
                b[i-1][j-1] = 'le'


    # for row in c:
    #     for column in row:
    #         print(column, end=' ')

    #     print("")

    # for row in b:
    #     for column in row:
    #         print(column, end=' ')

    #     print("")
    return b, c

def print_lcs(b, s1, i, j):
    if i == -1 or j == -1:
        return
    elif b[i][j] == 'lu':
        print_lcs(b, s1, i-1, j-1)
        print(s1[i])
    elif b[i][j] == 'up':
        print_lcs(b, s1, i-1, j)
    else:
        print_lcs(b, s1, i, j-1)

s1, s2 = 'ABCBDAB', 'BDCABA'
b, c = lcs_length(s1, s2)
print_lcs(b, s1, len(s1)-1, len(s2)-1)
```