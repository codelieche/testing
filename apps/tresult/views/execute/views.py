# -*- coding:utf-8 -*-
"""
这个是显示execute相关的View
"""
from django.shortcuts import render
from django.views.generic import View


class ReportView(View):
    """
    测试报告view
    """
    def get(self, request, pk):
        content = {

        }
        return render(request, 'result/report.html', content)