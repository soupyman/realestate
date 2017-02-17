#!/usr/bin/env python 
# -*- coding: utf-8 -*-
########################################################################
#
# Copyright (c) 2016 tangweimin All Rights Reserved
#
########################################################################

"""
@author: soup
"""

import log
import sys
import MySQLdb
import threading
import traceback
import atexit

from args import *

class db(object):
    '''
    realestate project db class
    '''
    __lock = threading.Lock()
    __log = log.log('db')
    __ins = None

    __house_fields = ['code','community','link','brief','measure','unit_price','total_price','sign_time','floor',
        'direction','decoration','elevator','year','school','subway','bedroom','livingroom']
    __community_fiels = ['name','code' ,'district','bizcycle','subway','school','link','latitude', 'longitude']


    def __dec_lock_func(func):  
        '''
        decoration function for db process.
        lock before db operation.
        '''
        def work(*args,**kwargs):
            ret = False
            db.__lock.acquire() 

            try: 
                ret = func(*args,**kwargs)  
            except Exception,e:
                db.__log.critical(e.message)
                db.__log.critical( 'traceback.print_exc():%s',traceback.print_exc())
                db.__log.critical( 'traceback.format_exc():%s',traceback.format_exc())

            db.__lock.release()  
            return ret  

        return work  

    @__dec_lock_func
    def __new__(cls, *args, **kw):
        if cls.__ins is None:
            cls.__ins = super(db,cls).__new__(cls)
            atexit.register(cls.__del__, cls.__ins)

            # host = "rds7di028yhg19m2v656o.mysql.rds.aliyuncs.com"
            # user = "alphago"
            # pw = "Alphago0311"
            # dbn = 'realestate'
            host = "127.0.0.1"
            user = "root"
            pw = "root"
            dbn = 'realestate'

            cls.__ins._db = MySQLdb.connect(host,user,pw,dbn ,charset="utf8")
            cls.__log.info('connect to db(%s:%s) with UP(%s:%s)',host,dbn,user,pw)

            reset = arg().r

            if True == reset :
                cls.__log.warning('reset db!!!')
                cls.__ins.__resetdb()

        return cls.__ins
        

    def __del__(self):
        '''
        close db connection
        '''
        self._db.close()
        self.__log.info('close db after use!!!')

    def get_community(self):
        '''
        get a default community
        '''
        community = {}

        for f in db.__community_fiels:
            community.update({f : ''})

        return community

    @__dec_lock_func 
    def community_finished(self, name):
        """
        check name location 
        """
    
        cursor = self._db.cursor(cursorclass = MySQLdb.cursors.DictCursor)
        sql = 'select * from community where name = "%s"' % name.strip() 
        db.__log.info(sql);
        cursor.execute(sql)
        values = cursor.fetchone()
        cursor.close()

        if values == None:
            return False
        elif (values['latitude'] == None or values['longitude'] == None):
            return False
        else:
            return True

    @__dec_lock_func 
    def update_community(self, community):
        """
        insert a community whit following fields
        # id 小区名 小区编号 所在区 商圈 地铁 学区 链接 
        """
    
        cursor = self._db.cursor(cursorclass = MySQLdb.cursors.DictCursor)
        sql = 'select * from community where code = "%s"' % community['code'].strip() 
        db.__log.info(sql);
        cursor.execute(sql)

        values = cursor.fetchone()

        if values == None:
            ks = ''
            vs = ''
            for f in db.__community_fiels:
                ks += f + ','
                vs += '\''+community[f].strip()+'\','
            ks = ks.rstrip(',')
            vs = vs.rstrip(',')

            sql = "insert into community (%s) values (%s)" % (ks, vs)

            db.__log.info(sql)

            cursor.execute(sql)

            self._db.commit()
        else:
            sql = 'UPDATE community SET '
            update = False
            for f in db.__community_fiels:
                if community[f].strip() != values[f]:
                    sql += f +'='+ community[f].strip() + ', '
                    update = True
            if update:
                sql = sql.rstrip(', ')
                sql = sql + ' where id='+values['id']
                db.__log.info(sql)

                cursor.execute(sql)

                self._db.commit()
            else:
                db.__log.warning('this community %s is duplicate.', community['name'])

        cursor.close()
        return True

    @__dec_lock_func 
    def get_communitys(self,ctn,offset,lenth):
        '''
        get communitys from offset to offset+ lenth
        '''
        cursor = self._db.cursor(cursorclass = MySQLdb.cursors.DictCursor)
        sql = ''
        if ctn:
            sql = 'select * from community where crawl = (select min(crawl) from community) limit %d offset %d' % (lenth,offset) 
        else:
            sql = 'select * from community limit %d offset %d' % (lenth,offset) 
        db.__log.info(sql)
        cursor.execute(sql)
        self._db.commit()
        communitys =  cursor.fetchall()
        cursor.close()
        return communitys

    @__dec_lock_func 
    def inc_community_crawl(self,code):
        '''
        update community crawl field by inc 1
        '''
        cursor = self._db.cursor()
        sql = 'update community set crawl = crawl+1 where code = \'%s\' ' % code 
        db.__log.info(sql)
        cursor.execute(sql)
        self._db.commit()
        ret =  cursor.rowcount
        cursor.close()
        return ret

    def get_house(self):
        '''
        get a default house 
        #id 编号 小区 连接 简介 面积 单价 总价 成交时间 楼层 朝向 装修 电梯 年代 学区 地铁 几房 几厅 
        '''
        house = {}
        for f in db.__house_fields:
            house.update({f : ''})

        return house
    
    @__dec_lock_func 
    def update_deal_history(self,house):
        """
        insert a deal with following fields
        #id 编号 小区 连接 简介 面积 单价 总价 成交时间 楼层 朝向 装修 电梯 年代 学区 地铁 几房 几厅 
        """
        
        cursor = self._db.cursor(cursorclass = MySQLdb.cursors.DictCursor)
        sql = 'select * from deal where code = "%s"' % house['code'].strip() 
        db.__log.info(sql);
        cursor.execute(sql)

        values = cursor.fetchone()

        if values == None:
            ks = ''
            vs = ''
            for f in db.__house_fields:
                ks += f + ','
                vs += '\''+house[f].strip()+'\','
            ks = ks.rstrip(',')
            vs = vs.rstrip(',')

            sql = "insert into deal (%s) values (%s)" % (ks, vs)
            
            db.__log.info(sql)

            cursor.execute(sql)

            self._db.commit()
        else:
            sql = 'UPDATE deal SET '
            update = False
            for f in db.__house_fields:
                if house[f].strip() != values[f]:
                    sql += f +'="'+ house[f].strip() + '", '
                    update = True
            if update:
                sql = sql.rstrip(', ')
                sql = sql + (' where id=%d ' % values['id'])
                db.__log.info(sql)

                cursor.execute(sql)

                self._db.commit()
            else:
                db.__log.warning('this house %s is duplicate in deal.', house['brief'])

        cursor.close()
        return True

    @__dec_lock_func 
    def get_districts(self,ctn,offset,lenth):
        '''
        get districts from offset to offset+lenth
        '''
        cursor = self._db.cursor(cursorclass = MySQLdb.cursors.DictCursor)
        sql = ''
        if ctn:
            sql = 'select * from district where crawl = (select min(crawl) from district) limit %d offset %d' % (lenth,offset) 
        else:
            sql = 'select * from district limit %d offset %d' % (lenth,offset) 
        db.__log.info(sql)
        cursor.execute(sql)
        self._db.commit()
        districts =  cursor.fetchall()
        cursor.close()
        return districts

    @__dec_lock_func 
    def inc_district_crawl(self,name):
        '''
        update district with crawl field by +1
        '''
        cursor = self._db.cursor()
        sql = 'update district set crawl = crawl+1 where name = \'%s\'' % name 
        db.__log.info(sql)
        cursor.execute(sql)
        self._db.commit()
        ret =  cursor.rowcount
        cursor.close()
        return ret

    def __resetdb(self):
        '''
        warning !!!!
        this function will delete all data in db.
        and reinit the db, only call it in very neccrssary.
        '''
        regions=["东城","西城","朝阳","海淀","丰台","石景山","通州","昌平","大兴",\
            "亦庄开发区","顺义","房山","门头沟","平谷","怀柔","密云","延庆","燕郊"]

        dbc = db.__db.cursor()
        
        # id 区名
        dbc.execute('DROP TABLE IF EXISTS district')
        dbc.execute("create table if not exists district (\
            id int NOT NULL AUTO_INCREMENT primary key,\
            name varchar(64),\
            latitude VARCHAR(32), \
            longitude VARCHAR(32), \
            crawl int(32) default 0)\
            ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8")

        for rg in regions:
            sql = "insert into district (name) value ('%s')" % rg
            dbc.execute(sql)


        # id 小区名 小区编号 所在区 商圈 地铁 学区 链接 
        dbc.execute('DROP TABLE IF EXISTS community')
        dbc.execute("create table if not exists community (\
            id int(32) NOT NULL AUTO_INCREMENT primary key, \
            name varchar(128), \
            code varchar(128), \
            district varchar(128),\
            bizcycle varchar(128),\
            subway varchar(128),\
            school varchar(128),\
            link varchar(256), \
            latitude varchar(32),  \
            longitude varchar(32), \
            crawl int(32) default 0) \
            ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8")
    
        #id 编号 小区 连接 简介 面积 单价 总价 成交时间 楼层 朝向 装修 电梯 年代 学区 地铁 几房 几厅 
        dbc.execute('DROP TABLE IF EXISTS deal')
        dbc.execute("create table if not exists deal (\
            id int(32) NOT NULL AUTO_INCREMENT primary key, \
            code varchar(128),\
            community varchar(128),\
            link varchar(256) ,\
            brief varchar(256), \
            measure varchar(64), \
            unit_price varchar(64), \
            total_price varchar(64),\
            sign_time varchar(64), \
            floor varchar(64), \
            direction varchar(64), \
            decoration varchar(64), \
            elevator varchar(64), \
            year varchar(64), \
            school varchar(64), \
            subway varchar(64), \
            bedroom varchar(64), \
            livingroom varchar(64))\
            ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8")
    
        #id 编号 小区 连接 简介 面积 单价 总价 楼层 朝向 装修 电梯 年代 学区 地铁 几房 几厅 
        dbc.execute('DROP TABLE IF EXISTS sale')
        dbc.execute("create table if not exists sale (\
            id int(32) NOT NULL AUTO_INCREMENT primary key, \
            code varchar(128),\
            community varchar(128),\
            link varchar(256) ,\
            brief varchar(256), \
            measure varchar(64), \
            unit_price varchar(64), \
            total_price varchar(64),\
            floor varchar(64), \
            direction varchar(64), \
            decoration varchar(64), \
            elevator varchar(64), \
            year varchar(64), \
            school varchar(64), \
            subway varchar(64), \
            bedroom varchar(64), \
            livingroom varchar(64))\
            ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8")

        db.__db.commit()
        dbc.close()
        return True


if __name__=="__main__":

    db1 = db(reset = False)
    db2 = db()
    db3 = db()
    print id(db1)
    print id(db2)
    print id(db3)

    # dis = mdb.get_districts(False ,0,10)
    # print dis
    # # com1 = db.get_community()
    # com1 = {'name' : '东润枫景' , 'district' : '朝阳' ,'bizcycle' : '朝阳公园' ,\
    # 'link' : 'no link', 'subway' : 'nosubway' , 'code' : '123','school' : 'waiguoyu'}
    # com2 = {'name' : '西山公馆' , 'district' : '海淀' ,'bizcycle' : '西二旗' ,\
    # 'link' : 'no link', 'subway' : 'nosubway' , 'code' : '321','school' : 'waiguoyu'}
    # mdb.insert_community(com1)
    # mdb.insert_community(com2)

    # coms = mdb.get_communitys(True , 0,5)
    # print coms


    # deal = {'code' : '12345456' , 'link' : 'http://aeqer/fadfe' ,'name' : '123' ,\
    # 'link2' : 'no link', 'baseinfo' : 'aoe' , 'community' : '123'}
    #db.insert_history(deal)



    