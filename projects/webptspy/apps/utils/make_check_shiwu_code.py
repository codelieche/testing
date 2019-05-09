# -*- coding:utf-8 -*-
"""
生成检查事务的代码
"""
import json
import random


from tcase.models import Case, Shiwu


header_model = '''# -*- coding: utf-8 -*-
import requests

from locust_events_ext import ShiwuDataHandle

session = requests.Session()
cookies_str = "{cookies}"
jar = requests.cookies.RequestsCookieJar()
for cookie in [i.split('=') for i in cookies_str.split(';') if i]:
    jar.set(cookie[0], cookie[1])
session.cookies = jar

'''

shiwu_data_model = '''
data_{id} = ShiwuDataHandle(body={body}, cycle={cycle})
'''

shiwu_check_code_model = '''
data = data_{id}.get()
try:
    if data:
        r = session.{method}('{url}', {arg_name}=data)
    elif "{method}" == "get":
        r = session.{method}('{url}')
except Exception as e:
    r = None
'''

tail_model = '''
if r:
    if r.ok:
         # print('{"status": "success", "msg": "%s"}' % r.text)
         print('{"status": "success", "code": "%s"}' % r.status_code)
    else:
        print('{"status": "failure", "msg": "%s"}' % r.status_code)
        # print('{"status": "failure", "msg": "%s"}' % r.text)
else:
    print({"status": "error", "msg": ""})

'''


def make_shiwu_data(shiwu):
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
    return data_i


def get_shiwu_data_and_code(shiwu):
    data_content = make_shiwu_data(shiwu)

    # get使用params参数，其它使用data
    if shiwu.method == 'get' or shiwu.method == "delete":
        arg_name = 'params'
    else:
        arg_name = 'data'
    # 格式化代码
    url = 'http://{}{}'.format(shiwu.project.address, shiwu.url)
    # print(url)
    code_content = shiwu_check_code_model.format(
        id=shiwu.pk,
        method=shiwu.method,
        url=url,
        arg_name=arg_name
    )

    return "{}\n{}".format(data_content, code_content)


def make_check_shiwu_code(shiwu, start_shiwu=None, cookies=''):
    """
    把事务转换成函数
    :param shiwu: Shiwu object
    :return: 返回代码
    """
    # 先处理star, 再处理start_shiwu，最后处理要测的事务
    start_content = header_model.format(cookies=cookies)

    start_shiwu_code = ""
    run_shiwu_code = get_shiwu_data_and_code(shiwu)
    if start_shiwu:
        start_shiwu_code = get_shiwu_data_and_code(start_shiwu)

    return start_content + '\n' + start_shiwu_code + '\n' + run_shiwu_code +\
        '\n' + tail_model

