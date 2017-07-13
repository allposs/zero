#!/usr/bin/env python
# -*- coding:utf-8 -*-

from flask import Flask,request,render_template,redirect,session
from config.config import db_config,page_config
from dbutil.dbutil import DB
import json
from tools.tools import uuid1_hex

app = Flask(__name__)
app.secret_key = '\xca\x0c\x86\x04\x98@\x02b\x1b7\x8c\x88]\x1b\xd7"+\xe6px@\xc3#\\'

db = DB(host=db_config['host'], mysql_user=db_config['user'], mysql_pass=db_config['passwd'], \
                mysql_db=db_config['db'])

page_config.setdefault('favicon','/static/images/favicon.ico')
page_config.setdefault('title','cmdb')
page_config.setdefault('brand_name','cmdb')

   
@app.route('/login',methods=['GET','POST'])
def login():
    if 'username' in session:
        return redirect('/')
    if request.method == "POST":
        name = request.form.get('username')
        passwd = request.form.get('password')
        print (name)
        print (passwd)
        obj = {"result":1}
        if name and passwd:
            sql = 'select * from Users_Info where Users="%s" and Passwd="%s"'%(name,passwd)
            print (sql)
            cur = db.execute(sql)
            if cur.fetchone():
                obj["result"] = 0
                session['username'] = name
        return json.dumps(obj)            
    else:
        return render_template('login.html')
@app.route('/logout')
def logout():
    session.pop('username')
    return redirect('/login')

@app.route('/page/<template>')
def render(template):
    if 'username' in session:
        return render_template('page/'+template+'.html',data=page_config,username=session['username'])
    else:
        return redirect('/login')
 
@app.route('/api/<template>',methods=['GET','POST'])
def api(template):
        if request.method == "POST":
            if template == "listapi" :
                print(request.form)
                
                MysqlTables = 'servers_info'
                sql = "select * from %s;" %(MysqlTables)
                SqlData = db.Mysql_2_Json(sql,1)  
                return SqlData 

            elif template == "delapi":
                DelData = request.form.getlist("UUID[]")
                print(DelData)
                rows = []
                JsonData={}
                total = 0
                for x in DelData:
                    Dict = {}
                    Dict["UUID"] = x
                    sql = 'DELETE FROM servers_info WHERE UUID = "%s"' %(x)
                    rows.append(Dict)
                    total += 1
                JsonData["total"] = total
                JsonData["SqlType"]="Detele"
                JsonData["SqlTable"]="servers_info"
                JsonData["rows"]=rows
                data = json.dumps(JsonData)
                db.Mysql_2_Json(data,0)
                data = "已删除"
                return data
            elif template == "updateapi":
                rows=[]
                JsonData={}
                total = 1
                Dict = {}
                for k in request.form :
                    Dict[k] = request.form[k]
                rows.append(Dict)
                JsonData["total"] = total
                JsonData["SqlType"]="Update"
                JsonData["SqlTable"]="servers_info"
                JsonData["rows"]=rows
                data = json.dumps(JsonData)
                db.Mysql_2_Json(data,0)
                print(data)
                data = "已添加"
                return data   
            elif template == "addapi": 
                rows=[]
                JsonData={}
                total = 1
                Dict = {}
                Dict["UUID"] = uuid1_hex()
                for k in request.form :
                    Dict[k] = request.form[k]
                rows.append(Dict)
                JsonData["total"] = total
                JsonData["SqlType"]="Insert"
                JsonData["SqlTable"]="servers_info"
                JsonData["rows"]=rows
                data = json.dumps(JsonData)
                db.Mysql_2_Json(data,0)
                print(data)
                data = "已添加"
                return data         
            else:
                print("error")

@app.route('/')
def index():
    return redirect('/page/view')


if __name__ == '__main__':
    app.run(debug=True,port=8080,host='127.0.0.1')