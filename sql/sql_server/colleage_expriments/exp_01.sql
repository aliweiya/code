create database EDUC on 
    (name='EDUC_data',
    filename='D:\jxgl\EDUC.mdf',
    size=10MB,maxsize=60MB,filegrowth=5%)
    log on (name='EDUC_log',
    filename='D:\jxgl\EDUC.ldf',
    size=4MB,maxsize=10MB,filegrowth=1MB)
create database userdb on
    (name='userdb',
     filename='D:\jxgl\userdb.mdf')
drop database userdb