# -*- coding:utf-8 -*-
"""
整站api相关的路由配置
"""
from django.conf.urls import url, include

urlpatterns = [
    url(r'^execute/', include('tresult.urls.api_execute', namespace="execute")),
    url(r'^case/', include('tcase.urls.api', namespace='case')),

]
