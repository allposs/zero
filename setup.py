#!/usr/bin/env python
# _*_coding:utf-8_*_
import pymysql


conn = pymysql.connect(host='127.0.0.1', port=3306, user='root', passwd='redhat',) 
cur = conn.cursor()
DBint = cur.execute("SELECT * FROM information_schema.SCHEMATA where SCHEMA_NAME='cmdb';")
if DBint == 0 :
    cur.execute("CREATE DATABASE cmdb")
    cur.execute("USE cmdb")
    cur.execute("create table Servers_Info \
( \
   UUID                 varchar(38) not null,\
   Asset_Number         varchar(10) not null,\
   Service_Model        text,\
   CPU_Numbers          TINYINT,\
   CPU_Model            text,\
   Memory_Numbers       tinyint,\
   Memory_Model         text,\
   Memory_Capacity      tinyint,\
   Disk_Numbers         tinyint,\
   Disks_Model          text,\
   Disks_Capacity       tinyint,\
   NetworkCar_Model     text,\
   NetworkCar_Numbers   tinyint,\
   primary key (UUID)\
)")

    cur.execute("create table Users_Info\
(\
   UUID                 varchar(38) not null,\
   Users                varchar(20) not null,\
   Passwd               Varchar(20) not null,\
   Name                 Nvarchar(20),\
   Mail                 varchar(50),\
   Car                  int(11)\
)")
    cur.execute("INSERT INTO `cmdb`.`users_info` (`UUID`, `Users`, `Passwd`, `Name`) VALUES ('23f87b528d0f11e696a7f45c89a82eee', 'admin', 'redhat', 'admin')")
    conn.commit()
    conn.close()
else:
    print("error")
    conn.close()