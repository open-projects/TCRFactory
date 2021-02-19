# TCR-Factory: a Web Application for TCR Repertoire Sequencing.
# D. Malko
# 2021

from django.shortcuts import render


def index(request):
    context = {}
    return render(request, 'index.html', context)


def signup_error(request):
    context = {'signup_error': 1}
    return render(request, 'index.html', context)

