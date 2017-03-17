# _*_ coding:utf-8 _*_

"""
这个是api相关的form表单
"""

from django import forms


class StatsCSVForm(forms.Form):
    """
    统计数据的form表单
    """
    execute = forms.IntegerField(label="用例")
    csv_type = forms.CharField(max_length=10, label="统计类型")
    content = forms.CharField(widget=forms.Textarea, label="内容")
