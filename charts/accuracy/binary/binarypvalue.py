#Generates success and total number of trials for each k. Those values are then used in the file pvalues.nb to generate pvalues.
import sqlite3
from sklearn import ensemble
import random
import math


import search


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


modelDataX=[]
modelDataY=[]
for x in range(len(data)):
    for y in range(len(data[0])):
        if data[x][y]>0:
            tempX=data[x][:]
            tempX[y]+=-1
            tempY=[y,x]
            tempX.append(x)
            modelDataX.append(tempX)
            modelDataY.append(tempY)

modelDataXTrain=[]
modelDataYTrain=[]
modelDataYTest=[]
modelDataXTest=[]
for x in modelDataX:
    if x[len(x)-1]>500:
        modelDataXTest.append(x[:len(x)-1])
    else:
        modelDataXTrain.append(x[:len(x)-1])

for x in modelDataY:
    if x[1]>500:
        modelDataYTest.append(x[0])
    else:
        modelDataYTrain.append(x[0])
#print(modelDataX)



#model=ensemble.RandomForestClassifier()


#model.fit(modelDataX[0:14000],modelDataY[0:14000])




#print(model.score(modelDataX[14000:16000],modelDataY[14000:16000]))
#for x in n_estimators1:
 #  for y in max_features1:
  #    for z in max_depth1:
   #      model=ensemble.RandomForestClassifier(n_estimators=x, max_features=y, max_depth=z)
    #     model.fit(modelDataX[0:14000],modelDataY[0:14000])
     #    print([x,y,z])
      #   print(model.score(modelDataX[14000:16000],modelDataY[14000:16000]))
       #  accuracies.append([x,y,z,model.score(modelDataX[14000:16000],modelDataY[14000:16000])])

#print(accuracies)



fullTest=[]

for x in range(1000):
    temp=[]
    for i in range(len(cats)):
        temp.append(random.randint(0,1))
    fullTest.append(temp)




#print(model.predict(fullTest))
##coef=model.feature_importances_
#model.predict(modelDataX[1:3])
#print(coef[0])

#print(modelDataX[16000:17100])
#print(modelDataY[16000:17100])
#model=ensemble.RandomForestClassifier(warm_start='true',n_jobs=3,n_estimators=100, max_features='auto',criterion='gini',bootstrap='true', max_depth=100)
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
            if newprobs[ind][1] > 0.000000000000001:
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



model=ensemble.RandomForestClassifier(n_estimators=20, max_features='auto', max_depth=20, random_state=3)

model.fit(modelDataXTrain,modelDataYTrain)

scores=[]
for k in range(1,6):
    scores.append(realScore(modelDataXTest, modelDataYTest,k))


print scores


