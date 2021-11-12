from django.shortcuts import render
from django.http import HttpResponse, response
import pickle
import json
import numpy as np
import pandas as pd
# def initialize():
#     global model
#     with open("titanic/titanic.pickle",'rb') as f:
#         model=pickle.load(f)
#         print(type(model))
        

#     return model

def model(x):
    df=pd.read_csv("titanic/titanic.csv")
    df.drop(['PassengerId','Name','SibSp','Parch','Ticket','Cabin','Embarked'],axis="columns",inplace=True)
    target=df.Survived
    inputs=df.drop(["Survived"],axis="columns")
    dummies=pd.get_dummies(inputs.Sex)
    inputs=pd.concat([inputs,dummies],axis='columns')
    inputs.drop('Sex',axis='columns',inplace=True)
    inputs.Age=inputs.Age.fillna(inputs.Age.mean())
    from sklearn.model_selection import train_test_split
    x_train,x_test,y_train,y_test=train_test_split(inputs,target,test_size=0.2)
    from sklearn.naive_bayes import GaussianNB
    model=GaussianNB()
    model.fit(x_train,y_train)
    return model.predict([x])[0]
# def index(request):
#     location=initialize()
#     data={
#         'locations':__locations
#     }
#     return render(request,'houseprice.html',{'data':data})
def estimate_titanic(request):
    if request.method=="GET":
        return render(request,'titanic/houseprice.html',{})
    else:
        pclass=int(float(request.POST.get('class')))
        gender=request.POST.get('gender')
        age=request.POST.get('age')
        fare=request.POST.get('fare')
        x = np.zeros(5)
        x[0] = pclass
        x[1] = age
        x[2]=fare
        if gender=="Female":
            x[4] = 1
        else :
            x[3]=1
        print(x)
        prd=model(x)
        print(prd)
        if(prd==0):
            text="Not Survived"
        else:
            text="Survived"
        data = {
            'selected_class':pclass,
            'selected_gender':gender,
            'age':age,
            'fare':fare,
            'price':text
                
         }
        return render(request,'titanic/houseprice.html',{'data':data})