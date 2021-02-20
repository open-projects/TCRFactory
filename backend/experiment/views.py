# TCR-Factory: a Web Application for TCR Repertoire Sequencing.
# D. Malko
# 2021

import re
import os.path
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.http import Http404
from django.urls import reverse
from django.contrib.auth.decorators import login_required

from .models import Experiment
from .settings import APPLICATION_TYPE, WORKFLOW_TYPE, ASSAY_TYPE, CHEMISTRY, REVCOMPL, DEFAULT_READS, FILE_VERSION
from sample.models import Sample
from filestorage.models import File, cleanup


#@login_required
def stock(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('index:index'))

    experiment_list = Experiment.objects.order_by('id').reverse()
    for experiment in experiment_list:
        out_file = experiment.output_file
        try:
            # check the status of the experiment
            file_list = File.objects.filter(experiment_id=experiment.id)
            if not file_list:
                experiment.output_status = 'incomplete'
                experiment.save()
            elif experiment.output_status == 'ready' and not os.path.exists(out_file):
                experiment.output_status = 'waiting'
                experiment.save()
            elif experiment.output_status == 'ongoing' and os.path.exists(out_file):
                experiment.output_status = 'ready'
                experiment.save()
            elif experiment.output_status == 'waiting' and os.path.exists(out_file):
                experiment.output_status = 'ready'
                experiment.save()
        except Exception:
            raise Http404("Can't check the experiment status!")

    context = {
        'experiment_list': experiment_list,
        'num_of_experiments': len(experiment_list),
    }

    return render(request, 'experiment_stock.html', context)


def set(request, experiment_id=0):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('index:index'))

    if experiment_id:
        try:
            experiment = Experiment.objects.get(id=experiment_id)
        except Exception:
            #raise Http404("Experiment does not exist")
            return HttpResponseRedirect(reverse('experiment:experiment_stock'))

        experiment.status = request.POST['experiment_status']
        experiment.iem_file_version = request.POST['iem_file_version']
        experiment.name = re.sub(r'[ _]+', '_', request.POST['experiment_name'])
        experiment.workflow = request.POST['workflow']
        experiment.application = request.POST['application']
        experiment.assay = request.POST['assay']
        experiment.chemistry = request.POST['chemistry']
        experiment.description = request.POST['description']
        experiment.reads_1 = int(request.POST['reads_1'])
        experiment.reads_2 = int(request.POST['reads_2']) if request.POST['reads_2'] else 0
        experiment.rev_compl = request.POST['rev_compl']

        experiment.save()

    else:
        try:
            experiment = Experiment(status=request.POST['experiment_status'],
                                    iem_file_version=request.POST['iem_file_version'],
                                    name=re.sub(r'[ _]+', '_', request.POST['experiment_name']),
                                    workflow=request.POST['workflow'],
                                    application=request.POST['application'],
                                    assay=request.POST['assay'],
                                    chemistry=request.POST['chemistry'],
                                    description=request.POST['description'],
                                    reads_1=request.POST['reads_1'],
                                    reads_2=request.POST['reads_2'] if request.POST['reads_2'] else 0,
                                    rev_compl=request.POST['rev_compl'],
                                   )
            experiment.save()
        except Exception:
            raise Http404("Bad request for New Experiment")

    return HttpResponseRedirect(reverse('experiment:experiment_stock'))


