# -*- coding:utf-8 -*-
"""
用户相关的路由配置
"""
from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^login/', views.LoginView.as_view(), name='login'),
]