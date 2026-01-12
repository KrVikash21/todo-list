from django.contrib import admin
from django.urls import path
from django.http import HttpResponse
from . import views
from todoList.views import home, login, signup, add_todo, signout, delete_todo, change_status, otp, pass_login, pass_signup, set_language




urlpatterns = [

    path('', views.home, name='home'), 
    path('login/', views.login, name='login'),
    path('signup/', views.signup, name='signup'),
    path('add-todo/', views.add_todo, name='add_todo'),
    path('signout/', views.signout, name='signout'),
    path('delete-todo/<int:id>', views.delete_todo, name='delete_todo'),
    path('change-status/<int:id>/<str:status>', views.change_status, name='change_status'),
    path('otp/<str:uid>/', views.otp, name='otp'),
    path('pass-login/', pass_login, name='pass_login'),
    path('pass-signup/', pass_signup, name='pass_signup'),
    path('view-todo/<int:id>', views.view_todo, name='view_todo'),
    path('set-language/', set_language, name='set_language'),

    
]
