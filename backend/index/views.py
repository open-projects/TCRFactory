# TCR-Factory: a Web Application for TCR Repertoire Sequencing.
# D. Malko
# 2021

from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse


def index(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect(reverse('experiment:experiment_stock'))

    context = {'signup_error': 0, 'signin_error': 0}
    return render(request, 'index.html', context)


def signup_error(request):
    context = {'signup_error': 1, 'signin_error': 0}
    return render(request, 'index.html', context)


def signin_error(request):
    context = {'signup_error': 0, 'signin_error': 1}
    return render(request, 'index.html', context)

