# -*- coding:utf-8 -*-
"""
项目相关的路由
"""
from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^list/$', views.ProjectListView.as_view()),
    url(r'^list/(?P<page>\d+?)/$', views.ProjectListView.as_view(),
        name='list'),
]
