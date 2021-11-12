from django.urls import path

from . import views

urlpatterns = [
    # path('', views.index, name='index'),
    path('',views.estimate_onehot,name="estimate_onehot"),

]