from django.urls import path

from . import views

app_name = 'filestorage'
urlpatterns = [
    path(r'data_cleanup/', views.data_cleanup, name='data_cleanup'),
    path(r'data_upload/', views.FileUploadView.as_view(), name='data_upload'),
]
