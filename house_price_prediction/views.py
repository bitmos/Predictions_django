from django.shortcuts import render
from django.http import HttpResponse, response
import pickle
import json
import numpy as np
def initialize():
    global __locations
    global __data_columns
    global __model
    with open("house_price_prediction/columns.json", 'r')as f:
        __data_columns = json.load(f)['data_columns']
        __locations = __data_columns[3:]
    
    with open("house_price_prediction/banglore_home_prices_model.pickle", 'rb') as f:
        __model = pickle.load(f)
    return __locations,__data_columns,__model


# def index(request):
#     location=initialize()
#     data={
#         'locations':__locations
#     }
#     return render(request,'houseprice.html',{'data':data})
def estimate(request):
    initialize()
    if request.method=="GET":
        data={
            'locations':__locations
        }
        return render(request,'house_price_prediction/houseprice.html',{'data':data})
    else:
        print("pOST METHOD")
        loc=request.POST.get('location')
        print(loc)
        sqft=int(request.POST.get('area'))
        bhk=int(request.POST.get('bhk'))
        bath=int(request.POST.get('bath'))
        try:
            loc_index = __data_columns.index(loc.lower())
        except:
            loc_index = -1

        x = np.zeros(len(__data_columns))
        x[0] = sqft
        x[1] = bath
        x[2] = bhk
        if loc_index >= 0:
            x[loc_index] = 1
        price=round(__model.predict([x])[0], 2)
        data = {
              'selected' :loc,
              'bhk' : bhk,
              'bath' : bath,
              'area':sqft,
              'price':price
         }
        return render(request,'house_price_prediction/houseprice.html',{'data':data})
         
    