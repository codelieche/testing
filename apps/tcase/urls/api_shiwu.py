# -*- coding:utf-8 -*-
from django.conf.urls import url

from ..views.api_shiwu import ShiwuAddApiView, ShiwuEditView,\
    ShiwuCheckApiView, ShiwuCloneApiView

urlpatterns = [
    url('^add/$', ShiwuAddApiView.as_view(), name="add"),
    # 编辑事务
    url(r'^(?P<pk>\d+)/edit/$', ShiwuEditView.as_view(), name="edit"),
    # 检查事务
    url(r'^check/$', ShiwuCheckApiView.as_view(), name='check'),
    # 克隆事务
    url(r'^clone/$', ShiwuCloneApiView.as_view(), name='clone')
]
