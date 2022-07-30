from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('login/', auth_views.LoginView.as_view(template_name='join/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('signup/', views.signup, name='signup'),
    path('myInfo/', views.myInfo, name='myInfo'),
    path('admin/', views.admin, name='admin'),
    path('admin/userList/', views.userList, name='userList'),
    path('admin/userList/<str:userName>/', views.userInfo, name='userInfo'),
    path('admin/boardList/', views.boardList, name='boardList'),
    path('admin/boardList/<int:question_id>/', views.boardInfo, name='boardInfo'),
    path('admin/userList/<str:userName>/delete/', views.user_delete, name='user_delete'),
    path('admin/boardList/<int:question_id>/delete/', views.board_delete, name='board_delete'),

]