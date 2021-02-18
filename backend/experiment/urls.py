'''
TCRpiper - a pipeline for TCR sequences treatment. Copyright (C) 2020  D. Malko
'''

from django.urls import path

from . import views

app_name = 'experiment'
urlpatterns = [
    path('', views.stock, name='experiment_stock'),
    path('get/', views.get, name='experiment_new'),
    path('set/<int:experiment_id>/', views.set, name='experiment_set'),
    path('get/<int:experiment_id>/', views.get, name='experiment_get'),
    path('del/<int:experiment_id>/', views.delete, name='experiment_del'),
    path('arch/<int:experiment_id>/', views.archive, name='experiment_arch'),
    path('sub/<int:experiment_id>/', views.submit, name='experiment_sub'),
    path('proc/<int:experiment_id>/', views.processing, name='experiment_proc'),
    path('open/<int:experiment_id>/', views.open, name='experiment_open'),
]
