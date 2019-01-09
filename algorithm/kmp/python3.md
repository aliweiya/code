```python
def get_next(s):
    _next = [0 for i in range(len(s))]
    _next[0] = -1

    i, j = 0, -1
    while i < len(s)-1:
        if j == -1 or s[i] == s[j]:
            i += 1
            j += 1
            _next[i] = j

        else:
            j = _next[j]

    return _next

def kmp(_str, _pattern):
    _next = get_next(_pattern)



print(kmp("ababababca", "abababca"))
```