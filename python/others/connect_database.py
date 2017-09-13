# -*- coding: utf-8 -*-

# ---------------------------------------------------------
# mysql
# ---------------------------------------------------------

import MySQLdb

conn=MySQLdb.connect(host="localhost", port=3306, user="test", passwd="test", db="test", charset="utf8") 

cursor = conn.cursor()

# ---------------------------------------------------------
# mongo
# ---------------------------------------------------------
# pymongo
from pymongo import MongoCLient
client = MongoClient('mongodb://test:test@localhost:227017/test')
# or
client = MongoClient('localhost', '27017')
db = client['test']
db.authenticate('test', 'test')

# mongoengine
from mongoengine import connect
connect('mongodb://test:test@test:27017/test')
# or
connect(db='test',
    host='localhost',
    port=27017,
    username='test',
    password='test')

# ---------------------------------------------------------
# hive
# ---------------------------------------------------------
from pyhive import hive

cursor = hive.connect("10.0.0.122").cursor()
cursor.execute("SELECT * from table_name")
print cursor.fetchone()


