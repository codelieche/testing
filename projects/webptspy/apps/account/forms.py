# -*- coding:utf-8 -*-
"""
用户相关的表单
"""
from django import forms


class LoginForm(forms.Form):
    username = forms.CharField(label="用户名")
    password = forms.CharField(label="密  码", widget=forms.PasswordInput)
