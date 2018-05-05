#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
@author:piepis
@file:ConnectMySQL.py
@time:2017-12-199:32
@desc: 连接查询数据库
'''
try : #python3 的时候用 pymysql
    import pymysql as MySQLdb
except  ImportError :#python2 的时候用 mysqldb
    import  MySQLdb
from OperationUtil.log.log import Log
'''
sql:Mysql语句 connect :连接信息 reCount：运单数据 result 运单结果
update_delect_sql :更新,删除sql insert_sql:插入数据库语句
excute_select_one_record：查询一条 excute_select_many_record ：查询所有
'''
class DBUtil(object):
    '''操作数据库'''
    def __init__(self,host,port,user,passwd,dbname,charset):
        self.logger = Log()
        try:
            self.connect = MySQLdb.connect(
                host = host,
                port = port,
                user = user,
                passwd = passwd,
                db = dbname,
                charset = charset
            )
        except Exception as e:
            self.logger.error('Database Initialization Connection Failed 1 : {0}'.format(e))
            raise

    def update_delect_sql(self,sql):
        '''执行更新，删除sql语句'''
        self.logger.info('sql:{0}'.format(sql))
        try:
            cur = self.connect.cursor()
            cur.execute(sql)
            cur.close()
            self.connect.commit()
        except Exception as e:
            self.logger.info('Execute sql failed ! : {0}'.format(e))
            self.connect.rollback()
            self.connect.close()
            raise
    def insert_sql(self,sql,data):
        '''执行 插入一条 sql语句'''
        self.logger.info('sql:{0}'.format(sql))
        try:
            cur = self.connect.cursor()
            cur.execute(sql,data)
            cur.close()
            self.connect.commit()
        except Exception as e:
            self.logger.info('Execute sql failed ! : {0}'.format(e))
            self.connect.rollback()
            self.connect.close()
            raise
    def insert_many_sql(self,sql,data):
        '''执行 插入多条 sql语句'''
        self.logger.info('sql:{0}'.format(sql))
        try:
            cur = self.connect.cursor()
            cur.executemany(sql,data)
            cur.close()
            self.connect.commit()
        except Exception as e:
            self.logger.info('Execute sql failed ! : {0}'.format(e))
            self.connect.rollback()
            self.connect.close()
            raise
    def excute_select_one_record(self,query):
        '''执行sql语句：select,返回结果只包含一条数据'''
        self.logger.info('query:{0}'.format(query))
        try:
            cur = self.connect.cursor()
            cur.execute(query)
            return cur.fetchone()
        except Exception as e:
            self.logger.info('Execute sql failed ! : {0}'.format(e))
            self.connect.close()
            raise

    def excute_select_many_record(self,query):
        '''执行sql语句：select，返回结果包含多条数据'''
        self.logger.info('query:{0}'.format(query))
        try:
            cur = self.connect.cursor()
            cur.execute(query)
            return cur.fetchall()
        except Exception as e:
            self.logger.info('Execute sql failed ! : {0}'.format(e))
            self.connect.close()
            raise
    def ConnectClose(self):
        self.connect.close()