# -*- coding:utf-8 -*-
"""
项目Post表单Form信息
"""
from django import forms
from .models import ServerInfo


class ServerInfoModelForm(forms.ModelForm):
    """
    Project ServerInfo Model form
    """
    class Meta:
        model = ServerInfo
        fields = ('project', 'test_db', 'product_db', 'test_deployment',
                  'product_deployment', 'test_server', 'product_server')
