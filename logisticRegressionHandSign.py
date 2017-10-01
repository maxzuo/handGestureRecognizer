import numpy

fileSource = "positivePoints.txt"
X=[]
X1 = []

lines = list(open(fileSource, 'r'))
hands =[]
for line in lines:
    #line = "(xx,yy):(xx,yy):(xx,yy)"
    pointsStringTogether = line.split(":")
    #pointsStringTogether = ["(xx,yy)", "(xx,yy)", "(xx,yy)", ]
    pointsString = []
    hand = []
    for point in pointsStringTogether:
        pointsString.append((point[1:-1]).split(","))
    for point in pointsString:
        pointNum = []
        for xy in point:
            pointNum.append(int(xy))
        hand.append(pointNum)
    hands.append(hand)

fileSource = "negativePoints.txt"

lines = list(open(fileSource, 'r'))
negativeHands =[]
for line in lines:
    #line = "(xx,yy):(xx,yy):(xx,yy)"
    pointsStringTogether = line.split(":")
    #pointsStringTogether = ["(xx,yy)", "(xx,yy)", "(xx,yy)", ]
    pointsString = []
    hand = []
    for point in pointsStringTogether:
        pointsString.append((point[1:-1]).split(","))
    for point in pointsString:
        pointNum = []
        for xy in point:
            pointNum.append(int(xy))
        hand.append(pointNum)
    negativeHands.append(hand)

 for hand in hands:
 	xCoor = []
 	for point in hand:
 		xCoor.append(point[0])
