# -*- coding:utf-8 -*-
from django.conf.urls import url
from ..views import api_execute

urlpatterns = [
    # http://127.0.0.1:8000/api/1.0/execute/123/delete/
    url(r'^(?P<pk>\d+)/delete/$', api_execute.ExecuteDeleteApiView.as_view(),
        name='delete')
]
