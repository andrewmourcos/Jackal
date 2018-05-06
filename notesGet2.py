import cv2
import numpy as np

video = cv2.VideoCapture(1)

while(True):
	ret, frame = video.read()
	frame = frame[80:220, 0:1000]

	gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

	blur = cv2.GaussianBlur(gray,(5,5),0)

	outerBox = cv2.adaptiveThreshold(blur, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 5, 2)
	outerBox = cv2.bitwise_not(outerBox)

	edges = cv2.Canny(outerBox,100,100)

	kernel = cv2.getStructuringElement(cv2.MORPH_RECT,(5,5))

	dilation = cv2.dilate(edges,kernel,iterations = 2)

	key = []
	_, contours, _ = cv2.findContours(dilation,cv2.RETR_LIST,cv2.CHAIN_APPROX_SIMPLE)
	for cnt in contours:
		x,y,w,h = cv2.boundingRect(cnt)
		area = cv2.contourArea(cnt)
		digit=edges[y:y+h,x:x+w]
		if (area > 3000 and area < 14000):
			cv2.rectangle(frame,(x,y),(x+w,y+h),(200,0,0),2)
			key.append([x,y,w,h])
		else:
			pass

	key.sort(key=lambda x: x[0])
	num = 0
	letters = ["a", "b", "c", "d", "e", "f", "g", "a", "b", "c"]

	# labels
	for box in key:
		font = cv2.FONT_HERSHEY_SIMPLEX
		cv2.putText(frame, letters[num],(box[0],box[1]), font, 1,(0,0,255),2,cv2.LINE_AA)
		num += 1

	cv2.imshow("dude", frame)
	cv2.imshow("yeet", edges)
	cv2.imshow("fam", dilation)

	if cv2.waitKey(30) & 0xFF == ord('q'):
		break

cap.release()
cv2.destroyAllWindows()