# TCR-Factory: a Web Application for TCR Repertoire Sequencing.
# D. Malko
# 2021

import re
import os
import shutil
from django.db import models
from django.conf import settings


def path2dir(instance, filename):
    # a file will be uploaded to MEDIA_ROOT/experiment_<id>/<filename>
    return 'experiment_{}/{}'.format(instance.experiment_id, filename)


class File(models.Model):
    experiment_id = models.IntegerField(db_index=True, default=0)
    file = models.FileField(upload_to=path2dir)
    date = models.DateTimeField(auto_now_add=True)


def cleanup(experiment_id):
    files = list()
    dirs = set()
    for item in File.objects.filter(experiment_id=experiment_id):
        files.append(item.file.url)
        dirs.add(re.sub(r'/[^/]+$', '', item.file.path))

        item.file.delete()
        item.delete()

    for dir in dirs:  # remove the rest files
        shutil.rmtree(dir)

    for root, dirs, files in os.walk(settings.MEDIA_ROOT):  # cleanup empty dirs
        for d in dirs:
            dir = os.path.join(root, d)
            if not os.listdir(dir):  # check if dir is empty
                os.rmdir(dir)

    return files

