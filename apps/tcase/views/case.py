# -*- coding:utf-8 -*-
from django.shortcuts import render
from django.views.generic import View

from ..models import Case
# Create your views here.


class CaseListView(View):
    """
    网站首页View
    """
    def get(self, request):
        all_case = Case.objects.all()
        return render(request, 'case/list.html', {
            'all_case': all_case,
        })
