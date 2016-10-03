import sqlite3
from sklearn import ensemble
import random
import matplotlib.pyplot as plt
import math
from sklearn.externals import joblib
import search
import numpy as np



conn = sqlite3.connect('/Users/jkogan/Documents/RealEstateProject/TheRealRealEstateProjectDatabase.db')

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

catPerc=[]
for x in range(len(data[0])):
    catPerc.append(0)


for x in range(len(data)):
    for y in range(len(data[0])):
        catPerc[y]+=data[x][y]

for x in range(len(cats)):
    catPerc[x]=[cats[x],float(catPerc[x])/float(len(data))]

def byValue(num):
    return num[1]


fullCats=sorted(catPerc, key=lambda x: x[1]) 
# write it
fullCats.reverse()
print fullCats

f = open('/Users/jkogan/Documents/RealEstateProject/charts/StoreAmounts/frequencies.txt','w')
for r in fullCats:    
    f.write(str(r[0])+'\t'+str(r[1])+'\n') # python will convert \n to os.linesep
f.close()

names=[]
nums=[]
for part in fullCats:
    names.append(part[0])
    nums.append(part[1])

"""plt.bar(range(10),nums[:10])
plt.xticks([x+0.6 for x in range(10)],
        names[:10],
           size='small',
           rotation=-60,
           # rotation='vertical',
           )
plt.tight_layout(pad=0.4, w_pad=3.5, h_pad=5.0)
plt.ylabel("Percent of Malls Store of Category N Appears In")
plt.savefig('/Users/jkogan/Documents/RealEstateProject/charts/StoreAmounts/10storeFrequencies.pdf')
plt.close()"""

fig = plt.figure()
subplot1 = fig.add_subplot(111)
plt.bar(range(10),nums[:10])
plt.xticks([x+0.6 for x in range(10)],
        names[:10],
           size='small',
           rotation=-60,
           # rotation='vertical',
           )
#plt.tight_layout(pad=0.4, w_pad=3.5, h_pad=5.0)

plt.ylabel("Percentage of Malls That Contain A Store Of Category S")
fig.tight_layout()

plt.savefig('/Users/jkogan/Documents/RealEstateProject/charts/StoreAmounts/10storeFrequencies.pdf')
plt.close()



