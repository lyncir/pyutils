# -*- coding: utf-8 -*-
"""
    .filename
    ~~~~~~~~~~~~~~

    Description

    :create by: lyncir
    :date: 2018-11-27 10:28:12 (+0800)
    :last modified date: 2018-11-27 15:11:21 (+0800)
    :last modified by: lyncir
"""
import peewee

from model import Model


# class TcMinisterGroup(Model):

#     GroupId = int
#     MinisterId = int
#     NeedItem = str
#     StrengthenBuffList = str
#     BuffTypeList = str
#     TalentUnlock = str
#     ClothesItemId = int
#     StrengthenLvLimit = int

class TcMinisterGroup(Model):

    class Meta:
        primary_key = peewee.CompositeKey("GroupId", "MinisterId")

    GroupId = peewee.IntegerField(default=1)
    MinisterId = peewee.IntegerField()
    NeedItem = peewee.CharField(default="[]", max_length=127, null=True)
    StrengthenBuffList = peewee.CharField(default="[]", max_length=1023, null=True)
    BuffTypeList = peewee.CharField(default="[]", max_length=1023, null=True)
    TalentUnlock = peewee.CharField(default="{}", max_length=127, null=True)
    ClothesItemId = peewee.IntegerField(default=0)
    StrengthenLvLimit = peewee.IntegerField(default=0)
