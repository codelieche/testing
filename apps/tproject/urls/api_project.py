# -*- coding:utf-8 -*-
"""
项目相关的路由
"""
from django.conf.urls import url
from ..views import api_project

urlpatterns = [
    url(r'^list/$', api_project.ProjectListApiView.as_view(), name="list"),
    url(r'^serverinfo/$', api_project.UpdateProjectServerInfoApiView.as_view(),
        name="serverinfo"),
]
