from django.urls import path
from . import views

app_name = 'main'

urlpatterns = [
     path('test/', views.test),
     path('test/result/', views.result),
    path('', views.index),
    path('mypage/', views.mypage, name='mypage'),
    path('mypage/private_info/', views.mypage, name='mypage'),
    path('mypage/purchase/', views.purchase, name='purchase'),
    path('mypage/subscribe/', views.mypage),

    path('main/popup.html', views.servicePopup),
    path('cart/', views.cart, name='cart'),
]