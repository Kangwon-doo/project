from django.urls import path
from . import views

urlpatterns = [
    path('subscribe/', views.guide, name = 'subscribe'),
    path('subscribe/result', views.result, name = 'result'),
]