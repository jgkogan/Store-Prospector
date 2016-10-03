#This file generates the total successes and trials for all of the cardinal models. These are then used in the Mathematica pvalue analysis.

import sqlite3
import math
from sklearn import ensemble




import search
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

modelDataX1=[]
modelDataY1=[]
for x in range(len(data)):
    for y in range(len(data[0])):
        if data[x][y]>0:
            tempX=data[x][:]
            tempX[y]+=-1.0
            
            tempX.append(x)
            
            tempY=[y,x]
            modelDataX1.append(tempX)
            modelDataY1.append(tempY)

#for x in range(len(modelDataX1)):
#    for y in range(len(modelDataX1[0])):
#        modelDataX1[x][y]=modelDataX1[x][y]**scalar


modelDataX1Train=[]
modelDataY1Train=[]
modelDataY1Test=[]
modelDataX1Test=[]
for x in modelDataX1:
    if x[len(x)-1]>500:
        modelDataX1Test.append(x[:len(x)-1])
    else:
        modelDataX1Train.append(x[:len(x)-1])

for x in modelDataY1:
    if x[1]>500:
        modelDataY1Test.append(x[0])
    else:
        modelDataY1Train.append(x[0])



modelDataX2=[]
modelDataY2=[]
for x in range(len(data)):
    for y in range(len(data[0])):
        if data[x][y]>0:
            tempX=data[x][:]
            tempX[y]+=-2.0
            if tempX[y]<0:
                tempX[y]=0
            
            tempX.append(x)
            tempY=[y,x]
            
            modelDataX2.append(tempX)
            modelDataY2.append(tempY)


modelDataY2Test=[]
modelDataX2Test=[]
for x in modelDataX2:
    if x[len(x)-1]>500:
        modelDataX2Test.append(x[:len(x)-1])
    

for x in modelDataY2:
    if x[1]>500:
        modelDataY2Test.append(x[0])
  




modelDataX3=[] 
modelDataY3=[]
for x in range(len(data)):
    for y in range(len(data[0])):
        if data[x][y]>0:
            tempX=data[x][:]
            tempX[y]+=-3.0
            if tempX[y]<0:
                tempX[y]=0
            
            
            tempX.append(x)
            tempY=[y,x]
            
            modelDataX3.append(tempX)
            modelDataY3.append(tempY)



modelDataY3Test=[]
modelDataX3Test=[]
for x in modelDataX3:
    if x[len(x)-1]>500:
        modelDataX3Test.append(x[:len(x)-1])


for x in modelDataY3:
    if x[1]>500:
        modelDataY3Test.append(x[0])
  


modelDataX4=[]
modelDataY4=[]
for x in range(len(data)):
    for y in range(len(data[0])):
        if data[x][y]>0:
            tempX=data[x][:]
            tempX[y]+=-4.0
            if tempX[y]<0:
                tempX[y]=0
            tempY=[y,x]
            
            tempX.append(x)
            
            modelDataX4.append(tempX)
            modelDataY4.append(tempY)


modelDataY4Test=[]
modelDataX4Test=[]
for x in modelDataX4:
    if x[len(x)-1]>500:
        modelDataX4Test.append(x[:len(x)-1])


for x in modelDataY4:
    if x[1]>500:
        modelDataY4Test.append(x[0])


modelDataX5=[]
modelDataY5=[]
for x in range(len(data)):
    for y in range(len(data[0])):
        if data[x][y]>0:
            tempX=data[x][:]
            tempX[y]+=-5.0
            if tempX[y]<0:
                tempX[y]=0
            tempY=[y,x]
          

            tempX.append(x)
            
            modelDataX5.append(tempX)
            modelDataY5.append(tempY)



modelDataY5Test=[]
modelDataX5Test=[]
for x in modelDataX5:
    if x[len(x)-1]>500:
        modelDataX5Test.append(x[:len(x)-1])
   
for x in modelDataY5:
    if x[1]>500:
        modelDataY5Test.append(x[0])
   


modelDataX6=[]
modelDataY6=[]
for x in range(len(data)):
    for y in range(len(data[0])):
        if data[x][y]>0:
            tempX=data[x][:]
            tempX[y]+=-6.0
            if tempX[y]<0:
                tempX[y]=0
            tempY=[y,x]
            

            tempX.append(x)
            modelDataX6.append(tempX)
            modelDataY6.append(tempY)


modelDataY6Test=[]
modelDataX6Test=[]
for x in modelDataX6:
    if x[len(x)-1]>500:
        modelDataX6Test.append(x[:len(x)-1])
    

for x in modelDataY6:
    if x[1]>500:
        modelDataY6Test.append(x[0])
    



def realScore(dX,dY,k):
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
            if newprobs[ind][1] > 0:
                finalprobs.append(newprobs[ind])

            else:
                break

        mallswithin=[]
        for x in finalprobs:
            mallswithin.append(x[0])

        return mallswithin

    fullList=[]
    for x in range(len(dX)):
        fullList.append(storesPicked(dX[x]))

    right=0
    total=0

    for a in range(len(dY)):
        valTemp=search.sequentialSearch(dY[a],fullList[a][0:k])
        if valTemp==-1:
            total+=1
        else:
            total += 1
            right+=1

    return float(right),float(total)

model=ensemble.RandomForestClassifier(n_estimators=20, max_features='auto',max_depth=20,random_state=3)
model.fit(modelDataX1Train,modelDataY1Train)


scores1=[]
scores2=[]
scores3=[]
scores4=[]
scores5=[]
scores6=[]


for k in range(1,6):
   scores1.append(realScore(modelDataX1Test,modelDataY1Test,k))
   scores2.append(realScore(modelDataX2Test,modelDataY2Test,k))
   scores3.append(realScore(modelDataX3Test,modelDataY3Test,k))
   scores4.append(realScore(modelDataX4Test,modelDataY4Test,k))
   scores5.append(realScore(modelDataX5Test,modelDataY5Test,k))
   scores6.append(realScore(modelDataX6Test,modelDataY6Test,k))
   



print scores1
print scores2
print scores3
print scores4
print scores5
print scores6
