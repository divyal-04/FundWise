from django.contrib import admin
from django.urls import path,include
from .views import *

urlpatterns = [
    path('login/', Login, name='login'),
    path('register/', Register, name='register'),
    path('logout/', Logout, name='logout'),
    path('forget-password/', ForgetPassword, name='forget_password'),
    path('change-password/<str:token>/', ChangePassword, name='change_password'),
    path('submit-form/', submit_form, name='submit_form'),
    path('', Login),  # Set login as the default page
    path('welcome/', welcome, name='welcome'),

]

