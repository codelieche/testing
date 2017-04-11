# -*- coding:utf-8 -*-
"""
这个是创建测试用例文件的工具:
测试用例文件，主要有三部分：
locustfile的TaskSet子类、Httplocust子类、
locustfile、固定的文件头部和文件底部
默认储存在 项目Base_DIR的上一级目录 ../scripts中
"""

import os
from django.conf import settings


file_header = '''
# -*- coding:utf-8 -*-
import sys


from locust import HttpLocust, TaskSet, task, events
from locust import runners
import requests

from db_collect import CollectOperation
from locust_events_ext import LocustEventsExt


'''

file_tail = '''
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
host_target = 'http://HOST_TARGET_FOR_REPLACE'
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
'''


def make_case_file(code_content, file_name, case_id,
                   host_target='http://127.0.0.1:8000'):
    """
    创建测试用例代码文件
    :param code_content: 测试代码主体内容
    :param file_name: 测试代码文件名
    :param case_id: 测试用例的id，需要通过它获取最新的execute
    :param host_target: 保存数据库的服务器地址
    :return:
    """
    case_file_name = file_name
    if not file_name.endswith('.py'):
        case_file_name = file_name + '.py'

    base_dir_parent = os.path.dirname(settings.BASE_DIR)
    script_dir = os.path.join(base_dir_parent, 'scripts')
    file_path = os.path.join(script_dir, case_file_name)

    # 判断目录是否存在，不存在的话创建一个
    if not os.path.exists(script_dir):
        os.mkdir(script_dir)

    # 判断文件是否存在
    if os.path.exists(file_path):
        return False
    with open(file_path, 'w', encoding="UTF-8") as f:
        # 先对file_tail的case_id进行替换
        file_tail_new = file_tail.replace('CASE_ID_FOR_REPLACE', str(case_id))
        file_tail_new2 = file_tail_new.replace('HOST_TARGET_FOR_REPLACE',
                                              str(host_target))
        f.write(file_header)
        f.write(code_content)
        f.write('\n')
        f.write(file_tail_new2)
        f.close()
        return True
