'''
TCRpiper - a pipeline for TCR sequences treatment. Copyright (C) 2020  D. Malko
'''

from django.conf import settings


# open - the experiment has been initiated
# closed - the experiment is ready to be sequenced and processed
# archived - the experiment is complete and deactivated
EXPERIMENT_STATUS = (('open', 'Open'), ('closed', 'Closed'), ('archived', 'Archived'))

# incomplete - tha data is incomplete, the task can't be running
# waiting - server is busy, the task can't be running
# ongoing - the task is running
# ready - the task has finished
RESULT_STATUS = (('incomplete', 'Incomplete'), ('waiting', 'Waiting'), ('ongoing', 'Ongoing'), ('ready', 'Ready'))

WORKFLOW_TYPE = (('GenerateFASTQ', 'Generate FASTQ'), ('other', 'Other'))
APPLICATION_TYPE = (('FASTQ Only', 'FASTQ Only'), ('other', 'Other'))
ASSAY_TYPE = (('TruSeq HT', 'TruSeq HT'), ('other', 'Other'))
CHEMISTRY = (('Amplicon', 'Amplicon'), ('other', 'Other'))
REVCOMPL = (('0', 'No'), ('1', 'Yes'))
DEFAULT_READS = 166
FILE_VERSION = 4

