# -*- coding:utf-8 -*-
"""
execute相关的view
"""
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import View
from django.core.urlresolvers import reverse

from tresult.views.execute.views import ReportView
from ..models import Execute
from ..tasks import run_execute


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
    # 需要做的事情：
    1、判断状态是不是stoped、failure、success。如果是就跳转去报告页面
    2、判断状态是不是running：如果是就直接进入running页面
    3、如果状态是created、ready。先改变状态为running
    4、异步启动locust的服务器。
    5、通过api开启测试，并收集数据
    6、后续：逐渐增加并发用户数
    7、每10秒重新渲染一次页面：js调用api来实现
    """

    def get(self, request, pk):
        execute = get_object_or_404(Execute, pk=pk)
        # 如果execute的状态不是running那么就跳转去report页面
        print(execute.status)
        if execute.status in ['stoped', 'failure', 'success']:
            return redirect(reverse('execute:report', args=[pk]))
        elif execute.status in ['created', 'ready']:
            # 如果状态是created、ready。需要启动下后台的locust服务
            run_execute.delay(execute_id=execute.id,
                              host='http://www.wodehappy.com')
            # 在这个异步的run_execute函数中，做了4件事情
            # 1、寻找可以用的端口号，启动脚本
            # 2、点击开始执行
            # 3、逐步的添加并发用户数，直到失败，或者直到指定时间
            # 4、try catch finaly  最后判断execute 如果还是running就停止locust脚本
            # TODO：等待编码
        content = {
            'execute': execute,
        }
        return render(request, 'execute/running.html', content)
