#This file contains code that generates the accuracy charts for the cardinal model.
import sqlite3
import math
from sklearn import ensemble
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

import makeTestData

import search

#Here you should specify the number of stores removed in the creation of the test data. Make the number between 1 and 3.
storesRemoved=1


conn = sqlite3.connect('../../../database.db')

c = conn.cursor()

c.execute("SELECT type FROM StoreTypes")
oldcats=c.fetchall()
cats=list(map((lambda x: x[0]), oldcats))



c.execute("SELECT * FROM fullDataGrid")
data=c.fetchall()
for i in range(len(data)):
    data[i]=list(data[i])[1:len(data)]



conn.close()
scalar=.8


trainDataX=[]
trainDataY=[]
for x in range(len(data[:500])):
    for y in range(len(data[0])):
        if data[x][y]>0:
            tempX=data[x][:]
            tempX[y]+=-1.0
            if tempX[y]<0:
                tempX[y]=0
            tempY=y
            trainDataX.append(tempX)
            trainDataY.append(tempY)




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

model.fit(trainDataX,trainDataY)
superscores=[]
for a in range(1,7):
    testDataX,testDataY=makeTestData.makeTestData(data[500:],storesRemoved,a)    
    scores=[]
    for k in range(1,6):
        scores.append(score(testDataX, testDataY,k))
    

    superscores.append(scores)




width=.9/6.0

  
rects1=plt.bar(range(5),superscores[0], width, color='red')
rects2=plt.bar([x+width for x in range(5)],superscores[1], width, color='white')
rects3=plt.bar([x+2*width for x in range(5)],superscores[2], width, color='blue')
rects4=plt.bar([x+3*width for x in range(5)],superscores[3], width, color='black')
rects5=plt.bar([x+4*width for x in range(5)],superscores[4], width, color='green')
rects6=plt.bar([x+5*width for x in range(5)],superscores[5], width, color='cyan')



plt.ylim(0,1.03)

plt.xticks([x+0.5 for x in range(0,5)],
        range(1,6),
           size='small',
           rotation=0,
           # rotation='vertical',
           )

plt.xlabel('Number of Stores In The Top K Considered Correct')
plt.ylabel('Accuracy')


red_patch = mpatches.Patch(facecolor='red', edgecolor='black', hatch='', lw=1,label="Predicting Categories That Need 1 Store")
white_patch = mpatches.Patch(facecolor='white', edgecolor='black', hatch='', lw=1,label="Predicting Categories That Need 2 Stores")
blue_patch = mpatches.Patch(facecolor='blue', edgecolor='black', hatch='', lw=1, label="Predicting Categories That Need 3 Stores")
black_patch = mpatches.Patch(facecolor='black', edgecolor='black', hatch='', lw=1,label="Predicting Categories That Need 4 Stores")
green_patch = mpatches.Patch(facecolor='green', edgecolor='black', hatch='', lw=1,label="Predicting Categories That Need 5 Stores")
cyan_patch = mpatches.Patch(facecolor='cyan', edgecolor='black', hatch='', lw=1,label="Predicting Categories That Need 6 Stores",)

plt.legend(handles=[red_patch, white_patch, blue_patch, black_patch,green_patch,cyan_patch],loc=2,fontsize=10)


def autolabel(rects,j):
    # attach some text labels
    for r in range(len(rects)):
        rect=rects[r]
        height = rect.get_height()
        plt.text(rect.get_x() + rect.get_width()/2, 1.03*height,
                str(round(superscores[j-1][r],2))[1:],
                ha='center', va='bottom', fontsize=6)

autolabel(rects1,1)
autolabel(rects2,2)
autolabel(rects3,3)
autolabel(rects4,4)
autolabel(rects5,5)
autolabel(rects6,6)




plt.tight_layout(pad=0.8, w_pad=0.8, h_pad=1.0)
plt.savefig('cardinalAccuracy'+str(storesRemoved)+'StoresRemoved.pdf')
plt.close()

