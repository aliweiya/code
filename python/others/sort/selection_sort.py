import random
def min(A,s):
    temp=s
    for i in range(s,len(A)):
        if A[temp]>=A[i]:
            temp=i
    return temp

def selection_sort(A):
    for i in range(0,len(A)):
        m=min(A,i)
        if(m!=i):
            temp=A[i]
            A[i]=A[m]
            A[m]=temp

maximum = 5
num = 0
A = []
while num<maximum:
    i=random.randint(0,1000)
    A.append(i)
    num=num+1

print(A)
selection_sort(A)
print(A)