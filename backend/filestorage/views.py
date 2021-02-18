import os
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views import View
from django import forms
from django.conf import settings

from .models import File, cleanup


class FileForm(forms.ModelForm):
    class Meta:
        model = File
        fields = ('experiment_id', 'file', )


class FileUploadView(View):
    def post(self, request):
        form = FileForm(self.request.POST, self.request.FILES)
        if form.is_valid():
            data = form.save()
            context = {
                'is_valid': True,
                'name': data.file.name,
                'url': data.file.url
            }
        else:
            context = {'is_valid': False}
        return JsonResponse(context)


def data_cleanup(request):
    cleanup(request.POST.get('experiment_id'))

    return redirect(request.POST.get('next'))

