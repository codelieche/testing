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
        fields = ('name', 'project', 'is_startup', 'method', 'url', 'cycle',
                  'body')


class ShiwuEditForm(forms.Form):
    """
    事务编辑Form
    """
    name = forms.CharField(label="事务名", max_length=100)
    project = forms.IntegerField(widget=forms.Select, label="项目")
    is_startup = forms.BooleanField(widget=forms.CheckboxInput, label="启动准备")
    method = forms.CharField(widget=forms.Select, label="请求类型")
    url = forms.CharField(max_length=100, label="网址")
    cycle = forms.BooleanField(widget=forms.CheckboxInput, label="数据可循环")
