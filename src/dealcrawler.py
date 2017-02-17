#!/usr/bin/env python
# -*- coding: utf-8 -*-
########################################################################
# 
# Copyright (c) 2016
# 
########################################################################

"""
This DealCrawlerT module crawl and parse html .

File: DealCrawlerT.py
Author: tangweimin
Date: 2016/12/12
"""

import re
import log
import db
import bs4
import args
import crawler
import traceback

class DealCrawlerT(crawler.CrawlerT):
    """
    DealCrawlerT Class .
    """
    _log = log.log('deal')

    def __init__(self, tp , urlptn, data, timeout = 10, interval = 10):
        """
        init Crawler instance
        args:
        type: list / info
        """
        super(DealCrawlerT, self).__init__(urlptn,data,timeout,interval)
        self._type = tp
        self._arg = args.arg()

    def work(self):
        """
        DealCrawlerT Class run method.
        爬取页面链接中的信息
        """

        if(self._type == 'list'):
            self._crawl_list()
        else :
            self._crawl_info()

    def _crawl_info(self):
        '''
        '''
        mdb = db.db()
        community = self._data[1]
        
        cj_list= self._soup.findAll('div',{'class':'info'})
        for cj in cj_list:

            info_dict = mdb.get_house()
            info_dict.update({'community': community})
            title = cj.find("div", {"class": "title"})  # html
            if title :
                brief = title.get_text().strip()
                info_dict.update({'brief': brief})

                bedroom = re.findall(ur'[\d|\.|\-]+(?=\u5ba4)', brief)
                livingroom =re.findall(ur'[\d|\.|\-]+(?=\u5385)',brief)
                measure =re.findall(ur"[\d|\.|\-]+(?=\u5e73\u7c73)",brief)

                info_dict.update({'bedroom': bedroom[0]})
                info_dict.update({'livingroom': livingroom[0]})
                info_dict.update({'measure': measure[0]})

                if title.a:
                    url = title.a.get('href');
                    if url :
                        code = re.findall(r'(\w*[0-9]+)\w*', url)
                        info_dict.update({'link': url})
                        info_dict.update({'code': code[0]})
                else:
                    DealCrawlerT._log.warning( 'can not find the code for this house !')
                    continue

            totalPrice = cj.find("div", {"class": "totalPrice"})  # html
            if totalPrice :
                totalPrice1 = totalPrice.find("span", {"class": "number"})  # html
                if totalPrice1 :
                    info_dict.update({'total_price': totalPrice1.get_text().strip()})

            unitPrice = cj.find("div", {"class": "unitPrice"})  # html
            if unitPrice:
                unitPrice1 = unitPrice.find("span", {"class": "number"})  # html
                if unitPrice1 :
                    info_dict.update({'unit_price': unitPrice1.get_text().strip()})

            houseinfo = cj.find("div", {"class": "houseInfo"})  # html
            # DealCrawlerT._log.info('hourse info :%s', houseinfo)
            if houseinfo :
                info = re.findall(r'[^|]+', houseinfo.get_text().strip())
                for hi in info :
                    if re.search(ur'电梯',hi) :
                        info_dict.update({'elevator': hi})
                    elif re.search(ur'东|南|西|北', hi) :
                        info_dict.update({'direction': hi})
                    elif re.search(ur'装', hi) :
                        info_dict.update({'decoration': hi})
                    else:
                        DealCrawlerT._log.error('unknow hourse info :%s', hi)

            positionInfo = cj.find("div", {"class": "positionInfo"})  # html
            if positionInfo :
                info = re.findall(r'[^)]+', positionInfo.get_text().strip())
                if len(info) == 2:
                    info[0] += ')'
                    info_dict.update({'floor': info[0].strip()})
                    info_dict.update({'year': info[1].strip()})
                else:
                    DealCrawlerT._log.error('parse error on :%s', positionInfo.get_text().strip())

            dealHouseInfo = cj.find("div", {"class": "dealHouseInfo"})  # html
            if dealHouseInfo :
                info_dict.update({'subway': dealHouseInfo.get_text().strip()})

            dealDate = cj.find("div", {"class": "dealDate"})  # html
            if dealDate :
                sign_time = dealDate.get_text().strip()
                if sign_time < self._arg.a:
                    self._state = 'finished'
                    DealCrawlerT._log.info( 'deal crawler finished for date deadline(%s, %s)!'%(sign_time, self._arg.a))
                    break
                info_dict.update({'sign_time': sign_time})

            info = 'code:%s , community:%s , link:%s , brief:%s , measure:%s ,unit_price:%s,total_price:%s,\
                sign_time:%s, floor:%s , direction:%s,decoration:%s,elevator:%s,year:%s,school:%s,subway:%s,\
                bedroom:%s,livingroom:%s' \
                % (info_dict['code'].strip(),info_dict['community'],info_dict['link'].strip(),info_dict['brief'].strip()\
                ,info_dict['measure'].strip(),info_dict['unit_price'].strip(),info_dict['total_price'].strip()\
                ,info_dict['sign_time'].strip(),info_dict['floor'].strip(),info_dict['direction'].strip()\
                ,info_dict['decoration'].strip(),info_dict['elevator'].strip(),info_dict['year'].strip()\
                ,info_dict['school'].strip(),info_dict['subway'].strip(),info_dict['bedroom']\
                ,info_dict['livingroom'])
            DealCrawlerT._log.info( info)

            mdb.update_deal_history(info_dict)

    def _crawl_list(self):
        """
        爬取小区的所有成交信息
        """

        content = self._soup.find('div',{'class':'page-box house-lst-page-box'})
        if content == None:
            DealCrawlerT._log.error('No deal found on: %s' , self._urlptn%self._data)
            return

        total_pages=0
        d="d="+content.get('page-data')
        exec(d)
        total_pages=d['totalPage']

        DealCrawlerT._log.info('in %s find %d pages of deal history. ' ,self._data, total_pages)

        threads=[]

        for i in range(total_pages):
            url_page = "http://bj.lianjia.com/chengjiao/pg%dc%s/" 
            url_data = (i+1 , self._data)

            crawler = DealCrawlerT('info',url_page,url_data)
            threads.append(crawler)

            if(True == self._arg.c):
                crawler.start()
                crawler.join()
                if crawler._state == 'finished':
                    break

        if(True != self._arg.c):
            for t in threads:
                t.start()
            for t in threads:
                t.join()


if __name__ == '__main__':

    db.db.open(False)

    urlptn = "http://bj.lianjia.com/chengjiao/c%s/" 
    data = '1111027380322'

    dd = DealCrawlerT('list', urlptn, data)
    dd.start()
    dd.join()

    db.db.close()


