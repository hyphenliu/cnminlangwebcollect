# -*- coding:utf-8 -*-
'''
Created on 2014年1月10日

@author: Hyphen.Liu
'''
import sqlite3
import time

import globalvar.utilGlobalVar as ugv

TABLEITEMS = 'id INTEGER PRIMARY KEY AUTOINCREMENT, domain VARCHAR(50) UNIQUE, sitename VARCHAR(50), indexpage VARCHAR(100), groupname VARCHAR(50), groupattrib VARCHAR(10), committime VARCHAR(15), icp VARCHAR(30), ip VARCHAR(20), server VARCHAR(50), worldrank VARCHAR(15), chinarank VARCHAR(15),coding VARCHAR(10), rate FLOAT, link VARCHAR(150), insertdate DATE'
ITEMSNAME = ['id','domain','sitename','indexpage','groupname','groupattrib',
             'committime','icp','ip','server','worldrank','chinarank','coding',
             'rate','link','insertdate']
TABLES = ['bo','ug','mn','kk','ky','ko','ii','za','th']
CREATETABLES = 'CREATE TABLE IF NOT EXISTS %s (%s)'

class DBstorage():
    '''
    :数据库操作，增、改、删
    '''
    def __init__(self):
        '''
        :数据库操作初始化，链接或创建数据库（数据库未存在则创建）
        '''
        self.db = sqlite3.connect(ugv.DATAPATH + ugv.DBNAME)#链接数据库（数据库不存在则创建数据库）
        self.db.text_factory = str                          #设置保存utf-8字符集
        self.cu = self.db.cursor()                          #游标
        self.datetime = time.strftime('%Y%m%d')
        self.init()
        
    def init(self):
        '''
        :初始化数据表确定所有语言数据表格已经存在
        '''
        for t in TABLES:
            self.db.execute(CREATETABLES%(t,TABLEITEMS))
        self.db.commit()
           
    def insert_data(self,lang,datalist): 
        '''
        :插入单条数据的语句
        :param lang: 需要插入的表名
        :param datalist: 被插入的数据
        '''
        datatuple = tuple(datalist)
        langdate = lang+self.datetime                       #以时间和语言命名的另一个数据表格
        self.db.execute(CREATETABLES%(langdate,TABLEITEMS)) #创建该数据表
        insert_sql1 = 'INSERT INTO %s VALUES (null,?,?,?,?,?,?,?,?,?,?,?,?,?,?,date())'%lang
        insert_sql2 = 'INSERT INTO %s VALUES (null,?,?,?,?,?,?,?,?,?,?,?,?,?,?,date())'%langdate
        try:
            self.cu.execute(insert_sql1,datatuple)          #插入总表
        except Exception, e:                                #插入值的时候出现重复域名的错误
            pass                                            #数据已经存在
        finally:
            try:
                self.cu.execute(insert_sql2,datatuple)      #插入分表
            except Exception,e:
                pass                                        #数据已经存在
        self.db.commit()
        self.close()
        
    def update_data(self,lang,datatuple,index):
        '''
        :执行单条更新操作
        :param lang: 需要更新的表名
        :param indextuple: 需要更新的数据项
        :param datatuple: 需要更新的数据
        '''
        update_sql = 'UPDATE %s SET %s = ? WHERE domain = ?'%(lang,ITEMSNAME[index+1])
        self.cu.execute(update_sql,datatuple)
        self.db.commit()
        self.close()
        
    def update_data_many(self,lang,datatuples):
        '''
        :执行多条更新操作
        :param lang: 需要更新的表名
        :param datatuple: 数据源组
        '''
        for dt in datatuples:
            if dt == '':                                    #列表第一个数为空，但占位
                continue
            datatuple = dt[0]
            index = dt[1]
            update_sql = 'UPDATE %s SET %s = ? WHERE domain = ?'%(lang,ITEMSNAME[index+1])
            self.cu.execute(update_sql,datatuple)
        self.db.commit()
        self.close()
        
    def delete_data(self,lang,domain):
        '''
        :执行单条删除操作
        :param lang: 需要删除数据的表名
        :param domain: 删除数据的域名
        '''
        delete_sql = 'DELETE FROM %s WHERE domain=?'%lang
        self.cu.execute(delete_sql,(domain,))               #只接受tuple，故此处转为tuple
        self.db.commit()
        self.close()
        
    def fetchall_data_total(self,lang,timetuple):
        '''
        :查询一定时间内入库的数据
        :param lang: 需要查询的表名
        :param timetuple: 需要查询的时间段，以tuple保存，格式2001-01-01
        '''
        fetch_sql = 'SELECT * FROM %s WHERE insertdate BETWEEN ? AND  ?'%lang
        self.cu.execute(fetch_sql,timetuple)
        rst = self.cu.fetchall()
        self.close()
        return rst
    
    def fetchall_data_single(self,lang):
        '''
        :查询表格里的所有内容
        :param lang: 需要查询的表格名称
        '''
        fetch_sql = 'SELECT * FROM %s'%lang
        try:
            self.cu.execute(fetch_sql)
        except Exception,e:
            return None
        rst = self.cu.fetchall()
        self.close()
        return rst
    
    def close(self):
        '''
        :关闭数据库
        '''
        self.cu.close()
        self.db.close()
        self.db = None
    