import numpy as np
import sys
sys.path.append("/usr/local/lib/python2.7/site-packages")
import cv2

cap = cv2.VideoCapture(0)
POINTS = []

ROI = []


while True:
	_, img = cap.read()

	cv2.rectangle(img, (0,0), (410, 410), 3)

	cv2.imshow("Original", img)

	k = cv2.waitKey(1) & 0xFF
	if k == ord('a'):
		
		roi = img[0:400, 0:400]
		ROI.append(roi)
	elif k == ord('q'):
		break

for roi in ROI:
	gray = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)
	blur = cv2.GaussianBlur(gray, (7, 7), 0)
	_, threshold = cv2.threshold(blur, 200,255,cv2.THRESH_BINARY_INV+cv2.THRESH_OTSU)

	_, contours, _ = cv2.findContours(threshold, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

	max_area = 0
	ci = 0
	count = []

	points = []
	
	for i in range(len(contours)):
		cont = contours[i]
		area = cv2.contourArea(cont)
		if area > max_area:
			max_area = area
			ci = i
		count = contours[ci]
	for point in count:
		points.append(point[0][0])
	POINTS.append(points)

cap.release()
cv2.destroyAllWindows()

filename = "positivePoints.txt" #"negativePoints.txt"

with open(filename, 'w') as f:
	for points in POINTS:
		line = ""
		for i in range(0, len(points) -1):
			line += str(points[1])
			if i != len(points) - 1:
				line += ":"
		f.write(line)

