from django.urls import path
from . import views

app_name = 'pybo'

urlpatterns = [
    path('',views.TempWizardView.as_view()),
    path('hmm',views.index),
]