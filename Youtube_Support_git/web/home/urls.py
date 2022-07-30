from django.urls import path
from . import views

urlpatterns = [
    #path('', views.home, name = 'home'),
    path('', views.home_01),
    path('support/', views.support),      
    path('search/', views.search, name='search')    
]