def get(request, experiment_id=0):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('index:index'))

    if experiment_id:
        try:
            experiment = Experiment.objects.get(id=experiment_id)
        except Exception:
            #raise Http404("Experiment does not exist")
            return HttpResponseRedirect(reverse('experiment:experiment_stock'))

        sample_list = Sample.objects.filter(experiment_id=experiment.id).order_by('id').reverse()
        context = {
            'experiment_id': experiment.id,
            'experiment_status': experiment.status,
            'iem_file_version': experiment.iem_file_version,
            'experiment_name': experiment.name,
            'description': experiment.description,

            'workflow': experiment.workflow,
            'application': experiment.application,
            'assay': experiment.assay,
            'chemistry': experiment.chemistry,
            'rev_compl': str(experiment.rev_compl),  # str() is important !!!

            'workflow_list': WORKFLOW_TYPE,
            'application_list': APPLICATION_TYPE,
            'assay_list': ASSAY_TYPE,
            'chemistry_list': CHEMISTRY,
            'rev_compl_list': REVCOMPL,
            'reads_1': experiment.reads_1,
            'reads_2': experiment.reads_2,
            'sample_list': sample_list,
            'num_of_samples': len(sample_list)
        }
    else:  # new experiment
        seqtype = None
        if request.method == "POST" and 'seqtype' in request.POST:
            seqtype = request.POST['seqtype']
        else:
            return HttpResponseRedirect(reverse('experiment:experiment_stock'))

        if seqtype == 'miseq':
            ...
        elif seqtype == 'nextseq':
            ...
        else:
            return HttpResponseRedirect(reverse('experiment:experiment_stock'))

        context = {
            'experiment_id': 0,
            'experiment_status': 'open',
            'iem_file_version': FILE_VERSION,
            'experiment_name': '',
            'description': '',

            'workflow': None,
            'application': None,
            'assay': None,
            'chemistry': None,
            'rev_compl': None,

            'workflow_list': WORKFLOW_TYPE,
            'application_list': APPLICATION_TYPE,
            'assay_list': ASSAY_TYPE,
            'chemistry_list': CHEMISTRY,
            'rev_compl_list': REVCOMPL,
            'reads_1': DEFAULT_READS,
            'reads_2': DEFAULT_READS,
            'sample_list': list(),
            'num_of_samples': 0
        }

    return render(request, 'experiment.html', context)


def delete(request, experiment_id):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('index:index'))

    try:
        experiment = Experiment.objects.get(id=experiment_id)
    except Exception:
        #raise Http404("Experiment does not exist")
        return HttpResponseRedirect(reverse('experiment:experiment_stock'))

    for sample in Sample.objects.filter(experiment_id=experiment_id):
        sample.delete()

    experiment.delete()

    return HttpResponseRedirect(reverse('experiment:experiment_stock'))


def archive(request, experiment_id):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('index:index'))

    try:
        experiment = Experiment.objects.get(id=experiment_id)
    except Exception:
        #raise Http404("Experiment does not exist")
        return HttpResponseRedirect(reverse('experiment:experiment_stock'))

    experiment.status = 'archived'
    experiment.save()

    return HttpResponseRedirect(reverse('experiment:experiment_stock'))


def submit(request, experiment_id):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('index:index'))

    try:
        experiment = Experiment.objects.get(id=experiment_id)
    except Exception:
        raise Http404("Experiment does not exist")
    experiment.status = 'closed'
    experiment.save()

    return HttpResponseRedirect(reverse('experiment:experiment_stock'))


def open(request, experiment_id):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('index:index'))

    try:
        experiment = Experiment.objects.get(id=experiment_id)
    except Exception:
        raise Http404("Experiment does not exist")
    experiment.status = 'open'
    experiment.save()

    return HttpResponseRedirect(reverse('experiment:experiment_stock'))


def processing(request, experiment_id=0):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('index:index'))

    if experiment_id:
        try:
            experiment = Experiment.objects.get(id=experiment_id)
        except Exception:
            #raise Http404("Experiment does not exist")
            return HttpResponseRedirect(reverse('experiment:experiment_stock'))

        sample_list = Sample.objects.filter(experiment_id=experiment.id).order_by('id').reverse()
        file_list = File.objects.filter(experiment_id=experiment.id)
        context = {
            'experiment_id': experiment.id,
            'experiment_status': experiment.status,
            'sample_list': sample_list,
            'num_of_samples': len(sample_list),
            'file_list': file_list,
            'num_of_files': len(file_list),
            'settings': [
                ['IEM File Version', experiment.iem_file_version],
                ['Experiment name', experiment.name],
                ['Description', experiment.description],
                ['Workflow', experiment.workflow],
                ['Application', experiment.application],
                ['Assay', experiment.assay],
                ['Chemistry', experiment.chemistry],
                ['Reverse/Complement', str(experiment.rev_compl)],  # str() is important !!!
                ['Reads 1', experiment.reads_1],
                ['Reads 2', experiment.reads_2]
            ]
        }
        return render(request, 'experiment_processing.html', context)
    return HttpResponseRedirect(reverse('experiment:experiment_stock'))

