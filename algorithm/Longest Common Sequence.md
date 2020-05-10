如果要暴力搜索解决LCS问题，就要穷举X的所有子序列，堆每个子序列检查它是否也是Y的子序列，记录找到的最长子序列。时间复杂度为`$O(2^n)$`


LCS的最优子结构：令`$X=\langle x_1,x_2,\cdots,x_m\rangle$`和`$Y=\langle y_1,y_2,\cdots,y_n\rangle$`为两个序列，`$Z=\langle z_1,z_2,\cdots,z_k\rangle$`为X和Y的任意LCS
- 若`$x_m=y_n$`，则`$z_k=x_m=y_n$`，且`$Z_{k-1}$`是`$X_{m-1}$`和`$Y_{n-1}$`的一个LCS
- 若`$x_m\ne y_n$`，那么
  - `$z_k\ne x_m$`意味着`$Z$`是`$X_{m-1}$`和`$Y$`的一个LCS
  - `$z_k\ne y_n$`意味着`$Z$`是`$X$`和`$Y_{n-1}$`的一个LCS


我们定义`$c[i, j]$`表示`$X_i$`和`$Y_i$`的LCS的长度。如果`$i=1$`或`$j=0$`，即一个序列长度为0，那么LCS的长度为0。则

```math
c[i,j]=\begin{cases}
0,&i=0或j=0\\
c[i-1, j-1] + 1,&i,j>0且x_i=y_i\\
max(c[i, j-1], c[i-1, j]),&i,j>0且x_i\ne y_i
\end{cases}
```

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