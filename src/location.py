#!/usr/bin/env python
# -*- coding: utf-8 -*-
########################################################################
#
# Copyright (c) 2016 tangweimin All Rights Reserved
#
########################################################################

"""
The location module is for user location geo coder.

File: location.py
Author: tangweimin
Date: 2016/12/12:

help doc url:
http://lbsyun.baidu.com/index.php?title=webapi/guide/webservice-geocoding

sql select nearest:
select * from community order by abs(latitude-40.03877292511365)+abs(longitude-116.32054336902259) asc limit 10;

select latitude,longitude from community where name='东润枫景二期' 

"""
import log
import time
import urllib2  
import datetime

class geo(object):
    """
    """
    __query_max__ = 5000 # 6000
    __query_cnt__ = 0
    __query_date__ = 0
    __log = log.log('geo')

    def __init__(self):
        self._base_url = 'http://api.map.baidu.com/geocoder/v2/'
        self._access_key = 'NCK8DsjwonMstFpUrxwI02SQtUL2BB2C'
        self._output_type = 'json'

    def coder(self, addr):
        # geo.check()
        ret  = None

        url = self._base_url + '?output=' + self._output_type +  \
            '&address=' + addr + '&city=' + '北京' + '&ak='  + self._access_key

        try:
            resp = eval(urllib2.urlopen(url).read()) 
        except Exception,e:
            return None

        if resp['status'] == 0:
            ret = resp['result']['location']

        geo.__log.info('%s is translate to %s' % (addr , ret))
        return ret

    @classmethod
    def check(cls):
        while(1):
            now = datetime.datetime.now()
            today = now.strftime('%Y-%m-%d')

            if cls.__query_date__ != today:
                cls.__query_date__ = today
                cls.__query_cnt__ = 0

            cls.__query_cnt__ += 1

            if(cls.__query_cnt__ > cls.__query_max__):
                cls.__log.warning('%s query %d times is too much! so go to sleep 60s.' \
                    % (cls.__query_date__ ,cls.__query_cnt__))
                time.sleep(60)
            else:
                break



    @classmethod
    def dump(cls):
        print cls.__query_cnt__
        print cls.__query_date__

if __name__ == '__main__':

    print datetime.datetime.now().strftime('%H')

    a = geo()

    a.coder('百度大厦')
    a.coder('温泉教师楼')
    a.coder('北新桥头条')
    a.coder('上地佳园')
    a.coder('龙湖唐宁one')

    geo.dump()


