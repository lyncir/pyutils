# -*- coding: utf-8 -*-
"""
    .filename
    ~~~~~~~~~~~~~~

    Description

    :create by: lyncir
    :date: 2018-11-27 10:28:12 (+0800)
    :last modified date: 2018-11-28 15:38:20 (+0800)
    :last modified by: lyncir
"""
import json

from model import Model
from dal_manager import PyDBLiteDALDescriptor


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

    GroupId = int
    MinisterId = int
    NeedItem = str
    StrengthenBuffList = str
    BuffTypeList = str
    TalentUnlock = str
    ClothesItemId = int
    StrengthenLvLimit = int


class BaseAdapter(object):
    """
    适配器基类

    >>> class ConcreteAdapter(BaseAdapter):
    ...         # __init__() -> 非必要
    ...         # 实现父类抽象方法 -> 必要
    ...         # 新增的功能方法 -> 非必要
    ...         # setter/getter方法 -> 必要
    """

    # 对应的具体模型类
    model_class = None
    # 对应的具体模型查询管理类
    objects = None

    def __init__(self, record=None):
        """
        :param record: 对应的具体模型记录
        """
        # 委托的适配对象
        self._record = record


class TcMinisterGroupAdapter(BaseAdapter):
    """
    TcMinisterGroup适配器
    """

    def asdict(self):
        return {
            'NeedItem': self.NeedItem,
            'BuffTypeList': self.BuffTypeList,
            'StrengthenBuffList': self.StrengthenBuffList,
            'MinisterId': self.MinisterId,
            'GroupId': self.GroupId,
            'TalentUnlock': self.TalentUnlock,
            'ClothesItemId': self.ClothesItemId,
            'StrengthenLvLimit': self.StrengthenLvLimit,
        }

    @property
    def StrengthenLvLimit(self):
        return self._record.StrengthenLvLimit

    @StrengthenLvLimit.setter
    def StrengthenLvLimit(self, val):
        self._record.StrengthenLvLimit = val

    @property
    def ClothesItemId(self):
        return self._record.ClothesItemId

    @ClothesItemId.setter
    def ClothesItemId(self, val):
        self._record.ClothesItemId = val

    @property
    def TalentUnlock(self):
        return json.loads(self._record.TalentUnlock)

    @TalentUnlock.setter
    def TalentUnlock(self, val):
        self._record.TalentUnlock = json.dumps(val)

    @property
    def NeedItem(self):
        return json.loads(self._record.NeedItem)

    @NeedItem.setter
    def NeedItem(self, val):
        self._record.NeedItem = json.dumps(val)

    @property
    def BuffTypeList(self):
        return json.loads(self._record.BuffTypeList)

    @BuffTypeList.setter
    def BuffTypeList(self, val):
        self._record.BuffTypeList = json.dumps(val)

    @property
    def StrengthenBuffList(self):
        return json.loads(self._record.StrengthenBuffList)

    @StrengthenBuffList.setter
    def StrengthenBuffList(self, val):
        self._record.StrengthenBuffList = json.dumps(val)

    @property
    def MinisterId(self):
        return self._record.MinisterId

    @MinisterId.setter
    def MinisterId(self, val):
        self._record.MinisterId = val

    @property
    def GroupId(self):
        return self._record.GroupId

    @GroupId.setter
    def GroupId(self, val):
        self._record.GroupId = val


TcMinisterGroupAdapter.model_class = TcMinisterGroup
TcMinisterGroupAdapter.objects = PyDBLiteDALDescriptor()
