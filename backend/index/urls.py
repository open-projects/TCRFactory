# TCR-Factory: a Web Application for TCR Repertoire Sequencing.
# D. Malko
# 2021

from django.urls import path
from django.contrib import admin

from . import views

app_name = 'index'
urlpatterns = [
    path('', views.index, name='index'),
    path('admin/', admin.site.urls),
]

