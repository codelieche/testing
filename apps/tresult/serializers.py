# -*- coding:utf-8 -*-
"""
rest_framework序列化模型
"""
from .models import Detail, Summary, StatsCSV, Log

from rest_framework import serializers


class DetailSerializer(serializers.ModelSerializer):
# class DetailSerializer(serializers.HyperlinkedModelSerializer):
    """
    测试结果Model序列化模型
    """
    # execute = serializers.ReadOnlyField(source='execute.id')
    # execute = serializers.PrimaryKeyRelatedField(read_only=False, many=False)

    class Meta:
        model = Detail
        # fields = ('id', 'execute', 'content', 'add_time', 'status')
        fields = ('id', 'execute', 'user_count', 'time_avg', 'total_rps',
                  'fail_ratio', 'num_requests', 'num_failures', 'add_time',
                  'status')


class SummarySerializer(serializers.ModelSerializer):
    """
    测试结果摘要序列化模型
    """
    class Meta:
        model = Summary
        fields = ('id', 'execute', 'user_count', 'total_rps', 'fail_ratio',
                  'time_min', 'time_avg', 'time_midian', 'time_max',
                  'num_requests', 'num_failures', 'status', 'add_time')


class StatsCSVSerializer(serializers.ModelSerializer):
    """
    测试结果统计CSV序列化模型
    """
    class Meta:
        model = StatsCSV
        fields = ('id', 'execute', 'csv_type', 'content', 'add_time')


class LogSerializer(serializers.ModelSerializer):
    """
    测试日志序列化模型
    """
    class Meta:
        model = Log
        fields = ('id', 'execute', 'log_type', 'content', 'add_time')
