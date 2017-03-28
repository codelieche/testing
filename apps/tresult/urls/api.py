# -*- coding:utf-8 -*-
"""
这个是api相关的路由配置文件
"""
from django.conf.urls import url

from tresult.views import api

urlpatterns = [
    # 添加stats路由
    url(r'^stats/add/$', api.AddStatsView.as_view(), name="add_stats"),
    # 添加summary
    url(r'^summary/add/$', api.AddSummaryView.as_view(), name="add_summary"),
]
