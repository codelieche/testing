# -*- coding:utf-8 -*-
from django.conf.urls import url

from ..views.api_shiwu import ShiwuAddApiView

urlpatterns = [
    url('^add/$', ShiwuAddApiView.as_view(), name="add"),
]
