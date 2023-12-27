from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.parent_login, name='parent_login'),
    path('register/', views.parent_register, name='parent_register'),
    path('change_password/<str:token>/', views.parent_change_password, name='parent_change_password'),
    path('forgot_password/', views.parent_forgot_password, name='parent_forgot_password'),
    path('dashboard/', views.parent_dashboard, name='parent_dashboard'),

]
