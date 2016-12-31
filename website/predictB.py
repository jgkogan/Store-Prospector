#Predictor is here
import sqlite3
from sklearn import ensemble
from sklearn.externals import joblib
import search
from fuzzywuzzy import process

def storeToCats(store):
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute("SELECT StoreName,StoreType FROM fullData")
    olddata=c.fetchall()
    data=list(map((lambda x: [x[0],x[1]]), olddata))
    conn.close()
    newdata=[]
    for x in data:
        if not (len(x[0]) >100):
            if not (len(x[0])<3):
                newdata.append(x)


    for x in range(len(newdata)):
        newdata[x]=[str(newdata[x][0]).lower().strip(),str(newdata[x][1]).lower().strip()]
        newdata[x][0] = newdata[x][0].replace("'", "")
        newdata[x][0] = newdata[x][0].replace(" ", "")
        newdata[x][0] = newdata[x][0].replace(".", "")
        newdata[x][0] = newdata[x][0].replace("-", "")
        newdata[x][0] = newdata[x][0].replace("_", "")
        newdata[x][0] = newdata[x][0].replace(";", "")
        newdata[x][0] = newdata[x][0].replace(":", "")
        newdata[x][0] = newdata[x][0].replace("(", "")
        newdata[x][0] = newdata[x][0].replace("&", "")
        newdata[x][0] = newdata[x][0].replace("*", "")
        newdata[x][0] = newdata[x][0].replace("\n", "")
        newdata[x][0] = newdata[x][0].replace("\r", "")



    halfdata=[]
    for x in newdata:
        halfdata.append(x[0])
    
    smallerdata=[]
    if len(str(store))==0:
        fuzzyStore=("",0)
        return 'Not found in database, it is most likely a local store.',fuzzyStore

    s1=str(store)[0]
    for x in halfdata:
        if x[0]==s1:
            smallerdata.append(x)

    fuzzyStore=process.extractOne(store,smallerdata)

    if fuzzyStore[1]>80:
        index=search.sequentialSearch(fuzzyStore[0], halfdata)
        final=(newdata[index][1])
        return final[1:len(final)-1],fuzzyStore
    else:
        return 'Not found in database, it is most likely a local store.',fuzzyStore






