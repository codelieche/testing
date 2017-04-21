# -*- coding:utf-8 -*-
from django import forms

from .models import Case


class CaseForm(forms.ModelForm):
    """
    测试用例Model Form
    """
    class Meta:
        model = Case
        fields = ('project', 'name', 'desc', 'code', 'status', 'cookies')
