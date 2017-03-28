# -*- coding:utf-8 -*-
"""
这个是api相关的路由配置文件
"""
from django.conf.urls import url

from tresult.views import apiview

urlpatterns = [
    # # 添加stats路由
    # url(r'^stats/add/$', api.AddStatsView.as_view(), name="add_stats"),
    # 添加summary
    # url(r'^summary/add/$', api.AddSummaryView.as_view(), name="add_summary"),

    # 执行结果
    # http://127.0.0.1:8000/api/1.0/execute/1/detail/
    url(r'execute/(?P<pk>\d+)/detail/$', apiview.execute_detail, name='detail'),
    # 执行摘要
    url(r'execute/(?P<pk>\d+)/summary/$', apiview.execute_summary,
        name='summary'),
    # 执行统计
    url(r'execute/(?P<pk>\d+)/stats/(?P<type_>.*?)/$', apiview.execute_stats,
        name='stats'),
    # 添加执行统计
    url(r'execute/stats/add/$', apiview.execute_add_stats
        ,
        name='add_stats'),
]
