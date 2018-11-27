# -*- coding: utf-8 -*-
"""
    .filename
    ~~~~~~~~~~~~~~

    生成测试数据

    :create by: lyncir
    :date: 2018-11-21 10:24:16 (+0800)
    :last modified date: 2018-11-26 11:38:28 (+0800)
    :last modified by: lyncir
"""
import time

import pymysql


size = 2000000

db_kwargs = {
    "host": 'localhost',
    "user": 'root',
    "password": '',
    "db": 'daqing2_profile_test',
    "charset": 'utf8mb4',
}


def main():

    start = time.time()

    sql = """
    INSERT INTO KeyWord (Word) VALUES ("测试"),("测试"),("测试"),("测试"),
    ("测试"),("测试"),("测试"),("测试"),("测试"),("测试");
    """

    conn = pymysql.connect(**db_kwargs)
    cur = conn.cursor()

    times = size / 10

    for _ in xrange(times):
        cur.execute(sql)
        conn.commit()

    end = time.time()

    print("total: ", end - start)


if __name__ == '__main__':
    main()
