# -*- coding:utf-8 -*-
"""
这个是显示execute相关的View
"""
import json

from django.shortcuts import render, get_object_or_404
from django.views.generic import View
from django.db import connection

from tcase.models import Execute
from tresult.models import Summary, StatsCSV, Log


class ReportView(View):
    """
    测试报告view
    """
    def get(self, request, pk):
        # 先获取到execute对象
        execute = get_object_or_404(Execute, pk=pk)

        # 获取摘要数据
        summary = Summary.objects.filter(execute=execute).last()

        # 获取时间、并发用户数、响应时间、每秒响应数
        cursor = connection.cursor()
        sql = "SELECT distinct add_time, user_count, time_avg, total_rps" \
              " FROM tresult_detail WHERE execute_id={} and" \
              " add_time > '{}'".format(pk, execute.time_start)
        # print(sql)
        cursor.execute(sql)
        data_result = cursor.fetchall()
        data_zip = zip(*data_result)
        echarts_data = {}
        i_index = 0
        for data in data_zip:
            data = list(data)
            i_index += 1
            if i_index == 1:
                time_new = []

                for i in range(len(data)):
                    time_new.append(i)
                #     time_new.append(str(i.strftime('%H:%M:%S')))
                echarts_data['add_time'] = time_new
            elif i_index == 2:
                echarts_data['user_count'] = data
            elif i_index == 3:
                echarts_data['time_avg'] = data
            else:
                echarts_data['total_rps'] = data

        # 获取request数据
        request_stats = StatsCSV.objects.filter(execute=execute,
                                                csv_type='request').last()
        if request_stats:
            stats_content = request_stats.content
            stats_content = stats_content.replace('"', '')
            stats_request_lines = [line for line in stats_content.split('\n')[1:]]
            stats_request = [line.split(',') for line in stats_request_lines]
            stats_request[-1][0] = ''
        else:
            stats_request = None

        # 获取response数据
        response_stats = StatsCSV.objects.filter(execute=execute,
                                                 csv_type='response').last()
        if response_stats:
            response_content = response_stats.content
            response_content = response_content.replace('"', '')
            response_lines = [line for line in response_content.split('\n')[1:]]
            stats_response = [line.split(',') for line in response_lines]
        else:
            stats_response = None

        # 获取错误日志
        error_logs = Log.objects.filter(execute_id=pk, log_type='error')
        all_error = []
        time_pre = None
        for log_i in error_logs:
            if time_pre == log_i.add_time:
                continue
            else:
                time_pre = log_i.add_time
            log_dic = {}
            j = json.loads(log_i.content)
            log_dic['total_rps'] = round(float(j['total_rps']), 2)
            log_dic['add_time'] = log_i.add_time
            log_dic['user_count'] = j['user_count']
            all_error.append(log_dic)

        content = {
            'execute': execute,
            'summary': summary,
            'echarts_data': echarts_data,
            'stats_request': stats_request,
            # 'stats_response': stats_response,
            'stats_response': [],
            'all_error': all_error,
        }
        return render(request, 'execute/report.html', content)


class ReportListView(View):
    """
    报告列表页
    """
    def get(self, request):
        """
        execute的列表页
        :param request:
        :return:
        """
        # 获取所有停止了的execute
        all_execute_stoped = Execute.objects.filter(status='stoped')
        # 获取到对应的summary
        all_reports = Summary.objects.filter(execute__in=all_execute_stoped)
        return render(request, 'execute/list.html', {
            'all_reports': all_reports
        })