# -*- coding: utf-8 -*-
"""
Module Description: 各数据源的数据访问调用接口
Date: 2016/12/3
Author:Bai Jin Ping
"""
import abc
from datetime import datetime, date


class IModelManager(object):
    """提供管理数据的管理接口"""
    __metaclass__ = abc.ABCMeta

    def all(self):
        """
        返回所有数据
        """

    def filter(self, **kwargs):
        """
        查询并返回一个列表

        # eq
        >>> # SELECT * FROM Table WHERE Gold = 10
        >>> objects.filter(Gold=10)
        >>> objects.filter(Gold__eq=10)
        # ne
        >>> # SELECT * FROM Table WHERE Gold != 10
        >>> objects.filter(Gold__ne=10)
        # lt
        >>> # SELECT * FROM Table WHERE Gold < 10
        >>> objects.filter(Gold__lt=10)
        # lte
        >>> # SELECT * FROM Table WHERE Gold <= 10
        >>> objects.filter(Gold__lte=10)
        # gt
        >>> # SELECT * FROM Table WHERE Gold > 10
        >>> objects.filter(Gold__gt=10)
        # gte
        >>> # SELECT * FROM Table WHERE Gold >= 10
        >>> objects.filter(Gold__gte=10)
        # in
        >>> # SELECT * FROM Table WHERE Gold in (10,20,30)
        >>> objects.filter(Gold__in=[10, 20, 30])
        # is
        >>> # SELECT * FROM Table WHERE MayNullStr is null
        >>> objects.filter(MayNullStr__is=None)
        # isnot
        >>> # SELECT * FROM Table WHERE MayNullStr is not null
        >>> objects.filter(MayNullStr__isnot=None)
        # like
        >>> # SELECT * FROM Table WHERE SomeStr like 'Me%'
        >>> objects.filter(SomeStr__like='Me%')
        >>> # SELECT * FROM Table WHERE SomeStr like '%Me'
        >>> objects.filter(SomeStr__like='%Me')
        >>> # SELECT * FROM Table WHERE SomeStr like '%Me%'
        >>> objects.filter(SomeStr__like='%Me%')
        """

    def columns(self, *fields):
        """
        限定查询返回的数据列.
        若尝试获取未在限定列表中的列的值,获取到的是默认值.
        >>> # SELECT * FROM Table WHERE Rid="rid" ==>> SELECT Name FROM Table WHERE Rid="rid"
        >>> objects.columns('Name').get(Rid='rid')
        >>> # SELECT * FROM Table WHERE Rid="rid" ==>> SELECT Name, Uid, Lv, SrvId FROM Table WHERE Rid="rid"
        >>> objects.columns('Name', 'Uid', 'Lv', 'SrvId').filter(Rid='rid')
        >>> objects.columns(*['Name', 'Uid', 'Lv', 'SrvId']).filter(Rid='rid')
        """

    def get(self, **kwargs):
        """
        查询并返回一个记录
        """

    def count(self, **kwargs):
        """
        返回查询结果集的记录数量
        >>> count()
        返回表的记录数
        >>> count(**kwargs)
        返回符合条件的记录数
        """

    def max(self, field_name):
        """
        返回指定字段当前的最大值

        >>> dal.max('Gold')
        >>> dal.column().filter().max('Gold')
        """

    def min(self, field_name):
        """
        返回指定字段当前的最小值

        >>> dal.min('Gold')
        >>> dal.column().filter().min('Gold')
        """

    def order(self, *fields):
        """
        排序的字段
        :param fields: 排序的字段列表，带'-'前缀则为降序，否则为升序
        :return:
        """

    def create(self, **kwargs):
        """
        创建一条记录并返回

        传入的参数可以不是主键，但若主键字段冲突/唯一索引字段冲突，则 会立刻报错

        :note 不论是否被事务包含,create会直接提交
        """

    def get_or_create(self, **kwargs):
        """
        查询是否存在，若不存在则创建一条新记录

        注意查询条件需要能够唯一指定一个记录，即查询条件的参数字段创建后不能发生改变
        :return record, is_new
        """

    def insert_many(self, data_list):
        """
        批量插入记录

        >>> data_list = [{'field1': 'val1-1', 'field2': 'val1-2'}, {'field1': 'val2-1', 'field2': 'val2-2'}]
        >>> objects.insert_many(data_list)
        :param data_list: 新纪录的字段数据列表
        :return:
        """

    def update(self, **kwargs):
        """
        更新符合条件的记录

        若不传入筛选条件，为了避免错误更新全表数据，会报错
        >>> objects.filter(X=0).update(X=3)   # 正常
        >>> objects.update(X=3)                    # 报错
        >>> objects.filter().update(X=3)         # 报错
        """

    def update_force(self, **kwargs):
        """
        更新符合条件的记录，只在需要更新全表数据时使用
        >>> objects.update_force(X=3)   # 正常，更新所有数据
        >>> objects.filter().update_force(X=3) # 正常，更新所有数据
        """

    def delete(self):
        """
        删除符合条件的记录

        若不传入筛选条件，为了避免错误删除全表数据，会报错
        >>> objects.filter(X=0).delete()   # 正常
        >>> objects.delete()                    # 报错
        >>> objects.filter().delete()         # 报错
        """

    def delete_force(self):
        """
        删除符合条件的记录，只在需要删除全表数据时使用
        >>> objects.delete_force()   # 正常，删除所有数据
        >>> objects.filter().delete_force() # 正常，删除所有数据
        """

    def sql_query(self, sql):
        """
        执行查询sql语句,返回[{record}, ...],直接在db执行,不保证数据是最新的
        >>> objects.sql_query('SELECT * FROM TbRole') # 正常,返回TbRole所有数据
        >>> objects.sql_query('INSERT INTO TbItem VALUES("guid", "1", "1", "3")') # 报错,不能执行INSERT语句
        >>> objects.sql_query('UPDATE TbRole SET Sex=0') # 报错,不能执行UPDATE语句
        >>> objects.sql_query('DELETE FROM TbTitle') # 报错,不能执行DELETE语句
        """


