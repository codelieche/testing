# -*- coding:utf-8 -*-
"""
这个文件主要是提供：
1、通过case的id获取到最近的execute id
2、如果最近的execute id是空 就创建一个
"""
from datetime import datetime

from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from django.views.generic import View

from utils.mixins import CsrfExemptMixin
from ..models import Case, Execute


class CaseExecute(CsrfExemptMixin, View):
    """
    通过Case id获取Execute的View
    # 如果是post，就表示，如果没有就创建一个，然后返回新的execute_id
    """
    def get(self, request, pk):
        case = get_object_or_404(Case, pk=pk)
        # 判断是否存在execute id
        if case.execute_id:
            return JsonResponse({'execute_id': case.execute_id})
        else:
            return JsonResponse({'execute_id': None})

    def post(self, request, pk):
        case = get_object_or_404(Case, pk=pk)
        # 判断是否存在execute id
        if case.execute_id:
            return JsonResponse({'execute_id': case.execute_id})
        else:
            # 表示还没有execute_id
            # 那就创建一个返回
            execute_name = case.name + datetime.now().strftime("%Y%m%d%H%M%S")
            execute = Execute.objects.create(case=case, name=execute_name)
            case.execute_id = execute.id
            case.save()
            return JsonResponse({'execute_id': case.execute_id})
