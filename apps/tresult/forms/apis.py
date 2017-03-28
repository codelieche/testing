# -*- coding:utf-8 -*-

"""
这个是api相关的form表单
"""

from django import forms

from ..models import Summary


class StatsCSVForm(forms.Form):
    """
    统计数据的form表单
    """
    execute = forms.IntegerField(label="用例")
    csv_type = forms.CharField(max_length=10, label="统计类型")
    content = forms.CharField(widget=forms.Textarea, label="内容")


class SummaryForm(forms.ModelForm):
    """摘要Form"""
    class Meta:
        model = Summary
        fields = ['execute', 'user_count', 'total_rps', 'fail_ratio',
                  'time_min', 'time_avg', 'time_midian', 'time_max',
                  'num_requests', 'num_failures', 'state']
