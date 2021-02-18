# TCR-Factory: a Web Application for TCR Repertoire Sequencing.
# D. Malko
# 2021

from django.urls import path

from . import views

app_name = 'accounts'
urlpatterns = [
    path(r'sign_in/', views.sign_in, name="sign_in"),
    path(r'sign_up/', views.sign_up, name="sign_up"),
    path(r'sign_out/', views.sign_out, name='sign_out'),
]

