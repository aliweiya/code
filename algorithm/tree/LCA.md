Lowest Common Ancestor

```python
class BiTree(object):
    def __init__(self):
        self.data = None
        self.left = None
        self.right = None


def generate_tree(l, index=0):
    """generate a binary tree using a list
    Params:
        l: list of data
        index: current element

    [1, 2, 3, 4] to    1
                      / \
                     2   3
                    /
                   4

    [1, -1, 2, -1, -1, 3, 4] to    1
                                    \
                                     2
                                    / \
                                   3   4
    """
    if index >= len(l):
        return None
    if l[index] == -1:
        return None

    T = BiTree()
    T.data = l[index]
    T.left = generate_tree(l, 2*index+1)
    T.right = generate_tree(l, 2*index+2)

    return T


def pre_order(T):
    if T is None:
        return

    print(T.data)
    pre_order(T.left)
    pre_order(T.right)

def InOrder(T):
    if T is None:
        return

    InOrder(T.left)
    print(T.data)
    InOrder(T.right)


def lowest_common_ancestor(T, n1, n2):
    if T == None or T.data == n1 or T.data == n2:
        return T
    left = lowest_common_ancestor(T.left, n1, n2)
    right = lowest_common_ancestor(T.right, n1, n2)

    if left != None and right != None:
        return T

    return right if left is None else left


if __name__ == '__main__':
    l = [1, 2, 3, 4]
    T = generate_tree(l)
    # pre_order(T)
    # print()
    # InOrder(T)
    print(lowest_common_ancestor(T, 4, 3).data)
```