# TCR-Factory: a Web Application for TCR Repertoire Sequencing.
# D. Malko
# 2021

import re
from django.template.loader import render_to_string
from sample.models import Sample
from primers.models import Barcode

def makeSamplesheet(experiment):
    sample_list = Sample.objects.filter(experiment_id=experiment.id).order_by('id')  # ordering is important !
    context = {
        'experiment': experiment,
        'sample_list': sample_list,
    }

    if experiment.type == 'MiSeq':
        return render_to_string('SampleSheet_I7.csv', context)
    if experiment.type == 'NextSeq':
        return render_to_string('SampleSheet_I7_I5.csv', context)

    return 'ERROR: wrong experiment type.'


def makeSampleinfo(experiment):
    paired = experiment.is_pared()

    n = 1
    sample_strings = list()
    for sample in Sample.objects.filter(experiment_id=experiment.id).order_by('id'):  # ordering is important !
        if sample.alfa_index_name:
            alfa_name = sample.get_alfa_name()
            chain = 'TRA'
            barcodes = ''
            if experiment.type == 'MiSeq':
                barcodes = sample.get_smart_seqcore()
            elif experiment.type == 'NextSeq':
                barcodes = Barcode.seqcore

            r1 = '_'.join((re.sub(r'_', '-', alfa_name), 'S' + str(n), 'L001', 'R1', '001.fastq.gz '))  # re.sub(r'_', '-', alfa_name) !!! illumina replaces '_' symbol by '-'
            r2 = ''
            if paired:
                r2 = '_'.join((re.sub(r'_', '-', alfa_name), 'S' + str(n), 'L001', 'R2', '001.fastq.gz '))  # re.sub(r'_', '-', alfa_name) !!! illumina replaces '_' symbol by '-'
            baseline = ''
            subject_id = ''
            antigen = ''
            reads_exp = sample.read_number

            sample_strings.append(
                '\t'.join((alfa_name, chain, barcodes, r1, r2, baseline, subject_id, antigen, str(reads_exp))))
            n += 1

        if sample.beta_index_name:
            beta_name = sample.get_beta_name()
            chain = 'TRB'
            barcodes = ''
            if type == 'MiSeq':
                barcodes = sample.get_smart_seqcore()
            elif type == 'NextSeq':
                barcodes = Barcode.seqcore

            r1 = '_'.join((re.sub(r'_', '-', beta_name), 'S' + str(n), 'L001', 'R1', '001.fastq.gz'))  # re.sub(r'_', '-', beta_name) !!! illumina replaces '_' symbol by '-'
            r2 = ''
            if paired:
                r2 = '_'.join((re.sub(r'_', '-', beta_name), 'S' + str(n), 'L001', 'R2', '001.fastq.gz'))  # re.sub(r'_', '-', beta_name) !!! illumina replaces '_' symbol by '-'
            baseline = ''
            subject_id = ''
            antigen = ''
            reads_exp = sample.read_number

            sample_strings.append(
                '\t'.join((beta_name, chain, barcodes, r1, r2, baseline, subject_id, antigen, str(reads_exp))))
            n += 1

    context = {
        'sample_strings': sample_strings,
    }

    return render_to_string('SampleInfo.csv', context)


