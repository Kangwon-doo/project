from django.urls import path
from . import views

app_name = 'pybo'

urlpatterns = [
    path('', views.index),
    path('mypage/', views.mypage, name='mypage'),
    path('mypage/info/', views.mypage),
    path('mypage/purchase/', views.mypage),
    path('mypage/subscribe/', views.mypage),

    path('cartlist/', views.cartlist),
    path('signin/', views.signin),
]