# -*- coding:utf-8 -*-

from django.shortcuts import get_object_or_404

from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from tcase.models import Execute

from ..models import Detail, Summary, StatsCSV
from ..serializers import DetailSerializer, StatsCSVSerializer
from ..serializers import SummarySerializer


@api_view(['GET', 'POST'])
def execute_detail(request, pk):
    """
    获取execute的结果
    """
    execute = get_object_or_404(Execute, pk=pk)
    if request.method == 'GET':
        detail_list = Detail.objects.filter(execute=execute)
        serializer = DetailSerializer(detail_list, many=True)
        return Response(serializer.data)

    elif request.method == "POST":
        # 添加execute结果的detail
        data = request.data
        # data['execute'] = pk
        detail_obj = DetailSerializer(data=data)
        if detail_obj.is_valid():
            detail_obj.save()
            return Response(detail_obj.data)
        else:
            print(request.data)
            print(detail_obj)

            return Response(detail_obj.errors,
                            status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'POST'])
def execute_summary(request, pk):
    """
    获取执行摘要
    :param request:
    :param pk: 执行测试execute的id
    :return:
    """
    try:
        execute = Execute.objects.get(pk=pk)
    except Execute.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    if request.method == 'GET':
        summary_list = Summary.objects.filter(execute=execute)
        # 如果列表为空，也会返回个[]
        serializer = SummarySerializer(summary_list, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        summary_obj = SummarySerializer(data=request.data)
        if summary_obj.is_valid():
            summary_obj.save()
            return Response(summary_obj.data)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)



@api_view(['GET'])
def execute_stats(request, pk, type_):
    """
    执行结果统计
    :param request:
    :param pk: execute的id
    :param type_: 统计结果的类型：request, response, exception
    :return:
    """
    try:
        execute = Execute.objects.get(pk=pk)
    except Execute.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    if request.method == 'GET':
        # stats_obj = StatsCSV.objects.get(execute=execute, csv_type=type_)
        stats_obj = get_object_or_404(StatsCSV, execute=execute, csv_type=type_)
        serializer = StatsCSVSerializer(stats_obj)
        print(serializer.data)
        return Response(serializer.data)
    else:
        return Response(status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def execute_add_stats(request):
    if request.method == 'POST':
        """
        POST添加统计信息
        """
        serializer = StatsCSVSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, template_name=None)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response(status=status.HTTP_400_BAD_REQUEST)