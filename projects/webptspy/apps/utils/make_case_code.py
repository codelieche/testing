# -*- coding:utf-8 -*-
"""
生成测试用例的代码
当Case的编码方式way使用shiwu的时候，需要把实物组件，转变成代码
"""
import json
import random

from tcase.models import Case, Shiwu


shiwu_data_model = '''
data_{id} = ShiwuDataHandle(body={body}, cycle={cycle})
'''

shiwu_code_model = '''
def shiwu_{id}(l):
    data = data_{id}.get()
    if data:
        l.client.{method}('{url}', {arg_name}=data, name='{name}')
    elif "{method}" == "get":
        l.client.{method}('{url}', name='{name}')
'''

locust_code_model = '''
class WebsiteTasks(TaskSet):
    tasks = {tasks}

    def on_start(self):
        cookies_str = "{cookies}"
        jar = requests.cookies.RequestsCookieJar()
        for cookie in [i.split('=') for i in cookies_str.split(';') if i]:
            jar.set(cookie[0], cookie[1])
        self.client.cookies = jar
        pass
        {on_start}


class WebsiteUser(HttpLocust):
    task_set = WebsiteTasks
    min_wait = 1000
    max_wait = 5000
'''


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

        for key in self.data:
            if self.types[key] == 'many':
                # 如果数值是many就需要处理下
                if self.cycle:
                    data[key] = random.sample(self.data[key], 1)[0]
                else:
                    self.max_cycle_num -= 1
                    l = len(self.data[key])
                    if l > self.max_cycle_num:
                        data[key] = self.data[key][self.max_cycle_num]
                    else:
                        data[key] = self.data[key][0]
            else:
                # 如果数据type是one 或者 list  直接返回值即可
                data[key] = self.data[key]
        return data


def make_shiwu_code(shiwu):
    """
    把事务转换成函数
    :param shiwu: Shiwu object
    :return: 返回代码
    """
    # get使用params参数，其它使用data
    if shiwu.method == 'get' or shiwu.method == "delete":
        arg_name = 'params'
    else:
        arg_name = 'data'

    # 格式化代码
    code_content = shiwu_code_model.format(
        id=shiwu.pk,
        method=shiwu.method,
        url=shiwu.url,
        arg_name=arg_name,
        name=shiwu.name
    )
    return code_content


def make_shiwu_data(case):
    # 取出所有的事务
    shiwu_list = case.shiwu_set.all()
    shiwu_data_list = []
    for shiwu in shiwu_list:
        body = shiwu.body
        # body = body.replace('\\r', '')
        # 把body的数据转成json
        j = json.loads(body)
        if type(j) == str:
            j = json.loads(j)
        # 获取shiwu_i_data
        body = str(j).replace('\\r', ''),
        if type(body) == tuple:
            body = body[0]
        data_i = shiwu_data_model.format(id=shiwu.id, body=body,
                                         cycle=shiwu.cycle)
        shiwu_data_list.append(data_i)
    # 返回组合后的字符串
    return ''.join(shiwu_data_list)


def make_case_code(case):
    """
    生成Case的代码
    :param case: Case object
    :return: 返回测试用例的代码
    """
    # 先得到Case shiwu data
    data_list_str = make_shiwu_data(case)
    # 获取到事务的方法
    shiwu_list = case.shiwu_set.all()
    shiwu_fun_list = []
    for shiwu in shiwu_list:
        shiwu_fun_i = make_shiwu_code(shiwu)
        shiwu_fun_list.append(shiwu_fun_i)
    # 把函数组合成一个字符串
    shiwu_fun_str = ''.join(shiwu_fun_list)
    # 编写WebsiteTask类  和WebsiteUser类
    tasks_str = "{"
    on_start_str = ""
    for shiwu in shiwu_list:
        if shiwu.is_startup:
            on_start_str += "shiwu_{}(self);".format(shiwu.id)
        else:
            task_i_str = "shiwu_{id}: 10,".format(id=shiwu.id)
            tasks_str += task_i_str
    # 闭合tasks_str
    tasks_str += '}'
    # 替换字符串
    locust_code = locust_code_model.format(tasks=tasks_str,
                                           cookies=case.cookies,
                                           on_start=on_start_str)

    code_content = data_list_str + shiwu_fun_str + locust_code
    return code_content
