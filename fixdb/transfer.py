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

sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))) + '/src')

import log
import sys
import MySQLdb
import location

cidx = 12479
didx = 76910

def transfer_community():
    global cidx
    lgs = location.geo()
    ldb = MySQLdb.connect('rds7di028yhg19m2v656o.mysql.rds.aliyuncs.com',"alphago","Alphago0311",'realestate' ,charset="utf8")
    tdb = MySQLdb.connect('alpha-go.tech',"root","root",'lianjia' ,charset="utf8")
    lcr = ldb.cursor(cursorclass = MySQLdb.cursors.DictCursor)
    tcr = tdb.cursor(cursorclass = MySQLdb.cursors.DictCursor)
    tsql = 'select count(*) as c from community'
    tcr.execute(tsql)
    cc = tcr.fetchone()
    while cidx < cc['c']:
        tsql = 'select * from community limit 1 offset %s ' % cidx
        tcr.execute(tsql)
        community = tcr.fetchone()
        lsql = 'select * from community where code="'+community['code']+'"'
        lcr.execute(lsql)
        finish = lcr.fetchone()
        if finish == None:
            print '%d community hit one update %s' % (cidx, community['name'])
            loc = lgs.coder(community['name'].encode('utf8'))
            if loc != None:
                community['latitude'] = '%.14f' % loc['lat']
                community['longitude'] = '%.14f' % loc['lng']
                lsql = 'insert into community \
                    (name,code,district,bizcycle,subway,school,link,latitude,longitude) \
                    values("'+community['name']+'","'+community['code']+'","'+community['district']+'","' \
                    +community['bizcycle']+'","'+community['subway']+'","'+community['school']+'","'+community['link'] \
                    +'","'+community['latitude']+'","'+community['longitude']+'")'
            else:
                lsql = 'insert into community \
                    (name,code,district,bizcycle,subway,school,link) \
                    values("'+community['name']+'","'+community['code']+'","'+community['district']+'","' \
                    +community['bizcycle']+'","'+community['subway']+'","'+community['school']+'","'+community['link']+'")'

            print lsql
            # break
            lcr.execute(lsql)
            ldb.commit()
        else:
            print '%d community hit one === %s' % (cidx, community['name'])
        cidx += 1

    ldb.close()
    tdb.close()
    return True

def transfer_deal():
    global didx
    lgs = location.geo()
    ldb = MySQLdb.connect('rds7di028yhg19m2v656o.mysql.rds.aliyuncs.com',"alphago","Alphago0311",'realestate' ,charset="utf8")
    tdb = MySQLdb.connect('alpha-go.tech',"root","root",'lianjia' ,charset="utf8")
    lcr = ldb.cursor(cursorclass = MySQLdb.cursors.DictCursor)
    tcr = tdb.cursor(cursorclass = MySQLdb.cursors.DictCursor)
    tsql = 'select count(*) as c from deal'
    tcr.execute(tsql)
    cc = tcr.fetchone()
    while didx < cc['c']:
        tsql = 'select * from deal limit 1 offset %s ' % didx
        tcr.execute(tsql)
        deal = tcr.fetchone()
        lsql = 'select * from deal where code="'+deal['code']+'"'
        lcr.execute(lsql)
        finish = lcr.fetchone()
        if finish == None:
            print '%d deal hit one update %s' % (didx, deal['code'])

            lsql = 'insert into deal \
                (code,community,link,brief,measure,unit_price,total_price,sign_time,floor,direction,\
                decoration,elevator,year,school,subway,bedroom,livingroom) \
                values("'+deal['code']+'","'+deal['community']+'","'+deal['link']+'","' \
                +deal['brief']+'","'+deal['measure']+'","'+deal['unit_price']+'","'+deal['total_price'] \
                +'","'+deal['sign_time']+'","'+deal['floor']+'","'+deal['direction']+'","'+deal['decoration']\
                +'","'+deal['elevator']+'","'+deal['year']+'","'+deal['school']+'","'+deal['subway']\
                +'","'+deal['bedroom']+'","'+deal['livingroom']+'")'

            print lsql
            # break
            lcr.execute(lsql)
            ldb.commit()
        else:
            print '%d deal hit one === %s' % (didx, deal['code'])
        didx += 1

    ldb.close()
    tdb.close()
    return True


if __name__=="__main__":

    while 1:
        try:
            if transfer_community() and transfer_deal():
                break
        except Exception,e:
                pass

    