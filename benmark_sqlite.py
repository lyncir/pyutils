# -*- coding: utf-8 -*-
"""
    .filename
    ~~~~~~~~~~~~~~

    Description

    :create by: lyncir
    :date: 2018-11-22 11:58:19 (+0800)
    :last modified date: 2018-11-26 16:55:25 (+0800)
    :last modified by: lyncir
"""
import time
import pymysql
import sqlite3


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

    # records = []
    # size = 1000
    # rows = cur.fetchmany(size)
    # print(time.time() - start)
    # while rows:
    #     records.extend(rows)
    #     rows = cur.fetchmany(size)
    #     time.sleep(0.1)

    end = time.time()
    print(len(records))
    print("Load data from mysql take {}s".format(end - start))

    # sqlite
    sqlite_start = time.time()

    sqlite_conn = sqlite3.connect(':memory:')
    c = sqlite_conn.cursor()

    c.execute("""CREATE TABLE KeyWord (
    Id INTEGER PRIMARY KEY,
    Word TEXT);
    """)

    sql = """
    INSERT INTO KeyWord (Id, Word) VALUES({}, "{}");
    """

    for record in records:
        k, v = record
        raw_sql = sql.format(k, v.encode('utf8'))
        c.execute(raw_sql)
        # break

    sqlite_end = time.time()
    print("Sqlite insert data take {}s".format(sqlite_end - sqlite_start))


if __name__ == '__main__':
    main()
