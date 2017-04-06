# -*- coding:utf-8 -*-
"""
测试结果相关的路由
"""
from django.conf.urls import url

from tresult.views.execute.views import ReportView
from ..views.execute import ExecuteView, ExecuteRunningView

urlpatterns = [
    # execute去running还是report页面的过渡路由
    url(r'(?P<pk>\d+)/$', ExecuteView.as_view(), name='go'),
    # execute running page
    url(r'^(?P<pk>\d+)/running/$', ExecuteRunningView.as_view(),
        name='running'),
    # 报告页
    url(r'^(?P<pk>\d+)/report/$', ReportView.as_view(), name='report'),
]