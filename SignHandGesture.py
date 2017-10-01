import numpy
import sys
sys.path.append("/usr/local/lib/python2.7/site-packages")
import cv2
import thread
import os
from datetime import datetime

fist_cascade = cv2.CascadeClassifier("fist.xml")
cap = cv2.VideoCapture(0)

prevTime = None

talked = False

prevFist = False
prevValue = 1200129120


def talk(word):
	os.system("say \'" + str(word) + "\'")


# prevTime = 

os.system("say 'Camera capture has begun.'")

# def findLocalMax(values):

# 	# print "YVALUES", values, "length", len(values)

# 	length = len(values)
# 	tens = (length- (length % 5))/5

# 	sumPoints = []
# 	maxPoints = []

# 	for ten in range(1, tens):
# 		sumPoints.append(sum(values[((ten-1)* 2):ten * 2])/2)
# 	sumPoints.append(sum(values[tens*2:-1])/2)

# 	print sumPoints

# 	# for i in range(4, (len(sumPoints)-(len(sumPoints)%4)))/4:
# 	# 	if sumPoints[4i - 3] > sumPoints[i] and sumPoints[i + 4] > sumPoints[i]:
# 	# 		maxPoints.append(sumPoints[i])
# 	# print "MAXPOINTS ", maxPoints
# 	return maxPoints

def findLocalMax(values):

	directions = []
	changes = 0

	changedValues = []


	for k in range(0, len(values) -1):
		if k % 12 == 0: changedValues.append(values[k])

	for i in range(0, len(changedValues) - 2):
		if changedValues[i] - changedValues[i+1] < -3:
			directions.append(-1)
		elif changedValues[i] - changedValues[i+1] > 3:
			directions.append(1)
	for j in range(0, len(directions) -1):
		# if directions[j] == 1 and directions[j+1] == -1: changes += 1
		if directions[j] == -1 and directions[j + 1] == 1: changes += 1
	# print "DIRECTIONS:", directions
	return changes

def findRefindMax(values):
	
	directions = []
	changes = 0

	changedValues = []

	for k in range(0, len(values) -1):
		if k % 3 == 0: changedValues.append(values[k])

	for i in range(0, len(changedValues) - 2):
		if changedValues[i] - changedValues[i+1] < -3:
			directions.append(-1)
		elif changedValues[i] - changedValues[i+1] > 3:
			directions.append(1)

	if len(changedValues) < 2:
		return 0

	if len(directions) < 5:
		return 0

	changeSizes = []
	leng = 0
	print "LENGTH:", len(directions)
	for j in range(0, len(directions) -1):
		# print "index: ", j
		if directions[j] == 1:
			leng = 0
		elif directions[j] == -1:
			leng += 1
		
		if directions[j] == -1 and directions[j + 1] == 1:
			changeSizes.append(leng)
	print "DIRECTIONS:", directions
	
	if len(changeSizes) < 2:
		return 0

	averageLength = int(sum(changeSizes)/4/len(changeSizes))
	for change in changeSizes:
		if change < 3:#averageLength:
			changeSizes.remove(change)
	return len(changeSizes)


