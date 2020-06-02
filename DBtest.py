#!/usr/bin/env python
# -*- coding:utf-8 -*-

import pymysql

conn = pymysql.connect(host='localhost', user="spider", password='R~!@34qwe-spider', port=3306)
cursor = conn.cursor()


sql = 'CREATE DATABASE db_stock12;'
result = cursor.execute(sql)
print(result)
print(cursor.fetchall())

sql = 'SHOW DATABASES;'
result = cursor.execute(sql)
print("show db:%s" % result)
print(cursor.fetchmany(size=3))

cursor.close()
conn.close()
