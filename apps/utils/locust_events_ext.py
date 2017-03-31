# -*- coding:utf-8 -*-
"""
Locust性能测试事件拓展
"""
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



