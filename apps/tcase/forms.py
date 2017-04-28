# -*- coding:utf-8 -*-
from django import forms

from .models import Case, Shiwu


class CaseForm(forms.ModelForm):
    """
    测试用例Model Form
    """
    class Meta:
        model = Case
        fields = ('project', 'name', 'desc', 'way', 'code', 'status', 'cookies')


class ShiwuForm(forms.ModelForm):
    """
    请求事务Model Form
    """
    class Meta:
        model = Shiwu
        fields = ('name', 'project', 'is_startup', 'method', 'url', 'body')
