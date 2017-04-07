# -*- coding:utf-8 -*-
"""
这个是显示execute相关的View
"""
from django.shortcuts import render, get_object_or_404
from django.views.generic import View

from tcase.models import Execute


class ReportView(View):
    """
    测试报告view
    """
    def get(self, request, pk):
        # 先获取到execute对象
        execute = get_object_or_404(Execute, pk=pk)

        content = {
            'execute': execute
        }
        return render(request, 'execute/report.html', content)
