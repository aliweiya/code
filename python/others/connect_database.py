# -*- coding: utf-8 -*-

# ---------------------------------------------------------
# mysql
# ---------------------------------------------------------

import MySQLdb

conn=MySQLdb.connect(host="localhost", port=3306, user="test", passwd="test", db="test", charset="utf8") 

cursor = conn.cursor()
cursor.execute("select count(1) from user_baseinfo where mobile REGEXP '^[1][35678][0-9]{9}$'")
cursor.fetchall()

# ---------------------------------------------------------
# mongo
# ---------------------------------------------------------
# pymongo
from pymongo import MongoCLient
client = MongoClient('mongodb://test:test@localhost:227017/test')
# or
client = MongoClient('localhost', 27017)
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

# ---------------------------------------------------------
# sqlite
# ---------------------------------------------------------
import sqlite3

SQL = """
    CREATE TABLE IF NOT EXISTS userinfo(
        username TEXT NOT NULL,
        password TEXT,
        PRIMARY KEY (username)
        );
"""

UPDATE = """
    UPDATE userinfo SET password='"123456"' WHERE username='MrTurtle';
"""

INSERT = """
    INSERT INTO userinfo VALUES('MrTurtle', '123');
"""

FIND = """
    SELECT * FROM userinfo;
"""

DELETE = """
    DELETE FROM userinfo WHERE username = 'MrTurtle';
"""

conn = sqlite3.connect('userinfo.db')

cur = conn.cursor()

cur.execute(SQL)
# cur.execute(DELETE)
cur.execute(INSERT)
conn.commit()
# cur.execute(FIND)
# cur.execute(UPDATE)


