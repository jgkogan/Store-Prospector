#Main file
from flask import Flask, g, render_template, request, redirect, flash, url_for, make_response
import sqlite3
import predictB
from sklearn.externals import joblib
from sklearn import ensemble
import numpy as np
app = Flask(__name__)



def revCats(cats):
	return np.matrix(np.transpose(np.split(np.asarray(cats),4))).flatten().tolist()

app.jinja_env.globals.update(revCats=revCats)



app.jinja_env.globals.update(sorted=sorted)

fuzzyStore=(None,None)

app.jinja_env.globals.update(len=len)

def myReplace(s,b,a):
	return s.replace(b,a)



app.jinja_env.globals.update(replace=myReplace)



conn = sqlite3.connect('database.db')
c = conn.cursor()
c.execute("SELECT type FROM StoreTypes")
oldcats=c.fetchall()
categories=list(map((lambda x: x[0]), oldcats))
conn.close()

global checks
with app.app_context():	
	checks=[]
	for x in range(len(categories)):
		checks.append(0)


@app.route('/predict', methods=['POST','GET'])
def predict():
	
	suggestions=[]
	readyForModel=[]
	storesarr=[]
	if request.method=='POST':
		if request.form['submit']=='Predict':


			for x in range(len(categories)):
				readyForModel.append(request.form.getlist(sorted(categories)[x]))

			totalStores=int(request.form.getlist('totalStores')[0])

			readyForModelReal=[]
			catsinmall=[]
			checks=[]
			for r in readyForModel:
				readyForModelReal.append(len(r))

				if len(r)==1:
					catsinmall.append(r[0])
					checks.append(1)
				else:
					checks.append(0)

			suggestions=predictB.predictor(readyForModelReal,totalStores)

			
			
			return render_template("predictB.html", totalStores=totalStores,catsinmall=catsinmall, suggestions=suggestions,checks=checks)
	


		if request.form['submit']=='Refresh':

			checks=[]
			for x in categories:
				checks.append(0)
			
			
			return render_template("indexB.html", totalStores=0,fuzzyStore=(None,None),storeTypes='',store=None, categories=sorted(categories), checks=checks)
	




		if request.form['submit']=='Search':
			totalStores=int(request.form.getlist('totalStores')[0])
			for x in range(len(categories)):
				readyForModel.append(request.form.getlist(sorted(categories)[x]))
			(checks)=[]
			for r in readyForModel:
				if len(r)==1:
					(checks).append(1)
				else:
					(checks).append(0)
			
			store=request.form['store']
			tempStore=store
			store=store.strip()
			store=store.lower()
			store = store.replace("'", "")
			store = store.replace(" ", "")
			store = store.replace(".", "")
			store = store.replace("-", "")
			store = store.replace("_", "")
			store = store.replace(";", "")
			store = store.replace(":", "")
			store = store.replace("(", "")
			store = store.replace(")", "")
			store = store.replace("&", "")
			store = store.replace("\n", "")
			store = store.replace("\r", "")
			store = store.replace("*", "")
			store= store.replace(",", "")
			
			storeTypes,fuzzyStore=predictB.storeToCats(store)
			#storeTypes=storeTypesold

			storeTypesArr=storeTypes.split(",")
			for s in range(len(storeTypesArr)):
				storeTypesArr[s]=storeTypesArr[s].replace("_"," ")

			storeTypes=",".join(storeTypesArr)
			
			return render_template("indexB.html", totalStores=totalStores, fuzzyStore=fuzzyStore, store=tempStore,storeTypes=storeTypes, categories=sorted(categories),checks=(checks))
	
	return redirect(url_for('homepage'))









@app.route('/model', methods=['POST','GET'])
def homepage():	

	if request.method=='POST':
		checks1=str(request.form.getlist('checks')[0])
		checks1=checks1.split('[')[1]
		checks1=checks1.split(']')[0]
		checks1=checks1.split(',')
		for x in range(len(checks1)):
			checks1[x]=int(checks1[x])
	
		checks11=checks1[:64/4]
		checks12=checks1[1*64/4:2*64/4]
		checks13=checks1[2*64/4:3*64/4]
		checks14=checks1[3*64/4:4*64/4]
		realChecks=[]
		for x in range(len(checks11)):
			realChecks.append(checks11[x])
			realChecks.append(checks12[x])
			realChecks.append(checks13[x])
			realChecks.append(checks14[x])

		totalStores=int(request.form.getlist('totalStores')[0])
		
		return render_template("indexB.html",totalStores=totalStores, fuzzyStore=(None,None), storeTypes='',store=None, categories=sorted(categories), checks=realChecks)

	return render_template("indexB.html",totalStores=0, fuzzyStore=(None,None), storeTypes='',store=None, categories=sorted(categories), checks=checks)







@app.route('/', methods=['POST','GET'])
def main():
	return render_template("index.html", fuzzyStore=(None,None), storeTypes='',store=None, categories=sorted(categories), checks=checks)


if __name__:
	app.run()



