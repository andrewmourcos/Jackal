import cv2
import numpy as np
import math 

img = cv2.imread("piano4.jpg")
img = img[460:670, 0:1280]

gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

blur = cv2.GaussianBlur(gray,(5,5),0)

outerBox = cv2.adaptiveThreshold(blur, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 5, 2)
outerBox = cv2.bitwise_not(outerBox)

edges = cv2.Canny(outerBox,100,100)

kernel = cv2.getStructuringElement(cv2.MORPH_RECT,(5,5))

dilation = cv2.dilate(edges,kernel,iterations = 2)
erosion = cv2.erode(dilation, kernel, iterations=1)


_, contours, _ = cv2.findContours(dilation,cv2.RETR_LIST,cv2.CHAIN_APPROX_SIMPLE)
idx =0 
for cnt in contours:
    idx += 1
    x,y,w,h = cv2.boundingRect(cnt)
    area = cv2.contourArea(cnt)
    digit=edges[y:y+h,x:x+w]
    if (area > 3000 and area < 10000 and w < 200):
    	cv2.rectangle(img,(x,y),(x+w,y+h),(200,0,0),2)
    else:
    	pass


cv2.imshow("dude", img)
cv2.imshow("yeet", edges)
cv2.imshow("fam", erosion)

cv2.waitKey(0)
cv2.destroyAllWindows()