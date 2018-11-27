# -*- coding: utf-8 -*-
"""
    .filename
    ~~~~~~~~~~~~~~

    Description

    :create by: lyncir
    :date: 2018-11-27 11:45:22 (+0800)
    :last modified date: 2018-11-27 15:12:25 (+0800)
    :last modified by: lyncir
"""
from pydblite.sqlite import Database


from model import render_column_definitions
from profile import TcMinisterGroup


db = Database(':memory:')
TcMinisterGroup.db = db


print(render_column_definitions(TcMinisterGroup))
# TcMinisterGroup.create_table()

# print(TcMinisterGroup.exists())


# print(db.keys())
# table = db['TcMinisterGroup']
# print(len(table))
# print(table.fields)
