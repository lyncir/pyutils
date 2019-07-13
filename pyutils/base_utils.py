# -*- coding: utf-8 -*-
"""
    utils.base_utils
    ~~~~~~~~~~~~~~~~~

    基础utils

    :create by: lyncir
    :date: 2018-12-05 10:38:59 (+0800)
    :last modified date: 2018-12-05 10:55:06 (+0800)
    :last modified by: lyncir
"""
from operator import attrgetter


def order_by(objects, fields):
    """
    对对象进行复合排序

    Example:

        order_by(students, '-grade, age')

    :params list objects: 对象列表
    :param str fields: 排序字段
    :return: 经过排序后的对象列表
    :rtype: objects
    """
    # 复合排序需要从右到左
    for field in fields.split(',')[::-1]:
        # 默认ASC
        reverse = False

        # 降序DESC
        if field.startswith('-'):
            _, field = field.split('-')
            reverse = True

        objects = sorted(objects, key=attrgetter(field), reverse=reverse)

    return objects
