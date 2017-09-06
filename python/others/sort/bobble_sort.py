import random

def BOBBLE_SORT(A):
    for i in range(0,len(A)):
        for j in range(i+1,len(A)):
            if A[j]<=A[i]:
                A[i], A[j] = A[j], A[i]


A=[]
maximum = 100
num=0
while num<maximum:
    i=random.randint(0,1000)
    A.append(i)
    num=num+1

print(A)
BOBBLE_SORT(A)
print(A)
