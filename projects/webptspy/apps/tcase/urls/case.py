# -*- coding:utf-8 -*-
from django.conf.urls import url
from tcase.views.case import CaseListView, CaseExecuteView, CaseAddView,\
    CaseEditView

urlpatterns = [
    url(r'^list/(?P<page>\d*?)/?$', CaseListView.as_view(), name="list"),
    # 执行测试用例，会跳转到execute报告页
    url(r'^(?P<pk>\d+)/execute/$', CaseExecuteView.as_view(), name='execute'),
    # 添加测试用例
    url(r'^add/?$', CaseAddView.as_view(), name="add"),
    # 编辑测试用例
    url(r'(?P<pk>\d+)/edit/$', CaseEditView.as_view(), name='edit'),
]
