"""
TCRpiper - a pipeline for TCR sequence treatment. Copyright (C) 2020  D. Malko
"""
from django.contrib import admin
from django.urls import include, path, re_path
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('admin/', admin.site.urls),
    path(r'', include('index.urls')),
    path(r'primers/', include('primers.urls')),
    path(r'experiment/', include('experiment.urls')),
    path(r'sample/', include('sample.urls')),
    path(r'configurator/', include('configurator.urls')),
    path(r'filestorage/', include('filestorage.urls')),
    path(r'pipeline/', include('pipeline.urls')),
    path(r'accounts/', include('accounts.urls')),
    #re_path(r'^$', include('tcrpiper.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)