class PyDBLiteDALDescriptor(object):
    """
    peewee数据访问管理类描述器
    """
    def __get__(self, instance, owner):
        return PyDBLiteDALManager(owner.model_class, owner)


class PyDBLiteDALManager(IModelManager):
    """管理peewee数据请求"""

    def __init__(self, model_class, po_class):
        self.model_class = model_class
        self.po_class = po_class
        self.db = model_class.database
        self.table = self.db[model_class.__name__]
        self.operations = {
            '=': '__eq__',
            'in': '__eq__',
            'ne': '__ne__',
            'lt': '__lt__',
            'lte': '__le__',
            'gt': '__gt__',
            'gte': '__ge__',
        }

    def all(self):
        """
        返回所有数据
        """
        return [self.po_class(self.dict2obj(**r)) for r in self.table]

    def create(self, **kwargs):
        """
        创建一条记录
        """
        rec_id = self.table.insert(**kwargs)
        record = self.table[rec_id]
        return self.po_class(self.dict2obj(**record))

    def insert_many(self, data_list):
        """
        插入多条数据
        """
        if not data_list:
            return

        self.table.insert(data_list)

    def get(self, **kwargs):
        """
        查询并返回一个记录
        """
        records = self.table(**kwargs)
        if records and len(records) > 0:
            return self.po_class(self.dict2obj(**records[0]))

    def filter(self, **kwargs):
        """
        查询并返回一个列表 多个条件是AND关系
        """
        filters = []
        for field_opt, val in kwargs.iteritems():
            field_opt_split = field_opt.rsplit('__')
            if len(field_opt_split) == 1:
                field = field_opt_split[0]
                opt = '='
            elif len(field_opt_split) == 2:
                field, opt = field_opt_split
            else:
                raise NotImplementedError

            # 如果in的元素是空集,则返回None
            if opt == 'in':
                if val:
                    # 列表元素转换为字符型
                    val = [str(v) if type(v) is not str else v for v in val]
                else:
                    return []

            f = self.table.filter(field)
            f = getattr(f, self.operations[opt])(val)
            filters.append(f)

        return [self.po_class(self.dict2obj(**r)) for r in reduce(lambda x, y: x & y, filters)]

    def dict2obj(self, **kwargs):
        """
        创建一个model对象
        """
        obj = object.__new__(self.model_class)
        obj.__dict__ = kwargs
        return obj


