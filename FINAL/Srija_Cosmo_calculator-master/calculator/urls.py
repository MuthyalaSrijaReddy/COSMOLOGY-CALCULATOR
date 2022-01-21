from django.urls import path

from . import views

urlpatterns = [
    path('page1/', views.index, name='index'),
    path('mycalculator/hai', views.hai, name='hai'),
    path('mycalculator/', views.calculatorForm, name="calculator")
]