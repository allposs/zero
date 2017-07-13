#!/usr/bin/env python
# _*_coding:utf-8_*_
import uuid

def dict_2_str_and(dictin):
    """
                        将字典变成，key='value' and key='value'的形式
    """
    tmplist = []
    for k, v in dictin.items():
        tmp = "%s='%s'" % (str(k),str(v))
        tmplist.append(' ' + tmp + ' ')
    return ' and '.join(tmplist)
 
def dict_2_str(dictin):
    """"
                         将字典变成，key='value',key='value' 的形式
    """
    tmplist = []
    for k, v in dictin.items():
        tmp = "%s='%s'" % (str(k), str(v))
        tmplist.append(' ' + tmp + ' ')
    return ','.join(tmplist)


def Get_Sql_Insert(table,SqlDict):
    """
                          生成insert的sql语句
    @table，插入记录的表名
    @dict,插入的数据，字典
    """     
    print(SqlDict)
    sql = 'insert into %s set ' % table
    sql += dict_2_str(SqlDict)
    return sql


def Get_Sql_Select(table, keys, conditions, isdistinct=0):
    """
                        生成select的sql语句
    @table，查询记录的表名
    @key，需要查询的字段
    @conditions,插入的数据，字典
    @isdistinct,查询的数据是否不重复
    """
    if isdistinct:
        sql = 'select distinct %s ' % ",".join(keys)
    else:
        sql = 'select  %s ' % ",".join(keys)
        sql += ' from %s ' % table
    if conditions:
        sql += ' where %s ' % dict_2_str_and(conditions)
    return sql


def Get_Sql_Update(table,value,conditions):
    """
                        生成update的sql语句
    @table，查询记录的表名
    @value，dict,需要更新的字段
    @conditions,插入的数据，字典
    """
    sql = 'update %s set ' % table
    sql += dict_2_str(value)
    if conditions:
        sql += ' where %s ' % dict_2_str_and(conditions)
    return sql


def Get_Sql_Detele(table,conditions):
    """
                生成detele的sql语句
    @table，查询记录的表名
    @conditions,插入的数据，字典
    """
    sql = 'delete from  %s  ' % table
    if conditions:
        sql += ' where %s ' % dict_2_str_and(conditions)
    return sql





def uuid1_hex():
    """
    return uuid1 hex string

    eg: 23f87b528d0f11e696a7f45c89a84eed
    """
    return uuid.uuid1().hex

def uuid4_hex():
    s_uuid=str(uuid.uuid4())
    l_uuid=s_uuid.split('-')
    s_uuid=''.join(l_uuid)
    return s_uuid
