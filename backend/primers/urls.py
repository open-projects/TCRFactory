'''
TCRpiper - a pipeline for TCR sequence treatment. Copyright (C) 2020  D. Malko
'''

from django.urls import path

from . import views

app_name = 'primers'
urlpatterns = [
    path('', views.index, name='index'),
]
