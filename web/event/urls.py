from django.urls import path
from . import views

urlpatterns = [
    path('', views.event, name='event'),
    path('rock/', views.event_rock, name='event_rock'),
    path('question/', views.event_question_set, name='event_question'),
]