while True:

	_, frame = cap.read()

	gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
	blur = cv2.GaussianBlur(gray, (7, 7), 0)
	edges = cv2.Canny(gray, 90, 90)
	color = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

	lower_green = numpy.array([30, 170, 30])
	upper_green = numpy.array([90, 255, 120])

	blurEdges = cv2.GaussianBlur(edges, (7, 7), 0)

	_, threshold = cv2.threshold(blur, 200,255,cv2.THRESH_BINARY_INV+cv2.THRESH_OTSU)


	#FIND A WAY TO FIND THE GREEN BRACELETS
	mask = cv2.inRange(color, lower_green, upper_green)
	res = cv2.bitwise_and(frame, frame, mask=mask)

	#MAKE GREEN BRACELETS GRAY FOR CORNER DETECTION (TO GET POINTS FOR THE ROI)
	grayRes = cv2.cvtColor(res, cv2.COLOR_BGR2GRAY)
	_, thresholdedRes = cv2.threshold(grayRes, 40, 255, cv2.THRESH_BINARY_INV+cv2.THRESH_OTSU)


	# canFindHand = true


	#CORNER DETECTION

	

	# dst = cv2.cornerHarris(thresholdedRes, blockSize, ksize, k[, dst[, borderType]])
	corners = cv2.goodFeaturesToTrack(thresholdedRes, 20, 0.1, 10)

	if type(corners) == type(None):
		corners = []
	# print corners
	roiColor = None
	roiThreshold = None
	roiRange = []

	maxPoints = []
	minPoints = []

	if len(corners) != 0:
		corners = numpy.int0(corners)
		# Find the range of x values
		xValues = []

		biggestX = 0
		smallestX = 0

		#Find the average y value
		yValues = []
		averageY = 0

		for corner in corners:
			# print "I've got a corner?"
			# iterate through all the values
			x, y = corner.ravel()
			# print "x"
			# print x
			# print xValues
			xValues.append(x)
			# print xValues
			yValues.append(y)

		# print xValues
		averageY = int(sum(yValues)/len(yValues))
		xValues.sort()


		# print "YOLO"
		# print xValues

		biggestX = xValues[-1]
		smallestX = xValues[0]

		if smallestX - 100 <= 0:
			smallestX =1
		else: smallestX -= 100


		biggestY = int(averageY - (biggestX-smallestX) * 2.8)
		if biggestY < 0:
			biggestY = 1
			
		roiRange = [(smallestX, (biggestY)), ((biggestX + 200),  averageY)]

		#make ROI for processing
		# print roiRange
		# print smallestX
		# print biggestX + 200
		# print biggestY
		# print averageY

		roiColor = frame[(biggestY):averageY, smallestX: (biggestX + 200)]
		roiThreshold = threshold[(biggestY):averageY, smallestX: (biggestX + 200)]
		cv2.rectangle(frame, roiRange[0], roiRange[1], (255, 100, 100), 4)
		cv2.circle(frame, roiRange[0], 20, (0, 0, 255), 1)
		cv2.circle(frame, roiRange[1], 20, (0, 0, 255), 1)

	max_area = 0
	ci = 0
	count = []
	maxPoints = []
	refinedMax = []

	if type(roiThreshold) != type(None):
		_, contours, _= cv2.findContours(roiThreshold, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
		cv2.imwrite("roiThreshold.png", roiColor)
		# print "roiColor:",roiColor.shape
		# print "roiThresh",roiThreshold.shape
		# print "roiRange (" + str(roiRange[1][0] - roiRange[0][0]) + ", " + str(roiRange[1][1] - roiRange[0][1]) + ")"
		# print contours
		xvalues = []
		yvalues = []
		for i in range(len(contours)):
			cont = contours[i]
			area = cv2.contourArea(cont)
			if area > max_area:
				max_area = area
				ci = i
			count = contours[ci]
			xvalues.append(count[0][0][0])
			# yvalues.append(count[0][0][1])
			# print count[0][0]
			# print len(count[0])
			for point in count:
				yvalues.append(point[0][1])
			# print yvalues
		maxPoints = findLocalMax(yvalues)
		refinedMax = findRefindMax(yvalues)



	# print count
	# break

	# _, contours, _= cv2.findContours(threshold, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

	# # print contours

	# count1 = []
	# ci = 0
	# ci = max_area
		
	# for i in range(len(contours)):
	# 	cont = contours[i]
	# 	area = cv2.contourArea(cont)
	# 	if area > max_area:
	# 		max_area = area
	# 		ci = i
	# 	count1 = contours[ci]

	#edit threshold to fit current background

	# drawing = numpy.zeros(frame.shape,numpy.uint8)
	# cv2.drawContours(blur,[count],0,(10,255,10),2)
	# cv2.drawContours(blur,[hull],0,(0,0,255),2)

	output = ""

	# fingerValue = (refinedMax)
	# if fingerValue == prevValue:
	# 	output = str(fingerValue) + " fingers"

	# prevValue = fingerValue
	fingerValue = (refinedMax)
	if fingerValue == prevValue and type(fingerValue) != type(None):
		output = str(fingerValue) + " fingers"
		if type(prevTime) == type(None):
			prevTime == datetime.now()
		elif (datetime.now() - prevTime).seconds >= 2 and not talked:
			thread.start_new_thread(talk, tuple([fingerValue]))
			talked = True
			print "called talk"
		elif (datetime.now() - prevTime).seconds >= 2 and talked:
			prevTime = datetime.now()
	else:
		talked = False
		output = ""
		prevTime = datetime.now()

	prevValue = fingerValue


	font = cv2.FONT_HERSHEY_SIMPLEX
	cv2.putText(frame, output, (40, 650), font, 4, (0, 0, 245), 2, cv2.LINE_AA)

	if len(count) != 0:
		hull = cv2.convexHull(count)
		# print "PRINTING"
		# print count
		print "MaxPoints:", (refinedMax)
		# print yvalues
		# for maxPoint in maxPoints:
		# 	cv2.circle(frame, (100, maxPoint), 20, (0, 0, 255), 1)
		cv2.polylines(roiColor, [count], 2, (0, 255, 0), 2)
		# cv2.polylines(frame, [count], 2, (0, 255, 0), 2)
		# pts = numpy.array([[200, 80], [900, 1000], [700, 80], [819, 172], [329, 622]], numpy.int32)
		# cv2.polylines(frame, [count], False, (0, 255, 0), 2)
		# print int(roiRange[0][0])
		# print roiColor.shape
		frame[roiRange[0][1]:roiRange[0][1]+roiColor.shape[0], roiRange[0][0]:roiRange[0][0]+roiColor.shape[1]] = roiColor

	
	# cv2.imshow("hsv", thresholdedRes)
	cv2.imshow("blur", blurEdges)
	# cv2.imshow("threshold", threshold)
	cv2.imshow("color", frame)
	# cv2.imshow("blur", blur)

	# cv2.imshow("blurEdges", blurEdges)
	k = cv2.waitKey(1) & 0xFF
	if k == ord('q'):
		break


cap.release()
cv2.destroyAllWindows()

