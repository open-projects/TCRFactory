from django.shortcuts import render
from django.http import HttpResponse
from django.http import Http404
from django.template import loader

import re
from datetime import datetime


def index(request):
    context = {}
    return render(request, 'index.html', context)

