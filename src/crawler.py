#!/usr/bin/env python
# -*- coding: utf-8 -*-
########################################################################
# 
# Copyright (c) 2016
# 
########################################################################

"""
This crawlerT module crawl and parse html .

File: crawler.py
Author: tangweimin
Date: 2016/12/12
"""

import time
import datetime
import log
import json
import random
import urllib
import urllib2  
import threading
import cookielib
import bs4
import sys
reload(sys)
sys.setdefaultencoding("utf-8")

class CrawlerT(threading.Thread):
    """
    CrawlerT Class .
    """
    __query_max__ = 100000
    __query_cnt__ = 0
    __query_date__ = 0
    __log = log.log('crawler')


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

    def __init__(self, urlptn, data, timeout = 10, inverval = 10):
        """
        init Crawler instance
        """
        super(CrawlerT, self).__init__()
        self._timeout = timeout
        self._interval = inverval
        self._urlptn = urlptn
        self._data = data
        self._hdr = self._get_hdr()
        cj = cookielib.CookieJar()
        pcr = urllib2.HTTPCookieProcessor(cj)
        self._opener = urllib2.build_opener(pcr)
        self._state = 'ok'
        self._soup = None

    def _request(self):
        CrawlerT.check()

        url = self._urlptn % self._data

        # rits = random.randint(1,self._interval)
        rits = random.randint(1,self._interval) / 10.0
        CrawlerT.__log.info('sleep %f s and crawle url %s .' % (rits, url))

        time.sleep(rits)

        req = urllib2.Request(url,headers=self._hdr)
        resp = self._opener.open(req,timeout=self._timeout)
        source_code = resp.read()
        plain_text=unicode(source_code)#,errors='ignore')
        self._soup = bs4.BeautifulSoup(plain_text,'lxml')

    def _human_mock(self):
        mock_url = 'http://captcha.lianjia.com/human/'
        ret = False
        self._state = 'mocking'

        for i in range(1000): 
            
            time.sleep(0.1)

            human_box = self._soup.find('form',{'class':'human'})
            if human_box == None:
                CrawlerT.__log.error('can not find human_box!!!!')
                return;

            data = {}
            test = random.randint(0,3)

            greq = urllib2.Request(mock_url,headers=self._hdr)
            grsp = self._opener.open(greq)
            gret = grsp.read()
            #CrawlerT.__log.debug('mock_url return: %s',gret)

            data['uuid'] = gret[-15:-2]
            data['_csrf'] = human_box.find('input',{'name':'_csrf'})['value']
            data['bitvalue'] = 1<<test
        
            post_data = urllib.urlencode(data)
            CrawlerT.__log.debug('try mock %d with: %s'% (i , post_data))

            preq = urllib2.Request(mock_url, data = post_data,headers=self._hdr)
            prsp = self._opener.open(preq)
            pret = prsp.read()
            CrawlerT.__log.debug('mock result: %s',pret)

            rst = json.loads(pret)

            if rst['error'] == False:
                CrawlerT.__log.debug('mock success! after %d times' ,(100 - i))
                self._state = 'ok'
                ret = True
                break

        return ret

    def _get_hdr(self):

        _hds=[{'User-Agent':'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6'},\
            {'User-Agent':'Mozilla/5.0 (Windows NT 6.2) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.12 Safari/535.11'},\
            {'User-Agent':'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.2; Trident/6.0)'},\
            {'User-Agent':'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:34.0) Gecko/20100101 Firefox/34.0'},\
            {'User-Agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/44.0.2403.89 Chrome/44.0.2403.89 Safari/537.36'},\
            {'User-Agent':'Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_8; en-us) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50'},\
            {'User-Agent':'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-us) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50'},\
            {'User-Agent':'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0'},\
            {'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.6; rv:2.0.1) Gecko/20100101 Firefox/4.0.1'},\
            {'User-Agent':'Mozilla/5.0 (Windows NT 6.1; rv:2.0.1) Gecko/20100101 Firefox/4.0.1'},\
            {'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_0) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.56 Safari/535.11'},\
            {'User-Agent':'Opera/9.80 (Macintosh; Intel Mac OS X 10.6.8; U; en) Presto/2.8.131 Version/11.11'},\
            {'User-Agent':'Opera/9.80 (Windows NT 6.1; U; en) Presto/2.8.131 Version/11.11'}]
        hdr = _hds[random.randint(0,len(_hds)-1)]
        return hdr

    def state(self):
        return self._state

    def fail(self , forwhat):
        #save to fail db
        # pass
        CrawlerT.__log.error('crawler %s failed!!!' % forwhat)

    def run(self):
        """
        Crawler Class run method.
        """
        try: 

            self._request()
            if self._soup.find('form',{'class':'human'}) :
                self._human_mock()
                self._request()

            self.work()

        except Exception,e:
            url = self._urlptn % self._data
            CrawlerT.__log.critical(e.message)
            self.fail(url)
            self._state = 'ko'


        


