# -*- coding: utf-8 -*-
"""
    .filename
    ~~~~~~~~~~~~~~

    Description

    :create by: lyncir
    :date: 2018-11-27 11:31:06 (+0800)
    :last modified date: 2018-11-27 15:39:25 (+0800)
    :last modified by: lyncir
"""
import peewee

# python 与 sqlite 数据类型转换
DATA_TYPES = {
    'CHAR': 'TEXT',
    'VARCHAR': 'TEXT',
    'INT': 'INTEGER',
    'FLOAT': 'REAL',
}

PEEWEE_INNER_ATTRS = [
    'DoesNotExist',
    'Database',
    'db',
]


def attrs(obj):
    """
    返回一个对象的属性值字典
    """
    return dict(i for i in vars(obj).items() if i[0][0] != '_')


def render_column_definitions(model):
    """
    为model创建sqlite 列定义
    """
    model_attrs = attrs(model).items()
    model_attrs = {k: v for k, v in model_attrs if k not in PEEWEE_INNER_ATTRS}
    return [(k, DATA_TYPES[v.field.field_type]) for k, v in model_attrs.items()]


class Model(peewee.Model):

    @classmethod
    def create_table(cls, mode='open'):
        cls.db.create(cls.__name__, *render_column_definitions(cls), mode=mode)

    @classmethod
    def exists(cls):
        return cls.__name__ in cls.db
