#This file contains functions that help generate test data
import random
import itertools

def makeTestData(testData,k):
	testDataX=[]
	testDataY=[]
	tempX=[]
	tempY=[]
	for mall in testData:
		tempX,tempY=convertAMall(k,mall)
		testDataX.append(tempX)
		testDataY.append(tempY)

	testDataX=list(itertools.chain.from_iterable(testDataX))
	testDataY=list(itertools.chain.from_iterable(testDataY))

	return testDataX,testDataY
		

def convertAMall(k,mall):
	tempX=[]
	tempY=[]
	newMallsX=[]
	newMallsY=[]
	possibleCats=[]
	for x in range(len(mall)):
		if mall[x]==1:
			possibleCats.append(x)

	combos=list(itertools.combinations(possibleCats, k))
	rcombos= sorted(combos, key=lambda k: random.random())[:100]
	realcombos = [list(elem) for elem in rcombos]
	ex=0
	for y in range(len(realcombos)):

		tempX=mall[:]
		for part in realcombos[y]:	
			tempX[part]+=-1

		newMallsX.append(tempX)
		newMallsY.append(realcombos[y])
		realMallsX=newMallsX
		

	return newMallsX,newMallsY