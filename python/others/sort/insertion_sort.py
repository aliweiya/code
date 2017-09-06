import random

def insertion_sort(list_i):
    j=0
    for i in range(1,maximum):
        while j<i:
            if list_i[i]<=list_i[j]:
                list_i.insert(j,list_i[i])
                del list_i[i+1]
            else:
                j=j+1
        j=0

maximum=10
list_i=[]
num=0
while num<maximum:
    i=random.randint(0,7)
    list_i.append(i)
    num=num+1
    
print(list_i)
insertion_sort(list_i)
print(list_i)
