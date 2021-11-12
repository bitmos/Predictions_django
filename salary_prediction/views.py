from django.shortcuts import render
from django.http import HttpResponse, response
import pickle
import json
import numpy as np
def initialize():
    global data_columns
    global model
    with open("salary_prediction/columns.json", 'r') as f:
        data_columns = json.load(f)
            

    global __model
    with open("salary_prediction/salary_prediction.pickle", 'rb') as f:
        model = pickle.load(f)
        

    return data_columns,model


# def index(request):
#     location=initialize()
#     data={
#         'locations':__locations
#     }
#     return render(request,'houseprice.html',{'data':data})
def estimate_salary(request):
    initialize()
    if request.method=="GET":
        data={
            'company':data_columns['company'],
            'job':data_columns['job'],
            'degree':data_columns['degree']
        }
        return render(request,'salary_prediction/houseprice.html',{'data':data})
    else:
        loc=request.POST.get('location')
        company=request.POST.get('company')
        job=request.POST.get('job')
        degree=request.POST.get('degree')

        x = np.zeros(3)
        if (company=="google"):
            x[0]=2
        elif (company=="abc pharma"):
            x[0]=1
        if (job=="sales executive"):
            x[1]=2
        elif (job=="business manager"):
            x[1]=1
        if (degree=="masters"):
            x[2]=1
        
        price=round(model.predict([x])[0], 2)
        if price == 1 :
            t="More than 100k"
        else:
            t="Less than 100k"
        data = {
            'selected_company':company,
            'selected_job':job,
            'selected_degree':degree,
            'price':price,
            'text':t
                
         }
        return render(request,'salary_prediction/houseprice.html',{'data':data})
         
    