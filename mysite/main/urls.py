from django.urls import path
from . import views

app_name = 'pybo'

urlpatterns = [
     path('test/', views.index),
     path('test/result/', views.result),
]