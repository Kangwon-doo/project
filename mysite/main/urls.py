from django.urls import path
from . import views

app_name = 'pybo'

urlpatterns = [
    path('', views.index),
    path('mypage/', views.mypage, name='mypage'),
    path('mypage/private_info/', views.mypage, name='mypage'),
    path('mypage/purchase/', views.mypage),
    path('mypage/subscribe/', views.mypage),

    path('main/popup.html', views.servicePopup),
    path('basket/', views.basket),
    path('signin/', views.signin),
]