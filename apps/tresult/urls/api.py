# _*_ coding:utf-8 _*_
"""
这个是api相关的路由配置文件
"""
from django.conf.urls import url

from tresult.views import api

urlpatterns = [
    url('^stats', api.StatsView.as_view(), name="add_stats")
]
