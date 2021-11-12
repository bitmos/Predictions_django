from django.shortcuts import render
import pickle
import json
import numpy as np
# Create your views here.
def initialize():
    global data_columns
    global __model
    with open("house_price_with_one_hot_encoding/columns.json", 'r') as f:
        data_columns = json.load(f)

    global __model
    with open("house_price_with_one_hot_encoding/price.pickle", 'rb') as f:
        __model = pickle.load(f)
    return data_columns,__model

def estimate_onehot(request):
    initialize()
    if request.method=="GET":
        data={
            'locations':data_columns['towns']
        }
        return render(request,'house_price_with_one_hot_encoding/houseprice.html',{'data':data})
    else:
        loc=request.POST.get('location')
        sqft=int(request.POST.get('area'))

        x = np.zeros(3)
        if (loc=="monroe township"):
            x[0]=1
        
        elif (loc=="robinsville"):
            x[1]=1
            
        x[2]=sqft
        price=round(__model.predict([x])[0], 2)
        data = {
              'selected' :loc,
              'area':sqft,
              'price':price
         }
        return render(request,'house_price_with_one_hot_encoding/houseprice.html',{'data':data})
