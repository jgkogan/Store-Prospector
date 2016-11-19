# Store-Prospector
Jonathan Kogan, Dennis Shasha, Roy Lowrance, and Risbabh Jain

A machine learning approach to predicting the types of tenants to fill vacancies in shopping centers. This repository contains a few main things: the data, the code for the machine learning model, the online Store Prospector system, and the code used in the analysis of the successfulness of the model (e.g code for charts). 

The official paper explaining the research can be found at https://www.cs.nyu.edu/media/publications/TR2016-984.pdf.

Overall, the method isn't ready to be used in the shopping center industry yet; but with better and more extensive data, the methods used in this research can easily be reused in creating the next version of a machine learning system that predicts what store types should fill vacancies.

Here are the instructions on how to use the system. 
First, make sure you have python 2, scikit-learn and if you would like to implement the website, Flask as well.

The charts files contains the analyses of the model. The actual models' code can be found within the binary and cardinal folders. To run any file, just keep the file structures the same and call the files from your terminal. They will generate the charts.

To run the website, you need flask. The instructions on how to use flask can be found in its official documentation, but to just be able to use our website, follow these simple steps. Go into the website's folder, run EXPORT FLASK_APP=init.py and then run the command flask run. This will then put the website up locally for you to find with your web browser. 

If you want to build off of our code, all that is really needed is the part where we import the data and train the model. Then run the model.predict_proba line and you will get the the probability of how much the model thinks you should add a certain store. The higher probability means it is more certain that you should add the store to your center. To find out what the numbers mean, you can look in the database to see what category each number corresponds to.

If you have any questions contact Jonathan Kogan at jgkogan@icloud.com or Professor Dennis Shasha at shasha@cims.nyu.edu.


