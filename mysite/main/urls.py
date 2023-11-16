from django.urls import path
from . import views

app_name = 'main'

urlpatterns = [
<<<<<<< HEAD
     path('test/', views.test),
     path('test/result/', views.result),
=======
    path('test/', views.test, name='test'),
    path('test/result/', views.result, name='result'),
>>>>>>> 7c74a337878871921a1648c2342bcaa36a8eef0a
    path('', views.index),
    path('mypage/', views.mypage, name='mypage'),
    path('mypage/private_info/', views.mypage, name='mypage'),
    path('mypage/purchase/', views.purchase, name='purchase'),
    path('mypage/subscribe/', views.mypage),
    path('main/popup.html', views.servicePopup),
<<<<<<< HEAD
    path('cart/', views.cart, name='cart'),
=======
    path('basket/', views.basket),
    path('review/create/<int:coffee_id>', views.review, name='submit')
>>>>>>> 7c74a337878871921a1648c2342bcaa36a8eef0a
]