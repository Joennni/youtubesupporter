from django.urls import path
from . import views

urlpatterns = [
    path('', views.movie_list, name='movie_list'),
    path('detail/<str:name>/', views.movie_detail, name='movie_detail'),
    path('reserve/<str:name>/', views.reserve, name='reserve'),
    path('reserve/<str:name>/<str:date>/', views.reserve, name='select_date'),
    path('reserve/<str:name>/<str:date>/<str:user>/<int:price>/result/', views.reserve_result, name='reserve_result'),
]