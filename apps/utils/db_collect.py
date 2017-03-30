# -*- coding:utf-8 -*-
"""
这个是数据收集的脚步
"""
import json
from datetime import datetime

import requests


class CollectOpOprater(object):
    """
    数据收集操作类
    """
    def __init__(self, execute, host='127.0.0.1', port=8089,
                 host_target='http://127.0.0.1:8000'):
        """
        初始化数据收集操作对象实例
        :param execute: 执行测试 execute的id
        :param host: locust性能测试的host，默认是:http://127.0.0.1
        :param port: locust性能测试启动web的端口号，默认：8089
        :param host_target: 数据收集目标网址，通过host_target来保存数据
        """
        self.execute = execute
        self.host = host
        self.port = port
        self.host_locust = "http://{}:{}/".format(self.host, self.port)
        if host_target[-1] == '/':
            self.host_target = host_target
        else:
            self.host_target = host_target + '/'
        # 保存个时间，detail数据是每5秒储存一次
        self.now = 0

    def add_detail(self):
        """
        保存详细数据
        :return:
        """
        if (datetime.now() - self.now).seconds < 5:
            # 如果现在的时间和self.now的差距小于5秒，就返回
            return

        # 每5秒间隔保存数据一次
        # 有时候detail同一时间会保存多条记录，这里不做处理，有重复没关系
        url = '{}stats/requests'
        r = requests.get(url)
        if r.ok:
            # 请求ok后，对数据进行处理post到服务器上
            result = r.json()
            status = result['state']
            # 只当状态是running、stoped的情况下，才进行下一步操作
            if status not in ['running', 'stoped']:
                return
            # 更新self.now
            self.now = datetime.now()

            # 得到的是json格式的，stats是一个统计列表，最后一条是总共的汇总
            total_stats = result['state'][-1]
            data = {
                'execute': self.execute,
                'user_count': total_stats['user_count'],
                'time_avg': total_stats['avg_response_time'],
                'total_rps': total_stats['current_rps'],
                'fail_ratio': result['fail_ratio'],
                'num_requests': total_stats['num_requests'],
                'num_failures': total_stats['num_failures'],
                'add_time': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                'status': status,
            }
            # POST数据到服务器
            post_url = '{}api/1.0/execute{}/detail/'.format(self.host_target,
                                                            self.execute)
            response = requests.post(post_url, data)
            print("添加detail数据：", response.ok)

    def add_summary(self):
        """
        向Django服务器添加summary数据
        :return:
        """
        # 对'http://127.0.0.1:8089/stats/requests'的数据进行处理
        url = self.host_locust + 'stats/requests'
        # 先用requests获取数据
        r = requests.get(url)
        if r.ok:
            # 如果ok把得到的数据格式化处理后post到服务器上
            result = r.json()
            # 得到的是json格式的，stats是一个统计列表，最后一条是总共的汇总
            total_stats = result['stats'][-1]
            data = {
                'execute': self.execute,
                'user_count': total_stats['user_count'],
                'total_rps': total_stats['current_rps'],
                'fail_ratio': result['fail_ratio'],
                'time_min': total_stats['min_response_time'],
                'time_avg': total_stats['avg_response_time'],
                'time_midian': total_stats['median_response_time'],
                'time_max': total_stats['max_response_time'],
                'num_requests': total_stats['num_requests'],
                'num_failures': total_stats['num_failures'],
                'status': result['state'],
                'add_time': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            }

            # 构建post的url
            post_url = '{}api/1.0/execute{}/summary/'.format(self.host_target,
                                                             self.execute)
            # 用requests发送数据到服务器
            response = requests.post(post_url, data=data)
            print("添加summary数据：", response.ok)
        else:
            print("请求失败")

    def add_stats(self):
        """
        添加统计数据
        :return:
        """
        # locust服务器提供了csv统计数据下载的链接
        stats_csv_url = {
            'request': '{}stats/requests/csv'.format(self.host_locust),
            'response': '{}stats/distribution/csv'.format(self.host_locust)
        }
        for csv_type, url in stats_csv_url:
            # 获取数据
            r = requests.get(url)
            data = {
                'execute': self.execute,
                'content': r.content,
                'csv_type': csv_type,
                'add_time': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            }
            # 发送数据到后台
            post_url = '{}api/1.0/execute/stats/add/'
            response = requests.post(post_url, data)
            print("添加stats数据:{}:{}".format(csv_type, response.ok))
