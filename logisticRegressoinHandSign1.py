import numpy as np

fileSource = "positivePoints.txt"
X=[]
Y=[]

lines = list(open(fileSource, 'r'))
learningRate =0.005
hands =[]
for line in lines:
    #line = "yy:yy:yy:yy"
    pointsStringTogether = line.split(":")
    pointsString = []
    hand = []
    for point in pointsStringTogether:
        hand.append(int(point))

fileSource = "negativePoints.txt"

lines = list(open(fileSource, 'r'))
negativeHands =[]
for line in lines:
    #line = "yy:yy:yy:yy"
    pointsStringTogether = line.split(":")
    pointsString = []
    hand = []
    for point in pointsStringTogether:
        negativeHands.append(int(point))

Y = [1] * len(hands) + [0] * len(negativeHands)

max_length = 0

lengthsInit = hands + negativeHands
lengths = []

for length in lengthsInit:
    lengths.append(len(length))

for hand in hands:
    x = [0] * (max_length + 1)
    x[0] = 1
    for i in range(0, len(hand) - 1):
        x[i+1] = hand[i]
    X.append(x)


#
#Everything to do with Logistic Regression
#


def cost():
    global Y
    c = 0
    h = hypothesis()
    
    for (x, y), value in np.ndenumerate(h):
        if Y[0, y] == 0:
            if value != 1:
                c -= (1 - Y[0, y]) * math.log(1 - value)
            elif value == 1:
                c += 1000000000000000
        else:
            if value != 0:
                c -= Y[0, y] * math.log(value)
            elif value == 1:
                c += 1000000000000000
    return c

def hypothesis():
    global X, parameters
    px = parameters.T * X.T
    for (x, y), value in np.ndenumerate(px):
        px[x, y] = 1/(1 + math.e ** (-value))

    return px

def descend():
    global Y, parameters, learningRate
    m = float(Y.shape[0])
    gradient = learningRate * 1.0 / m * summation()
    parameters = parameters - gradient.T

def summation():
    global Y, X
    h = hypothesis().T
    sumValue = []
    for y in xrange(0, X.shape[1]):
        s = 0
        for (x1, y1), value in np.ndenumerate(h):
            s += (value - Y[0, x1]) * X[x1, y]
        sumValue.append(s)
    sumValue = np.matrix(sumValue, dtype=float)
    return sumValue

def main():
    global Y, X, learningRate
    Y = np.matrix(Y, dtype = float)
    X = np.matrix(X, dtype = float)
    count = 0
    c = 10000000000000
    prevCost = 1000000
    initialCost = None
    while True:
        prevCost = c
        c = cost()
        if initialCost == None:
            initialCost = c
        if prevCost < c and prevCost != None and initialCost != None:
            # print "ERROR1"
            learningRate *= 0.95
            count = 0
            c = 10000000000000
            prevCost = 1000000
            initialCost = None
        elif prevCost == cost:
            print "Finished on Convergence"
            break
        elif prevCost <= .05 * initialCost:
            break
        descend()
        count += 1
        if count % 10000 == 0:
            print c
        if count % 1000000 == 0:
            print "Parameters:\n\n" + str(parameters) + "\n\n"
    print parameters
    print "Number of iterations: " + str(count)
    os.system('say "Task completed"')

if __name__ == "__main__":
    main()


