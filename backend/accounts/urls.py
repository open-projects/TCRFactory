from django.urls import path
from django.contrib import admin

from . import views

app_name = 'accounts'
urlpatterns = [
    path(r'sign_in/', views.sign_in, name="sign_in"),
    path(r'sign_up/', views.sign_up, name="sign_up"),
    path(r'sign_out/', views.sign_out, name='sign_out'),
]

