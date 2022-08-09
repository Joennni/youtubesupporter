from django.urls import path

from board.models import Comment1
from . import views
from .views import *

urlpatterns = [
    path('answer/create/<int:question_id>/', views.answer_create, name='answer_create'),
    path('<int:question_id>/', views.detail, name='detail'),
    path('', views.index, name='index'),
    path('question/create/', views.question_create, name='question_create'),
    path('question/modify/<int:question_id>/', views.question_modify, name='question_modify'),
    path('question/delete/<int:question_id>/', views.question_delete, name='question_delete'),
    path('SoHyun_Act/', views.SoHyun_Act, name = 'SoHyun_Act'),
    path('SoHyun_Com/', views.SoHyun_Com, name = 'SoHyun_Com'),
    path('SoHyun_Cap/', views.SoHyun_Cap),
    path('SoHyun_Htag/', views.SoHyun_Htag),
    path('SoHyun_Script/', views.SoHyun_Script),
    path('SangA_Act/', views.SangA_Act, name = 'SangA_Act'),
    path('SangA_Com/', views.SangA_Com, name = 'SangA_Com'),
    path('SangA_Cap/', views.SangA_Cap),
    path('SangA_Htag/', views.SangA_Htag),
    path('SangA_Script/', views.SangA_Script),
    path('MinHee_Act/', views.MinHee_Act, name = 'MinHee_Act'),
    path('MinHee_Com/', views.MinHee_Com, name = 'MinHee_Com'),
    path('MinHee_Cap/', views.MinHee_Cap),
    path('MinHee_Htag/', views.MinHee_Htag),
    path('MinHee_Script/', views.MinHee_Script),
    path('JiHyun_Act/', views.JiHyun_Act, name = 'JiHyun_Act'),
    path('JiHyun_Com/', views.JiHyun_Com, name = 'JiHyun_Com'),
    path('JiHyun_Cap/', views.JiHyun_Cap),
    path('JiHyun_Htag/', views.JiHyun_Htag),
    path('JiHyun_Script/', views.JiHyun_Script),
    path('login_chart/', views.login_chart),
    path('scatter_chart/', views.Scatter_chart),
    path('test_base/', views.base_view)    
]