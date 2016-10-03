#This file generates the simple cardinal model accuracy chart.
import sqlite3
import math
from sklearn import ensemble
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import copy



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
tempdata = copy.copy(data)


modelDataX1=[]
modelDataY1=[]
for x in range(len(data)):
    for y in range(len(data[0])):
        if data[x][y]>0:
            tempX=data[x][:]
            tempX[y]+=-1
            tempX.append(x)
            tempY=[y,x]
            modelDataX1.append(tempX)
            modelDataY1.append(tempY)


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

    return float(right)/float(total)

model=ensemble.RandomForestClassifier(n_estimators=20, max_features='auto',max_depth=20,random_state=3)
model.fit(modelDataX1Train,modelDataY1Train)


scores=[]
for k in range(1,6):
   scores.append(realScore(modelDataX1Test,modelDataY1Test,k))







  
rects=plt.bar(range(5),scores, color='red')



plt.ylim(0,1)

plt.xticks([x+0.4 for x in range(0,5)],
        range(1,6),
           size='small',
           rotation=0,
           # rotation='vertical',
           )

plt.text(.9,.9,"Cardinal Model In Which The Number of Stores of")
plt.text(.9,.85,"Each Type Other Than The Left Out Store Is Given")

plt.xlabel('Number of Stores In The Top K Considered Correct')
plt.ylabel('Accuracy')


def autolabel(rects):
    # attach some text labels
    for r in range(len(rects)):
        rect=rects[r]
        height = rect.get_height()
        plt.text(rect.get_x() + rect.get_width()/2., 1.05*height,
                str(round(scores[r],4)),
                ha='center', va='bottom')

autolabel(rects)


plt.tight_layout(pad=0.8, w_pad=0.8, h_pad=1.0)
plt.savefig('simpleCardinal.pdf')
plt.close()





