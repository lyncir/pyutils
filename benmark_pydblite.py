# -*- coding: utf-8 -*-
"""
    .filename
    ~~~~~~~~~~~~~~

    Description

    :create by: lyncir
    :date: 2018-11-26 11:14:53 (+0800)
    :last modified date: 2018-11-26 11:27:52 (+0800)
    :last modified by: lyncir
"""
import time
import pymysql
from pydblite.sqlite import Database, Table


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
    SELECT * FROM KeyWord;
    """

    conn = pymysql.connect(**db_kwargs)
    cur = conn.cursor()

    cur.execute(sql)

    records = cur.fetchall()

    end = time.time()
    print("Load data from mysql take {}s".format(end - start))

    # pydblite
    dblite_start = time.time()

    db = Database(':memory:')
    table = Table('KeyWord', db)
    table.create(('Id', 'INTEGER'), ('Word', 'TEXT'))
    table.open()

    for record in records:
        k, v = record
        table.insert(Id=k, Word=v)
        # break

    print(len(table))

    dblite_end = time.time()
    print("pydblite insert data take {}s".format(dblite_end - dblite_start))


if __name__ == '__main__':
    main()
