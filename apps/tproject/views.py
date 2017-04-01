# -*- coding:utf-8 -*-
from django.shortcuts import render
from django.views.generic import View

from .models import Project
# Create your views here.


class ProjectListView(View):
    """
    项目列表View
    """
    def get(self, request, page=1):
        """
        :param request:
        :param page: 页码
        :return:
        """
        return render(request, 'index.html')
