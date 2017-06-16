# -*- coding:utf-8 -*-
"""
整站api相关的路由配置
"""
from django.conf.urls import url, include

urlpatterns = [
    url(r'^case/', include('tcase.urls.api_case', namespace='case')),
    # 执行测试用例 execute的api
    url(r'^execute/', include('tresult.urls.api_execute', namespace="execute")),
    # execute删除api
    url(r'^execute/', include('tcase.urls.api_execute', namespace='execute')),
    # 请求事务相关的api
    url('^shiwu/', include('tcase.urls.api_shiwu', namespace='shiwu')),
    # 项目相关的api
    url('^project/', include('tproject.urls.api_project', namespace='project')),
]
