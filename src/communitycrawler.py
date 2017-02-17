#!/usr/bin/env python
# -*- coding: utf-8 -*-
########################################################################
# 
# Copyright (c) 2016
# 
########################################################################

"""
This community crawlerT module crawl  and parse html .

File: CommunityCrawlerT.py
Author: tangweimin
Date: 2016/12/12
"""

import re
import log
import db
import bs4
import location
import crawler


class CommunityCrawlerT(crawler.CrawlerT):
    """
    CommunityCrawlerT Class .
    """
    _log = log.log('community')

    def __init__(self, tp , urlptn, data, timeout = 10, interval = 10):
        """
        init Crawler instance
        args:
        type: list / info
        """
        super(CommunityCrawlerT, self).__init__(urlptn,data,timeout,interval)
        self._type = tp
        self._geo = location.geo()


    def work(self):
        """
        CommunityCrawlerT Class run method.
        爬取页面链接中的信息
        """

        if(self._type == 'list'):
            self._crawl_list()
        else :
            self._crawl_info()

    def _crawl_info(self):
        '''
        '''
        community_list=self._soup.findAll('div',{'class':'info'})
        url = self._urlptn % self._data
        mdb = db.db()

        for xq in community_list:

            info_dict=mdb.get_community()

            title = xq.find("div", {"class": "title"})  # html
            name = title.get_text().strip()
            if False == mdb.community_finished(name) : 
                info_dict['name'] = name

                loc = self._geo.coder(name)
                info_dict['latitude'] = '%.14f' % loc['lat']
                info_dict['longitude'] = '%.14f' % loc['lng']

                url = title.a.get('href')
                info_dict.update({'link': url})
                code = re.findall(r'(\w*[0-9]+)\w*', url)

                info_dict.update({'code': code[0]})

                taginfo = xq.find("div", {"class": "tagList"})  # html
                if taginfo.span:
                    info_dict.update({'subway': taginfo.span.get_text()})
                else:
                    CommunityCrawlerT._log.warning('%s on %s has no taginfo?!',info_dict['name'], url)

                info_dict.update({'district': xq.find('a', {'class': 'district'}).text})
                info_dict.update({'bizcycle': xq.find('a', {'class': 'bizcircle'}).text})

                info = 'name:%s , code:%s , district:%s , bizcycle:%s , subway:%s , school:%s , link:%s, lat:%s,lng:%s.' % \
                (info_dict['name'], info_dict['code'],info_dict['district'],info_dict['bizcycle'],info_dict['subway'],\
                    info_dict['school'],info_dict['link'],info_dict['latitude'],info_dict['longitude'])
                CommunityCrawlerT._log.info( info)

                mdb.update_community(info_dict)

    def _crawl_list(self):
        """
        爬取所有小区信息
        """
        
        page_box = self._soup.find('div',{'class':'page-box house-lst-page-box'})

        if page_box == None:
            CommunityCrawlerT._log.error(' _crawl_list failed on %s. ' , self._data)
            return

        total_pages = 0

        d="d="+page_box.get('page-data')
        exec(d)
        total_pages=d['totalPage']

        CommunityCrawlerT._log.info(' find %d pages of communite. ' , total_pages)

        
        threads=[]

        for i in range(total_pages):
            url_page = "http://bj.lianjia.com/xiaoqu/%s/pg%d/" 
            url_data = (self._data,i+1)
            crawl = CommunityCrawlerT('info',url_page,url_data)
            threads.append(crawl)


        for t in threads:
            t.start()
        for t in threads:
            t.join()

if __name__ == '__main__':
    urlptn = u"http://bj.lianjia.com/xiaoqu/rs%s/" 
    data = '朝阳'.decode('utf-8')

    db.db.open(False)

    cc = CommunityCrawlerT('list', urlptn, data)
    cc.start()
    cc.join()

    db.db.close()


