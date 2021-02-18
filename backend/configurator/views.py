# TCR-Factory: a Web Application for TCR Repertoire Sequencing.
# D. Malko
# 2021

from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.urls import reverse

from experiment.models import Experiment
from .models import makeSamplesheet, makeSampleinfo
from .settings import SAMPLE_INFO_FILENAME, SAMPLE_SHEET_FILENAME


def samplesheet(request, experiment_id=0):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('index:index'))

    if experiment_id:
        try:
            experiment = Experiment.objects.get(id=experiment_id)
        except Exception:
            #raise Http404("Experiment does not exist")
            return HttpResponseRedirect(reverse('experiment:experiment_stock'))

    message = makeSamplesheet(experiment)
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="' + SAMPLE_SHEET_FILENAME + '"'
    response.write(message)

    return response


def sampleinfo(request, experiment_id=0):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('index:index'))

    if experiment_id:
        try:
            experiment = Experiment.objects.get(id=experiment_id)
        except Exception:
            #raise Http404("Experiment does not exist")
            return HttpResponseRedirect(reverse('experiment:experiment_stock'))

    message = makeSampleinfo(experiment)
    response = HttpResponse(content_type='text/txt')
    response['Content-Disposition'] = 'attachment; filename="' + SAMPLE_INFO_FILENAME + '"'
    response.write(message)

    return response

