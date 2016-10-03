import sqlite3
from sklearn import ensemble
import random
import matplotlib.pyplot as plt
import math
from sklearn.externals import joblib
import search


conn = sqlite3.connect('../../database.db')

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


storeNums=[]
for x in range(len(data[0])):
    storeNums.append(0)

for x in range(len(data)):
    for y in range(len(data[0])):
        storeNums[y]+=data[x][y]

totalStores=sum(storeNums)


modelDataX1=[]
modelDataY1=[]
for x in range(len(storeNums)):
    if storeNums[x]>0:
        tempX=storeNums
        tempX[x]+=-1
        tempY=x
        modelDataX1.append(tempX)
        modelDataY1.append(tempY)


for x in range(len(modelDataX1)):
    for y in range(len(modelDataX1[0])):
        modelDataX1[x][y]=float(modelDataX1[x][y])/float(sum(modelDataX1[x]))



modelDataXTest=[]
modelDataYTest=[]
for x in range(len(data)):
    for y in range(len(data[0])):
        if data[x][y]>0:
            tempX=data[x][:]
            tempX[y]+=-1
            tempY=y
            modelDataXTest.append(tempX)
            modelDataYTest.append(tempY)

for x in range(len(modelDataXTest)):
    for y in range(len(modelDataXTest[0])):
        modelDataXTest[x][y]=float(modelDataXTest[x][y])/float(sum(modelDataXTest[x]))






#correctCats is based on store frequencies
correctCats=[0,2,5,1,4]

def realScore(dX,dY,k):
    right=0
    total=0
    for y in dY:
        if y in correctCats[:(k+1)]:
            right+=1
        
        total+=1

    return float(right)/float(total)




scores=[]
for k in range(5):
   scores.append(realScore(modelDataXTest,modelDataYTest,k))


  
rects=plt.bar(range(5),scores, color='red')

def autolabel(rects):
    for r in range(len(rects)):
        rect=rects[r]
        height = rect.get_height()
        plt.text(rect.get_x() + rect.get_width()/2., 1.05*height,
                str(round(scores[r],4)),
                ha='center', va='bottom')

autolabel(rects)


plt.ylim(0,1)

plt.xticks([x+0.4 for x in range(0,5)],
        range(1,6),
           size='small',
           rotation=0,
           # rotation='vertical',
           )

plt.xlabel('Number of Stores In The Top K Considered Correct')
plt.ylabel('Accuracy')


plt.text(.65,.90,"Base Line Model where if we remove a store and then predict the")
plt.text(.8,.85,"store type based on store frequencies, the probability that")
plt.text(.8,.80,"we predict the correct store type is shown below. It is low.")




plt.tight_layout(pad=0.8, w_pad=0.8, h_pad=1.0)
plt.savefig('frequencies.pdf')
plt.close()
