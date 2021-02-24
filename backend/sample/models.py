# TCR-Factory: a Web Application for TCR Repertoire Sequencing.
# D. Malko
# 2021

from django.db import models
from primers.models import Smart, Index
import re


COMPLEMENT = {'A': 'T', 'C': 'G', 'G': 'C', 'T': 'A'}


class Sample(models.Model):
    experiment_id = models.IntegerField(db_index=True)
    name = models.CharField(max_length=200, default='')
    project = models.CharField(max_length=200)
    ident = models.CharField(max_length=200)
    plate = models.CharField(max_length=200, default='')
    well = models.CharField(max_length=200, default='')
    cell_number = models.IntegerField(default=0)
    read_number = models.IntegerField(default=0)
    smart_name = models.CharField(max_length=200, default='')
    smart_benchling = models.CharField(max_length=200, default='')
    alfa_subsample_ident = models.CharField(max_length=200, default='')  # sample_ID = sample_ident + alfa_subsample_ident
    alfa_index_name = models.CharField(max_length=200, default='')
    alfa_index_benchling = models.CharField(max_length=200, default='')
    beta_subsample_ident = models.CharField(max_length=200, default='')  # sample_ID = sample_ident + beta_subsample_ident
    beta_index_name = models.CharField(max_length=200, default='')
    beta_index_benchling = models.CharField(max_length=200, default='')
    comments = models.TextField(default='')
    date = models.DateField(auto_now_add=True)
    owner = models.CharField(max_length=200, default='Unknown')

    def type(self):
        if self.alfa_index_name == '' and self.beta_index_name == '':
            return 'ab'
        elif self.alfa_index_name == '':
            return 'a'
        else:
            return 'b'

    def get_alfa_ident(self):
        ident = str(self.ident) + '_' + str(self.alfa_subsample_ident)
        ident = re.sub(r'[ _]+', '_', ident)
        return ident

    def get_beta_ident(self):
        ident = str(self.ident) + '_' + str(self.beta_subsample_ident)
        ident = re.sub(r'[ _]+', '_', ident)
        return ident

    def get_alfa_name(self):
        ident = str(self.ident) + '_' + str(self.alfa_subsample_ident)
        ident = re.sub(r'[ _]+', '_', ident)
        return ident

    def get_beta_name(self):
        ident = str(self.ident) + '_' + str(self.beta_subsample_ident)
        ident = re.sub(r'[ _]+', '_', ident)
        return ident

    def get_smart(self):
        for smart in Smart.objects.filter(name=self.smart_name):
            return smart
        return None

    def get_smart_seqcore(self):
        for smart in Smart.objects.filter(name=self.smart_name):
            return smart.seqcore
        return ''

    def get_smart_seqcore_rev(self):
        for smart in Smart.objects.filter(name=self.smart_name):
            if len(smart.seqcore) > 0:
                seqcore = "".join(COMPLEMENT.get(base, base) for base in reversed(smart.seqcore))
            return seqcore
        return ''

    def get_alfa_index(self):
        for index in Index.objects.filter(name=self.alfa_index_name):
            return index
        return None

    def get_alfa_index_seqcore(self):
        for index in Index.objects.filter(name=self.alfa_index_name):
            seqcore = index.seqcore
            if len(seqcore) > 0:
                return seqcore
        return ''

    def get_alfa_index_seqcore_rev(self):
        for index in Index.objects.filter(name=self.alfa_index_name):
            seqcore = index.seqcore
            if len(seqcore) > 0:
                seqcore = "".join(COMPLEMENT.get(base, base) for base in reversed(seqcore))
                return seqcore
        return ''

    def get_beta_index(self):
        for index in Index.objects.filter(name=self.beta_index_name):
            return index
        return None

    def get_beta_index_seqcore(self):
        for index in Index.objects.filter(name=self.beta_index_name):
            seqcore = index.seqcore
            if len(seqcore) > 0:
                return seqcore
        return ''

    def get_beta_index_seqcore_rev(self):
        for index in Index.objects.filter(name=self.beta_index_name):
            seqcore = index.seqcore
            if len(seqcore) > 0:
                seqcore = "".join(COMPLEMENT.get(base, base) for base in reversed(seqcore))
                return seqcore
        return ''

    def get_chain(self):
        if self.alfa_index_name != '' and self.beta_index_name == '':
            return 'TRA'
        if self.alfa_index_name == '' and self.beta_index_name != '':
            return 'TRB'
        return 'TRX'


class UsedBarcode:
    def __init__(self, sample):
        self.sample_ident = sample.ident
        self.owner = sample.owner
        self.smart_name = sample.smart_name
        self.smart_seqcore = sample.get_smart_seqcore()
        self.alfa_index_name = sample.alfa_index_name
        self.alfa_index_seqcore = sample.get_alfa_index_seqcore()
        self.beta_index_name = sample.beta_index_name
        self.beta_index_seqcore = sample.get_beta_index_seqcore()


class IdContainer:
    def __init__(self):
        self.barcodes = list()
        self.smarts = set()
        self.indexes = set()

    def append(self, barcode):
        self.barcodes.append(barcode)
        if barcode.smart_seqcore:
            self.smarts.add(barcode.smart_seqcore)
        if barcode.alfa_index_seqcore:
            self.indexes.add(barcode.alfa_index_seqcore)
        if barcode.beta_index_seqcore:
            self.indexes.add(barcode.beta_index_seqcore)

