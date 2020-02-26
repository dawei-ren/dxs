from flask import jsonify, request
from functools import wraps
from config import CFG
import json


def common_resp(success, data):
    return jsonify({'success': success, 'data': data})


def get_filter(query_str, allowed_keys=None):
    filters = []
    for k, v in query_str.items():
        if k in allowed_keys:
            if k == 'name':
                filters.append(r'%s like "%%%s%%"' % (k, v))
            else:
                filters.append('%s="%s"' % (k, v))
    return filters


def get_sort(query_str):
    fields = query_str.getlist('sortby')
    orders = query_str.getlist('order')
    if fields and orders:
        return [{'field': k, 'order': v} for k, v in zip(fields, orders)]
    else:
        return [{'field':'created_time', 'order': 'desc'}]


def get_limit(query_str):
    page = query_str.get('page')
    page_size = query_str.get('pageSize')
    if page and page_size:
        page = int(page)
        page_size = int(page_size)
        offset = (page - 1) * page_size
        return {'offset': offset, 'count': page_size}


def data_val(data, needed=None, no_needed=None):
    '''
    判断传入数据是否缺少needed里面的元素或者为空值, 多出no_needed里面的元素
    :param data:  dict
    :param needed:
    :param no_needed:
    :return:
    '''
    needed = needed or []
    no_needed = no_needed or []
    data_keys = set(list(data.keys()))
    diff = set(needed) - data_keys
    if diff:
        return False, '%s 不能为空' % diff

    for k, v in data.items():
        if k in needed:
            if v is None or v == '':
                return False, '%s 不能为空' % k
        if k in no_needed:
            return False, '不需要传 %s' % k
    return True, ''