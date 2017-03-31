# -*- coding:utf-8 -*-
"""
用户相关的路由配置
"""
from django.conf.urls import url

from . import views

urlpatterns = [
    # 用户登录
    url(r'^login/', views.LoginView.as_view(), name='login'),
    # 退出登录
    url(r'^logout/', views.LogoutView.as_view(), name='logout'),
]