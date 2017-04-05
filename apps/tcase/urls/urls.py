# -*- coding:utf-8 -*-
from django.conf.urls import url
from tcase.views.case import CaseListView

urlpatterns = [
    url(r'^list/$', CaseListView.as_view(), name="list"),
]
