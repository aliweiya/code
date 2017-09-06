import random

def MERGE(A,p,q,r):
    L=[]
    R=[]
    for i in range(p,q+1):
        L.append(A[i])
    for j in range(q+1,r+1):
        R.append(A[j])
    i=0
    j=0
    k=p
    while(i<len(L) and j<len(R)):
        if L[i]<=R[j]:
             A[k]=L[i]
             i=i+1
             k=k+1
        else:
             A[k]=R[j]
             j=j+1
             k=k+1
    while i<len(L):
        A[k]=L[i]
        i=i+1
        k=k+1
    while j<len(R):
        A[k]=R[j]
        j=j+1
        k=k+1

def MERGE_SORT(A,p,r):
    if p<r:
        q=int((p+r)/2)
        MERGE_SORT(A,p,q)
        MERGE_SORT(A,q+1,r)
        MERGE(A,p,q,r)

maximum = 100
num=0
A=[]
while num<maximum:
    i=random.randint(0,1000)
    A.append(i)
    num=num+1

print(A)
MERGE_SORT(A,0,maximum-1)
print(A)