class PeeweeDALDescriptor(object):
    """
    peewee数据访问管理类描述器
    """
    def __get__(self, instance, owner):
        return PeeweeDALManager(owner.model_class, owner)


class PeeweeDALManager(IModelManager):
    """管理peewee数据请求"""

    def __init__(self, model_class, po_class):
        import peewee
        assert issubclass(model_class, peewee.Model)
        self.model_class = model_class
        self.po_class = po_class

        # 过滤条件
        self._filter = {}
        # 查询字段
        self._columns = []
        # 条件连接符，只支持一种类型
        self._operator = 'AND'
        # 排序字段
        self._order = []
        # 限制记录数
        self._limit = None
        # 偏移量
        self._offset = 0

    #################
    # 查询方法（链式调用）
    #################

    def columns(self, *fields):
        """
        返回的数据列
        :param fields:
        """
        if self._columns:
            raise ValueError("Don't call columns() twice")

        for field in fields:
            if field not in self._columns:
                self._columns.append(field)
        return self

    def _all(self):
        return self.model_class.select()

    def filter(self, **kwargs):
        """
        查询并返回一个列表
        """
        cdt = {}
        for k, v in kwargs.iteritems():
            if '__' not in k:
                # 默认比较相等
                k += '__eq'
            cdt[k] = v

        self._filter.update(cdt)
        return self

    def order(self, *fields):
        """
        排序的字段
        :param fields:
        :return:
        """
        if self._order:
            # 因为排序字段的次序有意义，所以不允许调用多次，一次性定义好
            raise ValueError("Don't call order() twice")

        self._order = list(fields)
        return self

    def limit(self, limit, offset=0):
        """
        限制记录条数
        :param limit:
        :param offset:
        :return:
        """
        assert limit > 0 and offset >= 0

        self._limit = limit
        self._offset = offset
        return self

    #################
    # 具体操作方法（立即执行操作并返回结果）
    #################

    def all(self):
        """
        返回所有数据
        """
        return [self.po_class(data) for data in self._all()]

    def get(self, **kwargs):
        """
        查询并返回一个记录
        """
        record_set = self.filter(**kwargs).limit(1)._select_query()
        if record_set and len(record_set) > 0:
            return self.po_class(record_set[0])

    def count(self):
        """
        返回查询结果集的记录数量
        >>> objects.filter().count()
        """
        import peewee

        # 获得count时,不能设置offset
        assert self._offset == 0

        result = self._select_query()
        return result.aggregate(peewee.fn.Count('*'))

    def max(self, field_name):
        if self._columns and field_name not in self._columns:
            # 调用max前用column
            raise ValueError("Field(%s) not in result set!" % field_name)

        import peewee
        result = self._select_query()
        return result.aggregate(peewee.fn.Max(getattr(self.model_class, field_name)))

    def min(self, field_name):
        if self._columns and field_name not in self._columns:
            # 调用min前用column
            raise ValueError("Field(%s) not in result set!" % field_name)

        import peewee
        result = self._select_query()
        return result.aggregate(peewee.fn.Min(getattr(self.model_class, field_name)))

    def create(self, **kwargs):
        # with PeeweeTransaction(propagation=TransactionPropagation.REQUIRES_NEW):
        data = self.model_class.create(**kwargs)
        return data if data is None else self.po_class(data)

    def get_or_create(self, **kwargs):
        po_obj = self.get(**kwargs)
        if po_obj:
            return po_obj, False

        po_obj = self.create(**kwargs)
        return po_obj, True

    def insert_many(self, data_list):
        if not data_list:
            return
        self.model_class.insert_many(data_list).execute()

    def update(self, **kwargs):
        if not self._filter:
            raise ValueError("Can't update table without filter condition.Try use update_force")

        return self._do_update(**kwargs)

    def update_force(self, **kwargs):
        return self._do_update(**kwargs)

    def delete(self):
        if not self._filter:
            raise ValueError("Can't delete table without filter condition.Try use delete_force")

        return self._do_delete()

    def delete_force(self):
        return self._do_delete()

    def _expressions(self):
        """
        构造查询筛选参数列表
        """
        import peewee

        expressions = []
        for field_opt, val in self._filter.iteritems():
            field, opt = field_opt.rsplit('__')

            # 如果in的元素是空集,则返回None
            if opt == 'in' and not val:
                return

            # 支持eq, lt, lte, gt, gte, ne, in, is, isnot, like
            pw_opt = peewee.DJANGO_MAP.get(opt)
            # 增加isnot支持
            if opt == 'isnot':
                pw_opt = peewee.OP.IS_NOT
            if not pw_opt\
                    or pw_opt in ['ilike', 'regexp']:  # 不支持的方法
                raise NotImplementedError('Unsupported filter condition:(%s)' % opt)

            exp = peewee.Expression(
                lhs=getattr(self.model_class, field),
                op=pw_opt,
                rhs=val
            )
            expressions.append(exp)
        return expressions

    def _select_query(self):
        """
        构造peewee.SelectQuery对象并返回
        """

        # 筛选列
        clns = [getattr(self.model_class, cln) for cln in self._columns]
        select_obj = self.model_class.select(*clns)

        # 排序
        if self._order:
            order_clauses = []
            for order_field in self._order:
                # ASC field
                if order_field[0] != '-':
                    clause = getattr(self.model_class, order_field).asc()
                # DESC field
                else:
                    clause = getattr(self.model_class, order_field[1:]).desc()
                order_clauses.append(clause)

            select_obj = select_obj.order_by(*order_clauses)

        # limit, offset
        if self._limit:
            select_obj = select_obj.limit(self._limit)
        if self._offset:
            select_obj = select_obj.offset(self._offset)

        # 查询条件
        expressions = self._expressions()

        if expressions is None:
            return []

        return select_obj if not expressions else select_obj.where(*expressions)

    def _update_query(self, **kwargs):
        """
        构造peewee.UpdateQuery对象并返回
        """
        return self.model_class.update(**kwargs)

    def _delete_query(self):
        """
        构造peewee.DeleteQuery对象并返回
        """
        return self.model_class.delete()

    def _do_update(self, **kwargs):
        update_obj = self._update_query(**kwargs)
        expressions = self._expressions()
        if expressions is None:
            return
        if not expressions:
            return update_obj.execute()
        else:
            return update_obj.where(*expressions).execute()

    def _do_delete(self):
        delete_obj = self._delete_query()
        expressions = self._expressions()
        if expressions is None:
            return
        if not expressions:
            return delete_obj.execute()
        else:
            return delete_obj.where(*expressions).execute()

    def sql_query(self, sql):
        import peewee
        db = self.model_class._meta.database
        if isinstance(db, peewee.MySQLDatabase):
            from pymysql.cursors import DictCursor
            conn = db.get_conn()
            with conn.cursor(DictCursor) as cursor:
                cursor.execute(sql)
                result = cursor.fetchall()
                return result

        elif isinstance(db, peewee.SqliteDatabase):
            conn = db.get_conn()
            cursor = conn.cursor()
            cursor.execute(sql)
            res = cursor.fetchall()
            result = []
            for row in res:
                rcd = {}
                for idx, col in enumerate(cursor.description):
                    rcd[col[0]] = row[idx]
                result.append(rcd)
            return result

    #################
    # MAGIC METHODS #
    #################
    def __len__(self):
        """支持len()"""
        return len(self._record_set)

    def __iter__(self):
        """支持遍历"""
        for po in self._record_set:
            yield po

    def __getitem__(self, index):
        """支持分片slice"""
        return self._record_set[index]

    @property
    def _record_set(self):
        """缓存的结果集"""
        if hasattr(self, '_cache_rs'):
            return self._cache_rs

        # 执行查询并缓存
        record_set = self._select_query()
        po_set = []
        if record_set:
            po_set = [self.po_class(record) for record in record_set]
        self._cache_rs = po_set
        return self._cache_rs


