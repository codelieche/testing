# -*- coding:utf-8 -*-
"""
测试结果相关的路由
"""
from django.conf.urls import url
from ..views.execute import views


urlpatterns = [
    url(r'^execute/(?P<pk>\d+)/report/$', views.ReportView.as_view(),
        name='report'),
]