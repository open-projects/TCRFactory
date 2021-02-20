# TCR-Factory: a Web Application for TCR Repertoire Sequencing.
# D. Malko
# 2021

import shutil
from django.db import models

from sample.models import Sample
from filestorage.models import cleanup
from .settings import EXPERIMENT_STATUS, FILE_VERSION, WORKFLOW_TYPE, APPLICATION_TYPE
from .settings import ASSAY_TYPE, CHEMISTRY, REVCOMPL, RESULT_STATUS, EXPERIMENT_TYPES


class Experiment(models.Model):
    status = models.CharField(max_length=200, choices=EXPERIMENT_STATUS, default='open')
    # [Header]
    iem_file_version = models.CharField(max_length=200, default=FILE_VERSION)
    name = models.CharField(max_length=200)
    date = models.DateField(auto_now_add=True)
    workflow = models.CharField(max_length=200, choices=WORKFLOW_TYPE, default='GenerateFASTQ')
    application = models.CharField(max_length=200, choices=APPLICATION_TYPE, default='FASTQ Only')
    assay = models.CharField(max_length=200, choices=ASSAY_TYPE, default='TruSeq HT')
    chemistry = models.CharField(max_length=200, choices=CHEMISTRY, default='Amplicon')
    description = models.TextField(default='')
    # [Reads]
    reads_1 = models.IntegerField(default=0)
    reads_2 = models.IntegerField(default=0)
    # [Settings]
    rev_compl = models.IntegerField(choices=REVCOMPL, default=0)
    # adapter = models.CharField(max_length=200, default='AGATCGGAAGAGCACACGTCTGAACTCCAGTCA')
    # adapter_read2 = models.CharField(max_length=200, default='AGATCGGAAGAGCGTCGTGTAGGGAAAGAGTGT')
    output_status = models.CharField(max_length=200, choices=RESULT_STATUS, default='incomplete')
    output_dir = models.CharField(max_length=200, default='')
    output_file = models.CharField(max_length=200, default='')
    type = models.CharField(max_length=200, choices=EXPERIMENT_TYPES, default='miseq')

    def delete(self, using=None, keep_parents=False):
        try:
            cleanup(self.id)  # delete files associated with the Experiment object
            shutil.rmtree(self.output_dir)  # delete the rest files
        except Exception:
            print("can't remove output dir for experiment {}".format(self.id))
        super().delete(using=using, keep_parents=keep_parents)  # delete the Experiment object

    def num_of_samples(self):
        sample_list = Sample.objects.filter(experiment_id=self.id)
        return len(sample_list)

    def is_pared(self):
        if self.reads_1 and self.reads_2:
            return True
        return False

