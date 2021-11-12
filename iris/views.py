from django.shortcuts import render
from django.http import HttpResponse, response
import pickle
import json
import numpy as np
def initialize():
    global target
    global model
    with open('iris/columns.json','r') as f:
        target=json.load(f)["data_columns"]
    
    with open("iris/iris.pickle",'rb') as f:
        model=pickle.load(f)
    return model,target


# def index(request):
#     location=initialize()
#     data={
#         'locations':__locations
#     }
#     return render(request,'houseprice.html',{'data':data})
def estimate_iris(request):
    initialize()
    if request.method=="GET":
        return render(request,'iris/houseprice.html',{})
    else:
        slength=int(request.POST.get('slength'))
        swidth=int(request.POST.get('swidth'))
        plength=int(request.POST.get('plength'))
        pwidth=int(request.POST.get('pwidth'))

        x = np.zeros(4)
        x[0] = slength
        x[1] = swidth
        x[2] = plength
        x[3]=pwidth
        price=target[model.predict([x])[0]]
        data = {
              'price':price
         }
        return render(request,'iris/houseprice.html',{'data':data})
         
    