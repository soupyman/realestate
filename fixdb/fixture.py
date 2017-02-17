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
import os
import sys
import MySQLdb
sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))) + '/src')

import log
import location
import pinyin

nidx = 0
# iidx = 0

def community_null_lbs():
    global nidx
    lbs = location.geo()
    db = MySQLdb.connect('rds7di028yhg19m2v656o.mysql.rds.aliyuncs.com',"alphago","Alphago0311",'realestate' ,charset="utf8")
    cr = db.cursor(cursorclass = MySQLdb.cursors.DictCursor)

    sql = 'select count(*) as c from community'
    cr.execute(sql)
    cd = cr.fetchone()
    while nidx < cd['c']:
        sql = 'select * from community limit 1 offset %s ' % nidx
        cr.execute(sql)
        community = cr.fetchone()
        if community['latitude'] == None or community['longitude'] == None :
            print '%d community lbs NULL %s' % (nidx, community['name'])
            loc = lbs.coder(community['name'].encode('utf8'))
            if loc == None:
                print 'try + bj'
                loc = lbs.coder('北京'+community['name'].encode('utf8'))
            if loc != None:
                latitude = '%.14f' % loc['lat']
                longitude = '%.14f' % loc['lng']
                sql = 'update community set latitude = "%s" , longitude = "%s" where id=%s'%(latitude,longitude,community['id'])
                print sql
                cr.execute(sql)
                db.commit()
                # break
            else:
                print 'translate location failed on %s'% community['name']
        else:
            print '%d %s has lbs (%s, %s)'%(nidx,community['name'],community['latitude'],community['longitude'])

        nidx += 1

    db.close()
    return True

def community_incorrect_lbs():
    lbs = location.geo()
    db = MySQLdb.connect('rds7di028yhg19m2v656o.mysql.rds.aliyuncs.com',"alphago","Alphago0311",'realestate' ,charset="utf8")
    cr = db.cursor(cursorclass = MySQLdb.cursors.DictCursor)

    sql = 'select * from community where latitude < 38 or latitude > 42 or longitude < 114 or longitude > 118'
    cr.execute(sql)
    invalidcommunity = cr.fetchall()
    for cd in invalidcommunity :
        print '%s community lbs invalid (%s,%s)' % ( cd['name'],cd['latitude'],cd['longitude'])
        loc = lbs.coder('北京' + cd['name'].encode('utf8'))
        if loc != None:
            latitude = '%.14f' % loc['lat']
            longitude = '%.14f' % loc['lng']
            sql = 'update community set latitude = "%s" , longitude = "%s" where id=%s'%(latitude,longitude,cd['id'])
            print sql
            cr.execute(sql)
            db.commit()
            # break
        else:
            print 'translate location failed on %s'% cd['name']


    db.close()
    return True


def district_path():
    translater = pinyin.PinYin()

    # db = MySQLdb.connect('rds7di028yhg19m2v656o.mysql.rds.aliyuncs.com',"alphago","Alphago0311",'realestate' ,charset="utf8")
    db = MySQLdb.connect('127.0.0.1',"root","root",'realestate' ,charset="utf8")
    cr = db.cursor(cursorclass = MySQLdb.cursors.DictCursor)
    sql = 'alter table district add path varchar(64) after name'
    cr.execute(sql)
    db.commit()
    sql = 'select * from district'
    cr.execute(sql)
    districts = cr.fetchall()
    for d in districts:
        sql = 'update district set path = "'+ str(translater.convert(string=d['name'],join=True)) + '" where id = '+ str(d['id'])
        cr.execute(sql)
        print sql
    db.commit()
    db.close()
    return True


if __name__=="__main__":

    while 1:
        try:
            if district_path() :
                break
        except Exception,e:
                print e
                break

    