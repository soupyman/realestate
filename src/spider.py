#!/usr/bin/env python
# -*- coding: utf-8 -*-
########################################################################
#
# Copyright (c) 2016
#
########################################################################

"""
The spider module crawl specific URL pattern .

File: spider.py
Author: tangweimin
Date: 2016/12/12

"""

import os
import sys
import logging
import datetime
import time
import db
import log
import args
import master
import dealcrawler
import communitycrawler

class spider():
    """spider main class"""   

    __log = log.log('spider')

    def crawl_community(self):
        '''
        crawl communitys which is crawl least
        '''
        continue_flag = args.arg().c
        mdb = db.db()
        index = 0
        districts = mdb.get_districts(continue_flag , index,10)

        while len(districts) > 0:
            for d in districts:
                urlptn = "http://bj.lianjia.com/xiaoqu/%s/" 
                name = d['path']

                cc = communitycrawler.CommunityCrawlerT('list', urlptn, name)
                cc.start()
                cc.join()

                if cc.state() == 'ok':
                    mdb.inc_district_crawl(name)
                else:
                    self.__log.warning('skip community inc crawl for state(%s) not ok.', cc.state())

            index += 10
            districts = mdb.get_districts(continue_flag , index,10)

    def crawl_deal(self):
        '''
        crawl house deals which is crawl least
        '''
        continue_flag = args.arg().c
        mdb = db.db()
        index = 0
        communitys = mdb.get_communitys(continue_flag ,index,10)

        while communitys and len(communitys) > 0:
            for c in communitys:
                urlptn = "http://bj.lianjia.com/chengjiao/c%s/" 
                code = c['code']

                dd = dealcrawler.DealCrawlerT('list', urlptn, code)
                dd.start()
                dd.join()

                if dd.state() == 'ok':
                    mdb.inc_community_crawl(code)
                else:
                    self.__log.warning('skip deal inc crawl for state(%s) not ok.', dd.state())

            index += 10     
            communitys = mdb.get_communitys(continue_flag ,index,10)

        print 'finished crawl deal with index %d' % index


    def wait_untill(self,hour):
        """
        spider function to untill hour clock.
        for run function every day.
        """
        self.__log.info('crawler waite untill %s.' % hour)

        now = datetime.datetime.now().strftime('%H')
        while now != hour:
            time.sleep(600); # sleep 10 minutes
            now = datetime.datetime.now().strftime('%H')


    def __init__(self):
        """
        spider main entrance

        """
        skip = args.arg().s

        while 1 :
            if False == skip:
                self.crawl_community()

            self.crawl_deal()
            self.__log.info('crawler finished once at %s.' % datetime.datetime.now().strftime('%m-%d %H:%M'))

            self.wait_untill('2')
            # break

if __name__ == '__main__':

    mgr = master.MasterP()

    if mgr.is_worker():
        spider()

