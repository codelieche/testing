# -*- coding:utf-8 -*-
"""
项目相关的路由
"""
from django.conf.urls import url
from ..views.project import ProjectListView, ProjectDetailView

urlpatterns = [
    url(r'^list/$', ProjectListView.as_view()),
    url(r'^list/(?P<page>\d+?)/$', ProjectListView.as_view(),
        name='list'),
    url(r'(?P<pk>\d+)/$', ProjectDetailView.as_view(), name='detail'),
]
