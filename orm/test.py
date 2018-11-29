# -*- coding: utf-8 -*-
"""
    .filename
    ~~~~~~~~~~~~~~

    Description

    :create by: lyncir
    :date: 2018-11-27 11:45:22 (+0800)
    :last modified date: 2018-11-29 11:27:20 (+0800)
    :last modified by: lyncir
"""
from model import render_column_definitions
from profile import TcMinisterGroup, TcMinisterGroupAdapter


print(render_column_definitions(TcMinisterGroup))
TcMinisterGroup.create_table()

print(TcMinisterGroup.exists())


record = TcMinisterGroupAdapter.objects.create(GroupId=1)
print(record.GroupId)

records = TcMinisterGroupAdapter.objects.all()
print(records)
for r in records:
    print r.GroupId


data_list = [
    {"GroupId": 2},
    {"GroupId": 3},
]

TcMinisterGroupAdapter.objects.insert_many(data_list)


record = TcMinisterGroupAdapter.objects.get(GroupId=2)
print(record.GroupId)


records = TcMinisterGroupAdapter.objects.filter(GroupId__in=[1, 2, 4])
for r in records:
    print r
