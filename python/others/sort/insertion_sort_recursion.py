import random

def insert(A,l):
    for i in range(0,l):
        if A[i]>=A[l]:
            A.insert(i,A[l])
            del A[l+1]

def insertion_sort_recursion(A,l):
    if l>0:
        insertion_sort_recursion(A,l-1)
        insert(A,l-1)

maximum = 100
A = []
num = 0
while num<maximum:
    i=random.randint(0,100)
    A.append(i)
    num=num+1

print(A)
insertion_sort_recursion(A,len(A))
print(A)
