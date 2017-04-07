# -*- coding:utf-8 -*-
"""
这个是execute执行结果 相关api的路由配置文件
"""
from django.conf.urls import url

from tcase.views.api import ExecuteUpdateStatus
from tresult.views.execute import api

from ..views.execute.locust_handle import LocustStart, LocustAddUser,\
    LocustStop

urlpatterns = [
    # 执行结果
    # http://127.0.0.1:8000/api/1.0/execute/1/detail/
    url(r'(?P<pk>\d+)/detail/$', api.execute_detail, name='detail'),
    # 执行摘要
    url(r'(?P<pk>\d+)/summary/$', api.execute_summary, name='summary'),
    # 执行统计
    url(r'(?P<pk>\d+)/stats/(?P<type_>.*?)/$', api.execute_stats, name='stats'),
    # 添加执行统计
    url(r'^stats/add/$', api.execute_add_stats, name='add_stats'),
    # 获取日志
    url(r'(?P<pk>\d+)/log/$', api.execute_log, name='log'),
    # 添加日志
    url(r'^log/add/$', api.execute_add_log, name='add_log'),

    # 更新execute的状态
    # http://127.0.0.1:8000/api/1.0/execute/6/update/status/
    url(r'(?P<pk>\d+)/update/status/', ExecuteUpdateStatus.as_view(),
        name='update_status'),

    # 开启locust
    url('^locust/start/$', LocustStart.as_view(), name='locust_start'),
    # 增加locust用户数
    url('^locust/user/add/$', LocustAddUser.as_view(), name='locust_user_add'),
    # 停止locust
    url('^locust/stop/$', LocustStop.as_view(), name='locust_stop'),
]