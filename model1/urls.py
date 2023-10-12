from django.urls import path
from . import views

urlpatterns=[
    path('home/',views.home,name="home"),
    path('output/',views.output,name="output"),
    path('give_img/',views.give_img, name="give_img")
]