# -*- coding:utf-8 -*-
"""
这个是数据收集的脚步
"""
import json
from datetime import datetime

import requests


class CollectOperation(object):
    """
    数据收集操作类
    """
    def __init__(self, execute, host_locust='127.0.0.1', port=8089,
                 host_target='http://127.0.0.1:8000'):
        """
        初始化数据收集操作对象实例
        :param execute: 执行测试 execute的id
        :param host: locust性能测试的host，默认是:http://127.0.0.1
        :param port: locust性能测试启动web的端口号，默认：8089
        :param host_target: 数据收集目标网址，通过host_target来保存数据
        """
        self.execute = execute
        self.host_locust = host_locust
        self.port = port
        if host_locust.startswith('http://'):
            self.host_locust = '{}:{}'.format(self.host_locust, self.port)
        self.host_locust = "http://{}:{}/".format(self.host_locust, self.port)

        print(self.host_locust)
        if host_target[-1] == '/':
            self.host_target = host_target
        else:
            self.host_target = host_target + '/'
        # 保存个时间，detail数据是每5秒储存一次
        self.now = datetime.now()

    def add_detail(self):
        """
        保存详细数据
        :return:
        """
        print('add detail')
        if (datetime.now() - self.now).seconds < 5:
            # 如果现在的时间和self.now的差距小于5秒，就返回
            return

        # 每5秒间隔保存数据一次
        # 有时候detail同一时间会保存多条记录，这里不做处理，有重复没关系
        url = '{}stats/requests'.format(self.host_locust)
        r = requests.get(url)
        if r.ok:
            # 请求ok后，对数据进行处理post到服务器上
            result = r.json()
            status = result['state']
            # print(result)
            import time
            # time.sleep(10)
            # 只当状态是running、stoped的情况下，才进行下一步操作
            if status not in ['running', 'stoped']:
                return
            # 更新self.now
            self.now = datetime.now()

            # 得到的是json格式的，stats是一个统计列表，最后一条是总共的汇总
            total_stats = result['stats'][-1]
            data = {
                'execute': self.execute,
                'user_count': result['user_count'],
                'time_avg': total_stats['avg_response_time'],
                'total_rps': total_stats['current_rps'],
                'fail_ratio': result['fail_ratio'],
                'num_requests': total_stats['num_requests'],
                'num_failures': total_stats['num_failures'],
                'add_time': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                'status': status,
            }
            # POST数据到服务器
            post_url = '{}api/1.0/execute/{}/detail/'.format(self.host_target,
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
                'user_count': result['user_count'],
                'total_rps': total_stats['current_rps'],
                'fail_ratio': result['fail_ratio'],
                'time_min': total_stats['min_response_time'],
                'time_avg': total_stats['avg_response_time'],
                'time_median': total_stats['median_response_time'],
                'time_max': total_stats['max_response_time'],
                'num_requests': total_stats['num_requests'],
                'num_failures': total_stats['num_failures'],
                'status': result['state'],
                'add_time': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            }

            # 构建post的url
            post_url = '{}api/1.0/execute/{}/summary/'.format(self.host_target,
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
        for csv_type, url in stats_csv_url.items():
            # 获取数据
            r = requests.get(url)
            data = {
                'execute': self.execute,
                'content': r.content,
                'csv_type': csv_type,
                'add_time': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            }
            # 发送数据到后台
            post_url = '{}api/1.0/execute/stats/add/'.format(self.host_target)
            response = requests.post(post_url, data)
            print("添加stats数据:{}:{}".format(csv_type, response.ok))

    def trigger_start(self, locust_count=100, hatch_rate=1):
        """
        触发开始测试
        :param locust_count: 并发用户数
        :param hatch_rate: 用户每秒访问频率
        :return:
        """
        url = '{}swarm'.format(self.host_locust)
        # 通过post传递数据触发
        data = {
            'locust_count': locust_count,
            'hatch_rate': hatch_rate
        }
        response = requests.post(url, data)
        print("locust_count: {}, result: {}".format(locust_count, response.ok))

    def trigger_stop(self):
        """
        触发stop
        :return:
        """
        stop_url = '{}stop'.format(self.host_locust)
        # get访问stop的页面就可以实现测试停止
        response = requests.get(stop_url)
        print('停止测试:{}'.format(response.ok))

    def change_user(self, locust_count=100, hatch_rate=1):
        """
        改变并发用户数
        :param locust_count: 并发用户数
        :param hatch_rate: 用户访问频率
        :return:
        """
        self.trigger_start(locust_count, hatch_rate)
