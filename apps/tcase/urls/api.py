# -*- coding:utf-8 -*-
from django.conf.urls import url
from ..views import api

urlpatterns = [
    # http://127.0.0.1:8000/api/1.0/case/1/executeid/
    url(r'(?P<pk>\d+)/executeid/$', api.CaseExecute.as_view(),
        name='get_currect_execute_id'),

]