#This file contains code that generates the accuracy charts for the binary model.

import sqlite3
from sklearn import ensemble
import random
import matplotlib.pyplot as plt
import math
import makeTestData


import search

#Specify the number of stores removed from each target in the test set here. The number should be anywhere from 1-3. 
numRemoved=1

conn = sqlite3.connect('../../../database.db')
c = conn.cursor()

c.execute("SELECT type FROM StoreTypes")
oldcats=c.fetchall()
cats=list(map((lambda x: x[0]), oldcats))


c = conn.cursor()

c.execute("SELECT type FROM StoreTypes")
oldcats=c.fetchall()
cats=list(map((lambda x: x[0]), oldcats))



c.execute("SELECT * FROM fullDataGrid")
data=c.fetchall()
for i in range(len(data)):
    data[i]=list(data[i])[1:len(data)]

conn.close()


for x in range(len(data)):
    for y in range(len(data[0])):
        if data[x][y]>0:
            data[x][y]=1

modelDataXTrain=[]
modelDataYTrain=[]
for x in range(len(data[:500])):
    for y in range(len(data[0])):
        if data[x][y]>0:
            tempX=data[x][:]
            tempX[y]+=-1
            tempY=y
            modelDataXTrain.append(tempX)
            modelDataYTrain.append(tempY)






def score(dX,dY,k):
    def storesPicked(dXpart):
        probs=model.predict_proba([dXpart])
        newprobs = []
        for x in range(len(probs[0])):
            newprobs.append([x, probs[0][x]])

        newprobs.sort(key=lambda x: x[1], reverse=True)
        finalprobs = []
        not0 = False
        ind = 0
        for ind in range(len(newprobs)):
            if newprobs[ind][1] > 0.000000000000001:
                finalprobs.append(newprobs[ind])

            else:
                break

        mallswithin=[]
        for x in finalprobs:
            mallswithin.append(x[0])

        return mallswithin

    predictions=[]
    for x in range(len(dX)):
        predictions.append(storesPicked(dX[x]))


    right=0.0
    total=0.0
    for a in range(len(dY)):
        for b in range(len(dY[a])):
            if dY[a][b] in predictions[a][:k]:
                right+=1.0
                break
        total+=1.0

    return float(right)/float(total)








model=ensemble.RandomForestClassifier(n_estimators=20, max_features='auto', max_depth=20, random_state=3)

model.fit(modelDataXTrain,modelDataYTrain)


#The numRemoved variable below is the number of stores removed from the target category in the test data
testDataX,testDataY=makeTestData.makeTestData(data[500:],numRemoved)


scores=[]
for k in range(1,6):
    scores.append(score(testDataX, testDataY,k))





rects=plt.bar(range(0,5),scores)
plt.xticks([x+0.4 for x in range(0,5)],
        range(1,6),
           size='medium',
           rotation=0,
           # rotation='vertical',
           )

def autolabel(rects):
    for r in range(len(rects)):
        rect=rects[r]
        height = rect.get_height()
        plt.text(rect.get_x() + rect.get_width()/2., 1.01*height,
                str(round(scores[r],4)),
                ha='center', va='bottom')

autolabel(rects)
plt.yticks(size='medium')
plt.xlabel('Number of Stores In The Top K Considered Correct')
plt.ylabel('Accuracy')
plt.text(1.75,.99,"Binary Model Accuracy")
plt.ylim(0,1.025)
plt.tight_layout(pad=0.8, w_pad=0.8, h_pad=1.0)
plt.savefig('binaryAccuracy'+str(numRemoved)+'Removed.pdf')
plt.close()

