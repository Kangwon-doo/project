

from django.urls import path
from . import views

app_name = 'pybo'

urlpatterns = [
    path('test/', views.test, name='test'),
    path('test/result/', views.result, name='result'),
    path('', views.index),
    path('mypage/', views.mypage, name='mypage'),
    path('mypage/private_info/', views.mypage, name='mypage'),
    path('mypage/purchase/', views.purchase, name='purchase'),
    path('mypage/subscribe/', views.mypage),
    path('main/popup.html', views.servicePopup),
    path('basket/', views.basket),
    path('review/create/<int:coffee_id>', views.review, name='submit')
    #path('mypage/delete/', views.delete, name= 'delete'     )
]