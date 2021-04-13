# TCR-Factory: a Web Application for TCR Repertoire Sequencing.
# D. Malko
# 2021

from django.db import models
import re


INDEX_TYPE = (('alfa', 'Alfa'), ('beta', 'Beta'))
INDEX_END = (('I7', 'I7'), ('I5', 'I5'))


def norm_index_type(type):
    if len(type) > 0:
        type = type.lower()
        if type == 'alpha':
            type = 'alfa'
        for itype in INDEX_TYPE:
            if type == itype[0]:
                return type
    return ''


class Smart(models.Model):
    name = models.CharField(max_length=200, unique=True)
    seq = models.CharField(db_index=True, max_length=200, unique=True)
    source = models.CharField(max_length=200)
    date = models.DateField(auto_now_add=True)
    comment = models.TextField(default='')
    seqcore = models.CharField(db_index=True, max_length=200, default='')
    seqmarked = models.CharField(max_length=200, default='')

    @classmethod
    def create(cls, name, seq, source, comment=''):
        seq = seq.upper()
        pattern = re.search(r'([^N]*)(N[NATGCU]+)(.*)', seq)
        if pattern:
            subseq = pattern.group(2)
            subseq = re.sub(r'U', 'T', subseq)
            seqm = pattern.group(1).lower() + subseq + pattern.group(3).lower()
        else:
            raise Exception("Can't find a barcode pattern in the smart sequence.")

        return cls(name=name, seq=seq, source=source, comment=comment, seqcore=subseq, seqmarked=seqm)


class Index(models.Model):
    name = models.CharField(max_length=200, unique=True)
    type = models.CharField(max_length=200, choices=INDEX_TYPE)
    seq = models.CharField(db_index=True, max_length=200, unique=True)
    source = models.CharField(max_length=200)
    date = models.DateField(auto_now_add=True)
    comment = models.TextField(default='')
    seqcore = models.CharField(db_index=True, max_length=200, default='')
    seqmarked = models.CharField(max_length=200, default='')
    end = models.CharField(max_length=200, choices=INDEX_END, default='')

    @classmethod
    def create(cls, name, type, seq, source, comment='', end=''):
        seq = seq.upper()
        pattern = re.search(r'^(.{24})([NATGCU]{6})(.*)', seq)
        if pattern:
            subseq = pattern.group(2)
            subseq = re.sub(r'U', 'T', subseq)
            seqm = pattern.group(1).lower() + subseq + pattern.group(3).lower()
        else:
            raise Exception("Can't find a barcode pattern in the index sequence.")

        return cls(name=name, type=type, seq=seq, source=source, comment=comment, seqcore=subseq, seqmarked=seqm, end=end)

