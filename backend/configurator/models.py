import re
from django.db import models
from django.template.loader import render_to_string
from sample.models import Sample


def makeSamplesheet(experiment):
    sample_list = Sample.objects.filter(experiment_id=experiment.id).order_by('id')  # ordering is important !
    context = {
        'experiment': experiment,
        'sample_list': sample_list,
    }

    return render_to_string('SampleSheet.csv', context)


def makeSampleinfo(experiment):
    paired = experiment.is_pared()

    n = 1
    sample_stings = list()
    for sample in Sample.objects.filter(experiment_id=experiment.id).order_by('id'):  # ordering is important !
        if sample.alfa_index_name:
            alfa_name = sample.get_alfa_name()
            chain = 'TRA'
            barcodes = sample.get_smart_seqcore()
            r1 = '_'.join((re.sub(r'_', '-', alfa_name), 'S' + str(n), 'L001', 'R1', '001.fastq.gz '))  # re.sub(r'_', '-', alfa_name) !!! illumina replaces '_' symbol by '-'
            r2 = ''
            if paired:
                r2 = '_'.join((re.sub(r'_', '-', alfa_name), 'S' + str(n), 'L001', 'R2', '001.fastq.gz '))  # re.sub(r'_', '-', alfa_name) !!! illumina replaces '_' symbol by '-'
            baseline = ''
            subject_id = ''
            antigen = ''
            reads_exp = sample.read_number

            sample_stings.append(
                '\t'.join((alfa_name, chain, barcodes, r1, r2, baseline, subject_id, antigen, str(reads_exp))))
            n += 1

        if sample.beta_index_name:
            beta_name = sample.get_beta_name()
            chain = 'TRB'
            barcodes = sample.get_smart_seqcore()
            r1 = '_'.join((re.sub(r'_', '-', beta_name), 'S' + str(n), 'L001', 'R1', '001.fastq.gz'))  # re.sub(r'_', '-', beta_name) !!! illumina replaces '_' symbol by '-'
            r2 = ''
            if paired:
                r2 = '_'.join((re.sub(r'_', '-', beta_name), 'S' + str(n), 'L001', 'R2', '001.fastq.gz'))  # re.sub(r'_', '-', beta_name) !!! illumina replaces '_' symbol by '-'
            baseline = ''
            subject_id = ''
            antigen = ''
            reads_exp = sample.read_number

            sample_stings.append(
                '\t'.join((beta_name, chain, barcodes, r1, r2, baseline, subject_id, antigen, str(reads_exp))))
            n += 1

    context = {
        'sample_stings': sample_stings,
    }

    return render_to_string('SampleInfo.csv', context)


