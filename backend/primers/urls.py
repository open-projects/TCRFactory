# TCR-Factory: a Web Application for TCR Repertoire Sequencing.
# D. Malko
# 2021

from django.urls import path

from . import views

app_name = 'primers'
urlpatterns = [
    path('', views.index, name='index'),
]
