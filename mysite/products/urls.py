from django.urls import path
from . import views

app_name = 'products'

urlpatterns = [
    path('coffee/', views.coffee, name = 'coffee'),
    path('MD/', views.MD),
    path('coffee/<int:coffee_id>/', views.coffee_detail, name = 'coffee_detail'),
    path('roastery/<int:roastery_id>/', views.roastery_detail, name = 'roastery_detail'),
    path('survey/', views.SurveyWizardView.as_view()),
    path('survey-review/<int:userid>', views.survey_reviews, name = 'review test'),
    path('review-submit/<int:userid>', views.review_create, name='review-submit'),
]