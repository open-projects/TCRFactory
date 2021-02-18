# TCR-Factory: a Web Application for TCR Repertoire Sequencing.
# D. Malko
# 2021

from django.urls import path

from . import views

app_name = 'pipeline'
urlpatterns = [
    path('get/<int:experiment_id>/', views.get, name='pipeline_get'),
    path('download/<int:experiment_id>/', views.download, name='pipeline_download'),
]
