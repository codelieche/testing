# -*- coding:utf-8 -*-
"""
这个是api相关的路由配置文件
"""
from django.conf.urls import url, include

# from tresult.views.execute import api as execute_api

urlpatterns = [
    url(r'^execute/', include('tresult.urls.execute', namespace="execute")),
    # # 执行结果
    # # http://127.0.0.1:8000/api/1.0/execute/1/detail/
    # url(r'execute/(?P<pk>\d+)/detail/$', execute_api.execute_detail,
    #     name='detail'),
    # # 执行摘要
    # url(r'execute/(?P<pk>\d+)/summary/$', execute_api.execute_summary,
    #     name='summary'),
    # # 执行统计
    # url(r'execute/(?P<pk>\d+)/stats/(?P<type_>.*?)/$', execute_api.execute_stats,
    #     name='stats'),
    # # 添加执行统计
    # url(r'execute/stats/add/$', execute_api.execute_add_stats, name='add_stats'),
]