def predictor(storesInMall,totalStores):
    conn = sqlite3.connect('database.db')

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

    trainData=data[:500]
    #sums=[]
    #for x in trainData:
    #    sums.append([x,sum(x)])
    sums1=[134, 12, 81, 64, 58, 62, 46, 69, 34, 73, 57, 53, 69, 93, 64, 22, 63, 151, 97, 116, 116, 307, 93, 130, 56, 34, 150, 72, 92, 70, 52, 107, 51, 41, 28, 72, 32, 47, 67, 45, 87, 50, 19, 20, 30, 36, 68, 103, 44, 131, 37, 33, 113, 84, 56, 32, 114, 89, 66, 220, 56, 85, 45, 111, 258, 93, 52, 52, 37, 42, 70, 64, 49, 160, 51, 61, 136, 35, 85, 85, 12, 92, 113, 74, 65, 76, 148, 79, 38, 142, 16, 143, 120, 113, 35, 67, 63, 113, 45, 37, 78, 105, 139, 50, 93, 71, 162, 40, 88, 36, 115, 82, 37, 55, 69, 47, 57, 42, 144, 99, 52, 107, 42, 44, 57, 164, 109, 93, 76, 59, 74, 100, 175, 89, 77, 84, 97, 49, 35, 85, 96, 96, 37, 60, 57, 119, 182, 137, 68, 35, 112, 58, 67, 70, 108, 87, 72, 108, 73, 83, 86, 40, 61, 34, 44, 92, 92, 67, 51, 177, 39, 143, 111, 129, 91, 100, 45, 99, 202, 160, 37, 36, 206, 36, 165, 76, 55, 113, 86, 36, 77, 42, 35, 80, 64, 172, 37, 103, 42, 48, 71, 246, 84, 58, 70, 37, 58, 73, 40, 151, 63, 33, 33, 125, 53, 55, 89, 123, 78, 119, 74, 164, 63, 80, 58, 141, 88, 43, 81, 81, 110, 72, 157, 85, 102, 41, 65, 102, 58, 132, 75, 185, 50, 99, 110, 43, 43, 63, 57, 62, 38, 83, 40, 36, 56, 81, 96, 60, 39, 46, 105, 105, 61, 113, 45, 35, 128, 149, 132, 59, 102, 92, 64, 63, 84, 40, 67, 41, 24, 62, 96, 56, 39, 106, 44, 70, 145, 60, 57, 127, 136, 94, 62, 75, 132, 76, 18, 121, 8, 49, 37, 167, 172, 50, 103, 155, 97, 153, 65, 219, 146, 147, 71, 45, 157, 58, 91, 130, 42, 49, 74, 73, 59, 77, 49, 75, 50, 68, 13, 51, 84, 79, 68, 87, 65, 104, 41, 81, 65, 77, 84, 48, 92, 62, 181, 122, 183, 183, 13, 99, 54, 75, 56, 172, 60, 58, 71, 36, 83, 78, 38, 75, 46, 112, 44, 176, 92, 136, 173, 44, 110, 54, 65, 128, 146, 48, 58, 66, 109, 50, 76, 46, 70, 64, 72, 176, 151, 69, 178, 123, 69, 30, 106, 296, 296, 157, 104, 23, 233, 59, 62, 36, 70, 70, 167, 41, 54, 90, 41, 51, 53, 21, 60, 50, 62, 127, 92, 59, 63, 172, 36, 70, 86, 69, 46, 228, 112, 42, 63, 40, 44, 43, 153, 78, 61, 75, 90, 65, 62, 43, 69, 49, 53, 34, 52, 57, 109, 53, 152, 169, 170, 132, 126, 35, 127, 45, 46, 39, 93, 146, 11, 74, 111, 49, 63, 65, 63, 35, 122, 45, 114, 121, 68, 37, 102, 138, 89, 68, 67, 104, 64, 55, 177, 40, 65, 65, 43, 120, 42, 63, 81, 73, 110, 43, 149, 86, 82, 39, 85, 74, 68, 87, 114, 8, 180, 148, 119, 119, 8, 201, 125, 98, 159, 158, 96, 76, 79, 120, 79, 96, 95, 59, 73, 176, 332, 51, 67, 176, 64, 144, 62, 130, 27, 97, 151, 46, 81, 34, 35, 35, 108, 61, 44, 131, 67, 49, 110, 72, 38, 107, 85, 81, 89, 102, 45, 106, 65, 40, 69, 85, 124, 121, 55, 56, 99, 143, 138, 75, 28, 62, 70, 85, 77, 110, 48, 121, 152, 156, 89, 120, 74, 42, 108, 42, 42, 174, 33, 54, 218, 90, 43, 104, 108, 118, 89, 59, 74, 80, 41, 83, 213, 82, 157, 71, 128, 168, 77, 36, 41, 48, 159, 44, 89, 174, 28, 53, 120, 181, 59]
    sums=[]
    for x in range(len(trainData)):
        sums.append([trainData[x],sums1[x]])


    trainData=[]
    for x in range(len(sums)):
        sums[x][1]=abs(sums[x][1]-totalStores)

    trainData=sorted(sums, key=lambda x: x[1])[:100]

    
    fullTrainData=[]

    for x in range(len(trainData)):
        tempX=trainData[x][0][:]
            
        fullTrainData.append(tempX)





    for x in range(len(fullTrainData)):
        for y in range(len(fullTrainData[0])):
            if fullTrainData[x][y]>0:
                fullTrainData[x][y]=1



    def scoreMall(inputX,mall):
        mallScore=0
        for x in range(len(inputX)):
            if inputX[x]==1 and mall[x]==0:
                mallScore+=1

        return mallScore

    unsorted=[]
    for x in range(len(fullTrainData)):
        unsorted.append([scoreMall(storesInMall,fullTrainData[x]),fullTrainData[x]])


    sortedTrainData=sorted(unsorted, key=lambda x: x[0],reverse=False)[:]
    modelDataX=[]
    modelDataY=[]
    for x in range(len(sortedTrainData)):
        for y in range(len(sortedTrainData[0][1])):
            if sortedTrainData[x][1][y]>0:
                tempX=sortedTrainData[x][1][:]
                tempX[y]+=-1
                tempY=y
                modelDataX.append(tempX)
                modelDataY.append(tempY)




    model=ensemble.RandomForestClassifier(n_estimators=20, max_features='auto', max_depth=20, random_state=3)

    model.fit(modelDataX,modelDataY)


    storesDict={}
    for x in range(len(sorted(cats))):
        storesDict[sorted(cats)[x]]=storesInMall[x]


    realStoresInMall=[]
    for x in range(len(cats)):
        realStoresInMall.append(storesDict[cats[x]])

    probs=model.predict_proba([realStoresInMall])
    newprobs=[]
    for x in range(len(probs[0])):
        newprobs.append([x,probs[0][x]])


    newprobs.sort(key=lambda x: x[1],reverse=True)
    finalprobs=[]
    not0=False
    ind=0
    for ind in range(len(newprobs)):
        if newprobs[ind][1]>0.00000000000000001:
           finalprobs.append(newprobs[ind])

        else:
            break

    finalprobswithcats=[]
    for x in finalprobs:
        finalprobswithcats.append([cats[x[0]],x[1]])

    return finalprobswithcats[:10]
#print storeToCats("walgreen")
#print predictor([1, 0, 1, 1, 1, 1, 1, 0, 1, 0, 1, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 1, 0, 1, 1, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0],20)
#temp=[]
#for x in range(64):
#    temp.append(1)

#print predictor(temp,100)

