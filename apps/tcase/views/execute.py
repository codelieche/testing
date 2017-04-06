# -*- coding:utf-8 -*-
"""
execute相关的view
"""
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import View
from django.core.urlresolvers import reverse

from tresult.views.execute.views import ReportView
from ..models import Execute


class ExecuteView(View):
    """
    进入execute的调度View
    如果execute的状态是created、ready就进入running的页面
    如果是其它状态，就进入report页面
    # 因为running  和 report 整合到一起代码量太大，就分开成2个
    """
    def get(self, request, pk):
        execute = get_object_or_404(Execute, pk=pk)
        if execute.status in ['created', 'ready', 'running']:
            return redirect(reverse('execute:running', args=[pk]))
        return redirect(reverse('execute:report', args=[pk]))


class ExecuteRunningView(View):
    """
    执行execute的View
    """
    def get(self, request, pk):
        execute = get_object_or_404(Execute, pk=pk)
        # 如果execute的状态不是running那么就跳转去report页面
        if execute.status in ['stoped', 'failure', 'success']:
            return redirect(reverse('execute:report', args=[pk]))

        return render(request, 'execute/running.html')
