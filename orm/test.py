# -*- coding: utf-8 -*-
"""
    .filename
    ~~~~~~~~~~~~~~

    Description

    :create by: lyncir
    :date: 2018-11-27 11:45:22 (+0800)
    :last modified date: 2018-12-05 09:44:54 (+0800)
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
    {"GroupId": 2, "MinisterId": 9},
    {"GroupId": 3, "MinisterId": 10},
    {"GroupId": 4, "MinisterId": 11},
    {"GroupId": 4, "MinisterId": 12},
]

TcMinisterGroupAdapter.objects.insert_many(data_list)


record = TcMinisterGroupAdapter.objects.get(GroupId=2)
record.update(MinisterId=11)
print(record.GroupId, type(record), record._record.__dict__)


records = TcMinisterGroupAdapter.objects.filter(GroupId__in=[1, 2, 3, 4], order='-GroupId,-MinisterId')
for r in records:
    print(111, r._record.__dict__)
