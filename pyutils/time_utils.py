# -*- coding: utf-8 -*-
"""
    utils.time_utils
    ~~~~~~~~~~~~~~~~~

    时间相关

    * 始终使用 "offset-aware" datetime对象,即带时区.
    * 始终以 UTC 格式存储, 仅与用户交互时进行时区转换
    * 始终使用ISO 8601 作为输入输出字符串格式

    :create by: lyncir
    :date: 2018-11-17 15:23:50 (+0800)
    :last modified date: 2019-01-25 09:47:53 (+0800)
    :last modified by: lyncir
"""
import datetime
import pytz
import tzlocal
import dateutil.parser


def utc_now():
    """
    获取当前时间

    :return: 带时区的UTC时间
    :rtype: datetime
    """
    return pytz.utc.localize(datetime.datetime.utcnow())


def local_datetime(utc_dt_aware, tz=None):
    """
    从UTC时区时间转换为本地时间

    :param datetime utc_dt_aware: UTC时间
    :param str tz: 本地时区字符串
    :return: 带时区的本地时间
    :rtype: datetime
    """
    if tz is None:
        tz = tzlocal.get_localzone().zone

    # 时区都为UTC
    if tz == 'UTC':
        return utc_dt_aware

    return utc_dt_aware.astimezone(pytz.timezone(tz))


def utc_datetime(local_dt_aware, tz='UTC'):
    """
    从本地时区时间转为UTC时间

    :param datetime local_dt_aware: 本地时间
    :param str tz: 本地时区字符串
    :return: 带时区的UTC时间
    :rtype: datetime
    """
    # 时区一致
    if local_dt_aware.tzinfo == pytz.timezone(tz):
        return local_dt_aware

    return local_dt_aware.astimezone(pytz.timezone(tz))


def str_to_datetime(dt_str, tz='UTC'):
    """
    解析ISO 8601字符串时间格式

    eg:
        2018-02-04T19:30:00+08:00

    :param str dt_str: 时间字符串
    :param str tz: 时区
    :return: 带时区的时间
    :rtype: datetime
    """
    dt_aware = dateutil.parser.parse(dt_str)

    # 时区一致
    if dt_aware.tzinfo == pytz.timezone(tz):
        return dt_aware

    return dt_aware.astimezone(pytz.timezone(tz))


def to_timestamp(dt_aware):
    """
    转换时间为时间戳

    :param datetime dt_aware: 带时区的时间
    :return: 时间戳
    :rtype: float
    """
    return dt_aware.timestamp()


def timestamp_to_datetime(ts, tz='UTC'):
    """
    时间戳转换为带时区时间

    :param float ts: 时间戳
    :param str tz: 时区字符串
    :return: 带时区的时间
    :rtype: datetime
    """
    # 转成未带时区的本地时间
    dt = datetime.datetime.utcfromtimestamp(ts)
    dt_aware = pytz.utc.localize(dt)

    if tz is None:
        tz = tzlocal.get_localzone().zone

    # 都为UTC时间
    if tz == 'UTC':
        return dt_aware

    return dt_aware.astimezone(pytz.timezone(tz))
