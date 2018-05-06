import numpy as np
import cv2

video = cv2.VideoCapture("piano.mov")

while(True):
	ret, frame = video.read()

	gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

	# get bitwise image
	ret, thresh = cv2.threshold(gray, 110, 255, 0)

	# bitwise = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 3, 4)
	bitwise = cv2.bitwise_not(thresh)

	# get white keys
	hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

	# lower_black = np.array([0,0,0])
	# upper_black = np.array([255,100,100])

	lower_white = np.array([0, 10, 130])
	upper_white = np.array([170, 110, 255])

	mask = cv2.inRange(hsv, lower_white, upper_white)
	res = cv2.bitwise_and(frame,frame, mask= mask)

	cv2.imshow("yeet", bitwise)

	if cv2.waitKey(30) & 0xFF == ord('q'):
		break

cap.release()
cv2.destroyAllWindows()