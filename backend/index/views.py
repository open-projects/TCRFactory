# TCR-Factory: a Web Application for TCR Repertoire Sequencing.
# D. Malko
# 2021

from django.shortcuts import render


def index(request):
    context = {}
    return render(request, 'index.html', context)

