'''
TCRpiper - a pipeline for TCR sequence treatment. Copyright (C) 2020  D. Malko
'''

from django.urls import path

from . import views


app_name = 'sample'
urlpatterns = [
    path('get/<int:experiment_id>/', views.get, name='sample_new'),
    path('get/<int:experiment_id>/', views.save, name='sample_save'),
    path('get/<int:experiment_id>/<int:sample_id>/', views.get, name='sample_get'),
    path('set/<int:experiment_id>/<int:sample_id>/', views.set, name='sample_set'),
    path('del/<int:experiment_id>/<int:sample_id>/', views.delete, name='sample_del'),
]
