# -*- coding: utf-8 -*-
import cv2  
import numpy as np  
import matplotlib.pyplot as plt


#读取图像
img = cv2.imread('cap_union_new_getcapbysig_back.jpg')
print(img.shape)
# lenna_img = cv2.cvtColor(img,cv2.COLOR_BGR2RGB)

grayImage = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

#Prewitt算子
kernelx = np.array([[1,1,1],[0,0,0],[-1,-1,-1]],dtype=int)
kernely = np.array([[-1,0,1],[-1,0,1],[-1,0,1]],dtype=int)
x = cv2.filter2D(grayImage, cv2.CV_16S, kernelx)
y = cv2.filter2D(grayImage, cv2.CV_16S, kernely)
#转uint8
absX = cv2.convertScaleAbs(x)       
absY = cv2.convertScaleAbs(y)    
Prewitt = cv2.addWeighted(absX,0.5,absY,0.5,0)

edges = cv2.Canny(Prewitt, 50, 120)
minLineLength = 100
maxLineGap = 50
lines = cv2.HoughLinesP(edges, 1.0, np.pi/2, 90, minLineLength, maxLineGap)

horizontal = None
vertical = None
length = None
for line in lines:
    if line[0][0] == line[0][2]:
        vertical = line[0]
    else:
        horizontal = line[0]

length = horizontal[2] - horizontal[0]

left_up = (min(horizontal[0], horizontal[2]), min(vertical[1], vertical[3]))
bottom_right = (left_up[0] + length, left_up[1] + length)

print(left_up, bottom_right)

cv2.rectangle(img, left_up, bottom_right, (0,255,0), 2)

plt.imshow(img)
plt.show()