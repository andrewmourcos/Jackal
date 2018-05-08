import cv2
import numpy as np
import os
import time

video = cv2.VideoCapture("Media/piano5.mov")
notes=[]
while(True):
	ret, frame = video.read()
	if not ret:
		break
	frame = frame[80:220, 0:1000]

	gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

	blur = cv2.GaussianBlur(gray,(5,5),0)

	outerBox = cv2.adaptiveThreshold(blur, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 5, 2)
	outerBox = cv2.bitwise_not(outerBox)

	edges = cv2.Canny(outerBox,100,100)

	kernel = cv2.getStructuringElement(cv2.MORPH_RECT,(5,5))

	dilation = cv2.dilate(edges, kernel, iterations = 2)

	key = []
	_, contours, _ = cv2.findContours(dilation,cv2.RETR_LIST,cv2.CHAIN_APPROX_SIMPLE)
	for cnt in contours:
		x,y,w,h = cv2.boundingRect(cnt)
		area = cv2.contourArea(cnt)
		digit=edges[y:y+h,x:x+w]
		# if (area > 3000 and area < 14000):
		if(area > 1000 and area < 5000):
			cv2.rectangle(frame,(x,y),(x+w,y+h),(200,0,0),2)
			key.append([x,y,w,h])
		else:
			pass

	key.sort(key=lambda x: x[0])
	num = 0
	letters = ["a", "b", "c", "d", "e", "f", "g", "a'", "b'", "c'", "d'", "e'", "f'", "g'","a'", "b'", "c'", "d'", "e'", "f'", "g'"]

	# labels
	label = []
	for box in key:
		font = cv2.FONT_HERSHEY_SIMPLEX
		cv2.putText(frame, letters[num],(box[0],box[1]), font, 1,(0,0,255),2,cv2.LINE_AA)
		label.append([letters[num],box[0],box[1]])
		num += 1

	lastvalue = 0
	for l in label:
		diff = abs(l[1] - lastvalue)
		if diff > 130:
			notes.append(l[0])
			cv2.putText(frame, l[0],(450,100), font, 4,(255,0,0),5,cv2.LINE_AA)
		lastvalue = l[1]

	cv2.imshow("dude", frame)



	if cv2.waitKey(30) & 0xFF == ord('q'):
		break

notes = notes[0::8]
file = open('lily.ly', 'w')

file.write('\\version "2.18.2" \n \language "english" \n \\relative{\n \clef "treble_8"')

for i in notes:
	file.write(i)
	file.write("\n")
file.write("}")
file.close()
os.system("lilypond lily.ly")
os.system("open lily.pdf")

cap.release()
cv2.destroyAllWindows()