'''
TCRpiper - a pipeline for TCR sequences treatment. Copyright (C) 2020  D. Malko
'''

from django.urls import path

from . import views

app_name = 'pipeline'
urlpatterns = [
    path('get/<int:experiment_id>/', views.get, name='pipeline_get'),
    path('download/<int:experiment_id>/', views.download, name='pipeline_download'),
]
