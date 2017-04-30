# -*- coding:utf-8 -*-
"""
请求事务，需要把前端传过来的，key，value，type组合成字典
编辑事务的时候，需要把保存的body字典数据分解成字符串(type, key, value)元组列表
"""
import json


def shiwu_str_to_json(type_list=[], key_list=[], value_list=[]):
    """
    把前端传过来的type、key、value组合成json
    :param type_list:
    :param key_list:
    :param value_list:
    :return: 返回json的字符格式
    """
    body_json = {}
    # 组合三列为元组列表
    if len(type_list) == len(key_list) == len(value_list) != 0:
        shiwu_body_list = zip(type_list, key_list, value_list)
    else:
        # 传入的三个参数，长度不一致，或者是空
        return json.dumps(body_json)

    types = {}
    # 对shiwu_body_list进行处理：
    for body_i in shiwu_body_list:
        # 每个key都有type
        body_json['types'] = {}
        # 先查看type类型：one、many、list
        type_, key, value = body_i
        # 如果三个值都不为空，才继续
        if type_ and key and value:
            # 如果type_ 是one
            if type_ == "one":
                body_json[key] = value
                types[key] = type_
            elif type_ == "list" or type_ == "many":
                # 如果是list就每一行是个元素
                # value根据换行符分割，且过滤空行
                value_list = [line for line in value.split('\n') if line]
                # 保存type_ 和 value 去body_json中
                body_json[key] = value_list
                types[key] = type_
            else:
                # 传入的type有误
                pass
    # 最后把types保存到body_json中
    body_json['types'] = types
    # 对传入的zip处理完后，返回json的字符串内容
    return json.dumps(body_json)


def shiwu_str_to_list(body):
    """
    把json的字符串，重新处理成数组，每个元素是(type, key, value)
    :param body:
    :return: [(type, key, value)]
    """
    # 第一步：把body字符串转换成json
    body_json = json.loads(body)
    if type(body_json) == str:
        body_json = json.loads(body_json)
    # 第二步：处理数据
    if not body_json:
        return []
    body_result = []
    if 'types' in body_json:
        types = body_json['types']
    else:
        types = {}
    for key in body_json:
        if key != 'types':
            if key in types:
                body_i = (types[key], key, body_json[key])
            else:
                body_i = ('one', key, body_json[key])
            body_result.append(body_i)
    # 返回结果
    return body_result

