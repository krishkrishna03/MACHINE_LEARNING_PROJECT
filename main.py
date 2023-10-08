import numpy as np #imported numpy library and changed the name as np
import pandas as pd #imported pandas library and changed the name as pd
from sklearn.linear_model import LogisticRegression  # imported the logisticregression model from sklearn.linear_model library
from sklearn.model_selection import train_test_split #imported the train_test_split from sklearn.model_selection to split the data set as requried parts
from sklearn.metrics import accuracy_score #Impoerted this accuracy_score modelue to check the accuracy of the model
from flask import Flask,render_template,request
reg1 = LogisticRegression() #loaded the model to reg variable
d2 = pd.read_csv('your_newherodata.csv') #loaded the data using pandas to df varaiable
dic = { "flying":0, "superhuman strength":1, "will power":2, "Superhuman Reflexes":3,"Teleportation":4,"Super Speed":5,"Shape shifing":6,"Time Travel":7,"Elasticity":8,"Heat Vision":9} #dictionary with powers as keys and a values for each powers
d2['Values'] = d2['abilities'].apply(lambda x: dic.get(x,-1)) #making a values column based on the abilities column
X1 = d2[['strengths','weaknesses','sucessrate','missionscompleted','Values']] #assigned three columns in the dataset to X variable  these are feature variables
y1 = d2['Mission'] # loaded the mission column to the y variable this is target column
X_train, X_test, y_train, y_test = train_test_split(X1, y1, test_size=0.2, random_state=42) #here splitinng the data to 20% for testing and the 80% for training and the random state is used for to split tha data in the same way every time you run the code
reg1.fit(X_train,y_train) #loading the data to the logistic regression model by using the .fit()
pred = reg1.predict(X_test)#predicted the X_test and stored in pred variable
acc1 = accuracy_score(y_test, pred) #checking the accuracy of the model by accuracy_score

app = Flask(__name__) #loading the Flask module to app variable
@app.route('/') #creating a route path
def first():
    return render_template('firstpage.html') #rendering the firstpage.html template

@app.route('/predict',methods=['GET','POST']) #creating another route for next page
def sec():
    dic = {"flying": 0, "superhuman strength": 1, "will power": 2, "Superhuman Reflexes": 3, "Teleportation": 4,
           "Super Speed": 5, "Shape shifing": 6, "Time Travel": 7, "Elasticity": 8, "Heat Vision": 9}
    selected_power = request.form['abilities'] #taking input from firstpage.html and storing it in a varaiable
    mapped_number = dic.get(selected_power)
    stren = request.form['strengths']
    selected_option = request.form['weaknesses']
    mapped_value = 0
    if selected_option == 'Yes':
        mapped_value = 1
    elif selected_option == 'No':
        mapped_value = 0
    sucess_rate = request.form['successrate']
    miscom = request.form['missioncompleted']

    prelist = [stren,mapped_value,sucess_rate,miscom,mapped_number] #taking the input and storing in a list called prelist
    numeric_list = [int(x) if isinstance(x, str) else x for x in prelist] #converting the string values in the list into numeric values
    #print(prelist)
    prelist1 = np.array(numeric_list).reshape(1,-1) #converting the list into an array and reshaping it into a single row and multiple column
    prediction = reg1.predict(prelist1)#made a prediction from the given input data and stored in a prediction variable
    print(prediction)
    return render_template('secondpage.html',prediction=prediction)  #returing the template


if __name__=='__main__'  :
    app.run(debug=True,host="0.0.0.0",port=248) #running the flask app and creating a local server for common ip address