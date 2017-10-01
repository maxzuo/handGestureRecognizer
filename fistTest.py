import numpy
import sys
sys.path.append("/usr/local/lib/python2.7/site-packages")
import cv2
import os
import thread

fist_cascade = cv2.CascadeClassifier("fist.xml")
cap = cv2.VideoCapture(0)

fourcc = cv2.VideoWriter_fourcc(*'XVID')

out = cv2.VideoWriter("fistTest.mov", fourcc, 20.0, (640, 480))

prevFist = False
talked = False

os.system("say 'Camera capture has begun.'")

def talk():
	os.system("say 'Fist'")

while True:

	_, frame = cap.read()

	gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

	fists = fist_cascade.detectMultiScale(gray, 1.3, 5)
	if type(fists) == type(None):
		fists = []
	fist = False
	if len(fists) > 0 and prevFist == True:
		fist = True
		if not talked:
			talked = True
			thread.start_new_thread(talk, ())
			# os.system("say 'Fist in frame'")
	elif len(fists) > 0 and prevFist == False:
		prevFist = True
	else:
		prevFist = False
		talked = False

	font = cv2.FONT_HERSHEY_SIMPLEX
	cv2.putText(frame, "Fist? " + str(fist), (40, 200), font, 4, (0, 0, 245), 15, cv2.LINE_AA)

	cv2.imshow("color", frame)

	k = cv2.waitKey(1) & 0xFF
	if k == ord('q'):
		break


cap.release()
cv2.destroyAllWindows()

