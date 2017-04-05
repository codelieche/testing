# -*- coding:utf-8 -*-
"""
这个文件主要是提供：
1、通过case的id获取到最近的execute id
2、如果最近的execute id是空 就创建一个
"""
from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from django.views.generic import View

from ..models import Case

class CaseExecute(View):
    """
    通过Case id获取Execute的View
    """
    def get(self, request, pk):
        case = get_object_or_404(Case, pk=pk)
        # 判断是否存在execute id
        if case.execute_id:
            return JsonResponse({'execute_id': case.execute_id})
        else:
            return JsonResponse({'execute_id': None})
