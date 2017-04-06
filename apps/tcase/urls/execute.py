# -*- coding:utf-8 -*-
"""
测试结果相关的路由
"""
from django.conf.urls import url
from tresult.views.execute.views import ReportView


urlpatterns = [
    url(r'^(?P<pk>\d+)/report/$', ReportView.as_view(), name='report'),

]