########################################
#   ↓统一查询接口相关实现↓
########################################
class DALDescriptor(object):
    """
    数据服务访问管理类描述器
    """

    def __get__(self, instance, owner):
        return DALManager(owner.model_class, owner)


class DALManager(IModelManager):

    def __init__(self, model_class, po_class):
        import orm.models
        assert issubclass(model_class, orm.models.Model)

        self.model_class = model_class
        self.po_class = po_class

        self.datasource = model_class.get_datasource()

        # 过滤条件
        self._filter = {}
        # 查询字段
        self._columns = []
        # 条件连接符，只支持一种类型
        self._operator = 'AND'
        # 排序字段
        self._order = []
        # 限制记录数
        self._limit = None
        # 偏移量
        self._offset = 0

        from framework.dal.orm.controller_api import ORMController
        self.orm_controller = ORMController

    #################
    # 具体操作方法（立即执行操作并返回结果）
    #################
    @staticmethod
    def _verify_empty_list_condition(conditions):
        """
        检查筛选条件字典是否存在空列表条件, 若存在则不做任何处理直接返回:
        - 对于查询, 直接返回空列表
        - 对于更新/删除, 直接返回0(表示无记录被更新/删除)
        :conditions 条件字典
        :return bool
        """
        for filter_key, filter_val in conditions.iteritems():
            if filter_key.endswith('__in') and not filter_val:
                return True

        return False

    def execute(self):
        # 使用in条件查询但in集合为空,直接返回空列表
        if self._verify_empty_list_condition(self._filter):
                return []

        # 限定列查询对于事务内查询限制比较大, 因此需要特殊处理
        if self._columns:
            # 将主键字段也添加到columns条件中,使事务内查询的二次比对能够正常执行
            for field in self.model_class.get_primary_keys():
                if field not in self._columns:
                    self._columns.append(field)

            # 如果有指定排序字段, 要将排序字段也添加到columns条件中,使事务内查询二次比对后的本地排序能够正常执行
            for field in self._order:
                field = field[1:] if field.startswith('-') else field
                if field not in self._columns:
                    self._columns.append(field)

        return self.orm_controller.select_model(self.model_class,
                                                conditions=self._filter,
                                                columns=self._columns,
                                                order=self._order,
                                                limit=self._limit,
                                                offset=self._offset)

    def all(self):
        with self.datasource:
            all_rcds = self.orm_controller.select_model(self.model_class, conditions={})
            return [self.po_class(data) for data in all_rcds]

    def get(self, **kwargs):
        with self.datasource:
            res = self.filter(**kwargs).limit(1).execute()
            if res:
                return self.po_class(res[0])

    def count(self):
        with self.datasource:
            result = self.orm_controller.count(mdl_cls=self.model_class, conditions=self._filter)
            return 0 if not result else result

    def max(self, field_name):
        with self.datasource:
            return self.orm_controller.max(mdl_cls=self.model_class, field_name=field_name, conditions=self._filter)

    def min(self, field_name):
        with self.datasource:
            return self.orm_controller.min(mdl_cls=self.model_class, field_name=field_name, conditions=self._filter)

    def create(self, **kwargs):
        with self.datasource:
            instance = self.model_class(**kwargs)
            self.orm_controller.insert(instance)
            instance._isnew = False
            instance.clear_update_dict()
            return self.po_class(instance)

    def get_or_create(self, **kwargs):
        po_obj = self.get(**kwargs)
        if po_obj:
            return po_obj, False

        po_obj = self.create(**kwargs)
        return po_obj, True

    def insert_many(self, data_list):
        if not data_list:
            return

        with self.datasource:
            self.orm_controller.insert_many(self.model_class, obj_list=data_list)

    @staticmethod
    def _parse_args(update_kwargs):
        """
        解析更新的字典值
        :param update_kwargs:
        :return:
        """
        for field_name in update_kwargs:
            v = update_kwargs[field_name]
            if isinstance(v, datetime):
                v = v.replace(microsecond=0).__str__()
            elif isinstance(v, date):
                v = str(v)
            update_kwargs[field_name] = v

    def _do_update(self, **kwargs):
        if self._verify_empty_list_condition(self._filter):
            return 0

        self._parse_args(kwargs)

        with self.datasource:
            return self.orm_controller.update_by_conditions(self.model_class,
                                                            conditions=self._filter,
                                                            values=kwargs)

    def update(self, **kwargs):
        if not self._filter:
            raise ValueError("Can't update table without filter condition.Try use update_force")

        self._do_update(**kwargs)

    def update_force(self, **kwargs):
        self._filter = {}
        self._do_update(**kwargs)

    def _do_delete(self):
        if self._verify_empty_list_condition(self._filter):
            return 0

        with self.datasource:
            return self.orm_controller.delete_by_conditions(self.model_class, conditions=self._filter)

    def delete(self):
        if not self._filter:
            raise ValueError("Can't delete table without filter condition.Try use delete_force")

        self._do_delete()

    def delete_force(self):
        self._filter = {}
        self._do_delete()

    def sql_query(self, sql):
        with self.datasource:
            return self.orm_controller.execute_sql(sql)

    #################
    # 查询方法（链式调用）
    #################
    def columns(self, *fields):
        """
        返回的数据列
        :param fields:
        """
        if self._columns:
            raise ValueError("Don't call columns() twice")

        if not fields:
            return self

        for field in fields:
            if field not in self._columns:
                self._columns.append(field)

        return self

    def filter(self, **kwargs):
        """
        查询并返回一个列表
        """
        cdt = {}
        for k, v in kwargs.iteritems():
            if '__' not in k:
                # 默认比较相等
                k += '__eq'
            if isinstance(v, datetime):
                v = v.replace(microsecond=0).__str__()
            elif isinstance(v, date):
                v = str(v)
            cdt[k] = v

        self._filter.update(cdt)
        return self

    def order(self, *fields):
        """
        排序的字段
        :param fields:
        :return:
        """
        if self._order:
            # 因为排序字段的次序有意义，所以不允许调用多次，一次性定义好
            raise ValueError("Don't call order() twice")

        self._order = list(fields)
        return self

    def limit(self, limit, offset=0):
        """
        限制记录条数
        :param limit:
        :param offset:
        :return:
        """
        assert limit > 0 and offset >= 0

        self._limit = limit
        self._offset = offset
        return self

    #################
    # MAGIC METHODS #
    #################
    def __len__(self):
        """支持len()"""
        return len(self._record_set)

    def __iter__(self):
        """支持遍历"""
        rs = self._record_set
        for po in rs:
            yield po

    def __getitem__(self, index):
        """支持分片slice"""
        return self._record_set[index]

    @property
    def _record_set(self):
        """缓存的结果集"""
        if hasattr(self, '_cache_rs'):
            return self._cache_rs

        with self.datasource:
            # 执行查询并缓存
            record_set = self.execute()
            po_set = []
            if record_set:
                po_set = [self.po_class(record) for record in record_set]
            self._cache_rs = po_set
            return self._cache_rs


########################################
#   ↓事务相关实现↓
########################################
class TransactionDelegator(object):
    """具体事务类委托对象"""
    transaction_class = None

    @classmethod
    def set_transaction_class(cls, concrete_transaction_class):
        """设置具体事务类,进程内只能设置一次"""
        cls.transaction_class = concrete_transaction_class

    def __new__(cls, *args, **kwargs):
        return cls.transaction_class(*args, **kwargs)
