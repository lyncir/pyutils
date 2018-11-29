# -*- coding: utf-8 -*-
"""
    .filename
    ~~~~~~~~~~~~~~

    Description

    :create by: lyncir
    :date: 2018-11-27 11:31:06 (+0800)
    :last modified date: 2018-11-29 18:02:12 (+0800)
    :last modified by: lyncir
"""
import inspect

from pydblite.sqlite import Database


# python 与 sqlite 数据类型转换
DATA_TYPES = {
    str: 'TEXT',
    int: 'INTEGER',
    float: 'REAL',
}


def attrs(obj):
    """
    返回一个对象的属性值字典
    """
    return {i: type(getattr(obj, i)) for i in dir(obj) if (not i.startswith('__') and not inspect.ismethod(getattr(obj, i)))}


def render_column_definitions(model):
    """
    为model创建sqlite 列定义
    """
    model_attrs = attrs(model).items()
    print model_attrs
    model_attrs = {k: v for k, v in model_attrs if k != 'database'}
    return [(k, DATA_TYPES[v]) for k, v in model_attrs.items()]


class Model(object):

    database = Database(':memory:')

    @classmethod
    def create_table(cls, mode='open'):
        cls.database.create(cls.__name__, *render_column_definitions(cls), mode=mode)

    @classmethod
    def exists(cls):
        return cls.__name__ in cls.database
