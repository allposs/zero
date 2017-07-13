#!/usr/bin/env python
#_*_coding:utf-8_*_
#import json,random
import pymysql
import time
import json
from tools.tools import Get_Sql_Insert,Get_Sql_Detele,Get_Sql_Select,Get_Sql_Update

class DB: 
    conn = None
    db = None
    host = None
    def __init__(self, host, mysql_user, mysql_pass, mysql_db):
        self.host = host
        self.mysql_user = mysql_user
        self.mysql_pass = mysql_pass
        self.mysql_db = mysql_db
    def connect(self):
        #self.conn = pymysql.connect(host=self.host, user=self.mysql_user, passwd=self.mysql_pass, db=self.mysql_db, charset="utf8", connect_timeout=600, compress=True,cursorclass = pymysql.cursors.DictCursor)
        self.conn = pymysql.connect(host=self.host, user=self.mysql_user, passwd=self.mysql_pass, db=self.mysql_db, charset="utf8", connect_timeout=600,)

        self.conn.autocommit(True)
    def execute(self, sql):
        try:
            cur = self.conn.cursor()
            cur.execute(sql)
        except (AttributeError, pymysql.OperationalError):
            try:
                cur.close()
                self.conn.close()
            except:
                pass
            time.sleep(1)
            try:
                self.connect()
                print ("reconnect DB")
                cur = self.conn.cursor()
                cur.execute(sql)
            except (AttributeError, pymysql.OperationalError):
                time.sleep(2)
                self.connect()
                print ("reconnect DB")
                cur = self.conn.cursor()
                cur.execute(sql)
    
        return cur
    def Mysql_2_Json(self,data,level=1):
        if level :
            cur = self.execute(data)
            SqlData = cur.fetchall()
            Fields = cur.description
            column_list = []
            rows=[]
            JsonData={}
            for i in Fields:
                column_list.append(i[0])
            total = 0 
            for row in SqlData:    
                result = {}
                total = total + 1                  
                for x in  range(len(column_list)):    
                    result[column_list[x]] = row[x]        
                    #jsondata=json.dumps(result,ensure_ascii=False) 
                rows.append(result)
            JsonData["total"] = total
            JsonData["rows"]= rows
            return json.dumps(JsonData)
        else :
            data = json.loads(data)
            if data["SqlType"] == "Insert":
                for cur in data["rows"]:
                    print(type(cur))
                    a= Get_Sql_Insert(data["SqlTable"],cur)
                    print(a)
            elif data["SqlType"] == "Detele":
                for cur in data["rows"]:
                    print(type(cur))
                    sql= Get_Sql_Detele(data["SqlTable"],cur)
                    print(self.execute(sql))
                    
            elif data["SqlType"] == "Update":
                for cur in data["rows"]:
                    UUID={}
                    UUID["UUID"]=cur["UUID"]
                    cur.pop("UUID")
                    cur.pop("Asset_Number")
                    sql= Get_Sql_Update(data["SqlTable"],cur,UUID)
                    print(self.execute(sql))
                    
            elif data["SqlType"] == "Select":
                print(data)
                for cur in data["rows"]:
                    print(type(cur))
                    a= Get_Sql_Select(data["SqlTable"],cur)
                    print(a)
            else:
                print("error")
                
