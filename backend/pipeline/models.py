'''
TCRpiper - a pipeline for TCR sequences treatment. Copyright (C) 2020  D. Malko
'''

import psutil
from django.db import models


class TaskQueue(models.Model):
    experiment_id = models.IntegerField(db_index=True)
    thread = models.IntegerField(db_index=True, default=0, unique=True)
    pid = models.IntegerField(db_index=True, default=0)
    cmd = models.CharField(max_length=200)
    output_file = models.CharField(max_length=200, default='')
    date = models.DateTimeField(auto_now_add=True)


def taskRemover():
    n = 0
    for task in TaskQueue.objects.all():
        pid = task.pid
        if pid > 0 and psutil.pid_exists(pid):
            process = psutil.Process(pid)
            # if the process becomes a zombie we will kill it and its children
            if process.status() == psutil.STATUS_ZOMBIE:
                for proc in process.children(recursive=True):
                    proc.kill()
                process.kill()
        else:
            # a process was not ran but the record was added to 'TaskQueue'
            task.delete()
            n += 1

    return n

