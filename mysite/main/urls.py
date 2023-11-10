from django.urls import path
from . import views

app_name = 'pybo'

urlpatterns = [
    path('', views.index),
    path('mypage/', views.mypage, name='mypage'),
    path('mypage/private_info/', views.mypage, name='mypage'),
    path('mypage/purchase/', views.purchase, name='purchase'),
    path('mypage/purchase/<int:purchase_id>/review/', views.purchase_review, name='purchase_review'), # <int:purchase_id> == 구매내역상품별id 값
    path('mypage/subscribe/', views.mypage),
    path('main/popup.html', views.servicePopup),
    path('basket/', views.basket),
    path('signin/', views.signin),
]