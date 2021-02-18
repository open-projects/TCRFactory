# TCR-Factory: a Web Application for TCR Repertoire Sequencing.
# D. Malko
# 2021

from django.urls import path

from . import views

app_name = 'configurator'
urlpatterns = [
    path('samplesheet/<int:experiment_id>/', views.samplesheet, name='get_samplesheet'),
    path('sampleinfo/<int:experiment_id>/', views.sampleinfo, name='get_sampleinfo'),
]
