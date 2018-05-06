import cv2
import numpy as np

video = cv2.VideoCapture("piano.mov")

while(True):
	ret, frame = video.read()
	frame = frame[0:300,0:620]

	gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

	ret, thresh = cv2.threshold(gray, 110, 255, 0)

	# get bounding boxes
	_, contours, _ = cv2.findContours(thresh,cv2.RETR_LIST,cv2.CHAIN_APPROX_SIMPLE)
	idx =0 
	for cnt in contours:
		area = cv2.contourArea(cnt)
		if(area > 300 and area < 10000):
			idx += 1
			x,y,w,h = cv2.boundingRect(cnt)
			digit=thresh[y:y+h,x:x+w]
			cv2.rectangle(frame,(x,y),(x+w,y+h),(200,0,0),2)
		else:
			pass

	cv2.imshow("yeet", frame)

	if cv2.waitKey(30) & 0xFF == ord('q'):
		break

cap.release()
cv2.destroyAllWindows()