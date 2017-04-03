"""webpts URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin

from tproject.views import ProjectListView

urlpatterns = [
    # 首页
    url(r'^$', ProjectListView.as_view(), name="index"),
    url(r'^admin/', admin.site.urls),
    # 项目相关的路由
    url(r'^project/', include('tproject.urls', namespace='project')),
    # 用户相关的路由
    url(r'^user/', include('account.urls', namespace='user')),
    # 测试结果api
    url(r'^api/1.0/', include('tresult.urls.api', namespace="api")),
    # 首页
    url(r'^', include('tcase.urls', namespace="tcase")),
    # 测试结果tresult app路由
    url(r'^', include('tresult.urls.result', namespace='result')),
]
