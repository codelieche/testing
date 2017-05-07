# -*- coding:utf-8 -*-
"""
Locust性能测试事件拓展
"""
import random

from locust import runners


class LocustEventsExt(object):
    """
    locust性能测试事件拓展
    """
    def __init__(self, operator, error_num_max=5):
        """
        :param operator: 是一个db_collect.CollectOperate的对象
        :param error_num_max: 当出现错误最多n次，后触发self.operate的stop事件
        """
        self.operator = operator
        # 还需要对，总共错误多少次后，触发停止事件
        self.error_num = 0
        self.error_num_max = error_num_max

    def on_request_success(self, request_type, name, response_time,
                           response_length):
        """
        当请求成功的时候触发
        :param request_type: 请求类型：GET、POST
        :param name: self.client传入的名字，默认是网址
        :param response_time: response返回的时间
        :param response_length: response返回的内容字节长度
        :return:
        """
        self.operator.add_detail()


    def on_request_failure(self, request_type, name, response_time,
                           exception):
        """
        当请求失败的时候触发
        :param request_type:
        :param name:
        :param response_time:
        :param exception:
        :return:
        """
        # 添加日志
        self.operator.add_log(log_type='error')
        self.operator.add_detail()
        self.error_num += 1
        if self.error_num >= self.error_num_max:
            print('已经出现错误{}次，将触发stop事件'.format(self.error_num))
            self.operator.trigger_stop()

    def on_request_stop(self):
        """
        当出现stop的时候，需要添加summary、state信息
        :return:
        """
        # 添加stop日志
        self.operator.add_log(log_type='stop')
        self.operator.add_summary()
        self.operator.add_stats()
        # 然后退出程序
        import sys
        sys.exit(0)

    def on_request_start(self):
        """
        当开始测试时候触发
        :return:
        """
        self.operator.add_log(log_type='start')


class ShiwuDataHandle:
    """
    事务数据处理
    """
    def __init__(self, body, cycle=True):
        """
        实例化
        :param body: 事务 body的json内容
        :param cycle: 事务 数据是否可循环
        """
        self.cycle = cycle
        if 'types' in body:
            self.types = body['types']
            del body['types']
            self.data = body
        else:
            self.data = body
            self.types = {}
        self.max_cycle_num = 100000
        self.handle()

    def handle(self):
        # 处理数据
        if not self.cycle:
            # 如果数据是不可以循环的，那么可能是只有一条数据，有可能是多条数据
            self.max_cycle_num = 1
            for key in self.data:
                # 如果value是list，而且types中key是manay
                if type(self.data[key]) == list and self.types[key] == 'many':
                    l = len(self.data[key])
                    # 如果长度大于max_cycle_num 就 重新赋值
                    if l > self.max_cycle_num:
                        self.max_cycle_num = l

    def get(self):
        # 返回body中的 key-> value数据
        data = {}
        if not self.cycle and self.max_cycle_num <= 0:
            # 如果循环是False 且 max_cycle_num次数已经成为0了
            return data
        self.max_cycle_num -= 1
        for key in self.data:
            if self.types[key] == 'many':
                # 如果数值是many就需要处理下
                if self.cycle:
                    data[key] = random.sample(self.data[key], 1)[0]
                else:
                    l = len(self.data[key])
                    # 按照顺序取值
                    index = l - self.max_cycle_num - 1
                    if index >= 0:
                        data[key] = self.data[key][index]
                    else:
                        data[key] = self.data[key][0]
            else:
                # 如果数据type是one 或者 list  直接返回值即可
                data[key] = self.data[key]
        return data
