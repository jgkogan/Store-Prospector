#This file contains functions that help generate test data
import random
import itertools

def makeTestData(testData,k,storesToSubtract):
	testDataX=[]
	testDataY=[]
	tempX=[]
	tempY=[]
	for mall in testData:
		tempX,tempY=convertAMall(k,mall,storesToSubtract)
		testDataX.append(tempX)
		testDataY.append(tempY)

	testDataX=list(itertools.chain.from_iterable(testDataX))
	testDataY=list(itertools.chain.from_iterable(testDataY))

	return testDataX,testDataY
		

def convertAMall(k,mall,storesToSubtract):
	tempX=[]
	tempY=[]
	newMallsX=[]
	newMallsY=[]
	possibleCats=[]
	for x in range(len(mall)):
		if mall[x]>0:
			possibleCats.append(x)

	combos=list(itertools.combinations(possibleCats, k))
	rcombos= sorted(combos, key=lambda k: random.random())[:100]
	realcombos = [list(elem) for elem in rcombos]
	
	for y in range(len(realcombos)):

		tempX=mall[:]
		for part in realcombos[y]:	
			tempX[part]+=-storesToSubtract
			if tempX[part]<0:
				tempX[part]=0

		newMallsX.append(tempX)
		newMallsY.append(realcombos[y])
		realMallsX=newMallsX
		

	return newMallsX,newMallsY