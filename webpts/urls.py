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
    # 网站api
    url(r'^api/1.0/', include('webpts.urls_api', namespace="api")),
    # 测试用例
    url(r'^case/', include('tcase.urls.case', namespace="case")),
    # execute相关的路由
    url(r'^execute/', include('tcase.urls.execute', namespace='execute')),
]
