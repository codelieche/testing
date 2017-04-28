# -*- coding:utf-8 -*-
from django.conf.urls import url

from ..views.api_shiwu import ShiwuAddApiView, ShiwuEditView

urlpatterns = [
    url('^add/$', ShiwuAddApiView.as_view(), name="add"),
    # 编辑事务
    url(r'^(?P<pk>\d+)/edit/$', ShiwuEditView.as_view(), name="edit"),
]
