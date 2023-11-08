from django.urls import path
from . import views

urlpatterns = [
    path('coffee/', views.coffee, name = 'coffee_list'),
    #path('MD/', views.MD),
    path('coffee/<int:coffee_id>/', views.coffee_detail, name = 'coffee_detail'),
    path('roastery/<int:roastery_id>/', views.roastery_detail, name = 'roastery_detail'),
    path('review/', views.reviews, name = 'review test'),
    path('review-submit/', views.review_create, name='review-submit'),
]