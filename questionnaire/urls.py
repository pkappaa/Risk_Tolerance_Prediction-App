from django.urls import path
from . import views

urlpatterns = [
    path('', views.questionnaire, name='questionnaire'),
    path('results/<uuid:uuid>/', views.results_view, name='results'), 
]