# -*- coding:utf-8 -*-
"""
locust性能测试脚本Demo
"""
import sys

from locust import HttpLocust, TaskSet, task, events
from locust import runners
import requests

from db_collect import CollectOperation
from locust_events_ext import LocustEventsExt


class TestTaskSet(TaskSet):
    """
    性能测试任务集合
    """
    def on_start(self):
        """
        实例化每个并发用户前都会执行一次这个方法
        :return:
        """
        # print('on_start')
        pass
        # print(runners.locust_runner)
        # print(dir(runners.locust_runner.options))

    @task(10)
    def task_01(self):
        self.client.get('/', timeout=10)
        l = runners.locust_runner
        # print(l.stats)
        # print(dir(l.stats))
        # print(l.stats.max_requests)

    @task(5)
    def task_about(self):
        self.client.get('/about.html', timeout=10)
        self.client.get('/book', timeout=10)


class PerformanceTesting(HttpLocust):
    """
    locust性能测试类
    """
    task_set = TestTaskSet
    min_wait = 2000
    max_wait = 5000

# 获取locust运行配置的信息
# locust --locustfile=locust_demo.py --port=8090 --host=http://test.com

# 做一个约定：
# 第三个参数存port,而且不要用简写，都用`--xxxx=yyyy`
print(sys.argv)
try:
    locust_port = int(sys.argv[2].split('=')[1])
    # 模版文件中的execute_id存放一个常量，每次执行，要修改这个值
    # execute_id = 'EXECUTE_ID_FOR_REPLACE'
    # execute_id = 2

except TypeError:
    print("locust port TypeError")
    sys.exit(-1)

CASE_ID = 'CASE_ID_FOR_REPLACE'
CASE_ID = 1
# 需要根据case_id，查询到最近执行的execute_id
get_execute_id_url = 'http://127.0.0.1:8000/api/1.0/case/%s/executeid/'\
                     % CASE_ID
execute_id = 0
try:
    response = requests.post(get_execute_id_url)
    # 如果代码中execute_id 不是整数，也退出
    execute_id = int(response.json()['execute_id'])
except Exception as e:
    print(e)
    sys.exit(1)

# host_target是保存数据库的服务器地址，注意替换！！！！！
host_target = 'http://127.0.0.1:8000'
# 先实例化Collect
operator = CollectOperation(execute=execute_id, host_locust="127.0.0.1",
                            port=locust_port,
                            host_target=host_target)
# 实例化LocustEventsExt
events_ext_obj = LocustEventsExt(operator=operator, error_num_max=5)

# 拓展locust的事件
events.locust_start_hatching += events_ext_obj.on_request_start
events.request_success += events_ext_obj.on_request_success
events.request_failure += events_ext_obj.on_request_failure
events.locust_stop_hatching += events_ext_obj.on_request_stop
