from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('login/', views.login_page, name='login_page'),
    path('signup/', views.create_user_page, name='signup_page'),
    path('home/', views.home_page, name='home_page'),
    path('module/<int:id>/', views.module_page, name='module_page'),
    path('logout/', views.logout_page, name='logout'),
]