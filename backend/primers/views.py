# TCR-Factory: a Web Application for TCR Repertoire Sequencing.
# D. Malko
# 2021

from django.shortcuts import render
from django.utils.encoding import smart_str
from django.urls import reverse
from django.http import HttpResponseRedirect

import re

from .models import Smart, Index, norm_index_type


def index(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('index:index'))

    # data upload
    num_uploaded_indexes = -1
    num_uploaded_smarts = -1
    duplicate_indexes = []
    duplicate_smarts = []
    active_indexes_i7 = 'show active'
    active_indexes_i5 = ''
    active_smarts = ''

    if request.POST:
        if request.FILES:
            # append data from a file
            file_type = None
            if 'inputIndexFile' in request.FILES:
                file_type = 'inputIndexFile'
            elif 'inputSmartFile' in request.FILES:
                file_type = 'inputSmartFile'
                active_indexes_i7 = ''
                active_smarts = 'show active'

            if file_type:
                csvfile = request.FILES[file_type]
                for row in re.split(r'\n', smart_str(csvfile.read())):
                    fields = re.split(r'\t', row)
                    if file_type == 'inputIndexFile':
                        if len(fields) == 5 and not re.match(r'source', fields[0]):
                            src = fields[0]
                            tp = norm_index_type(fields[1])
                            nm = fields[2]
                            sq = fields[3]
                            cmt = fields[4]
                            if len(src) > 0 and len(nm) > 0 and len(sq) > 0 and len(tp) > 0:
                                index = Index.create(nm, tp, sq.upper(), src, cmt)
                                if Index.objects.filter(name=nm).exists() or Index.objects.filter(seq=sq).exists():
                                    duplicate_indexes.append(index)
                                else:
                                    index.save()
                                    if num_uploaded_indexes == -1:
                                        num_uploaded_indexes = 0
                                    num_uploaded_indexes += 1
                    elif file_type == 'inputSmartFile':
                        if len(fields) == 4 and not re.match(r'source', fields[0]):
                            src = fields[0]
                            nm = fields[1]
                            sq = fields[2]
                            cmt = fields[3]
                            if len(src) > 0 and len(nm) > 0 and len(sq) > 0:
                                smart = Smart.create(nm, sq.upper(), src, cmt)
                                if Smart.objects.filter(name=nm).exists() or Smart.objects.filter(seq=sq).exists():
                                    duplicate_smarts.append(smart)
                                else:
                                    smart.save()
                                    if num_uploaded_smarts == -1:
                                        num_uploaded_smarts = 0
                                    num_uploaded_smarts += 1
        else:
            # delete data from models
            pattern_index = re.compile(r'indexCheck(\d+)')
            pattern_smart = re.compile(r'smartCheck(\d+)')
            show_tab_smart = 0
            for item in request.POST:
                p_index = re.match(pattern_index, item)
                p_smart = re.match(pattern_smart, item)
                if p_index:
                    index_id = p_index.group(1)
                    Index.objects.filter(id=index_id).delete()
                elif p_smart:
                    smart_id = p_smart.group(1)
                    Smart.objects.filter(id=smart_id).delete()
                    show_tab_smart = 1

            if show_tab_smart:
                active_indexes_i7 = ''
                active_smarts = 'show active'

    # data request
    index_list = Index.objects.order_by('id')
    smart_list = Smart.objects.order_by('id')
    context = {
        'index_list': index_list,
        'index_total': len(index_list),
        'smart_list': smart_list,
        'smart_total': len(smart_list),
        'num_uploaded_indexes': num_uploaded_indexes,
        'num_uploaded_smarts': num_uploaded_smarts,
        'duplicate_indexes': duplicate_indexes,
        'duplicate_smarts': duplicate_smarts,
        'active_indexes_i7': active_indexes_i7,
        'active_smarts': active_smarts,
    }
    return render(request, 'primers.html', context)

# end of main()
