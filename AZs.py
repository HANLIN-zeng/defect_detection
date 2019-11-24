# -*- coding: utf-8 -*-
import cv2
import numpy as np

img = cv2.imread("E://eraser.jpg",1)

kernel0 = np.ones((2,1),np.uint8)
kernel = np.ones((1,4),np.uint8)

img1 = cv2.GaussianBlur(img,(5,5),0)

opening_img = cv2.morphologyEx(img1, cv2.MORPH_OPEN, kernel)#待处理边缘

#cv2.imshow("img",img1)
canny_img = cv2.Canny(opening_img,50,150)

lines=cv2.HoughLinesP(canny_img, 1, np.pi/180,15,0,0)
#for i in range(len(lines)-1):
 #   for x1,y1,x2,y2 in lines[i]:
  #      cv2.line(img, (x1,y1), (x2,y2), (0,0,255), 2)

#缺陷检测
ret, thresh = cv2.threshold(canny_img, 127, 255,0)
contours,hierarchy = cv2.findContours(thresh,2,1)  
cnt = contours[0]  
hull = cv2.convexHull(cnt,returnPoints = False) 
defects = cv2.convexityDefects(cnt,hull)
for i in range(defects.shape[0]-1): 
    
    s,e,f,d = defects[i,0] 
    start = tuple(cnt[s][0]) 
    end = tuple(cnt[e][0]) 
    x1,y1 = cnt[s][0]
    x2,y2 = cnt[e][0]
    x3,y3 = cnt[s-1][0]
    x4,y4 = cnt[e-1][0]
    
    if (abs(x1-x3) <= 20 or abs(x2 - x4) <= 20):
        s = s + 1
        e = e + 1
    cv2.rectangle(img,((int)(x1+20),(int)(y1+20)),((int)(x2-20),(int)(y2-20)),(0,255,0),2)
    
    img_crop = img [(int)(y2-20) : (int)(y1+20),(int)(x2-20):(int)(x1+20)]#缺陷处放大    
    img_bigger = cv2.resize(img_crop, (0, 0), fx=3, fy=3, 
                              interpolation=cv2.INTER_NEAREST)


cv2.imshow("img_output",img)
#cv2.imshow('crop_img.jpg', img_crop)
cv2.imshow("img_bigger",img_bigger)

cv2.waitKey()
cv2.destroyAllWindows()